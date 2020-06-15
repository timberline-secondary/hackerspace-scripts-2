import pwd
from urllib.error import URLError
from urllib.request import urlopen
import subprocess

# from getpass import getpass


class ByteStyle:
    HEADER = '\033[95m'  # intense purple
    SUCCESS = '\033[92m'  # intense green
    WARNING = '\033[93m'  # intense yellow
    ERROR = '\033[91m'  # intense red
    ENDC = '\033[0m'  # resets
    BOLD = '\033[1m'  # makes it bold
    UNDERLINE = '\033[4m'  # underlines
    INPUT = '\033[1;33m'  # bold yellow
    # Y_N = '\033[0;33m'  # dark yellow (brown)
    Y_N = '\033[36m'  # cyan


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
    if len(title) > width - 4:
        title = title[:width - 7] + "..."
    print_styled("#" * width, color=ByteStyle.HEADER)
    print_styled("#" + title.center(width - 2, " ") + "#", color=ByteStyle.HEADER)
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
                print_success("File looks good.")
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


def host_exists(hostname, verbose=True):
    ping_cmd = ['ping', '-c 1', '-W 1', hostname]  # ping once with 1 second wait/time out
    if verbose:
        print_warning("Checking to see if {} is connected to the network.".format(hostname))

    compeleted = subprocess.run(ping_cmd)

    if compeleted.returncode != 0:  # not success
        if verbose:
            print_error("{} was not found on the network.  Is there a typo? Is the computer on?".format(hostname))
        return False
    else:
        if verbose:
            print_success("{} found on the network.".format(hostname))
        return True


def input_plus(prompt, default=None, validation_method=None):
    """ Gets styled user input with a defualt value and option to quit.  Returns 'q' if quitting.
    Validation_method is not yet implemented.
    """
    hints_str = "[q]uit"

    if default:
        hints_str += f" | [Enter] = {default}"

    prompt = prompt + " (" + hints_str + "): "
    response = input_styled(prompt).strip()
    if response == "":  # they just hit enter for default, or None
        return default
    elif response == "q":
        print("quitting...")
        return response 
    else:
        return response


def confirm(prompt, yes_is_default=True):
    """Ask the use to confirm an action (the prompt) with y or n."""

    if yes_is_default:
        yn_prompt = " [y]/n "
    else:
        yn_prompt = " y/[n] "

    do_it = input_styled(prompt + yn_prompt, color=ByteStyle.Y_N)

    if yes_is_default:
        if do_it == "" or do_it[0].lower() != 'n':
            return True
        else:
            return False
    else:
        if do_it == "" or do_it[0].lower() != 'y':
            return False
        else:
            return True


# def get_admin_pw():
#     # ask for admin password
#     while True:
#         password = getpass("Enter admin password: ")
#         print("Give me a moment to check the password...")
#         completed_process = subprocess.run(
#             ["su", "hackerspace_admin", ">", "/dev/null"], 
#             text=True,
#             input=password,
#             capture_output=False)
#         if completed_process.returncode == 0:
#             # it's good
#             return password
#         else:
#             # bad password
#             print_error("Incorrect Password. Try again.")
