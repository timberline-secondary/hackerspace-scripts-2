from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.User_Management import _utils as user_utils
from getpass import getpass

hostname = 'lannister'
server_username = 'hackerspace_admin'


def change_first_and_last_name():

    username, fullname = user_utils.get_and_confirm_user()
    if not username:
        return False

    print("OK, let's do this! Please enter first and last names seperately. They will be converted to all upper case.")

    new_first = utils.input_styled("What would you like to change their FIRST name to? ").upper()
    new_last = utils.input_styled("What would you like to change their LAST name to? ").upper()

    confirmed = utils.input_styled(f"Confirm you want to change {fullname} to {new_first} {new_last}? y/[n] ")

    if confirmed.lower() != 'y':
        print("Bailing...")
        return

    ldif_changes_dict = {
        'gecos': f"{new_first} {new_last}",
        'displayName': f"{new_first} {new_last}",
        'cn': new_first,
        'sn': new_last,
        'givenName': new_first,
    }

    success = user_utils.modify_user(username, ldif_changes_dict)

    if success:
        utils.print_success("Looks like it worked to me? Here's the new entry:")
        users_name = utils.get_users_name(username)
        utils.print_success(f"{username}: {users_name}")

    else:
        utils.print_error("Something appears to have gone wrong. Hopefully there's a useful error message somewhere up there.")
