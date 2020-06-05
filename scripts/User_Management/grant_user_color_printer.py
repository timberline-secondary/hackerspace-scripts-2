from scripts._utils import utils
from scripts.User_Management import _utils as user_utils

COLORPRINTER_GROUP = "colorprinter"


def grant_user_color_printer():

    fullname, username = user_utils.get_and_confirm_user()
    if not fullname:
        return False

    if not utils.confirm(f"Confirm you want to give {fullname} the ability to use the color printer?"):
        return False

    success = user_utils.add_user_to_group(username, COLORPRINTER_GROUP)

    return success
