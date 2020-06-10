
from scripts._utils import utils
from scripts._utils.ssh import SSH


HOSTNAME = 'tyrell'
SERVER_USERNAME = 'hackerspace_admin'


def create_downloads():

    ssh_connection = SSH(HOSTNAME, SERVER_USERNAME)

    response = ssh_connection.send_cmd('getent passwd {16000..20000}', sudo=True)

    user_list = response.splitlines()
    for username_line in user_list:
        username = username_line.split(":")[0]
        print(username)
        if utils.user_exists(username):
            dls = f"/nfshome/{username}/Downloads"
            if ssh_connection.file_exists(f"/nfshome/{username}"):
                if not ssh_connection.file_exists(dls):
                    print("home drive exists, make Download?")
                    # input()
                    ssh_connection.send_cmd(f"mkdir {dls}", sudo=True)
                    ssh_connection.send_cmd(f"chown {username}:students {dls}", sudo=True)
                else:
                    print("Downloads already exists, skipping...")
            else:
                print("no home dir, skipping")
