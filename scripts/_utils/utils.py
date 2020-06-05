import pwd
from urllib.error import URLError
from urllib.request import urlopen
from subprocess import run


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


def get_users_name(username: str):
    """Returns the first and last name (per gecos field) for a given username
    https://docs.python.org/3/library/pwd.html

    Arguments:
        username {str} -- ldap username

    Returns:
        [str] -- The user's Name (in gecos field) if they exist, else None if username doesn't exist
    """
    try:
        return pwd.getpwnam(username).pw_gecos
    except KeyError:
        print(f"Can't find that username: {username}")
        return None


def host_exists(hostname, verbose=True):
    ping_cmd = ['ping', '-c 1', '-W 1', hostname]  # ping once with 1 second wait/time out
    if verbose:
        print_warning("Checking to see if {} is connected to the network.".format(hostname))

    compeleted = run(ping_cmd)

    if compeleted.returncode != 0:  # not success
        if verbose:
            print_error("{} was not found on the network.  Is there a typo? Is the computer on?".format(hostname))
        return False
    else:
        if verbose:
            print_success("{} found on the network.".format(hostname))
        return True


def input_plus(prompt, default=None, validation_method=None):
    """ Gets styled user input with a defualt value and option to quit """
    hints_str = "[q]uit"

    if default:
        hints_str += f" | [Enter] = {default}"

    prompt = prompt + " (" + hints_str + "): "
    response = input_styled(prompt).strip()
    if response == "":  # they just hit enter for default, or None
        return default
    else:
        return response  # could be "q" to quit
