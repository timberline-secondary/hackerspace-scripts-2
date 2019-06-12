import os
from urllib.error import URLError
from urllib.request import urlopen


class ByteStyle:
    HEADER = '\033[95m'  # intense purple
    SUCCESS = '\033[92m'  # intense green
    WARNING = '\033[93m'  # intense yellow
    FAIL = '\033[91m'  # intense red
    ENDC = '\033[0m'  # resets
    BOLD = '\033[1m'  # makes it bold
    UNDERLINE = '\033[4m'  # underlines
    INPUT = '\033[1;33m'  # bold yellow
    Y_N = '\033[0;33m'  # dark yellow (brown)


def print_styled(color, text):
    print(color + text + ByteStyle.ENDC)


def input_styled(color, text):
    return input(color + text + ByteStyle.ENDC).strip()


def print_heading(title):
    width = 60
    title = title.upper()
    cwd = os.getcwd()
    if len(title) > width-4:
        title = title[:width-7] + "..."
    print_styled(ByteStyle.HEADER, "#" * width)
    print_styled(ByteStyle.HEADER, "#" + title.center(width-2, " ") + "#")
    # print_styled(ByteStyle.HEADER, "#" + cwd.center(width-2, " ") + "#")
    print_styled(ByteStyle.HEADER, "#" * width)
    print()


def verify_mimetype(file_url, mimetype_string):
    file_url = file_url.strip()
    try:
        with urlopen(file_url) as response:
            ct = response.info().get_content_type()
            if ct == mimetype_string:
                print_styled(ByteStyle.SUCCESS, "File looks good.")
                return True
            else:
                print_styled(ByteStyle.FAIL,
                             "Something is funky about this file. I expected type '{}' but got '{}'."
                                .format(mimetype_string, ct))
    except ValueError as e:
        print_styled(ByteStyle.FAIL, str(e))
    except URLError as e:
        print('That is a bad URL.')
        print_styled(ByteStyle.FAIL, str(e))

    return False



