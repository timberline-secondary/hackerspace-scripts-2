import paramiko
from getpass import getpass

#this code worked on by Nicholas (Tseilorin) Hopkins

class SSH():

    def __init__(self, hostname, username, password=None):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.pi_passwd = "hackerberry"
        self.pi_user = "pi"
        self.tv_turnoff_cmd = "echo standby 0 | cec-client -s -d 1"
        self.tv_turnon_cmd = "echo standby 1 | cec-client -s -d 1"
        self.reboot_cmd = "sudo reboot"
        self.ssh_client = None

    def __str__(self):
        return "SSH connection with {}@{}".format(self.username, self.hostname)

    def connect(self):
        if self.password is None:
            self.password=getpass("password: ")

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)

        except paramiko.ssh_exception.AuthenticationException:
            print ("\n\nConnection failed, credentials may be wrong.\n\n")
            return False
        except paramiko.ssh_exception.BadAuthenticationType:
            print ("\n\nConnection failed, password may be wrong or server does not allow this connection type.\n\n")
            return False
        except paramiko.ssh_exception.BadHostKeyException:
            print ("\n\nThe host key given by the SSH did not match what we were expecting.\n\n")
            return False
        except paramiko.ssh_exception.ChannelException:
            print ("\n\nThe attempt to open a new Channel failed.\n\n")
            return False
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ("\n\nMultiple connection attempts were made and none succeeded.\n\n")
            return False

        return True


    def send_cmd(self, command, sudo=False, cd=False, print_stdout=False):
        if not self.is_connected():
            return -1

        if self.ssh_client == None:
            print("SSH client not connected")
            return False

        if sudo:
            transport = self.ssh_client.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()

            session.exec_command("sudo {}".format(command))
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)

            stdin.write(self.password + "\n")
            stdin.flush()
        else:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)

        output = stdout.read()

        if print_stdout:
            print(output)

        return stdout.read()

    def close(self):
        self.ssh_client.close()

    def file_exists(self, filepath, filename):
        if not self.is_connected():
            return -1

        # link to docs for test -f command
        command = "test -f {}{}".format(filepath, filename)
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            return True
        else:
            return False

    def is_connected(self):
        client = self.ssh_client
        error_msg = "Not connected. You forgot to use .connect()"
        if client and client.get_transport() is not None and client.get_transport().is_active():
            try:
                transport = client.get_transport()
                transport.send_ignore()
                return True
            except EOFError as e:
                # not connected
                print(error_msg)
                return False

        print(error_msg)
        return False
