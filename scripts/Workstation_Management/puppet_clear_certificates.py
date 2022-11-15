from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH

puppet_host = 'puppet'
username = 'hackerspace_admin'


def puppet_command(computer_number, password):
    computer_host = utils.get_valid_hostname(computer_number)

    if computer_host is None:
        return

    remove_server_cert_cmd = "/opt/puppetlabs/bin/puppetserver ca clean --certname {}.hackerspace.tbl".format(computer_host)

    # now that we know we have a connected computer, ssh into it and try to run command
    ssh_connection_puppet = SSH(puppet_host, username, password)

    if not ssh_connection_puppet.is_connected():
        utils.print_warning("\nComputer is online, but can't connect. Maybe it's mining?\n")
        return False

    # run command
    ssh_connection_puppet.send_cmd(remove_server_cert_cmd, sudo=True)
    ssh_connection_puppet.close()

    utils.print_warning("Ok, I tried to remove the old certificates from the puppet server.")


def puppet_clear_certificates(hostname=None, password=None):
    if password is None:
        password = getpass("Enter the admin password: ")

    if hostname is None:
        hostname = utils.input_styled("Enter the computer numbers, seperated by spaces \n"
                                     "(where # is from hostname tbl-h10-#-s e.g: 2 15 30)\n"
                                     " or 'all' to run on all computers or [q]uit: ")

        if hostname == "q":
            print("Quitting this.")
            return None

        num_list = hostname.split()

        if num_list == "":
            return

        if num_list[0] == "all":
            num_list = [f"{i}" for i in range(0, 32)]  # list of strings.  0 will cause problem if int instead of str

        for num in num_list:
            utils.print_warning("Trying computer #{}...".format(num))
            puppet_command(num, password)
