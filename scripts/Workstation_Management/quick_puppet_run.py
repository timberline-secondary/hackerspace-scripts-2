from getpass import getpass
from scripts._utils import utils
from scripts.Workstation_Management.puppet_run import puppet_run


def quick_puppet_run(auto_fix_certificates=False, computer_number=None):
    password = getpass("Enter the admin password: ")
    numbers = utils.input_styled("Enter the computer numbers, seperated by spaces \n"
                                 "(where # is from hostname tbl-h10-#-s e.g: 2 15 30)\n"
                                 " or 'all' to run on all computers: ")

    num_list = numbers.split()

    if num_list[0] == "all":
        num_list = [f"{i}" for i in range(0, 32)]  # list of strings.  0 will cause problem if int instead of str

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        puppet_run(num, password, auto_fix_certificates=True)
