import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts._utils.movie_maker import movie_maker

from scripts.TVs.refresh_slideshow import refresh_slideshow

from scripts.TVs._utils import mime_types, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW, TV_ROOT

#this code worked on by Nicholas (Tseilorin) Hopkins

def is_video(file_extension):
    """ file should already have mimetype checked at this point! """
    video_extensions = [".avi", ".mpeg", ".mp4", ".ogv", ".webm", ".mkv"]
    return file_extension.lower() in video_extensions

def get_media_url():

    mime_type_good = False
    #creates a loop so it alwasy goes back to the start instead of exiting the code
    while not mime_type_good:
        media_url = utils.input_styled("Paste image (png, jpg) or video (mp4, avi, mpeg, etc.) url: \n")

        if media_url == "q":
            return None, None, None

        #takes url and breaks it into name with no extension, and the extension into variables
        parsed_url_tuple = urlparse(media_url)
        name_with_ext = os.path.basename(parsed_url_tuple.path)
        name_without_ext, extension = os.path.splitext(name_with_ext)

        # verifies mime type
        expected_mime_type = None # Reset
        try:
            expected_mime_type = mime_types[extension]
        except KeyError:
            # un supported extension
            expected_mime_type = None

        # checks if file is what it really says it is
        mime_type_good = utils.verify_mimetype(media_url, expected_mime_type)

        #returns necessary veriables to continue the code once mime type has been verified
    return media_url, name_without_ext, extension


def add_new_media(student_number=None, tv=None):
    media_url = True
    while media_url == True:
        #gets and checks the url of the file
        media_url, name_without_ext, extension = get_media_url()
        if media_url is None:
            return

        #collects information to name the file, and as to which tv to send it to
        student_number_input = utils.input_styled("Enter Student Number (default = {}): \n".format(student_number))
        if not student_number_input:
            pass
        else:
            student_number = student_number_input
        image_name = None
        name_good = utils.input_styled("What is the name of this image? (default = {}): \n".format(name_without_ext))
        if not name_good:
            image_name = name_without_ext
        else:
            image_name = name_good
        tv_input = utils.input_styled("What TV # are you sending this to? (default = {}): \n".format(tv))
        if not tv_input:
            pass
        else:
            tv = tv_input

        filename = student_number + ".z." + image_name + extension

        # Save videos directly in the tv's rtoot directory.
        if is_video(extension):
            filepath = "{}/tv{}/".format(TV_ROOT, tv)
        # Save images into a subfolder, which will be used to generate a slideshow video
        else:
            filepath = "{}/tv{}/{}/".format(TV_ROOT, tv, student_number)

        utils.print_warning("Sending {} to hightower to see if file exists already with that name.".format(filename))

        command = "wget -O {}{} {} && exit".format(filepath, filename, media_url)

        hostname = TV_FILE_SERVER
        username = TV_FILE_SERVER_USER
        password = TV_FILE_SERVER_PW

        #connects and checks to see if file with the same name already exisits
        ssh_connection = SSH(hostname, username, password)
        already_exists = ssh_connection.file_exists(filepath, filename)

        #if it does exist, asks user if they want to overwrite it
        while already_exists == True:
            should_we_overwrite = utils.input_styled(utils.ByteStyle.WARNING, "There is a file that already exists with that name. Do you want to overwrite it? (y/[n]) \n")
            if not should_we_overwrite or should_we_overwrite.lower()[0] == 'n':
                #calls the function to run through the name and extension grabbing process again
                media_url, name_without_ext, extension = get_media_url()
                if media_url is None:
                    return
                #asks user to change name of it
                name_good = utils.input_styled(utils.ByteStyle.Y_N, "What is the name of this image? \n")
                if not name_good:
                    image_name = name_without_ext
                else:
                    image_name = name_good
                    filename = student_number + ".z." + image_name + extension
                    command = "wget -O /home/pi-slideshow/tv{}/{} {} && exit".format(tv, filename, media_url)
                    already_exists = False
                    pass
            elif should_we_overwrite.lower()[0] == 'y':
                already_exists = False
                pass
            else:
                utils.print_styled("(y/n)", utils.ByteStyle.Y_N)

        # if file does not exist already it wgets it and places it in the correct tv folder
        if already_exists == False:

            # make sure the directory exists, if not create it:
            if not ssh_connection.file_exists(filepath):
                ssh_connection.send_cmd('mkdir {}'.format(filepath))

            ssh_connection.send_cmd(command)
            utils.print_success("{} was succesfully sent over to pi-tv{}".format(filename, tv))
            pass
        else:
            utils.print_error("Something went wrong. Expected true or false but got something else")

        # asks user if they want to add another image
        another_image = utils.input_styled("Would you like to add another image? ([y]/n) \n")
        if not another_image or another_image.lower()[0] == "y":
            media_url = True
        elif another_image.lower()[0] == "n":
            pass
        else:
            utils.print_styled( "(y/n)", utils.ByteStyle.Y_N)

    ssh_connection.close()

    make_movie = utils.input_styled("Do you want to generate a new video slideshow of this student's art? ([y]/n) \n")
    if not make_movie or make_movie.lower()[0] == "y":
        refresh_slideshow(student_number=student_number)
    elif make_movie.lower()[0] == "n":
        pass
    else:
        utils.print_styled("(y/n)", utils.ByteStyle.Y_N)
