import os
import pwd
from urllib.error import URLError
from urllib.request import urlopen


class ByteStyle:
    HEADER = '\033[95m'  # intense purple
    SUCCESS = '\033[92m'  # intense green
    WARNING = '\033[93m'  # intense yellow
    ERROR = '\033[91m'  # intense red
    ENDC = '\033[0m'  # resets
    BOLD = '\033[1m'  # makes it bold
    UNDERLINE = '\033[4m'  # underlines
    INPUT = '\033[1;33m'  # bold yellow
    Y_N = '\033[0;33m'  # dark yellow (brown)


def print_styled(text, color):
    print(color + text + ByteStyle.ENDC)

def print_success(text):
    print_styled(text, color=ByteStyle.SUCCESS)

def print_warning(text):
    print_styled(text, color=ByteStyle.WARNING)

def print_error(text):
    print_styled(text, color=ByteStyle.ERROR)

def input_styled(text, color=ByteStyle.INPUT):
    return input(color + text + ByteStyle.ENDC).strip()


def print_heading(title):
    width = 60
    title = title.upper()
    if len(title) > width-4:
        title = title[:width-7] + "..."
    print_styled("#" * width, color=ByteStyle.HEADER)
    print_styled("#" + title.center(width-2, " ") + "#", color=ByteStyle.HEADER)
    print_styled("#" * width, color=ByteStyle.HEADER)
    print()


def verify_mimetype(file_url, mimetype_string):
    if mimetype_string is None:
        print_error(" This media type is not supported.")
        return False
        
    file_url = file_url.strip()
    try:
        with urlopen(file_url) as response:
            ct = response.info().get_content_type()
            if ct == mimetype_string:
                print_success( "File looks good.")
                return True
            else:
                print_error("Something is funky about this file. I expected type '{}' but got '{}'.".format(mimetype_string, ct))
    except ValueError as e:
        print_error(str(e))
    except URLError as e:
        print('That is a bad URL.')
        print_error(str(e))

    return False

def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

# def check_student_number(student_number):
#     # this doesn't work, needs sudo to get other users.
#     verify_student = os.system("getent passwd | grep {}".format(student_number))
#     print(verify_student)
#     return verify_student