from scripts._utils import utils
from scripts.User_Management import _utils as user_utils
from getpass import getpass

AUTH_SERVER_HOSTNAME = 'lannister'
USERNAME = 'hackerspace_admin'


def add_new_user(username=None, first_name=None, last_name=None, password=None, ssh_connection=None, bulk_creation=False):

    if not username:
        username = user_utils.get_new_username()
        if not username:
            return False

    if not first_name or not last_name:
        first_name, last_name = user_utils.get_new_users_names(username)
        if not first_name:
            return False

    if bulk_creation:
        utils.print_warning(f"\nCreating account for {username} {first_name} {last_name}")
    else:
        if not utils.confirm(f"\nCreate account for {username} {first_name} {last_name}?", yes_is_default=False):
            return False

    # generate ldif file
    ldif = user_utils.generate_ldif_entry(username, first_name, last_name)

    # get pw now so we don't have to renter later
    if not password:
        password = getpass("Enter the admin password: ")

    success = user_utils.create_users_from_ldif(ldif, ssh_connection=ssh_connection, password=password)

    # create home dir for new user
    if success:
        return user_utils.create_home_dirs([username], password)
