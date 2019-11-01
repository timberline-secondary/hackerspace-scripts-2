import os, socket
from getpass import getpass
from scripts._utils import utils
from scripts.Workstation_Management.puppet_run import puppet_run

def quick_puppet_run(auto_fix_certificates=False, computer_number=None):
    password = getpass("Enter the admin password: ")
    numbers = utils.input_styled("Enter the computer numbers, seperated by spaces (where # is from hostname tbl-h10-#-s e.g: 2 15 30): ")

    num_list = numbers.split()

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        puppet_run(num, password, auto_fix_certificates=True)
    
    return