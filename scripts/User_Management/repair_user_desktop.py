import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH

hostname = 'tyrell'
username = 'hackerspace_admin'

def repair_user_desktop():
    ssh_connection = SSH(hostname, username)
    ssh_connection.connect()
    utils.print_warning("Make sure the student is logged out before running this repair.\n")
    student_number = utils.input_styled("Enter Student Number: \n")

    command = "sudo rm -r /nfshome/{}/.cache".format(student_number)
    ssh_connection.send_cmd(command, sudo=True, print_stdout=True)

    input("Hit enter to continue.\n")