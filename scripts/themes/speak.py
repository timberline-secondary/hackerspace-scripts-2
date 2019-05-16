from scripts._utils.ssh import SSH

hostname = "pi-themes"
username = "pi"
password = "hackerberry"

def speak():
    # get what the user wants to say
    ssh_connection = SSH(hostname, username, password)
    ssh_connection.connect()

    quitting = False
    while not quitting:
        dialogue_old = input("What would you like me to say? (q to quit): ")

        if dialogue_old == 'q':
            quitting = True

        else:

            #properly formats what they want to say (just puts it in quotes)
            dialogue_new = "\"{}\"".format(dialogue_old)

            #puts new dialogue into the command: https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/
            command = "sudo espeak {} 2>/dev/null".format(dialogue_new)

            #connects then sends command

            ssh_connection.send_cmd(command)


    ssh_connection.close()

