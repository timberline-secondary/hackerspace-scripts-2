import paramiko
import subprocess

class SSH():

    def __init__(self, hostname, username, password):
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


    def send_cmd(self, command, print_stdout=True):
        if not self.is_connected():
            return -1

        if self.ssh_client == None:
            print("SSH client not connected")
            return False

        stdin,stdout,stderr = self.ssh_client.exec_command(command)
        #
        # if print_stdout:
        #     for line in stdout.readlines():
        #         print (line.strip())
        #
        #
        # if print_stdout:
        #     for line in stdin.readlines():
        #         print (line.strip())
        #
        #
        # if print_stdout:
        #     for line in stderr.readlines():
        #         print (line.strip())

        return stdout.readlines()

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


# def turnoff_pi_tvs_cmd(hostname, pi_pwd, username):
#     return send_cmd(hostname, pi_pwd, username, tv_turnoff_cmd)
#
# def turn_on_pi_tvs_cmd(hostname, pi_pwd, username):
#     return send_cmd(hostname, pi_pwd, username, tv_turnon_cmd)
#
# def pi_cmd(pi_name, command):
# #     return send_cmd(pi_name, pi_passwd, pi_user, command)
#
# def login_send_cmd():
#     hostname_input = input("Which computer (hostname) would you like to send a command too? ")
#     name = input("What is the username? ")
#     password = getpass.getpass(prompt="What is the password? ")
#     command_input = input("What command would you like to run? ")
#     command = command_input
#     hostname = hostname_input
#     success =  send_cmd(hostname, password, name, command)
#     return success

#
# successful = False
# while not successful:
#     successful = login_send_cmd()
#



#this code worked on by Nicky (Tseilorin) Keith
