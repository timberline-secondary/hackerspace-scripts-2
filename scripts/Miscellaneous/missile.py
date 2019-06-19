from scripts._utils import utils
import os

def missile():
    utils.print_styled("Activating missile launcher.", utils.ByteStyle.BOLD)
    dir = os.getcwd()
    command = 'su -c "sudo -S /bin/sh {}/_launchStage2.sh" -m hackerspace_admin'.format(dir)
    os.system(command)