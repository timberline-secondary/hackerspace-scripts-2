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


def archive_users():
    ssh_connection = SSH(hostname, SERVER_USERNAME)
    for p in pwd.getpwall():
        username = p[0]
        user_id = pwd.getpwnam(username).pw_uid
        account_creation_year = int(str(user_id)[:2])
        is_not_system_user = 1000 < user_id < 60000
        is_older_than_five_years = current_year - account_creation_year >= 5

        if is_not_system_user and is_older_than_five_years:
            utils.print_error(f"Wiping home drive of user {user_id}: {username}\n")
            confirmation = utils.input_styled("Are you sure you wish it proceed? [y/N] (q to quit): \n")
            if confirmation[0].lower() == "y":
                ssh_connection.send_cmd(f"rm -rf {home_root}{username}/", sudo=True)
                utils.print_success(f'deleted {home_root}{username}/')
                ssh_connection.send_cmd(f"cp -R /etc/skel {home_root}{username}", sudo=True)
                utils.print_success(f'place skeleton to {home_root}{username}/')
            elif confirmation == "q":
                break
            else:
                pass
