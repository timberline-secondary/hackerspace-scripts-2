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
    first_name = utils.input_styled(utils.ByteStyle.INPUT, "First name: \n")
    last_name = utils.input_styled(utils.ByteStyle.INPUT, "Last name: \n")
    grad_year = utils.input_styled(utils.ByteStyle.INPUT, "Grad Year: \n")
    student_number = utils.input_styled(utils.ByteStyle.INPUT, "Student number: \n")

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
        custom_subject = utils.input_styled(utils.ByteStyle.INPUT, "Well then what are they in? \n")
        choose_subject = custom_subject
    else:
        pass

    tv = utils.input_styled(utils.ByteStyle.INPUT, "Which TV # are you sending this to?: \n")

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
    os.system('sed -i -e "s/SUBJECT/{}/g" {}'.format(choose_subject, temp_filepath_svg))

    # creates a png image from the svg
    os.system('inkscape -z -e {} -w 1920 -h 1080 {}'.format(temp_filepath_png, temp_filepath_svg))

    filepath_pi = "/home/pi-slideshow/tv{}/".format(tv)

    #scps into the tv photo directory
    command = 'sshpass -p "{}" scp {} {}@{}:{}'.format(pi.password, temp_filepath_png, username, hostname, filepath_pi)
    os.system(command)

    #removes all files it created
    os.system('rm {}'.format(temp_filepath_png))
    os.system('rm {}'.format(temp_filepath_svg))
    #os.system('rm {}.png'.format(filename))

    ssh_connection = SSH(hostname, username, pi.password)
    ssh_connection.connect()
    title_exists = ssh_connection.file_exists(filepath_pi, filename_png)

    if title_exists:
        utils.print_styled(utils.ByteStyle.SUCCESS, "{} was successfully sent over to TV {}".format(filename_png, tv))
        add_images = utils.input_styled(utils.ByteStyle.Y_N, "Would you like to add images to {}'s new shrine? ([y]/n)\n".format(first_name) )
        if not add_images or add_images.lower()[0] == "y":
            add_new_media.add_new_media(student_number, tv)
        else:
            utils.print_styled(utils.ByteStyle.FAIL, "The title image was not added.")
    else:
        utils.print_styled(utils.ByteStyle.FAIL, "{} was not sent to hightower. Is sshpass installed?".format(filename_png))
            