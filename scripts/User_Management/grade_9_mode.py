from scripts._utils import ssh, pi, utils

host_themes = "pi-themes"
tvs = ["1", "2", "3", "4"]

TV_OFF_CMD = "echo standby 0 | cec-client -s -d 1"
TV_ON_CMD = "echo on 0 | cec-client -s -d 1"


def engage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 0%")

    for tv_number in tvs:
        hostname = "pi-tv{}".format(tv_number)
        ssh_connection = ssh.SSH(hostname, pi.username, pi.password)

        ssh_connection.send_cmd(TV_OFF_CMD)
        ssh_connection.close()


def disengage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 100%")

    for tv_number in tvs:
        hostname = "pi-tv{}".format(tv_number)
        ssh_connection = ssh.SSH(hostname, pi.username, pi.password)

        ssh_connection.send_cmd(TV_ON_CMD)
        ssh_connection.close()


def grade_9_mode():
    confirmation = utils.input_styled("Do you want to engage grade 9s? [y/N] (q to quit): \n")
    if confirmation and confirmation[0].lower() == "y":
        engage()
    elif confirmation == "q":
        return False
    else:
        disengage()
