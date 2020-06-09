import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.TVs.refresh_slideshow import refresh_slideshow

from scripts.TVs._utils import mime_types, guess_tv, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW, TV_ROOT

# this code worked on by Nicholas (Tseilorin) Hopkins


def is_video(file_extension):
    """ file should already have mimetype checked at this point! """
    video_extensions = [".avi", ".mpeg", ".mp4", ".ogv", ".webm", ".mkv"]
    return file_extension.lower() in video_extensions


def get_media_url():

    mime_type_good = False
    # creates a loop so it alwasy goes back to the start instead of exiting the code
    while not mime_type_good:
        media_url = utils.input_styled("Paste image (png, jpg) or video (mp4, avi, mpeg, etc.) url: \n")

        if media_url == "q":
            return None, None, None

        # takes url and breaks it into name with no extension, and the extension into variables
        parsed_url_tuple = urlparse(media_url)
        name_with_ext = os.path.basename(parsed_url_tuple.path)
        name_without_ext, extension = os.path.splitext(name_with_ext)

        # verifies mime type
        expected_mime_type = None  # Reset
        try:
            expected_mime_type = mime_types[extension.lower()]
        except KeyError:
            # un supported extension
            expected_mime_type = None

        # checks if file is what it really says it is
        mime_type_good = utils.verify_mimetype(media_url, expected_mime_type)

        # returns necessary veriables to continue the code once mime type has been verified
    return media_url, name_without_ext, extension


def add_new_media(username=None, tv=None):
    media_url = True
    while media_url:
        # gets and checks the url of the file
        media_url, name_without_ext, extension = get_media_url()
        if media_url is None:
            return

        # collects information to name the file, and as to which tv to send it to
        username_input = utils.input_styled("Enter username (default = {}): \n".format(username))
        if not username_input:
            pass
        else:
            username = username_input

        tv = guess_tv(username)
        tv_input = utils.input_styled("What TV # are you sending this to? (default = {}): ".format(tv))
        if not tv_input:
            pass
        else:
            tv = tv_input

        image_name = None
        name_good = utils.input_styled("What is the name of this image? (default = {}): ".format(name_without_ext))
        if not name_good:
            image_name = name_without_ext
        else:
            image_name = name_good

        filename = username + ".z." + image_name + extension

        # Save videos directly in the tv's rtoot directory.
        if is_video(extension.lower()):
            filepath = "{}/tv{}/".format(TV_ROOT, tv)
        # Save images into a subfolder, which will be used to generate a slideshow video
        else:
            filepath = "{}/tv{}/{}/".format(TV_ROOT, tv, username)

        utils.print_warning("Sending {} to hightower to see if file exists already with that name.".format(filename))

        # connects and checks to see if file with the same name already exisits
        ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)
        already_exists = ssh_connection.file_exists(filepath, filename)

        # if it does exist, asks user if they want to overwrite it  
        while already_exists and not utils.confirm(
                "There is a file that already exists with that name. Do you want to overwrite it?",
                yes_is_default=False
        ):
            # don't want to overwrite, so get a new name:
            image_name = utils.input_styled("Provide a different name for the image: ")
            filename = username + ".z." + image_name + extension
            # check again
            already_exists = ssh_connection.file_exists(filepath, filename)

        command = "wget -O {}{} '{}' && exit".format(filepath, filename, media_url)

        # make sure the directory exists, if not create it:
        if not ssh_connection.file_exists(filepath):
            ssh_connection.send_cmd('mkdir {}'.format(filepath))

        success = ssh_connection.send_cmd(command)
        if success:
            utils.print_success("{} was succesfully sent over to pi-tv{}".format(filename, tv))
        else:
            utils.print_error("Something went wrong.  Check the filename, is it wonky with weird characters?")

        # asks user if they want to add another image
        if utils.confirm("Would you like to add another image?"):
            media_url = True
        else:
            break

    ssh_connection.close()

    if utils.confirm("Do you want to generate a new video slideshow of this student's art?"):
        refresh_slideshow(username=username)
