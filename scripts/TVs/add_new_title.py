import os
import inquirer
from scripts._utils import utils, pi
from scripts._utils.ssh import SSH
from scripts.User_Management import _utils as user_utils
from scripts.TVs.add_new_media import add_new_media, refresh_slideshow

temp_dir = "/tmp/"
hostname = "hightower"
SERVER_USERNAME = "pi-slideshow"


def add_new_title():

    fullname, username = user_utils.get_and_confirm_user()

    # gets info of the student who made the art
    fullname_entered = utils.input_plus("Full name", fullname)
    if fullname_entered:
        fullname = fullname_entered
    else:
        fullname = fullname.title()
    grad_year = utils.input_styled("Grad Year: \n")

    last_name = username.split(".")[-1].title()  # get the last word if the username tyere.couture will get couture

    # https://pypi.org/project/inquirer/

    subject_list = [
        inquirer.List('subject',
                      message="What subject is the student in?",
                      choices=['Digital Art', 'Digital Photography', '3D Modelling & Animation', 'Custom subject:'],
                      ),
    ]

    choose_subject = inquirer.prompt(subject_list)["subject"]

    # gets user to input a custom subject if they so choose
    if choose_subject == "Custom subject:":
        custom_subject = utils.input_styled("Well then what are they in? \n")
        choose_subject = custom_subject

    default_tv = '1' if last_name.upper()[0] <= 'M' else '2'

    tv = utils.input_plus("Which TV # are you sending this to (1 for lastname A-M, 2 for N-Z, 3 for Grads)?", default_tv)

    if not tv:
        tv = default_tv

    filename = username + ".a.title"
    template = "_template.svg"
    source_file = "scripts/TVs/{}".format(template)
    temp_filepath_svg = "{}{}.svg".format(temp_dir, filename)
    filename_png = filename + ".png"
    temp_filepath_png = temp_dir + filename_png

    # creates copy of template with the filename it will use
    os.system("cp {} {}".format(source_file, temp_filepath_svg))

    # writes the student information into the copy of the svg template
    os.system('sed -i -e "s/FIRSTNAME LASTNAME/{}/g" {}'.format(fullname, temp_filepath_svg))

    os.system('sed -i -e "s/YYYY/{}/g" {}'.format(grad_year, temp_filepath_svg))

    # need to escape the ampersand character in "3D Modelling & Animation"
    os.system('sed -i -e "s/SUBJECT/{}/g" {}'.format(choose_subject.replace('&', '\&amp;'), temp_filepath_svg))

    # creates a png image from the svg
    os.system('inkscape -z -e {} -w 1920 -h 1080 {}'.format(temp_filepath_png, temp_filepath_svg))

    server_filepath = "tv{}/{}/".format(tv, username)

    # setup a connect so we can makesure the directory exists
    ssh_connection = SSH(hostname, SERVER_USERNAME, pi.password)
    # make sure the directory exists, if not create it:
    if not ssh_connection.file_exists(server_filepath):
        ssh_connection.send_cmd('mkdir {}'.format(server_filepath))

    # move image onto the server with scp (this will fail if they've never connected to hightower before, hence warning at bottom)
    command = 'sshpass -p "{}" scp {} {}@{}:{}'.format(pi.password, temp_filepath_png,
                                                       SERVER_USERNAME, hostname, server_filepath)

    os.system(command)

    # removes all temp files we created
    os.system('rm {}'.format(temp_filepath_png))
    os.system('rm {}'.format(temp_filepath_svg))

    # Check if file now exists on the server
    title_exists = ssh_connection.file_exists(server_filepath, filename_png)

    if title_exists:
        utils.print_success(f"{filename_png} was successfully sent over to TV {tv}")
        add_images = utils.confirm(f"Would you like to add images to {fullname}'s new shrine?")
        if add_images:
            add_new_media(username, tv)
        else:
            gen_video = utils.confirm("Would you like to regenerate the video file?")
            if gen_video:
                refresh_slideshow(username=username)
    else:
        utils.print_error(f"The title image '{filename_png}' was not added. Maybe inkscape isn't installed? Or it's possible you've never connected to this server before. \n\n"  
                          "Try connecting once first by typing `ssh hightower` into a terminal, then answering yes.")
