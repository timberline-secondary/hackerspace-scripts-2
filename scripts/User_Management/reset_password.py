import os, socket
from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management._utils import get_and_confirm_user

hostname = socket.gethostname() # can use the local computer
username = 'hackerspace_admin'
default_pw = 'wolf'

def reset_password():
    # student_number = utils.input_styled(
    #     'Enter the student number of the student whose password you want to reset to "{}": '.format(default_pw))

    password = getpass("Enter the admin password: ")

    print("Who's password do you want to reset?")

    student_number = get_and_confirm_user(password)
    
    ssh_connection = SSH(hostname, username, password)

    prompt_string = "{}@{}:~$".format(username, hostname)
    command_response_list = [
                                ("sudo passwd {}".format(student_number), "[sudo] password for {}:".format(username), None),
                                (password, "New password: ", None),
                                ("wolf", "Re-enter new password: ", None),
                                ("wolf", prompt_string, "password updated successfully"),
                            ]
    success = ssh_connection.send_interactive_commands(command_response_list)

    if success:
        utils.print_success("Password for {} successfully reset to {}".format(student_number, default_pw))
    else:
        utils.print_error("Something went wrong...")

    ssh_connection.close()