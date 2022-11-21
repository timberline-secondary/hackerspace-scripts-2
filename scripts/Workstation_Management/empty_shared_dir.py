import inquirer
from getpass import getpass
from humanize import naturalsize

from scripts._utils import utils
from scripts._utils.ssh import SSH

username = 'hackerspace_admin'
computer_host = None


def get_size(file, ssh_connection) -> str:
    try:
        file_size = ssh_connection.send_cmd(f"du /shared/{file} -s 2>/dev/null", print_stdout=False)
        return naturalsize(int(file_size.split("\t")[0]) * 1000)
    except:
        return "-- bytes"


def empty_command(computer_number=None, password=None):
    computer_host = utils.get_valid_hostname(computer_number)

    if computer_host is None:
        return

    # now that we know we have a connected computer, ssh into it and try to run command
    ssh_connection = SSH(computer_host, username, password)

    if not ssh_connection.is_connected():
        utils.print_warning("\nComputer is online, but can't connect. Maybe it's mining?\n")
        return False

    # get all dirs within /shared
    dirs = ssh_connection.send_cmd("dir /shared -m", print_stdout=False)

    # format the dirs names from /shared/<dir_name>/r/n -> <dir_name>, and add folder size with purple colour
    dirs = [n.strip() for n in dirs[:-2].split(",")]
    dir_list = [f"{dir_name} {utils.ByteStyle.HEADER}({get_size(dir_name, ssh_connection)}){utils.ByteStyle.ENDC}" for dir_name in dirs]

    questions = [
        inquirer.Checkbox('dirs',
                          message="Which would you like to empty? To select use arrow keys ←/→ and ENTER to confirm",
                          choices=[*dir_list, "ALL", "[Quit]"],
                          ),
    ]

    options = inquirer.prompt(questions)["dirs"]

    # Test for quit and ALL first
    if "[Quit]" in options or options == []:
        return False
    elif "ALL" in options:
        command = "rm -rf /shared/*"
    else:
        command = f'rm -rf {" ".join(["/shared/" + dir_name.split(" ")[0] for dir_name in options])}'

    ssh_connection.send_cmd(command, sudo=True)

    # test if still there
    command = f'ls -d {" ".join(["/shared/" + dir_name.split(" ")[0] for dir_name in options])} > /dev/null'
    stdin, stdout, stderr = ssh_connection.client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        utils.print_success("Successfully removed contents.")
    else:
        utils.print_error(f"Couldn't remove the contents of /shared/ for computer {computer_number}.")


def empty_shared_dir():
    password = getpass("Enter the admin password: ")
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
        empty_command(num, password)
