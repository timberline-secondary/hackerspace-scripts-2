import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils import pi
from scripts._utils.ssh import SSH

#this code worked on by Nicholas (Tseilorin) Hopkins

def get_image_url():

    mime_type_good = False
    #creates a loop so it alwasy goes back to the start instead of exiting the code
    while not mime_type_good:
        image_url = input("Paste the url to the image file you want to add. (q to quit): ").strip()

        if image_url == "q":
            return None, None, None

        #takes url and breaks it into name with no extension, and the extension into variables
        parsed_url_tuple = urlparse(image_url)
        name_with_ext = os.path.basename(parsed_url_tuple.path)
        name_without_ext, extension = os.path.splitext(name_with_ext)

        #verifies mime type
        expected_mime_type = None
        if extension == ".png":
            expected_mime_type = "image/png"
        elif extension == ".jpg" or extension == ".jpeg":
            expected_mime_type = "image/jpeg"

        # checks if file is what it really says it is
        mime_type_good = utils.verify_mimetype(image_url, expected_mime_type)

        #returns necessary veriables to continue the code once mime type has been verified
    return image_url, name_without_ext, extension


def add_new_image(student_number=None, tv=None):
    image_url = True
    while image_url == True:
        #gets and checks the url of the file
        image_url, name_without_ext, extension = get_image_url()
        if image_url is None:
            return

        #collects information to name the file, and as to which tv to send it to
        student_number_input = input(("Enter Student Number (default = {}): \n").format(student_number)).strip()
        if not student_number_input:
            pass
        else:
            student_number = student_number_input

        image_name = None
        name_good = input(("What is the name of this image? (default = {}): \n").format(name_without_ext)).strip()
        if not name_good:
            image_name = name_without_ext
        else:
            image_name = name_good

        tv_input = input(("What TV # are you sending this to? (default = {}): \n").format(tv)).strip()
        if not tv_input:
            pass
        else:
            tv = tv_input

        filename = student_number + ".z." + image_name + extension

        print("Sending {} to hightower to see if file exists already with that name.".format(filename))


        filepath = "/home/pi-slideshow/tv{}/".format(tv)
        command = "wget -O /home/pi-slideshow/tv{}/{} {} && exit".format(tv, filename, image_url)

        hostname = "hightower"
        username = "pi-slideshow"

        #connects and checks to see if file with the same name already exisits
        ssh_connection = SSH(hostname, username, pi.password)
        ssh_connection.connect()
        already_exists = ssh_connection.file_exists(filepath, filename)


        #if it does exist, asks user if they want to overwrite it
        if already_exists == True:
            while already_exists == True:
                should_we_overwrite = input("There is a file that already exists with that name. Do you want to overwrite it? (y/[n])")
                if not should_we_overwrite or should_we_overwrite.lower()[0] == 'n':
                    #calls the function to run through the name and extension grabbing process again
                    image_url, name_without_ext, extension = get_image_url()
                    if image_url is None:
                        return
                    #asks user to change name of it
                    name_good = input(
                        ("What is the name of this image? (default = {}): \n").format(name_without_ext)).strip()
                    if not name_good:
                        image_name = name_without_ext
                    else:
                        image_name = name_good
                        filename = student_number + ".z." + image_name + extension
                        command = "wget -O /home/pi-slideshow/tv{}/{} {} && exit".format(tv, filename, image_url)
                        already_exists = False
                        pass
                elif should_we_overwrite.lower()[0] == 'y':
                    already_exists = False
                    pass
                else:
                    print("(y/n)")

        #if file does not exist already it wgets it and places it in the correct tv folder
        if already_exists == False:
            ssh_connection.send_cmd(command)
            print(("{} was succesfully sent over to pi-tv{}").format(filename, tv))
            pass
        else:
            print("Something went wrong. Expected true or false but got something else")

        #asks user if they want to add another image
        another_image = input("Would you like to add another image? ([y]/n)")
        if not another_image or another_image.lower()[0] == "y":
            image_url = True
        elif another_image.lower()[0] == "n":
            pass
        else:
            print("y/n")

    ssh_connection.close()