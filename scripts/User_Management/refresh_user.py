from getpass import getpass

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
        utils.print_success(f"✓ Recovered {dir}")
    else:
        utils.print_warning(f"✗ {dir} not found")


def refresh_user():
    utils.print_warning("This will refresh a user's account by removing all their customizations and settings. However their files/documents will remain. This can be used if the user is experiences UI issues or having other weird problems with their account.")
    password = getpass("Enter the admin password: ")
    ssh_connection = SSH(hostname, SERVER_USERNAME, password)
    if not ssh_connection.is_connected():
        return False
    utils.print_error("ENSURE THE USER IS LOGGED OUT BEFORE PERFORMING THIS ACTION!\n")
    fullname, username = user_utils.get_and_confirm_user()

    if not fullname:
        return False

    home_dir = f"/nfshome/{username}"

    # First, make sure their home drive exists.  Sometimes home drive creation fails when
    # creating new users in bulk!
    if ssh_connection.dir_exists(home_dir):
        move = f"mv {home_dir} {home_dir}.bu"
        ssh_connection.send_cmd(move, sudo=True)
        utils.print_success(f"✓ Backing up home drive")
        skeleton = f"bash /nfshome/makehomedirs.sh {username}"
        ssh_connection.send_cmd(skeleton, sudo=True)
        utils.print_success(f"✓ Created skeleton")
        for dir in dirs:
            transfer_files(home_dir, dir, ssh_connection)
        if ssh_connection.dir_exists(home_dir):
            utils.print_success(f"✓ All files have been recovered")
            remove_backup = f"rm -rf {home_dir}.bu"
            ssh_connection.send_cmd(remove_backup, sudo=True)
            utils.print_success(f"✓ Removing old backup")
            change_ownership = f"chown -R '{username}:students' '{home_dir}'"
            ssh_connection.send_cmd(change_ownership, sudo=True)
            utils.print_success(f"✓ Changed ownership root → {username}")
            utils.print_success("Operation complete, please have the user log back in.")
        else:
            utils.print_error(f"✗ New home directory does not exist, reverting to backup.")
            revert_to_backup = f"mv {home_dir}.bu {home_dir}"
            ssh_connection.send_cmd(revert_to_backup, sudo=True)
            if ssh_connection.dir_exists(home_dir):
                utils.print_error("Reverted to backup successfully (No changes).")
            else:
                utils.print_error("FATAL (PANIC): Error while creating new home directory, could not revert to backup. (No home directory exists)")
                panic = f"bash /nfshome/makehomedirs.sh {username}"
                ssh_connection.send_cmd(panic, sudo=True)
                if ssh_connection.dir_exists(home_dir):
                    utils.print_success("A New home directory was able to be made.")
                else:
                    utils.print_error("FATAL (PANIC): COULD NOT CREATE NEW HOME DIRECTORY FOR USER.")
    else:
        # no home drive!  Need to make it
        utils.print_warning("No home drive detected, creating new home drive...")
        command = f"bash /nfshome/makehomedirs.sh {username}"
        ssh_connection.send_cmd(command, sudo=True)
        utils.print_success("Operation complete, please have the user log back in.")

    ssh_connection.close()
