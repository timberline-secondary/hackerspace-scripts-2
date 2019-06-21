import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from getpass import getpass

hostname = 'lannister'
username = 'hackerspace_admin'

def add_new_user():

    created = False
    while not created:
        student_number = utils.input_styled("Enter Student Number: \n")

        already_exists = utils.user_exists(student_number)
        if already_exists:
            utils.print_warning("An account for {} already exists.  Try resetting their password.".format(student_number))
        else:

            first_name = utils.input_styled("First Name: \n").upper()
            last_name = utils.input_styled("Last Name: \n").upper()

            create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(student_number, first_name, last_name))

            if create == 'y':
                password = getpass("Enter the admin password: ")

                ssh_connection = SSH(hostname, username, password)

                prompt_string = "{}@{}:~$".format(username, hostname)
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
