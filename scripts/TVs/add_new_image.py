import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH

#this code worked on by Nicholas (Tseilorin) Hopkins

def add_new_image(student_number=None, tv=None):
    have_good_type = False
    image_url = ""
    #gets and checks the url of the file

    while not have_good_type:
        image_url = input("Paste the url to the image file you want to add. (q to quit): ").strip()

        if image_url == "q":
            break

        parsed_url_tuple = urlparse(image_url)
        name_with_ext = os.path.basename(parsed_url_tuple.path)
        name_without_ext, extension = os.path.splitext(name_with_ext)

        expected_mime_type = None
        if extension == ".png":
            expected_mime_type = "image/png"
        elif extension == ".jpg" or extension == ".jpeg":
            expected_mime_type = "image/jpeg"

        # checks if file is what it really says it is
        mime_type_good = utils.verify_mimetype(image_url, expected_mime_type)

        have_good_type = mime_type_good

    if have_good_type: #then get file name

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
            password = "hackerberry"

            ssh_connection = SSH(hostname, username, password)
            ssh_connection.connect()
            already_exists = ssh_connection.file_exists(filepath, filename)

            if already_exists == True:
                print("There is a file that already exists with that name. Do you want to overwrite it? (yes/no)")
                overwrite = input(">")
                if overwrite == "no":
                    add_new_image()
                elif overwrite == "yes":
                    pass
                else:
                    print("\n(yes/no)\n")
            elif already_exists == False:
                print(("{} was succesfully sent over to pi-tv{}").format(filename, tv))
                pass
            else:
                print("Something went wrong. Expected true or false but got something else")

            ssh_connection.send_cmd(command)

            another_image = input("Would you like to add another image? ([yes]/no)")
            if not another_image or another_image == "yes":
                add_new_image(student_number, tv)
            elif another_image == "no":
                pass
            else:
                print("yes/no")

            ssh_connection.close()