from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.User_Management import _utils as user_utils

HOSTNAME = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'


def clean_user_files():

    who_to_clean = utils.input_styled("Enter a username or all? ")

    if who_to_clean == 'all':
        search_root = "/nfshome/*/"
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
    print("Emptying Downloads directory...")
    ssh_connection.send_cmd(f"find {search_root}/Downloads/* -delete", sudo=True)

    # remove .cache directory and contents
    print("Emptying .cache directory...")
    ssh_connection.send_cmd(f"rm -rf {search_root}/.cache/*", sudo=True)

    # empty trash
    print("Emptying Trash...")
    ssh_connection.send_cmd(f"rm -rf {search_root}/.local/share/Trash/files/*", sudo=True)

    # CR2 Files (raw images...massive sizes)
    print("Finding and deleting all CR2 files (raw images that are massive)...")
    ssh_connection.send_cmd(f"find {search_root}/ -type f -name '*.CR2' -delete", sudo=True)

    # empty any tmp directories
    print("Finding and emptying tmp and temp directories...")
    ssh_connection.send_cmd(f"find {search_root}/ -type d -name 'tmp' -delete", sudo=True)
    ssh_connection.send_cmd(f"find {search_root}/ -type d -name 'temp' -delete", sudo=True)

    # remove any files larger than 1G?
    print("Finding and deleting any files larger than 2G...")
    ssh_connection.send_cmd(f"find {search_root}/ -type f -size +2G -delete", sudo=True)

    print("Available space on the file server AFTER:")
    print("Filesystem                   Size  Used Avail Use% Mounted on")
    ssh_connection.send_cmd("df -h | grep nfshome")

    ssh_connection.close()
