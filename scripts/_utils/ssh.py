import paramiko
import threading
from time import time
from getpass import getpass
from .utils import print_error, print_success, print_warning, input_styled

# Paramiko Demos:
# https://github.com/paramiko/paramiko/tree/master/demos


# this code worked on by Nicholas (Tseilorin) Hopkins

class Session():

    def __init__(self, transport):
        self.session = transport.open_session()
        self.session.set_combine_stderr(True)
        self.session.get_pty()

    def send_cmd(self, command):
        self.session.exec_command(command)



class SSH():
    """
    Wrapper for paramiko common use cases

    Basic use (for sending single commands):
        ssh_connection = SSH(hostname, username, password=None) # will establish an ssh connection to the host and ask for password if not provided
        ssh_connection.send_cmd('ls')  # send a command and print the output.

    File use (for doing file operations):
        # add example

    Advanced use (for sending multiple or complex commands requiring interactivity or sudo)
        ssh_connection = SSH(hostname, username, password=None, threaded=True)
        ssh_connection.open_shell() # open an interactive shell on the host

        # need example hot to interact with code! Maybe send a tuple of input/output commands?
        
    """

    tv_turnoff_cmd = "echo standby 0 | cec-client -s -d 1"
    tv_turnon_cmd = "echo standby 1 | cec-client -s -d 1"

    def __init__(self, hostname, username, password=None):
        self.hostname=hostname
        self.username=username
        self.password=password

        self.client = None # the base connection, also used for simple commands
        self.transport = None # used for complex commands
        self.sftp = None  # used for file operations

        self.connect()
        self.connect_transport()
        self.connect_sftp()

    def __del__(self):
        self.close()

    def __str__(self):
        return "SSH connection with {}@{}".format(self.username, self.hostname)

    def connect(self):
        if self.password is None:
            self.password=getpass("password: ")

        # connect ssh client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)

        except paramiko.ssh_exception.BadAuthenticationType:
            print_error ("\n\nConnection failed, password may be wrong or server does not allow this connection type.\n\n")
            return False
        except paramiko.ssh_exception.AuthenticationException:
            print_error ("\n\nConnection failed, credentials may be wrong.\n\n")
            return False
        except paramiko.ssh_exception.BadHostKeyException:
            print_error ("\n\nThe host key given by the SSH did not match what we were expecting.\n\n")
            return False
        except paramiko.ssh_exception.ChannelException:
            print_error ("\n\nThe attempt to open a new Channel failed.\n\n")
            return False
        except paramiko.ssh_exception.NoValidConnectionsError:
            print_error ("\n\nMultiple connection attempts were made and none succeeded.\n\n")
            return False

        print_success("{} successful.".format(str(self)))
        return True

    def connect_transport(self):
        # connect transport for interactive shell and complicated commands etc
        # https://daanlenaerts.com/blog/2016/07/01/python-and-ssh-paramiko-shell/
        self.transport = self.client.get_transport()
    
    def connect_sftp(self):
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def get_open_session(self):
        """Opens a sessions for sending interactive commands
        
        Returns:
            paramiko.channel.Channel -- the session channel object
        """
        session = self.transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        return session

    def send_simple_cmd(self, command):
        """Sends a command to the host using the most basic paramiko method.
        Mostly here for documention to show alternate methods of using paramiko. Just use send_cmd()
        
        Arguments:
            command {str} -- the bash command
        
        Returns:
            str -- stdout of the command
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        output = str(stdout.read(), 'utf8') # convert from bytestring for newlines to work
        print (output)
        return output

    def send_cmd(self, command, sudo=False, print_stdout=True):
        """Sends a command to the host using a temporary session. Automatically provides the sudo password if needed.
        
        Arguments:
            command {str} -- The command.  To run a sudo command, do not add sudo in front, 
            instead set the sudo parameter to True.
        
        Keyword Arguments:
            sudo {bool} -- run the command as sudo. (default: {False})
            print_stdout {bool} -- Print the output of the command (default: {True})
        
        Returns:
            string -- the output from the command
        """
        if not self.is_connected():
            print_error("SSH client not connected")
            return False

        session = self.get_open_session()

        if sudo:
            command = "sudo " + command

        session.exec_command(command)
        stdout = session.makefile("rb", -1)

        if sudo:
            # provide the password to stdin
            stdin = session.makefile("wb", -1)
            stdin.write(self.password + "\n")
            stdin.flush()

        output = str(stdout.read(), 'utf8') # convert from bytestring for newlines to work
        output = output.replace(self.password, "*****")
        if print_stdout:
            print(output)
        return output

    def send_interactive_commands(self, command_response_list):
        """[summary]
        
        Arguments:
            command_response_list {list} -- a list of string triplets:  [(input, response_expected, response_contains), ], where
                input {str} -- the keystrokes to provide as input, this could be a command or interactive input.
                response_expected {str} -- the expected output if the command was successful, or the input was received as expected.
                    This string is compared to the end of the output, so if you are extecting a prompt after the last input, then
                    "$" will work just as well as "user@hostname:~$"
                response_contains {str} -- a string to look for WITHIN the output data.  Can be None.

            Example for resetting a user's password to 'wolf':
                [
                    ("sudo passwd username", "[sudo] password for admin_username: ", None),
                    (password, "New password: ", None),
                    ("wolf", "Re-enter new password: ", None),
                    ("wolf", "hackerspace_admin@tbl-hackerspace-13-s:~$ ", "password updated successfully"),
                ]
        Returns:
            bool -- whether successful or not
        """

        # e.g. "hackerspace_admin@tbl-hackerspace-13-s:~$ " <-- trailing space!
        prompt_string = "{}@{}:~$ ".format(self.username, self.hostname)
        channel = self.client.invoke_shell()
        channel.send(prompt_string + '\n')
        # wait for the prompt
        output = self.read_data(channel, prompt_string)
        print(prompt_string)

        if output is not None:

            # send commands/input
            for cmd, response, contains in command_response_list:
                # print("Sending command: ########  {} ##############".format(cmd))
                channel.send(cmd + '\n')
                output = self.read_data(channel, response, contains)
                
                if output is None:
                    return False
                else:
                    print(output)

        return True      

    def read_data(self, channel, response_expected, response_contains=None, timeout=5.0):
        """Read channel output until expected_reponse is found at the end of the output and, if applicable, the response_contains
        is found within, or timeout, whichever comes first. 
        
        Arguments:
            channel {paramiko.channel.Channel} -- the channel to read data from
            response_expected {str} -- a string to look for at the END of the output data

        Keyword Arguments:
            response_contains {str} -- a string to look for WITHIN the output data (default: {None})
            timeout {float} -- in seconds (default: {5.0})

        Returns:
            str -- the output data, None if timeout occurs
        """
        channel_data = ""
        start_time = time()
        response_found = False

        while True:
            elapsed_time = time() - start_time
            if channel.recv_ready():  # if there is data ready to receive
                # Get the data
                channel_data += str(channel.recv(9999), 'utf8') # receive max # of bytes

                # New data received, check if we got the expected output yet:
                if response_expected and channel_data.strip().endswith(response_expected.strip()):
                    # if we also need to look for content within the output, cehck that too
                    if response_contains is not None:
                        if response_contains in channel_data:
                            response_found = True
                    else:
                        response_found = True

                if response_found:
                    return channel_data
                    
            elif timeout < elapsed_time:
                print("Command timed out or unexpected response.")
                print("## Got response: ")
                print(channel_data)
                print("## Expected response: ")
                print(response_expected)
                print("\nABORTING...\n")
                return None 


    def close(self):
        if(self.client != None):
            self.client.close()
        # self.sftp.close()
        self.transport.close()

    def is_connected(self):
        error_msg = "Not connected."
        if self.client and self.client.get_transport() is not None and self.client.get_transport().is_active():
            try:
                transport = self.client.get_transport()
                transport.send_ignore()
                return True
            except EOFError as e:
                # not connected
                print_error(error_msg)
                return False

        print_error(error_msg)
        return False

    # https://daanlenaerts.com/blog/2016/07/01/python-and-ssh-paramiko-shell/
    # def process(self):
    #     while True:
    #         # Print data when available
    #         if self.shell != None and self.shell.recv_ready():
    #             alldata = self.shell.recv(1024)
    #             while self.shell.recv_ready():
    #                 alldata += self.shell.recv(1024)
    #             strdata = str(alldata, 'utf8')
    #             strdata.replace('\r', '') # remove windows carriage return character.. seems unecessary
    #             print(strdata, end='')
    #             if(strdata.endswith('$ ')):
    #                 print('\n$ ', end='')

    ######################### 
    #                       # 
    #  Convenience methods  #
    #                       #
    # #######################

    def copy_file(self, source, destination):
        """Copies a local file to the host
        
        Arguments:
            source {str} -- full or relative path to local file
            destination {str} -- full path to file on server, must include the destination file name
        """
        print ("Copying file {} to {}:/{}".format(source, self.hostname, destination))
        self.sftp.put(source, destination)

    def file_exists(self, filepath, filename):
        if not self.is_connected():
            return -1

        # link to docs for test -f command
        command = "test -f {}/{}".format(filepath, filename)
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            return True
        else:
            return False
