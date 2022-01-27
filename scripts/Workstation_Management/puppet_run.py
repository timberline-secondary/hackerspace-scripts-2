from getpass import getpass
from scripts.Workstation_Management.puppet_clear_certificates import puppet_clear_certificates

from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.Workstation_Management._remove_puppet_lock import remove_puppet_lock

puppet_host = 'puppet'
username = 'hackerspace_admin'
computer_host = None


def puppet_run(computer_number=None, password=None, auto_fix_certificates=False):
    if password is None:
        password = getpass("Enter the admin password: ")

    computer_host = utils.get_valid_hostname(computer_number)

    if computer_host is None:
        return

    # now that we know we have a connected computer, ssh into it and try to run puppet
    success = False
    ssh_connection = SSH(computer_host, username, password)

    if not ssh_connection.is_connected():
        utils.print_warning("\nComputer is online, but cant' connect. Maybe it's mining?\n") 

    puppet_command = '/usr/bin/puppet agent -t'

    while not success:
        utils.print_warning(
            "\nRunning puppet on {}.  This may take a while.  The ouput will appear when it's done for you to inspect...\n".format(computer_host))

        output_puppet_run = ssh_connection.send_cmd(puppet_command, sudo=True)

        if "Error: Could not request certificate: The certificate retrieved from the master does not match the agent's private key." in output_puppet_run:
            pass
        elif "alert certificate unknown" in output_puppet_run:
            pass
        elif "unable to get local issuer certificate" in output_puppet_run:
            pass
        elif "Notice: Run of Puppet configuration client already in progress" in output_puppet_run:
            if remove_puppet_lock(ssh_connection, password):
                pass
            else:
                utils.print_warning("\nIt appears that puppet is already running on {}.  Give it a few minutes and try again.\n".format(computer_host)) 
                break
        elif "command not found" in output_puppet_run:
            utils.print_warning("\nCouldn't find puppet.... why not? Try the other spot...") 
            break
        else:
            utils.print_success("\n\nSeems like everything worked ok!\n\n")
            break  # out of the while loop, all done

        # ## Handle certificate problem ###
        # Error: Could not request certificate: The certificate retrieved from the master does not match the agent's private key.
        # Certificate fingerprint: 26:DD:EC:AC:15:95:7C:4B:7C:DB:0C:C6:30:C8:1A:7D:FF:C1:7B:C8:A5:56:53:77:94:2A:C3:F2:98:B7:D6:6A
        # To fix this, remove the certificate from both the master and the agent and then start a puppet run, which will automatically regenerate a certificate.
        # On the master:
        # puppet cert clean tbl-hackerspace-2-s.hackerspace.tbl
        # On the agent:
        # 1a. On most platforms: find /etc/puppetlabs/puppet/ssl -name tbl-hackerspace-2-s.hackerspace.tbl.pem -delete
        # 1b. On Windows: del "\etc\puppetlabs\puppet\ssl\certs\tbl-hackerspace-2-s.hackerspace.tbl.pem" /f
        # 2. puppet agent -t
        #
        # Exiting; failed to retrieve certificate and waitforcert is disabled

        if not auto_fix_certificates:
            try_to_fix = utils.input_styled(
                "Looks like there was a certificate problem.  Usually this happens when a computer is re-imaged.  Want me to try to fix it? [y]/n ")

            if try_to_fix == 'n':
                break

        # first, remove certificate from agent:
        if "find /etc/puppetlabs/puppet/ssl" in output_puppet_run:  # old 16.04 installations
            remove_agent_cert_cmd = "find /etc/puppetlabs/puppet/ssl -name {}.hackerspace.tbl.pem -delete".format(computer_host)
        else:
            remove_agent_cert_cmd = "rm -rf /var/lib/puppet/ssl"  # just delete them all
        ssh_connection.send_cmd(remove_agent_cert_cmd, sudo=True)

        # now remove certificate from puppet server:
        puppet_clear_certificates(computer_host, password)

        # command_response_list = [
        #                             ("sudo passwd {}".format(student_number), "[sudo] password for {}:".format(username), None),
        #                             (password, "New password: ", None),
        #                             ("wolf", "Re-enter new password: ", None),
        #                             ("wolf", prompt_string, "password updated successfully"),
        #                         ]
        # success = ssh_connection.send_interactive_commands(command_response_list)

    ssh_connection.close()
