import os

from scripts._utils import utils
from scripts._utils.ssh import SSH

from .refresh_slideshow import copy_movie_maker_to_host, generate_new_movie_file

from scripts.TVs._utils import TV_FILE_SERVER, TV_FILE_SERVER_PW, TV_FILE_SERVER_USER, TV_ROOT


def regenerate_all_slideshows():
    utils.print_warning("This takes a LONG time, best to start this after school to let it run for few hours!")

    do_it = utils.confirm("Are you sure you want to recreate all the slideshow videos?", yes_is_default=False)

    if not do_it:
        return

    # connects and checks to see if file with the same name already exisits
    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    print("Updating movie maker script...")
    copy_movie_maker_to_host(ssh_connection)

    # Cycle through TV directories
    for tv in range(1, 5):
        filepath = "{}/tv{}/".format(TV_ROOT, tv)
        command = 'ls {}'.format(filepath)
        dir_contents = ssh_connection.send_cmd(command, print_stdout=False).split()

        for student_number in dir_contents:

            # TODO: check if it's a directory or not, skip non-directories
            test_dir_cmd = "test -d {}{}{} || echo nope".format(filepath, os.sep, student_number)
            not_a_dir = ssh_connection.send_cmd(test_dir_cmd, print_stdout=False)
            # note this is an empty string if dir exists
            if not_a_dir:
                continue  # skip to next one

            utils.print_success("Found art folder for {} on TV# {}".format(student_number, tv))

            # refresh the video
            utils.print_warning("\nGonna regenerate video slideshow now, THIS MIGHT TAKE A WHILE!")
            generate_new_movie_file(ssh_connection, student_number, tv, silent=True)

        utils.print_success("\nFinished TV #{}\n".format(tv))

    utils.print_success("Done!")
