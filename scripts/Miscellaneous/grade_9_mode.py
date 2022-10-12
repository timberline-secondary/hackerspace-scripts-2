from scripts._utils import ssh, pi, utils

host_themes = "pi-themes"
tvs = ["1", "2", "3", "4"]

TV_OFF_CMD = "echo standby 0 | cec-client -s -d 1"
TV_ON_CMD = "echo on 0 | cec-client -s -d 1"


def send_tvs_command(command):
    for tv_number in tvs:
        hostname = "pi-tv{}".format(tv_number)
        ssh_connection = ssh.SSH(hostname, pi.username, pi.password)

        ssh_connection.send_cmd(command)
        ssh_connection.close()


def engage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 0%")

    send_tvs_command(TV_OFF_CMD)


def disengage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 100%")

    send_tvs_command(TV_ON_CMD)


def grade_9_mode():
    confirmation = utils.input_styled("Do you want to engage grade 9s? [e]ngage/[D]isengage (q to quit): \n")
    if confirmation and confirmation[0].lower() == "e":
        engage()
    elif confirmation and confirmation[0].lower() == "q":
        return False
    else:
        disengage()
