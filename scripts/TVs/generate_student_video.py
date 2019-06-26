from scripts._utils.movie_maker import movie_maker
from scripts._utils import pi
from scripts._utils import utils
from pathlib import Path

import os

def generate_student_video(tv=None, student_number=None):
    hostname = "hightower"
    username = "pi-slideshow"
    tmp_slideshow = "/tmp/slideshow_images/"
    images_tmp_path = Path(tmp_slideshow)

    # if required variables are met, just passes through this part. also checks if a directory is amde and if not makes it

    if images_tmp_path.is_dir():
        pass
    else:
        os.system("mkdir {}".format(tmp_slideshow))

    if student_number:
        pass
    else:
        student_number = utils.input_styled("What is the students number? \n")

    if tv:
        pass
    else:
        tv = utils.input_styled("What tv is the student on? \n")

    student_video = "{}.a.movie.mp4".format(student_number)
    student_file_path_pi = "/home/pi-slideshow/tv{}/{}/{}.*".format(tv, student_number, student_number)
    tmp_path = "/tmp/"
    output_file = "/tmp/slideshow_images/{}".format(student_video)

    # gets all the images from pi-slideshowe and dumps it in tmp
    command_get_images = 'sshpass -p "{}" scp {}@{}:{} {} '.format(pi.password, username, hostname, student_file_path_pi, tmp_path)
    # move all student images from tmp into tmp folder previously created
    command_mv_images_to_folder = "mv {}{}* {} ".format(tmp_path, student_number, tmp_slideshow)

    # runs each command
    os.system(command_get_images)
    os.system(command_mv_images_to_folder)

    #makes a movie and puts the video into tmp 
    movie_maker(images_directory=tmp_slideshow, output_file=output_file)

    pi_file_path = "/home/pi-slideshow/tv{}/".format(tv)
    command_send_movie = 'sshpass -p "{}" scp {}{} {}@{}:{}'.format(pi.password, tmp_slideshow, student_video, username, hostname, pi_file_path)
    os.system(command_send_movie)

    # removes all downloaded images
    os.system("rm -r {}{}*".format(tmp_slideshow, student_number))