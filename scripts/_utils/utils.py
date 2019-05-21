import os
from urllib.error import URLError
from urllib.request import urlopen


class ByteStyle:
    HEADER = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_styled(color, text):
    print(color + text + ByteStyle.ENDC)


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



