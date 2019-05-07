import os
from urllib.parse import urlparse
from urllib.request import urlopen

from scripts._utils import utils
from scripts._utils.ssh import SSH

hostname = "pi-themes"
username = "pi"
password = "hackerberry"

def add_new_theme_2():
    #gets and checks the url of the file
    have_good_input = False
    mp3_url = ""
    while not have_good_input:
        mp3_url = input("Paste the url to the mp3 file you want to ad or [q]uit: ")

        if mp3_url == 'q':
            break

                #check content to ensure proper mp3 type
        try:
            with urlopen(mp3_url) as response:
                ct = response.info().get_content_type()
                if ct == "audio/mpeg":
                    utils.print_styled(utils.ByteStyle.SUCCESS, "File looks good.")
                    have_good_input = True
                else:
                    utils.print_styled(utils.ByteStyle.self.FAIL,
                                    "Something is funky about this file. I expected type 'audio/mpeg' but got '{}'."
                                        " Make sure it was properly exported to an mp3.".format(ct))
        except ValueError as e:
            utils.print_styled(utils.ByteStyle.FAIL, str(e))

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
            mp3_number = input(prompt)

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

        print("Sending %s to pi-themes." % filename)

        command = "wget -nc -O /media/THEMES/{} {} && exit".format(filename, mp3_url)
        filepath = "/media/THEMES/"

        ssh_connection = SSH(hostname, username, password)

        #checks if file exists, and if user wants to overwrite it
        ssh_connection.file_exists(filepath, filename)



        #connects to themes
        ssh_connection.connect()

        #sends the command
        ssh_connection.send_cmd(command)

        #closes ssh connection
        ssh_connection.close()
