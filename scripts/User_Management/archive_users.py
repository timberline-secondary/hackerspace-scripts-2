import pwd
import datetime
from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils

hostname = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'

home_root = "/nfshome/"

current_year = int(datetime.date.today().strftime(
    "%Y")[-2:])


PROTECTED_USERS = ['tylere.couture', 'hackerspace_admin']


def archive_users():
    ssh_connection = SSH(hostname, SERVER_USERNAME)
    for p in pwd.getpwall():
        username = p[0]
        user_id = pwd.getpwnam(username).pw_uid
        account_creation_year = int(str(user_id)[:2])
        is_not_system_user = 1000 < user_id < 60000
        is_older_than_five_years = current_year - account_creation_year >= 5

        if is_not_system_user and is_older_than_five_years and username not in PROTECTED_USERS:
            utils.print_error(f"Wiping home drive of user {user_id}: {username}, account created in 20{account_creation_year}\n")
            confirmation = utils.input_styled("Are you sure you wish it proceed? [y/N] (q to quit): \n")

            if confirmation and confirmation[0].lower() == "y":
                ssh_connection.send_cmd(f"rm -rf {home_root}{username}/", sudo=True)
                utils.print_warning(f'deleted {home_root}{username}/')
                skeleton = f"bash /nfshome/makehomedirs.sh {username}"
                ssh_connection.send_cmd(skeleton, sudo=True)
                utils.print_warning(f'place skeleton to {home_root}{username}/')
                if ssh_connection.dir_exists(f"{home_root}{username}"):
                    utils.print_success("User was successfully archived, skeleton placed.")
                else:
                    utils.print_error("FATAL: Unable to archive user (no home_dir)")
            elif confirmation == "q":
                break
            else:
                print("Skipping...")
