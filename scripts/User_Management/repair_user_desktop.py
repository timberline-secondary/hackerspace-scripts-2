import os
from urllib.parse import urlparse

from scripts._utils.utils import input_styled, print_warning, print_success, print_error
from scripts._utils.ssh import SSH

hostname = 'tyrell'
username = 'hackerspace_admin'

def repair_user_desktop():
    ssh_connection = SSH(hostname, username)
    print_warning("Make sure the student is logged out before running this repair.\n")
    student_number = input_styled("Enter username: \n")

    home_dir = "/nfshome/{}".format(student_number)

    # First, make sure their home drive exists.  Sometimes home drive creation fails when
    # creating new users in bulk!
    if ssh_connection.dir_exists(home_dir):
        command = "rm -r {}/.cache".format(home_dir)
        ssh_connection.send_cmd(command, sudo=True)
        print("I tried to delete their cache.  That usually solves the problem...")
        print_success("Have the student try logging in again.")
    else:
        # no home drive!  Need to make it
        print_warning("AH!  It appears they don't have a home drive! I gonna try to create one for them now...")
        command = "bash /nfshome/makehomedirs.sh {}".format(student_number)
        ssh_connection.send_cmd(command, sudo=True)
        print_success("Have the student try logging in again.")
        

    ssh_connection.close()