import pwd
import magic
from urllib.error import URLError
from urllib.request import urlopen
import subprocess

# from getpass import getpass

LOCALDOMAIN = "hackerspace.tbl"


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


def verify_mimetype(file_url, mimetype_string, local=False):
    if mimetype_string is None:
        print_error(" This media type is not supported.")
        return False

    file_url = file_url.strip()

    if local:
        try: 
            mt = magic.from_file(file_url, mime=True)
        except FileNotFoundError as e:
            print("Can't find this file.")
            print_error(str(e))          
    else:  # web url
        try:
            with urlopen(file_url) as response:
                mt = response.info().get_content_type()
        except ValueError as e:
            print_error(str(e))
        except URLError as e:
            print("That is a bad URL.")
            print_error(str(e))

    if mt == mimetype_string:
        print_success(f"File looks good: {mt}")
        return True
    else:
        print_error(f"Something is funky about this file. I expected type '{mimetype_string}' but got '{ct}'.")
        return False


def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def get_valid_hostname(computer_number=None):
    good_host = False
    while not good_host:
        if computer_number:
            computer_host = "tbl-h10-{}".format(computer_number)
        else:
            computer_host = input_styled("Which computer? (e.g. 'tbl-h10-12', or '192.168.3.125' or [q]uit) ")

        if computer_host == 'q':
            print("Quitting this.")
            return None

        good_host = host_exists(computer_host)

        if computer_number and not good_host:  # this computer # doesn't exist or can't connect
            return None

        if good_host:
            return computer_host


def host_exists(hostname, verbose=True, use_fqdn=True):
    if use_fqdn:
        hostname_2 = get_fqdn(hostname)
    else:
        hostname_2 = hostname

    ping_cmd = ['ping', '-c 1', '-W 1', hostname_2]  # ping once with 1 second wait/time out
    if verbose:
        print_warning("Checking to see if {} is connected to the network.".format(hostname_2))

    compeleted = subprocess.run(ping_cmd)

    if compeleted.returncode != 0:  # not success
        # Try again without fqdn, just in case
        if use_fqdn:
            return host_exists(hostname, verbose=True, use_fqdn=False)

        if verbose:
            print_error("{} was not found on the network.  Is there a typo? Is the computer on?".format(hostname))
        return False
    else:
        if verbose:
            print_success("{} found on the network.".format(hostname))
        return True


def get_fqdn(hostname):
    """ Appends the local domain "hackerspace.tbl" if it isn't already there """
    if LOCALDOMAIN not in hostname:
        hostname = f"{hostname}.{LOCALDOMAIN}"
    return hostname


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
