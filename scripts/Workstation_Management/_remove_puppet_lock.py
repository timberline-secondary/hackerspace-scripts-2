import re
from datetime import datetime
# from getpass import getpass
# from scripts._utils import utils
# from scripts.Workstation_Management.puppet_run import puppet_run
LOCK_PATH = "/var/cache/puppet/state/"
LOCK_FILE = "agent_catalog_run.lock"


def remove_puppet_lock(ssh_connection, password=None, ):

    # check when last puppet run was by reading motd
    motd = ssh_connection.send_cmd('cat /etc/motd')

    pattern = r"Last run: (.*)"

    time_str = re.search(pattern, motd.strip())

    if time_str is None:
        print("Not sure what's going on, I didn't find a time stamp in /etc/motd.")
        return False

    time_str = time_str.group(1)
    dt = datetime.strptime(time_str, "%a %d %b %Y %H:%M:%S %p %Z")

    print("Time of last puppet run: ", dt)

    time_since_last_puppet_run = datetime.now() - dt  # timedelta

    # should run every 30 minutes, but give 2 hours to be safe
    if time_since_last_puppet_run.seconds < 7200:
        return False

    print("Been more than 2 hours, so checking if puppet is locked...")
    if not ssh_connection.file_exists(LOCK_PATH, LOCK_FILE):
        return False

    print("FOUND LOCK FILE, REMOVING IT")

    ssh_connection.send_cmd(f"rm {LOCK_PATH}{LOCK_FILE}", sudo=True)

    if not ssh_connection.file_exists(LOCK_PATH, LOCK_FILE):
        print("***REMOVED***")
        return True
    else:
        print("***FAILED TO REMOVE***")
        return False
