

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
    title = title.upper()
    if len(title) > 46:
        title = title[:43] + "..."
    print_styled(ByteStyle.HEADER, "#" * 50)
    print_styled(ByteStyle.HEADER, "#" + title.center(48, " ") + "#")
    print_styled(ByteStyle.HEADER, "#" * 50)
    print()



