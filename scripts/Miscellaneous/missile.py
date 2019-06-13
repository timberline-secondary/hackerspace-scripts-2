from scripts._utils import utils
import os

def missile():
    utils.print_styled(utils.ByteStyle.BOLD, "Activating missile launcher.")
    os.system('su -c "sudo -S ./.launchStage2.sh" -m hackerspace_admin')