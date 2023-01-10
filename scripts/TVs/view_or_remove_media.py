import subprocess

import inquirer

from scripts.TVs.refresh_slideshow import refresh_slideshow
from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.TVs._utils import get_tv_containing_student, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW, TV_ROOT


def view_or_remove_media(username=None, tv=None):

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

        # Get media files for student
        media_command = "cd {}/tv{}/ && find {}.z.*".format(TV_ROOT, tv, username)
        media_files = ssh_connection.send_cmd(media_command, print_stdout=False).split()
        # command failed, return empty list
        if media_files[0].startswith("find"):
            media_files = []

        # Format media names to not have full path in name
        fixed_media_names = [media.split("/")[-1] for media in media_files]

        merge_point = len(dir_contents) - 1

        # Merge lists
        [dir_contents.append(file) for file in fixed_media_names]

        # Add quit option
        dir_contents.append("[Quit]")

        media_list = [
            inquirer.List('art',
                          message="Which file do you want to view?",
                          choices=dir_contents,
                          ),
        ]

        art_file = inquirer.prompt(media_list)["art"]
        if art_file == "[Quit]":
            return False

        # format art file fullpath
        if dir_contents.index(art_file) < merge_point + 1:
            art_file_full_path = filepath + art_file
        else:
            art_file_full_path = "{}/tv{}/".format(TV_ROOT, tv) + art_file

        # Show the image with Pillow
        # Transfer locally
        local_copy = "/tmp/" + art_file
        ssh_connection.get_file(art_file_full_path, local_copy)

        try:
            subprocess.run(["xdg-open", local_copy])
        except:
            utils.print_error(f"Unable to preview media at {local_copy}")

        delete_file = utils.confirm(
            "Would you like to delete {}? Hopefully it popped up for you".format(art_file),
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
            refresh = utils.confirm("Would you like to refresh the user's video slideshow?")
            if refresh:
                refresh_slideshow(username)
            else:
                utils.print_warning("\nDon't forget to refresh the user's video slideshow!\n")
            return True
