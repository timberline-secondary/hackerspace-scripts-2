from scripts._utils import utils
from getpass import getpass
import os

def missile():
    utils.print_styled(utils.ByteStyle.BOLD, "Activating missile launcher.")
    # password = getpass(utils.print_styled(utils.ByteStyle.INPUT, "Enter sudo password to continue: \n"))
    os.system("sudo su - && source /root/pyusb/bin/activate/ && cd /root/pyusb && python stormLauncher.py && deactivate")