from scripts._utils.ssh import SSH

hostname = "pi-themes"
username = "pi"
password = "hackerberry"

def speak():
    # get what the user wants to say
    dialogue_old = input("What would you like me to say?")

    confirmation = input("Are you sure you want me to say \"{}\"? ([y]/n)".format(dialogue_old))

    if not confirmation or confirmation == "y":
        #properly formats what they want to say (just puts it in quotes)
        dialogue_new = "\"{}\"".format(dialogue_old)

        #puts new dialogue into the command: https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/
        command = "sudo espeak {} 2>/dev/null".format(dialogue_new)

        #connects then sends command
        ssh_connection = SSH(hostname, username, password)
        ssh_connection.connect()
        ssh_connection.send_cmd(command)

        # asks user if they want to send another message
        another_dialogue = input("Would you like to say something else? ([y]/n)")
        if not another_dialogue or another_dialogue == "y":
            speak()
        elif another_dialogue == "n":
            pass
        else:
            print("[y]/n")

        #if user doesn't want to send another command it closes connection
        ssh_connection.close()
    #if user mistyped message they get another chance to retype
    elif confirmation == "no":
        print("\nLet's try again then. \n")
        speak()
    else:
        print("([y]/n)")

#this code made by Nicky (Tseilorin) Keith
