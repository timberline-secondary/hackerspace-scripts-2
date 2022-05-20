from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils

hostname = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'

dirs = ["Desktop", "Documents", "Music", "Pictures", "Public", "Templates", "Videos"]


def transfer_files(home_dir, dir, connection):
    if connection.dir_exists(f"{home_dir}.bu/{dir}"):
        transfer_desk = f"cp -R {home_dir}.bu/{dir} {home_dir}"
        connection.send_cmd(transfer_desk, sudo=True)
        utils.print_success(f"✓ Transferred {dir}")
    else:
        utils.print_warning(f"✗ {dir} not found")


def refresh_user():
    utils.print_warning("This will refresh a user, it will only carry over all default folders, except for Downloads.")
    ssh_connection = SSH(hostname, SERVER_USERNAME)
    utils.print_warning("Ensure the user is logged out before performing this action.\n")
    fullname, username = user_utils.get_and_confirm_user()

    if not fullname:
        return False

    home_dir = f"/nfshome/{username}"

    # First, make sure their home drive exists.  Sometimes home drive creation fails when
    # creating new users in bulk!
    if ssh_connection.dir_exists(home_dir):
        move = f"mv {home_dir} {home_dir}.bu"
        ssh_connection.send_cmd(move, sudo=True)
        copy = f"cp -R /etc/skel {home_dir}"
        ssh_connection.send_cmd(copy, sudo=True)
        for dir in dirs:
            transfer_files(home_dir, dir, ssh_connection)
        remove_backup = f"rm -rf {home_dir}.bu"
        ssh_connection.send_cmd(remove_backup, sudo=True)
        utils.print_success("Operation complete, please have the user log back in.")
    else:
        # no home drive!  Need to make it
        utils.print_warning("No home drive detected, creating new home drive...")
        command = f"bash /nfshome/makehomedirs.sh {username}"
        ssh_connection.send_cmd(command, sudo=True)
        utils.print_success("Operation complete, please have the user log back in.")

    ssh_connection.close()
