from scripts._utils import utils
from scripts._utils.ssh import SSH

puppet_host = 'puppet'
username = 'hackerspace_admin'


def puppet_command(computer_number, password):
    remove_server_cert_cmd = "/opt/puppetlabs/bin/puppetserver ca clean --certname {}.hackerspace.tbl".format(computer_number)

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
    num_list, password = utils.get_computers_prompt(hostname, password)

    # options was quit
    if num_list is None and password is None:
        return False

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        puppet_command(num, password)
