import os


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



