import os, socket
from getpass import getpass
from scripts._utils.ssh import SSH
from scripts._utils import utils

username = "hackerspace_admin"

def reinstall_graphics_drivers():
    password = getpass("Enter the admin password: ")
    numbers = utils.input_styled("Enter the computer numbers, seperated by spaces (where # is from hostname tbl-h10-#-s e.g: 2 15 30): ")

    num_list = numbers.split()

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
    
        good_host = False
        computer_host = "tbl-h10-{}-s".format(num)

        good_host = utils.host_exists(computer_host)

        if not good_host: # this computer # doesn't exist or can't connect
            utils.print_error("Host not found.  Does that computer exist? Is it on?")
            continue

        # now that we know we have a good host, ssh into it and try to run puppet
        ssh_connection = SSH(computer_host, username, password)

        nvidia_cmd = "bash /opt/NVIDIA-Linux-x86_64-430.50.run --disable-nouveau --run-nvidia-xconfig --no-x-check --silent"
        utils.print_warning = "Running command: {}".format(nvidia_cmd)
        utils.print_warning = "This may take a minute..."
        output = ssh_connection.send_cmd(nvidia_cmd, sudo=True)

        if "ERROR" in output:
            utils.print_error("It looks like something went wrong. Sorry!")
            print(output)
        else:
            utils.print_success("It looks like it worked.  Don't worry about those warnings.  I'm going to try to restart computer #{}".format(num))
            output = ssh_connection.send_cmd("/sbin/shutdown -r now", sudo=True)

        utils.print_success("\nComplete\n\n")
        ssh_connection.close()