import paramiko
import threading
from getpass import getpass
from .utils import print_error, print_success, print_warning, input_styled


#this code worked on by Nicholas (Tseilorin) Hopkins

class SSH():

    def __init__(self, hostname, username, password=None, transport=False):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.tv_turnoff_cmd = "echo standby 0 | cec-client -s -d 1"
        self.tv_turnon_cmd = "echo standby 1 | cec-client -s -d 1"
        self.client = None
        self.transport = None
        self.shell = None
        self.session = None

        self.connect()
        
        if transport:
            self.connect_transport()

    def __del__(self):
        self.close()

    def __str__(self):
        return "SSH connection with {}@{}".format(self.username, self.hostname)

    def connect_transport(self):
        # connect transport for interactive shell
        # https://daanlenaerts.com/blog/2016/07/01/python-and-ssh-paramiko-shell/

        #self.transport = paramiko.Transport((self.hostname, 22))
        #self.transport.connect(username=self.username, password=self.password)

        self.transport = self.client.get_transport()
        self.session = self.transport.open_session()
        self.session.set_combine_stderr(True)
        self.session.get_pty()

        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

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

    def invoke_shell(self):
        self.shell = self.client.invoke_shell()

    def send_shell_cmd(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print_error("Attempting to send a shell command but the shell isn't opened.  Need to call invoke_shell() first.")

    def open_shell(self):
        self.invoke_shell()
        while True:
            command = input_styled('').strip()
            self.send_shell_cmd(command)
            if command == 'exit':
                return

    def send_cmd(self, command, sudo=False, cd=False, print_stdout=True):
        if not self.is_connected():
            return -1

        if self.client == None:
            print_error("SSH client not connected")
            return False

        if sudo:
            transport = self.client.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()

            session.exec_command("sudo {}".format(command))
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)

            stdin.write(self.password + "\n")
            stdin.flush()
        else:
            stdin, stdout, stderr = self.client.exec_command(command)

        output = stdout.read()
        # convert from bytestring and fix newlines
        output = str(output, 'utf8')

        if print_stdout:
            print(output)

        return output

    def close(self):
        if(self.client != None):
            self.client.close()
        if(self.transport != None):
            self.transport.close()

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

    def is_connected(self):
        client = self.client
        error_msg = "Not connected. You forgot to use .connect()"
        if client and client.get_transport() is not None and client.get_transport().is_active():
            try:
                transport = client.get_transport()
                transport.send_ignore()
                return True
            except EOFError as e:
                # not connected
                print_error(error_msg)
                return False

        print_error(error_msg)
        return False

    # https://daanlenaerts.com/blog/2016/07/01/python-and-ssh-paramiko-shell/
    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '') # remove windows carriage return character.. seems unecessary
                print(strdata, end = "")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end = "")
