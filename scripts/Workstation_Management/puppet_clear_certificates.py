from getpass import getpass

from scripts._utils import utils
from scripts._utils.ssh import SSH

puppet_host = 'puppet'
username = 'hackerspace_admin'
computer_host = None


def puppet_clear_certificates(hostname=None, password=None):
    if password is None:
        password = getpass("Enter the admin password: ")

    if hostname is None:
        hostname = utils.input_styled("Which computer? (e.g. 'tbl-h10-12', or '192.168.3.125' or [q]uit) ")

        if hostname == 'q':
            print("Quitting this.")
            return None

    remove_server_cert_cmd = "/opt/puppetlabs/bin/puppetserver ca clean --certname {}.hackerspace.tbl".format(hostname)

    ssh_connection_puppet = SSH(puppet_host, username, password)
    ssh_connection_puppet.send_cmd(remove_server_cert_cmd, sudo=True)
    ssh_connection_puppet.close()

    utils.print_warning("Ok, I tried to remov the old certificates from the puppet server.")
