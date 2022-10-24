from getpass import getpass
from scripts._utils import utils
from scripts._utils.ssh import SSH

username = 'hackerspace_admin'
computer_host = None


def empty_command(computer_number=None, password=None):
    computer_host = utils.get_valid_hostname(computer_number)

    if computer_host is None:
        return

    # now that we know we have a connected computer, ssh into it and try to run command
    ssh_connection = SSH(computer_host, username, password)

    if not ssh_connection.is_connected():
        utils.print_warning("\nComputer is online, but can't connect. Maybe it's mining?\n")
        return False

    command = "rm -rf /shared/*"

    ssh_connection.send_cmd(command, sudo=True)
    if ssh_connection.send_cmd("ls /shared/") == "":
        utils.print_success("Successfully removed contents.")
    else:
        utils.print_error(f"Couldn't remove the contents of /shared/ for computer {computer_number}.")


def empty_shared_dir():
    password = getpass("Enter the admin password: ")
    numbers = utils.input_styled("Enter the computer numbers, seperated by spaces \n"
                                 "(where # is from hostname tbl-h10-#-s e.g: 2 15 30)\n"
                                 " or 'all' to run on all computers: ")

    num_list = numbers.split()

    if num_list[0] == "all":
        num_list = [f"{i}" for i in range(0, 32)]  # list of strings.  0 will cause problem if int instead of str

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        empty_command(num, password)
