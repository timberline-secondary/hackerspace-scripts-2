import subprocess

from scripts._utils import utils
from scripts._utils.pi import PI_LIST


def check_for_disconnected_pis(password=None):
    # if password is None:
    #     password = getpass("Enter the admin password: ")

    # https://itsfoss.com/how-to-find-what-devices-are-connected-to-network-in-ubuntu/
    cmd = ["nmap", "-sn", "192.168.43.0/24"]
    output = subprocess.run(cmd, capture_output=True, text=True).stdout

    # run twice, cus the pis seem to get sleepy and don't show up the first time, sometimes?!
    output = subprocess.run(cmd, capture_output=True, text=True).stdout
    found_at_least_one = False
    for pi in PI_LIST:
        if pi not in output:
            utils.print_warning(f"Pi named '{pi}' was not found connected to the network.")
            found_at_least_one = True

    if not found_at_least_one:
        utils.print_success(f"All the pis were found on the network:")
        print(f"\t{str(PI_LIST)}")
