from scripts._utils import ssh, pi, utils

hostname = "pi-projector"


def flex_schedule_off():
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)
    error = ssh_connection.send_cmd("rm /home/pi/clock/public/flex-toggle")
    if error != '':
        utils.print_success("Flex schedule is already OFF")
    else:
        utils.print_success("Flex schedule is now OFF")
        if utils.confirm("Clock requires a reboot to update; would you like to reboot now?"):
            pi.reboot_pi(hostname)
    ssh_connection.close()
