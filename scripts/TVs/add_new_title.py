import os
from urllib.parse import urlparse
from scripts._utils import utils
import inquirer
import getpass
from scripts._utils import pi
from scripts._utils.ssh import SSH


def add_new_title():
    #gets info of the student who made the art
    first_name = utils.input_styled(utils.ByteStyle.INPUT, "First name: \n")
    last_name = utils.input_styled(utils.ByteStyle.INPUT, "Last name: \n")
    grad_year = utils.input_styled(utils.ByteStyle.INPUT, "Grad Year: \n")
    student_number = utils.input_styled(utils.ByteStyle.INPUT, "Student number: \n")

    current_user = getpass.getuser()

    #https://pypi.org/project/inquirer/

    subject_list = [
        inquirer.List('subject',
                      message="What subject is the student in?",
                      choices=['Digital Art', 'Digital Photography', '3D Modelling & Animation', 'Custom subject:'],
                      ),
    ]

    choose_subject = inquirer.prompt(subject_list)["subject"]

    if choose_subject == "Custom subject:":
        custom_subject = utils.input_styled(utils.ByteStyle.INPUT, "Well then what are they in? \n")
        choose_subject = custom_subject
    else:
        pass

    tv = utils.input_styled(utils.ByteStyle.INPUT, "Which TV # are you sending this to?: \n")

    filename = student_number + ".a." + first_name + last_name
    template = "_template.svg"

    os.system("cp {} {}.svg".format(template, filename))
    os.system('sed -i -e "s/FIRSTNAME LASTNAME/{} {}/g" {}.svg'.format(first_name, last_name, filename))
    os.system('sed -i -e "s/YYYY/{}/g" {}.svg'.format(grad_year, filename))
    os.system('sed -i -e "s/SUBJECT/{}/g" {}.svg'.format(choose_subject, filename))
    os.system('inkscape -z -e {}.png -w 1920 -h 1080 {}.svg'.format(filename, filename))

    hostname = "hightower"
    username = "pi-slideshow"
    filepath_pi = "/home/pi-slideshow/tv{}/".format(tv)

    ssh_connection = SSH(hostname, username, pi.password)
    ssh_connection.connect()

    command = ""

    ssh_connection.send_cmd(command)
