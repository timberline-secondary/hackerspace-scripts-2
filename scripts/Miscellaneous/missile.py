from scripts._utils import utils
import os

def missile():
    utils.print_styled(utils.ByteStyle.BOLD, "Activating missile launcher.")
    os.system('sudo su root -c "source /root/pyusb/bin/activate/ && cd /root/pyusb && python stormLauncher.py && deactivate"')