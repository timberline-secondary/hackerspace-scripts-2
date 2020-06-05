from scripts._utils import utils
from scripts.User_Management import _utils as user_utils

TEACHER_GROUP = "teacher"
USB_ACCESS_GROUP = "dialout"


def make_user_a_teacher():

    fullname, username = user_utils.get_and_confirm_user()
    if not fullname:
        return False

    if not utils.confirm(f"Confirm you want to add {fullname} to the teacher group?"):
        return False

    success = user_utils.add_user_to_group(username, TEACHER_GROUP)

    if success:
        success = user_utils.add_user_to_group(username, USB_ACCESS_GROUP)

    return success
