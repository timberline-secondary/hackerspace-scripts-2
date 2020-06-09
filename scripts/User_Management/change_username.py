from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.User_Management import _utils as user_utils

from getpass import getpass

auth_hostname = 'lannister'
file_hostname = 'tyrell'
username = 'hackerspace_admin'


def change_username(current_username=None, new_username=None, auto=False, password=None):

    utils.print_warning("\nMake sure the student is logged out before making this change!\n")

    if not current_username:
        fullname, current_username = user_utils.get_and_confirm_user() 
        if not fullname:
            return False

    if not new_username:
        new_username = user_utils.get_new_username()
    if not new_username:
        return False

    if not auto:
        if not utils.confirm(f"Confirm you want to change {current_username} to {new_username}?", yes_is_default=False):
            print("Bailing...")
            return False

    if not password:
        password = getpass("Enter the admin password: ")
    ssh_connection = SSH(auth_hostname, username, password)
    command = "sudo ldaprenameuser {} {}".format(current_username, new_username)
    ssh_connection.send_cmd(command, sudo=True)
    ssh_connection.close()

    utils.print_warning("Now gonna change the name of their home directory to match the new username")

    ssh_connection = SSH(file_hostname, username, password)
    command = "mv /nfshome/{} /nfshome/{}".format(current_username, new_username)
    ssh_connection.send_cmd(command, sudo=True)
    ssh_connection.close()
    utils.print_success("Done!")

    utils.print_warning("Now gonna tell LDAP where the new home directory is")

    user_utils.modify_user(new_username, {'homeDirectory': f'/home/{new_username}'}, password)

    return True
