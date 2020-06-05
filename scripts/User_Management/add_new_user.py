from scripts._utils import utils
from scripts.User_Management import _utils as user_utils
from getpass import getpass

AUTH_SERVER_HOSTNAME = 'lannister'
USERNAME = 'hackerspace_admin'


def add_new_user():

    username = user_utils.get_new_username()
    if not username:
        return False

    first_name, last_name = user_utils.get_new_users_names(username)
    if not first_name:
        return False

    create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(username, first_name, last_name))

    if create[0].lower() != 'y':
        return False

    # generate ldif file
    ldif = user_utils.generate_ldif_entry(username, first_name, last_name)

    # get pw now so we don't have to renter later
    password = getpass("Enter the admin password: ")

    success = user_utils.create_users_from_ldif(ldif, password=password)

    # create home dir for new user
    if success:
        return user_utils.create_home_dirs([username], password)
