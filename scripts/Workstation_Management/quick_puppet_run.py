import os, socket
from getpass import getpass
from scripts._utils import utils
from scripts.Workstation_Management.puppet_run import puppet_run

def quick_puppet_run(auto_fix_certificates=False, computer_number=None):
    password = getpass("Enter the admin password: ")
    number = utils.input_styled("Enter the computer number: ")

    return puppet_run(number, password, auto_fix_certificates=True, )
