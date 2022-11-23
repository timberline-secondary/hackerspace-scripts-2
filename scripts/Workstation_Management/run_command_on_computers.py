from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH

username = 'hackerspace_admin'
computer_host = None


def run_command(computer_number=None, password=None, command=None, sudo=True):
    computer_host = utils.get_valid_hostname(computer_number)

    if command is None:
        return False, computer_host

    if computer_host is None:
        return False, "unknown host"

    # now that we know we have a connected computer, ssh into it and try to run command
    ssh_connection = SSH(computer_host, username, password)

    if not ssh_connection.is_connected():
        utils.print_warning("\nComputer is online, but can't connect. Maybe it's mining?\n")
        return False, computer_host

    # run command
    if type(command) == list:
        outputs = []
        for cmd in command:
            stdout = ssh_connection.send_cmd(cmd, sudo=sudo, print_stdout=False)
            outputs.append(stdout)

        return outputs, computer_host
    else:
        stdout = ssh_connection.send_cmd(command, sudo=sudo, print_stdout=False)
        return stdout, computer_host


def run_command_on_computers(print_stdout=True, sudo=False):
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

    outputs = []

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        output, computer = run_command(num, password, command, sudo=sudo)
        outputs.append({"name": computer, "output": output})

    if print_stdout:
        print(outputs)
        for com in outputs:
            utils.print_success(f"\nRan command with output of:\n")
            print("=" * 10 + f" {com['name']} " + "=" * 10 + ">\n")
            if type(com["output"]) == list:
                for out in com["output"]:
                    print(out)
            else:
                print(com["output"])
            print("<" + "=" * 30)
