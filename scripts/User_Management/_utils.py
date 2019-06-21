import os, socket
from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH

def check_student_number(student_number, password=None):
    hostname = socket.gethostname() # can use the local computer
    username = 'hackerspace_admin'
    if not password:
        password = getpass("Enter the admin password: ")

    ssh_connection = SSH(hostname, username, password)
    command = "getent passwd | grep {}".format(student_number)
    ssh_connection.send_cmd(command, sudo=True)