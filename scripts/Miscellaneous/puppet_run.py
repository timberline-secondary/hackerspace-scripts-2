import os, socket
from getpass import getpass
from subprocess import run

from scripts._utils import utils
from scripts._utils.ssh import SSH


server_host = 'puppet'
username = 'hackerspace_admin'
computer_host = None

def puppet_run():
    password = getpass("Enter the admin password: ")

    good_host = False
    while not good_host:
        computer_host = utils.input_styled("Which computer? (e.g. 'tbl-h10-12-s', or [q]uit) ")

        if computer_host == 'q':
            print("Quitting this.")
            return

        ping_cmd = ['ping', '-c 1', '-W 1', computer_host] # ping once with 1 second wait/time out
        utils.print_warning("Checking to see if {} is connected to the network.".format(computer_host))

        compeleted = run(ping_cmd)

        if compeleted.returncode != 0: # not success
            utils.print_error("{} was not found on the network.  Is there a typo? Is the computer on?".format(computer_host))
        else:
            utils.print_success("{} found on the network.".format(computer_host))
            good_host = True

    
    # now that we know we have a connected computer, ssh into it and try to run puppet
    # ssh_connection = SSH(computer_host, username, password)


        
    print("That's it for now")




        

        
        # ssh_connection = SSH(hostname, username, password)

    

    # prompt_string = "{}@{}:~$".format(username, hostname)
    # command_response_list = [
    #                             ("sudo passwd {}".format(student_number), "[sudo] password for {}:".format(username), None),
    #                             (password, "New password: ", None),
    #                             ("wolf", "Re-enter new password: ", None),
    #                             ("wolf", prompt_string, "password updated successfully"),
    #                         ]
    # success = ssh_connection.send_interactive_commands(command_response_list)

    # if success:
    #     utils.print_success("Password for {} successfully reset to {}".format(student_number, default_pw))
    # else:
    #     utils.print_error("Something went wrong...")

    # ssh_connection.close()