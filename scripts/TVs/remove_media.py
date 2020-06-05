import inquirer
from PIL import Image

from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.TVs._utils import get_tv_containing_student, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW, TV_ROOT


def remove_media(username=None, tv=None):

    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    username = utils.input_plus("Enter username", default=username)

    if username == "q":
        return False

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
            img = Image.open(local_copy)  
        except IOError:
            utils.print_error("File not found") 
            ssh_connection.close()
            return False

        w, h = img.size
        aspect_ratio = w / h
        thumb = img.resize((400, int(400 / aspect_ratio)))
        thumb.show()

        delete_file = utils.confirm(
            "Are you sure you want to delete {}? Hopefully it popped up for you".format(art_file),
            yes_is_default=False)

        if delete_file:
            cmd = "rm {}".format(art_file_full_path)
            ssh_connection.send_cmd(cmd, print_stdout=True)

            # confirm it's gone:
            if ssh_connection.file_exists(art_file_full_path):
                utils.print_error("\nNot sure what happened there, but the file didn't get deleted.  Sorry!")
            else:
                utils.print_success("\nThe file was successfully deleted.")

        # Keep deleting files ina  loop if they want to
        keep_going = utils.confirm("Remove another file for this student?")

        if not keep_going:
            ssh_connection.close()
            utils.print_warning("\nDon't forget to refresh the user's video slideshow!\n")
            return True
