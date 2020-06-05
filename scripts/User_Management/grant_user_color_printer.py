from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils


AUTH_SERVER_HOSTNAME = 'lannister'
USERNAME = 'hackerspace_admin'

COLORPRINTER_GROUP = "colorprinter"


def grant_user_color_printer():

    fullname, username = user_utils.get_and_confirm_user()
    if not fullname:
        return False

    if not utils.confirm(f"Confirm you want to give {fullname} the ability to use the color printer?"):
        return False

    password = getpass("Enter the admin password: ")
    ssh_connection = SSH(AUTH_SERVER_HOSTNAME, USERNAME, password)

    command = f"ldapaddusertogroup {username} {COLORPRINTER_GROUP}"

    success = ssh_connection.send_cmd(command, sudo=True)

    # success = ssh_connection.

    # if we were passed an ssh connection, leave it open, otherwise close it.

    ssh_connection.close()

    return success
