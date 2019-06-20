import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH

hostname = 'lannister'
username = 'hackerspace_admin'


def add_new_user():
    input("Under Construction...[Enter]")

    ssh_connection = SSH(hostname, username)

    created = False
    while not created:
        student_number = utils.input_styled("Enter Student Number: \n")
        first_name = utils.input_styled("First Name: \n").upper()
        last_name = utils.input_styled("Last Name: \n").upper()

        create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(student_number, first_name, last_name))

        if create is 'y':
            # ssh_connection.send_cmd('pwd', print_stdout=True)
            # ssh_connection.send_cmd('ls', print_stdout=True)
            # ssh_connection.send_cmd('cd hs-ldap', print_stdout=True)
            # ssh_connection.send_cmd('pwd', print_stdout=True)
            # ssh_connection.send_cmd('ls', print_stdout=True)
            command = 'bash hs-ldap/hs-ldapadduser.sh "{}" "{}" "{}"'.format(student_number, first_name, last_name)
            ssh_connection.send_cmd(command, sudo=True, print_stdout=True)
            created = True

        else:
            print("Aborted that one, try again. \n")

    input("\nHit enter to continue...\n")
    ssh_connection.close()

