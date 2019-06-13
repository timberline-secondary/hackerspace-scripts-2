import os
from urllib.parse import urlparse
from urllib.request import urlopen
from scripts._utils import pi

from scripts._utils import utils
from scripts._utils.ssh import SSH

hostname = "pi-themes"

def add_new_theme():
    #gets and checks the url of the file
    mp3_url = True
    while mp3_url == True:
        have_good_input = False
        mp3_url = ""
        while not have_good_input:
            mp3_url = utils.input_styled(utils.ByteStyle.INPUT, "Paste the url to the mp3 file you want to add. (q to quit): \n")

            if mp3_url == 'q':
                break

                    #check content to ensure proper mp3 type
            mime_type_good = utils.verify_mimetype(mp3_url, "audio/mpeg")

            have_good_input = mime_type_good

        if have_good_input: #then get file number

            have_good_input = False
            while not have_good_input:
                filename = os.path.basename(urlparse(mp3_url).path)
                name, ext = os.path.splitext(filename)
                #check if filename is already a number, and offer to use it
                try:
                    name = int(name)
                    good_name_already = True
                except ValueError:
                    good_name_already = False

                prompt = "What number (integers only) do you want to give it?" + (" [Enter] = {}".format(name) if good_name_already else "") + "\n"
                mp3_number = utils.input_styled(utils.ByteStyle.INPUT, prompt)

                try:
                    if good_name_already and not mp3_number:
                        mp3_number = name
                    else:
                        mp3_number = int(mp3_number)
                    have_good_input = True
                except ValueError:
                    utils.print_styled(utils.ByteStyle.FAIL, "Dude, that wasn't an integer! ")
                    have_good_input = False
            filename = "{}.mp3".format(mp3_number)

            # print("test: {}".format(filename))

            print("Sending {} to pi-themes to see if file exists already with that name.".format(filename))

            command = "wget -O /media/THEMES/{} {} && exit".format(filename, mp3_url)
            filepath = "/media/THEMES/"

            ssh_connection = SSH(hostname, pi.username, pi.password)

            ssh_connection.connect()
            #checks if file exists, and if user wants to overwrite it
            already_exists = ssh_connection.file_exists(filepath, filename)

            # asks user if they want to overwrite https://www.quora.com/I%E2%80%99m-new-to-Python-how-can-I-write-a-yes-no-question
            if already_exists == True:
                overwrite = utils.input_styled(utils.ByteStyle.WARNING, "There is a file that already exists with that name. Do you want to overwrite it? (y/[n]) \n")
                if not overwrite or overwrite.lower()[0] == "n":
                    mp3_url = True
                elif overwrite.lower()[0] == "y":
                    already_exists = False
                    pass
                else:
                    utils.print_styled(utils.ByteStyle.Y_N, "(y/n)")
            elif already_exists == False:
                pass
            else:
                utils.print_styled(utils.ByteStyle.FAIL,
                                   "Something went wrong. Expected true or false but got something else")

            #sends the command
            if already_exists == False:
                ssh_connection.send_cmd(command)

            another_code = utils.input_styled(utils.ByteStyle.Y_N, "Would you like to add another code? ([y]/n) \n")
            if not another_code or another_code.lower()[0] == "y":
                mp3_url = True
                pass
            elif another_code.lower()[0] == "n":
                mp3_url = False
            else:
                utils.print_styled(utils.ByteStyle.Y_N, "(y/n)")
            #closes ssh connection
            ssh_connection.close()
    utils.input_styled(utils.ByteStyle.INPUT, "Hit Enter to return to the main menu.")