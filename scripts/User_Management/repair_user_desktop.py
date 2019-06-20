import os
from urllib.parse import urlparse

from scripts._utils.utils import input_styled, print_warning, print_success, check_student_number
from scripts._utils.ssh import SSH

hostname = 'tyrell'
username = 'hackerspace_admin'

def repair_user_desktop():
    ssh_connection = SSH(hostname, username)
    print_warning("Make sure the student is logged out before running this repair.\n")
    student_number = input_styled("Enter Student Number: \n")

    command = "rm -r /nfshome/{}/.cache".format(student_number)
    ssh_connection.send_cmd(command, sudo=True)

    print_success("Have the student log in again. Their cache should be cleared now.")