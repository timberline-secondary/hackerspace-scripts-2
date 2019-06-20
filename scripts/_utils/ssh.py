import paramiko
import threading
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

    def __init__(self, hostname, username, password=None, threaded=False):
        self.hostname=hostname
        self.username=username
        self.password=password

        self.client = None # the base connection, also used for simple commands
        self.transport = None # used for complex commands
        self.sftp = None  # used for file operations

        self.connect()
        self.connect_transport(threaded)
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

    def connect_transport(self, threaded=False):
        # connect transport for interactive shell and complicated commands etc
        # https://daanlenaerts.com/blog/2016/07/01/python-and-ssh-paramiko-shell/
        self.transport = self.client.get_transport()
    
    def connect_sftp(self):
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    # def invoke_shell(self):
    #     self.shell = self.client.invoke_shell()

    # def send_shell_cmd(self, command):
    #     if(self.shell):
    #         self.shell.send(command + "\n")
    #     else:
    #         print_error("Attempting to send a shell command but the shell isn't opened.  Need to call invoke_shell() first.")

    # def open_shell(self):
    #     self.invoke_shell()
    #     while True:
    #         command = input_styled('').strip()
    #         self.send_shell_cmd(command)
    #         if command == 'exit':
    #             return

    def send_simple_cmd(self, command):
        """Sends a command to the host using the most basic paramiko method.
        Mostly here for documention, just use send_cmd()
        
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
        if print_stdout:
            print(output)
        return output

    def get_open_session(self):
        """Opens a sessions for sending interactive commands
        
        Returns:
            paramiko.channel.Channel -- the session channel object
        """
        session = self.transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        return session

    def close(self):
        if(self.client != None):
            self.client.close()
        self.sftp.close()
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
        command = "test -f {}{}".format(filepath, filename)
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            return True
        else:
            return False
            