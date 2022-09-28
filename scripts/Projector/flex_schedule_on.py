from scripts._utils import ssh, pi, utils

hostname = "pi-projector"


def flex_schedule_on():
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)
    if ssh_connection.file_exists("/home/pi/clock/public/flex-toggle"):
        ssh_connection.send_cmd("touch /home/pi/clock/public/flex-toggle")
        utils.print_success("Flex schedule is now ON")
        if utils.confirm("Clock requires a reboot to update; would you like to reboot now?"):
            pi.reboot_pi(hostname)
    else:
        utils.print_success("Flex schedule is already ON")
    ssh_connection.close()

