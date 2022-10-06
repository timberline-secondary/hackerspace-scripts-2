from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils

hostname = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'


def repair_user_desktop():
    password = getpass("Enter the admin password: ")
    ssh_connection = SSH(hostname, SERVER_USERNAME, password)
    utils.print_warning("Make sure the student is logged out before running this repair.\n")
    fullname, username = user_utils.get_and_confirm_user()

    if not fullname:
        return False

    home_dir = "/nfshome/{}".format(username)

    # First, make sure their home drive exists.  Sometimes home drive creation fails when
    # creating new users in bulk!
    if ssh_connection.dir_exists(home_dir):
        command = "rm -r {}/.cache".format(home_dir)
        ssh_connection.send_cmd(command, sudo=True)
        print("I tried to delete their cache.  That usually solves the problem...")
        utils.print_success("Have the student try logging in again.")
    else:
        # no home drive!  Need to make it
        utils.print_warning("AH!  It appears they don't have a home drive! I gonna try to create one for them now...")
        command = "bash /nfshome/makehomedirs.sh {}".format(username)
        ssh_connection.send_cmd(command, sudo=True)
        utils.print_success("Have the student try logging in again.")

    ssh_connection.close()
