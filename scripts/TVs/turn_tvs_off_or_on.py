import os
from urllib.parse import urlparse
from urllib.request import urlopen

from scripts.TVs._utils import TV_ON_CMD, TV_OFF_CMD, valid_tvs
from scripts._utils import pi

from scripts._utils import utils
from scripts._utils.ssh import SSH


def turn_tvs_off_or_on():
    which_tvs = None
    not_quitting = True
    while not_quitting:
        user_input = utils.input_styled("o[n] or of[f] or [q]uit? ")

        if user_input == 'n':
            cmd = TV_ON_CMD
        elif user_input == 'f':
            cmd = TV_OFF_CMD
        elif user_input == 'q':
            return
        else:
            utils.print_error("Sorry, I didn't understand \"{}\".  Hit 'n' for on or 'f' for off.".format(user_input))
            continue

        user_input = utils.input_styled("Which TV #? (default = ALL) ")

        if user_input == 'q':
            return
        elif not user_input:  # turn them all off 
            which_tvs = valid_tvs
        elif user_input in valid_tvs:
            which_tvs = user_input
        else:
            utils.print_error("Sorry, I didn't understand \"{}\".  Hit Enter to turn them all off, or enter a number for a specific TV.".format(user_input))
            continue

        for tv_number in which_tvs:
            hostname = "pi-tv{}".format(tv_number)
            ssh_connection = SSH(hostname, pi.username, pi.password)
            
            ssh_connection.send_cmd(cmd)
            ssh_connection.close()  

