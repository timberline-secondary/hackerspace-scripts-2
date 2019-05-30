import os
from urllib.parse import urlparse
from scripts._utils import utils
import inquirer
import getpass
from scripts._utils import pi
from scripts._utils.ssh import SSH

temp_dir = "/tmp/"

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

    #creates copy of template with the filename it will use
    os.system("cp scripts/TVs/{} {}{}.svg".format(template, temp_dir, filename))

    #writes the information in the newly created file (.svg), using the info you provided
    os.system('sed -i -e "s/FIRSTNAME LASTNAME/{} {}/g" {}{}.svg'.format(first_name, last_name, temp_dir, filename))
    os.system('sed -i -e "s/YYYY/{}/g" {}{}.svg'.format(grad_year, temp_dir, filename))
    os.system('sed -i -e "s/SUBJECT/{}/g" {}{}.svg'.format(choose_subject, temp_dir, filename))
    #turns the svg into a png
    os.system('inkscape -z -e {}{}.png -w 1920 -h 1080 {}{}.svg'.format(temp_dir, filename, temp_dir, filename))

    hostname = "hightower"
    username = "pi-slideshow"
    filepath_pi = "/home/pi-slideshow/tv{}/".format(tv)

    #scps into the tv photo directory
    command = "scp {}{}.png {}@{}:{}".format(temp_dir, filename, username, hostname, filepath_pi)
    os.system(command)

    #removes all files it created
    os.system('rm {}{}.png'.format(temp_dir, filename))
    os.system('rm {}{}.svg'.format(temp_dir, filename))
    os.system('rm {}.png'.format(filename))
