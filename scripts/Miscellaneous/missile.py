from scripts._utils import utils
import os
import subprocess
from getpass import getpass

STORM_LAUNCHER_LOCATION = os.environ['HOME']
STORM_LAUNCHER_DIR = '.stormlauncher'
CODE_DIR = 'stormLauncher'

FULL_DIR = STORM_LAUNCHER_LOCATION + os.sep + STORM_LAUNCHER_DIR + os.sep + CODE_DIR


def missile():

    # check if everything is already installed.  If not, install it.
    if not os.path.exists(STORM_LAUNCHER_LOCATION + os.sep + STORM_LAUNCHER_DIR):
        setup_stormLauncher()

    os.chdir(FULL_DIR)
    # pw = utils.get_admin_pw()
    pw = getpass("Enter admin password: ")
    # don't wait for this to finish before continuing, i.e. run in background
    command = 'su -c "echo {} | sudo -S /bin/bash launch.sh" -m hackerspace_admin'.format(pw)
    # os.system(command)
    subprocess.run([command, "/dev/null"], shell=True, check=True, text=True, input=pw)
    # proc = subprocess.Popen(command, shell=True, text=True)
    # proc.communicate(pw)

    # doesn't go back to control panel gracefully... prolly because virtualenv is still active for launcher
    quit()


def setup_stormLauncher():
    utils.print_warning("\nSTORMLAUNCHER has not been installed on this profile yet.  I'm gonna install it for you now...\n")
    os.chdir(STORM_LAUNCHER_LOCATION)
    os.mkdir(STORM_LAUNCHER_DIR)
    os.chdir(STORM_LAUNCHER_DIR)
    subprocess.run("git clone https://github.com/timberline-secondary/stormLauncher.git", shell=True, check=True)
    os.chdir(CODE_DIR)
    print(os.getcwd())
    # create virtual environment and install dependancies to it so launch script works
    subprocess.run("bash setup.sh", shell=True, check=True)
    utils.print_warning("\n...Install complete. LETS DO THIS!\n")
