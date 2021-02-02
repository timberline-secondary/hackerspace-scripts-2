from scripts._utils import ssh

username = "pi"
password = "hackerberry"

PI_TV_LIST = [
    "pi-tv1",
    "pi-tv2",
    "pi-tv3",
    "pi-tv4",
]

PI_LIST = PI_TV_LIST + [
    "pi-themes",
    "pi-projector"
]


def reboot_pi(hostname):
    ssh_connection = ssh.SSH(hostname, username, password)
    # https://stackoverflow.com/questions/26117712/executing-reboot-command-over-ssh-using-paramiko
    ssh_connection.send_cmd("shutdown -r now", sudo=True)
    ssh_connection.close()

    print("Rebooting... give it a moment to start back up before using.")
