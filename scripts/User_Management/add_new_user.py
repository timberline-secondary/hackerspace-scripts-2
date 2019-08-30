import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management._utils import get_student_name
from getpass import getpass

hostname = 'lannister'
username = 'hackerspace_admin'

def add_new_user(student_number=None, first_name=None, last_name=None, password=None, skip_existing_users=False):

    created = False
    while not created:
        if not student_number:
            student_number = utils.input_styled("Enter Student Number: \n")
        if not password:
            password = getpass("Enter the admin password: ")

        student = get_student_name(student_number, password)

        if student is not None:
            if skip_existing_users:
                utils.print_success("An account for {}, {}, already exists, skipping... ".format(student_number, student))
                return
            else:
                utils.print_warning("An account for {}, {}, already exists.  Try resetting their password if they can't log in.".format(student_number, student))
        else:
            
            if not first_name:
                first_name = utils.input_styled("First Name: \n")
            first_name = first_name.upper()

            if not last_name:
                last_name = utils.input_styled("Last Name: \n")
            last_name = last_name.upper()

            create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(student_number, first_name, last_name))

            if create.lower() == 'y':
                ssh_connection = SSH(hostname, username, password)

                main_command = 'bash hs-ldapadduser.sh "{}" "{}" "{}"'.format(student_number, first_name, last_name)

                command_response_list = [
                                    ("cd hs-ldap/", ":~/hs-ldap$", None),
                                    (main_command, "[sudo] password for hackerspace_admin: ", None),
                                    (password, "Enter LDAP Password: ", None),
                                    (password, "hackerspace_admin@tyrell's password: ", None),
                                    (password, "[sudo] password for hackerspace_admin: ", None),
                                    (password, ":~/hs-ldap$", "Set owner on: /nfshome/{}".format(student_number)),
                ]

                success = ssh_connection.send_interactive_commands(command_response_list)
                ssh_connection.close()

                if success:
                    utils.print_success('Successfully created account for {} {} {}'.format(student_number, first_name, last_name))
                    utils.print_success('Their default password will be "wolf"')
                    created = True
                else:
                    utils.print_error("Something went wrong there, hopefully useful info is printed above...let's try again\n")

            else:
                print("Aborted that one. \n")

                if utils.input_styled("Try again? [y]/n: ") == 'n':
                    return

    input("\nHit enter to continue...\n")
