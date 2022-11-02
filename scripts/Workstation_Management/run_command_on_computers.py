from getpass import getpass

import inquirer

from scripts._utils import utils
from scripts._utils.ssh import SSH

username = 'matthew.baker'
computer_host = None


def run_command(computer_number=None, password=None, command=None):
    computer_host = utils.get_valid_hostname(computer_number)

    if command is None:
        return

    if computer_host is None:
        return

    # now that we know we have a connected computer, ssh into it and try to run command
    ssh_connection = SSH(computer_host, username, password)

    if not ssh_connection.is_connected():
        utils.print_warning("\nComputer is online, but can't connect. Maybe it's mining?\n")
        return False

    # run command
    stdout = ssh_connection.send_cmd(command, print_stdout=False)
    utils.print_success(f"\nRan command with output of:\n")
    print("="*20 + ">\n")
    print(stdout)
    print("<" + "=" * 20)


def run_command_on_computers():
    password = getpass("Enter the admin password: ")
    command = utils.input_plus("Enter the command to run")
    numbers = utils.input_styled("Enter the computer numbers, seperated by spaces \n"
                                 "(where # is from hostname tbl-h10-#-s e.g: 2 15 30)\n"
                                 " or 'all' to run on all computers: ")

    num_list = numbers.split()

    if num_list == "":
        return

    if num_list[0] == "all":
        num_list = [f"{i}" for i in range(0, 32)]  # list of strings.  0 will cause problem if int instead of str

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        run_command(num, password, command)
