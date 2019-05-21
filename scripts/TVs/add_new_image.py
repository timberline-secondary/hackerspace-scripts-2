import os
from urllib.parse import urlparse
from urllib.request import urlopen

from scripts._utils import utils
from scripts._utils.ssh import SSH

#add new image to the tvs. ask user which tv to connect to, (if statement for each tv would be easiest). very similiar to add new theme. wget, format the name properly, check to make sure
#it is actually a photo or a video, check if a file with the same name already exists

def add_new_image():
    have_good_type = False
    image_url = ""
    #gets and checks the url of the file

    student_number = None
    TV_number = None

    while not have_good_type:
        image_url = input("Paste the url to the image file you want to add. (q to quit): ").strip()

        if image_url == "q":
            break

        file_extension = image_url[-4:]

        expected_mime_type = None
        if file_extension == ".png":
            expected_mime_type = "image/png"
        elif file_extension == ".jpg":
            expected_mime_type = "image/jpeg"
        else:
            print("I was expecting a png or jpg image file but that was something else.")

        # checks if file is what it really says it is
        mime_type_good = utils.verify_mimetype(image_url, expected_mime_type)

        have_good_type = mime_type_good

    if have_good_type: #then get file name

            ext = image_url[-4:]

            student_number = input("Enter Student Number\n")

            image_name = input("Name your image (MUST NAME IF YOU USED URL)\n")

            tv = input("What TV are you sending this to? (Just the number)\n")

            filename = student_number + ".z." + image_name + ext

            print("Sending {} to hightower to see if file exists already with that name.".format(filename))
            filepath = "/home/pi-slideshow/tv{}/".format(tv)
            command = "wget -O /home/pi-slideshow/tv{}/{} {} && exit".format(tv, filename, image_url)

            hostname = "hightower"
            username = "pi-slideshow"
            password = "hackerberry"

            ssh_connection = SSH(hostname, username, password)
            ssh_connection.connect()
            already_exists = ssh_connection.file_exists(filepath, filename)

            if already_exists == True:
                print("There is a file that already exists with that name. Do you want to overwrite it? (yes/no)")
                overwrite = input(">")
                if overwrite == "no" or "n":
                    add_new_image()
                elif overwrite == "yes" or "y":
                    pass
                else:
                    print("\n(yes/no)\n")
            elif already_exists == False:
                pass
            else:
                print("Something went wrong. Expected true or false but got something else")

            ssh_connection.send_cmd(command)


            another_image = input("Would you like to add another image? ([yes]/no)")
            if not another_image or another_image == "yes":
                add_new_image()
            elif another_image == "no":
                pass
            else:
                print("yes/no")

            ssh_connection.close()