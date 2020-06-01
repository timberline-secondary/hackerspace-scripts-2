import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.User_Management import _utils as user_utils
from getpass import getpass

hostname = 'lannister'
server_username = 'hackerspace_admin'

def change_first_and_last_name ():

    username, fullname = user_utils.get_and_confirm_user() 
    if not username:
        return False

    print("OK, let's do this! Please enter first and last names seperately. They will be converted to all upper case.")

    new_first = utils.input_styled("What would you like to change their FIRST name to? ").upper()
    new_last = utils.input_styled("What would you like to change their LAST name to? ").upper()

    confirmed = utils.input_styled("Confirm you want to change {} to {} {}? y/[n] ".format(fullname, new_first, new_last))

    if confirmed.lower() != 'y':
        print("Bailing...")
        return

    password = getpass("Enter the admin password: ")
    ssh_connection = SSH(hostname, server_username, password)
    main_command = "sudo ldapmodifyuser {}".format(username)
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
        users_name = utils.get_users_name(username)
        utils.print_success("{}: {}".format(username, users_name))

    else:
        utils.print_error("Something appears to have gone wrong. Hopefully there's a useful error message somewhere up there...")


