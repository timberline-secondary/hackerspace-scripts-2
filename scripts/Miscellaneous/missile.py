from scripts._utils import utils
import os

def missile():
    utils.print_styled(utils.ByteStyle.BOLD, "Activating missile launcher.")
    dir = os.getcwd()
    command = 'su -c "sudo -S {}/_launchStage2.sh" -m hackerspace_admin'.format(dir)
    os.system(command)