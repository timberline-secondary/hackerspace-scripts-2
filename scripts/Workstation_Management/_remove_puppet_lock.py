import re
# from getpass import getpass
# from scripts._utils import utils
# from scripts.Workstation_Management.puppet_run import puppet_run


def remove_puppet_lock(ssh_connection, password=None, ):

    # check when last puppet run was by reading motd
    motd = ssh_connection.send_cmd('cat /etc/motd')

    print(motd)

    pattern = r"Last run: (.*)$"

    time_str = re.search(pattern, motd)

    print("MOTD: ", time_str)

    return False
