from scripts._utils import utils
from scripts.User_Management import _utils as user_utils

GROUP = "docker"


def grant_user_advanced_usb_access():

    fullname, username = user_utils.get_and_confirm_user()
    if not fullname:
        return False

    if not utils.confirm(f"Confirm you want to add {fullname} to the {GROUP} group?"):
        return False

    success = user_utils.add_user_to_group(username, GROUP)

    return success
