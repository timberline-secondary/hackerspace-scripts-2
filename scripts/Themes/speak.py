from scripts._utils.ssh import SSH
from scripts._utils import pi
from scripts._utils import utils

hostname = "pi-themes"

#this code worked on by Nicholas (Tseilorin) Hopkins

def speak():
    # connects to pi themes
    ssh_connection = SSH(hostname, pi.username, pi.password)
    ssh_connection.connect()

    quitting = False
    while not quitting:
        #makes while loop and gets user input as to what to say
        dialogue_old = utils.input_styled(utils.ByteStyle.INPUT, "What would you like me to say? (q to quit): \n")

        if dialogue_old == 'q':
            quitting = True

        else:

            #properly formats what they want to say (just puts it in quotes)
            dialogue_new = "\"{}\"".format(dialogue_old)

            #puts new dialogue into the command: https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/
            command = "sudo espeak -a 200 {} 2>/dev/null".format(dialogue_new)

            #connects then sends command

            ssh_connection.send_cmd(command)


    ssh_connection.close()

