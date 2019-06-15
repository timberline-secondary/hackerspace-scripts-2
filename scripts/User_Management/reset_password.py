import os
from scripts._utils import utils
from getpass import getpass

def reset_password():
    sn = utils.input_styled(utils.ByteStyle.INPUT, 
        "Enter the student number of the student whose password you want to reset to 'wolf': ")

    pw = getpass("You'll have to enter the Hackerspace's admin password twice. Password: ")
    
    cmd = 'su -c "echo -e \\"{}\nwolf\nwolf\\" | sudo -S passwd {}" -m hackerspace_admin'.format(pw, sn)
    os.system(cmd)
    