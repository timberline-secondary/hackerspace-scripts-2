import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils
from getpass import getpass

AUTH_SERVER_HOSTNAME = 'lannister'
USERNAME = 'hackerspace_admin'

def add_new_user():

    username = user_utils.get_new_username()
    if not username:
        return False

    first_name, last_name = user_utils.get_new_users_names(username)

    create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(username, first_name, last_name))

    if create[0].lower() != 'y':
        return False

    # generate ldif file
    ldif = user_utils.generate_ldif_entry(username, first_name, last_name)

    #get pw now so we don't have to renter later
    password = getpass("Enter the admin password: ")
    
    success = user_utils.create_users_from_ldif(ldif, password=password)
    
    # create home dir for new user
    if success:
        return user_utils.create_home_dirs([username], password)
        # make_home_dirs_cmd = 'ssh -t hackerspace_admin@tyrell "sudo /nfshome/makehomedirs.sh {}"'.format(username)

        # command_response_list = [
        #                 (make_home_dirs_cmd, "hackerspace_admin@tyrell's password: ", None),
        #                 (password, "[sudo] password for hackerspace_admin: ", None),
        #                 (password, "$", None),
        # ]

        # # why are we doing this through lannister?  ssh direct to tyrell!!!
        # success = ssh_connection.send_interactive_commands(command_response_list)

        # if success:
        #     utils.print_success("Looks like it worked!  Unless you see some nasty errors above...")
        # else:
        #     utils.print_error("Something went wrong but I'm not smart enough to know what...")
