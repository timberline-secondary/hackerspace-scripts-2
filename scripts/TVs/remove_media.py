import os
import inquirer
from PIL import Image
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts._utils.movie_maker import movie_maker

from scripts.TVs.refresh_slideshow import refresh_slideshow

from scripts.TVs._utils import mime_types, get_tv_containing_student, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW, TV_ROOT

def remove_media(student_number=None, tv=None):

    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    username = utils.input_styled("Enter username (default = {}): \n".format(student_number))

    while True:

        tv = get_tv_containing_student(username)
        if tv is None:
            utils.print_error("No art found for {}".format(username))
            return False

        
        
        # get of list of the student's art and display the list
        filepath = "{}/tv{}/{}/".format(TV_ROOT, tv, username)
        command = 'ls {}'.format(filepath)
        dir_contents = ssh_connection.send_cmd(command, print_stdout=False).split()

        media_list = [
            inquirer.List('art',
                message="Which file do you want to delete? I'll display it first so you can confirm.",
                choices=dir_contents,
                ),
        ]

        art_file = inquirer.prompt(media_list)["art"]
        art_file_full_path = filepath + art_file

        # Show the image with Pillow
        # Transfer locally
        local_copy = "/tmp/" + art_file
        ssh_connection.get_file(art_file_full_path, local_copy)

        try:  
            img  = Image.open(local_copy)  
        except IOError:
            utils.print_error("File not found") 
            ssh_connection.close()
            return False
        
        w, h = img.size
        aspect_ratio = w/h
        thumb = img.resize((400, int(400/aspect_ratio)))
        thumb.show()

        delete_file = utils.input_styled("Are you sure you want to delete {}? Hopefully it popped up for you. (y/[n]) ".format(art_file))

        if delete_file and delete_file.lower()[0] == 'y':
            cmd = "rm {}".format(art_file_full_path)
            ssh_connection.send_cmd(cmd, print_stdout=True)

            # confirm it's gone:
            if ssh_connection.file_exists(art_file_full_path):
                utils.print_error("\nNot sure what happened there, but the file didn't get deleted.  Sorry!")
            else:
                utils.print_success("\nThe file was successfully deleted.")

        # Keep deleting files ina  loop if they want to
        keep_going = utils.input_styled("Remove another file for this student? (y/[n]) ")

        if not keep_going or keep_going.lower()[0] != 'y':
            ssh_connection.close()
            utils.print_warning("\nDon't forget to refresh the user's video slideshow!\n")
            return True
