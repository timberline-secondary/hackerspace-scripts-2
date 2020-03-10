import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from getpass import getpass

hostname = 'lannister'
username = 'hackerspace_admin'

def rename_user ():

    student_number = utils.input_styled("Enter Student Number: \n")
    password = getpass("Enter the admin password: ")

    student = utils.get_users_name(student_number)

    if student is None:
        utils.print_warning("I couldn't find an account for {}.  Sorry!".format(student_number))
    else:
        utils.print_success("Found {}: {}.".format(student_number, student))
        is_correct_student = utils.input_styled("Is this the correct student? y/[n] ")

        if is_correct_student.lower() != 'y':
            print("Bailing...")
            return

        print("OK, let's do this! Please enter first and last names seperately. They will be converted to all upper case.")

        new_first = utils.input_styled("What would you like to change their first name to? ").upper()
        new_last = utils.input_styled("What would you like to change their last name to? ").upper()

        confirmed = utils.input_styled("Confirm you want to change {} to {} {}? y/[n] ".format(student, new_first, new_last))

        if is_correct_student.lower() != 'y':
            print("Bailing...")
            return

        ssh_connection = SSH(hostname, username, password)

        main_command = "sudo ldapmodifyuser {}".format(student_number)

        EOF = '\x04'  # Ctrl + D

        command_response_list = [
                            (main_command, "[sudo] password for hackerspace_admin: ", None),
                            (password, "dc=tbl", None),
                            ("replace: gecos\ngecos: {} {}\n{}".format(new_first, new_last, EOF), '$', None),
                            (main_command, "dc=tbl", None),
                            ("replace: cn\ncn: {} {}\n{}".format(new_first, new_last, EOF), '$', None),
                            (main_command, "dc=tbl", None),
                            ("replace: displayName\ndisplayName: {}\n{}".format(new_last, EOF), '$', None),
                            (main_command, "dc=tbl", None),
                            ("replace: sn\nsn: {}\n{}".format(new_last, EOF), '$', None),
                            (main_command, "dc=tbl", None),
                            ("replace: givenName\ngivenName: {}\n{}".format(new_first, EOF), '$', None),
                            # (password, "[sudo] password for hackerspace_admin: ", None),
                            # (password, ":~/hs-ldap$", "Set owner on: /nfshome/{}".format(student_number)),
        ]

        success = ssh_connection.send_interactive_commands(command_response_list)

        if success:
            utils.print_success("Looks like it worked to me? Here's the new entry:")
            student = utils.get_users_name(student_number)
            utils.print_success("{}: {}".format(student_number, student))

        else:
            utils.print_error("Something appears to have gone wrong. Hopefully there's a useful error message somewhere up there...")


