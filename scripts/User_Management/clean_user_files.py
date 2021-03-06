import re

from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.User_Management import _utils as user_utils

HOSTNAME = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'

#####################
#
# THIS SCRIPT NEEDS WORK BEFORE USING
# specifically, the `find` command needs to be better configured
# see: https://unix.stackexchange.com/questions/592130/why-does-bash-find-command-not-return-files-in-home-local-share-trash-files/592151#592151
####################


def clean_user_files():

    who_to_clean = utils.input_styled("Enter a username or all? ")

    if who_to_clean == 'all':
        search_root = "/nfshome/*"
    else:
        fullname, username = user_utils.get_and_confirm_user(username=who_to_clean)
        if not fullname:
            return False
        # utils.print_warning("Make sure the student is logged out before running this repair.\n")

        search_root = f"/nfshome/{username}"

    ssh_connection = SSH(HOSTNAME, SERVER_USERNAME)

    print("Available space on the file server BEFORE:")
    print("Filesystem                   Size  Used Avail Use% Mounted on")
    ssh_connection.send_cmd("df -h | grep nfshome")

    # empty Downloads directory
    location = f"{search_root}/Downloads/*"
    num = count_files(location, ssh_connection)
    if num > 0:
        utils.print_warning(f"Emptying Downloads directory: {location}")
        utils.input_styled("Enter to continue...")
        delete_files(location, ssh_connection)

    # remove .cache directory and contents
    location = f"{search_root}/.cache/*"
    num = count_files(location, ssh_connection)
    if num > 0:
        utils.print_warning(f"Emptying .cache directory: {location}")
        utils.input_styled("Enter to continue...")
        delete_files(location, ssh_connection)

    # empty trash
    location = f"{search_root}/.local/share/Trash/files/*"
    num = count_files(location, ssh_connection)
    if num > 0:
        utils.print_warning(f"Emptying Trash: {location}")
        utils.input_styled("Enter to continue...")
        delete_files(location, ssh_connection)

    # CR2 Files (raw images...massive sizes)
    location = f"{search_root}"
    file_glob = '*.CR2'  # all files
    num = count_files(location, ssh_connection, file_glob)
    if num > 0:
        print("Finding and deleting all CR2 files (raw images that are massive)...")
        # delete_files(location, file_glob, ssh_connection)

    # # delete any tmp directory contents
    # location = f"{search_root}"
    # num = count_files(location, ssh_connection)
    # if num > 0:
    #     utils.print_warning(f"Emptying .cache directory: {location}")
    #     utils.input_styled("Enter to continue...")
    #     delete_files(location, ssh_connection)

    # large files
    location = f"{search_root}"
    size = '2G'
    utils.print_warning("This search can take a while, please be patient...")
    num = count_files(location, ssh_connection, size=size)
    if num > 0:
        utils.print_warning(f"Removing files larger than: {size}")
        utils.input_styled("Enter to continue...")
        delete_files(location, ssh_connection, size=size)

    print("Available space on the file server AFTER:")
    print("Filesystem                   Size  Used Avail Use% Mounted on")
    ssh_connection.send_cmd("df -h | grep nfshome")

    ssh_connection.close()


def count_files(location, ssh_connection, name_glob=None, size=None):
    command = generate_find_command(location, name_glob, size)
    command += " | wc -l"
    utils.print_warning(f"Searching for files with: {command}")
    # use double quotes as command may have single quotes within
    result = ssh_connection.send_cmd(f'bash -c "{command}"', sudo=True)
    # strip newlines from end of resulting output
    num = re.search(r'\d+$', result.strip()).group()  # get the number at the end of the output

    if num == '0':  # e.g. find: ‘/home/username/Downloads/*’: No such file or directory\n0
        utils.print_warning("No files found, skipping.")
    else:
        utils.print_warning(f"Found {num} files and directories to delete.")
    return int(num)


def delete_files(location, ssh_connection, name_glob=None, size=None):
    command = generate_find_command(location, name_glob, size)
    command += " -delete"  
    # run bash as sudo so wildcards are expanded as sudo and will have permissions to expand into all directories
    result = ssh_connection.send_cmd(f"bash -c '{command}'", sudo=True)
    if "No such file or directory" in result:
        utils.print_warning("Nothing found to delete.")
        return False
    else:
        utils.print_success("Deleted.")
        return True


def generate_find_command(location, name_glob=None, size=None):
    command = f"find {location}"
    if name_glob:
        command += f" -name '{name_glob}'"
    if size:
        command += f" -type f -size +{size}"
    return command
