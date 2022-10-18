import threading

from scripts.TVs._utils import valid_tvs, TV_OFF_CMD, TV_ON_CMD
from scripts._utils import ssh, pi, utils

host_themes = "pi-themes"


def tv_thread(command, tv_number):
    hostname = "pi-tv{}".format(tv_number)
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)

    ssh_connection.send_cmd(command)
    ssh_connection.close()


def send_tvs_command(command):
    global thread

    for tv_number in valid_tvs:
        thread = threading.Thread(target=tv_thread, args=(command, tv_number,))
        thread.start()

    # wait for threads to finish
    thread.join()


def engage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 0%")

    send_tvs_command(TV_OFF_CMD)


def disengage():
    ssh_connection = ssh.SSH(host_themes, pi.username, pi.password)
    ssh_connection.send_cmd("amixer sset 'Headphone',0 100%")

    send_tvs_command(TV_ON_CMD)


def grade_9_mode():
    utils.print_warning("Engaging grade 9 mode will:\n- Turn off TVs\n- Mute theme player\n")
    confirmation = utils.input_styled("Do you want to engage grade 9s? [e]ngage/[D]isengage (q to quit): ")
    if confirmation and confirmation[0].lower() == "e":
        engage()
    elif confirmation and confirmation[0].lower() == "q":
        return False
    else:
        disengage()
