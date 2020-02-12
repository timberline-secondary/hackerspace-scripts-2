import os
from urllib.parse import urlparse
from scripts._utils import utils
import inquirer
import getpass
from scripts._utils import pi
from scripts._utils.ssh import SSH
from scripts.TVs import add_new_media
import subprocess

temp_dir = "/tmp/"
hostname = "hightower"
username = "pi-slideshow"

def add_new_title():

    #gets info of the student who made the art
    first_name = utils.input_styled("First name: \n")
    last_name = utils.input_styled("Last name: \n")
    grad_year = utils.input_styled("Grad Year: \n")
    student_number = utils.input_styled("Student number: \n")

    #https://pypi.org/project/inquirer/

    subject_list = [
        inquirer.List('subject',
                    message="What subject is the student in?",
                    choices=['Digital Art', 'Digital Photography', '3D Modelling & Animation', 'Custom subject:'],
                    ),
    ]

    choose_subject = inquirer.prompt(subject_list)["subject"]

    #gets user to input a custom subject if they so choose
    if choose_subject == "Custom subject:":
        custom_subject = utils.input_styled("Well then what are they in? \n")
        choose_subject = custom_subject

    default_tv = '1' if last_name.upper()[0] <= 'M' else '2'

    tv = utils.input_styled("Which TV # are you sending this to (1 for lastname A-M, 2 for N-Z, 3 for Grads)? [Enter] = {}: \n".format(default_tv))

    if not tv:
        tv = default_tv

    filename = student_number + ".a." + first_name + last_name
    template = "_template.svg"
    source_file = "scripts/TVs/{}".format(template)
    temp_filepath_svg = "{}{}.svg".format( temp_dir, filename)
    filename_png = filename + ".png"
    temp_filepath_png = temp_dir + filename_png

    #creates copy of template with the filename it will use
    os.system("cp {} {}".format(source_file, temp_filepath_svg))

    # writes the student information into the copy of the svg template
    os.system('sed -i -e "s/FIRSTNAME LASTNAME/{} {}/g" {}'.format(first_name, last_name, temp_filepath_svg))

    os.system('sed -i -e "s/YYYY/{}/g" {}'.format(grad_year, temp_filepath_svg))

    # need to escape the ampersand character in "3D Modelling & Animation"
    os.system('sed -i -e "s/SUBJECT/{}/g" {}'.format(choose_subject.replace('&', '\&amp;'), temp_filepath_svg))

    # creates a png image from the svg
    os.system('inkscape -z -e {} -w 1920 -h 1080 {}'.format(temp_filepath_png, temp_filepath_svg))

    server_filepath = "tv{}/{}/".format(tv, student_number)

    # setup a connect so we can makesure the directory exists
    ssh_connection = SSH(hostname, username, pi.password)
    # make sure the directory exists, if not create it:
    if not ssh_connection.file_exists(server_filepath):
                ssh_connection.send_cmd('mkdir {}'.format(server_filepath))

    #move image onto the server with scp
    command = 'sshpass -p "{}" scp {} {}@{}:{}'.format(pi.password, temp_filepath_png, username, hostname, server_filepath)

    os.system(command)

    #removes all temp files we created
    # os.system('rm {}'.format(temp_filepath_png))
    # os.system('rm {}'.format(temp_filepath_svg))
    #os.system('rm {}.png'.format(filename))

    # Check if file now exists on the server
    title_exists = ssh_connection.file_exists(server_filepath, filename_png)

    if title_exists:
        utils.print_success("{} was successfully sent over to TV {}".format(filename_png, tv))
        # add_images = utils.input_styled(utils.ByteStyle.Y_N, "Would you like to add images to {}'s new shrine? ([y]/n)\n".format(first_name) )
        # if not add_images or add_images.lower()[0] == "y":
        #     add_new_media.add_new_media(student_number, tv)
    else:
        utils.print_error("The title image '{}' was not added. It's possible you've never connected to this server before. \n\n"  
        "Try connecting once first by typing `ssh hightower` into a terminal, then answering yes.".format(filename_png))
