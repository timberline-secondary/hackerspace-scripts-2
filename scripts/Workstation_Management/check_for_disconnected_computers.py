import subprocess

from scripts._utils import utils

FIRST = 0
LAST = 30


def check_for_disconnected_computers(password=None):
    # if password is None:
    #     password = getpass("Enter the admin password: ")

    computer_numbers = range(FIRST, LAST + 1)

    # https://itsfoss.com/how-to-find-what-devices-are-connected-to-network-in-ubuntu/
    # cmd = ["nmap -sn 192.168.43.0/24 | grep 'tbl-h10' | sort"]
    # output = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
    cmd = ["nmap", "-sn", "192.168.43.0/24"]
    output = subprocess.run(cmd, capture_output=True, text=True).stdout

    found_at_least_one = False
    for i in computer_numbers:
        host = f'tbl-h10-{i}'
        if host not in output:
            utils.print_warning(f"Computer {host} was not found on the network.")
            found_at_least_one = True

    if not found_at_least_one:
        utils.print_success(f"All computers from tbl-h10-{FIRST} to tbl-h10-{LAST} were found on the network.")
