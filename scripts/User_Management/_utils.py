import os, socket
from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH

def get_student_name(student_number, password=None):
    """Get a student's full name from their student number.  Return None if account doesn't exist.
    
    Arguments:
        student_number {str} -- username
    
    Keyword Arguments:
        password {str} -- admin password
    
    Returns:
        str -- student's full name, or None is student doesn't exist.
    """

    hostname = socket.gethostname() # can use the local computer
    username = 'hackerspace_admin'
    if not password:
        password = getpass("Enter the admin password: ")

    ssh_connection = SSH(hostname, username, password, verbose=False)

    # the ^ is regex for "starting with", and after the username should be a colon :
    # this ensures unique results
    command = "getent passwd | grep ^{}:".format(student_number)
    result = ssh_connection.send_cmd(command, sudo=True, print_stdout=False)

    ssh_connection.close()
    
    # results example, split on colons
    #  *****
    #  [sudo] password for hackerspace_admin: 
    #  9912345:x:16000:16000:John Doe:/home/9912345:/bin/bash

    user_info_list = result.split(':')

    # no user info returned, doesn't exist
    if len(user_info_list) == 2:
        return None
    else:
        return user_info_list[5]

def get_and_confirm_user(password=None):
    student = None
    while student is None:
        student_number = utils.input_styled("Enter student number: \n")
        if password is None:
            password = getpass("Enter the admin password: ")
        
        student = get_student_name(student_number, password)

        if student is not None:
            confirm = utils.input_styled("Confirm account: {}, {}? [y]/n".format(student_number, student))
            if confirm == 'n':
                student = None
            else:
                return student_number
        
            
#####################################
# /nfshome/makehomedirs.sh
# #!/bin/bash
# if [ $# -lt 1 ]; then
#     echo "Syntax: $_ USER[ USER[ ...]]" >&2
#     exit 1
# fi

# exit_code=0

# for user in "$@"; do
#     home="/nfshome/$user"
    
#     # Check whether user account exists first
#     USEREXISTS=$(getent passwd | grep ^$user:)
#     if [ ! "$USEREXISTS" ]; then
# 	echo $'\e[31m'"User does not exist: $user"$'\e[m'
#     elif [ -d "$home" ]; then
# 	echo $'\e[31m'"Home drive already exists: $home"$'\e[m'
#     else
# 	group="students"
#         cp -R /etc/skel "$home" && echo $'\e[32m'"Copied skeleton to: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to create: $home"$'\e[m' ) >&2
#         chown -R "$user:$group" "$home" && echo $'\e[32m'"Set owner on: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to set owner on: $home"$'\e[m' ) >&2
#     fi
# done
