import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils import pi
from scripts._utils.ssh import SSH

def add_title():
    first_name = utils.input_styled(utils.ByteStyle.INPUT + "First name:")
    last_name = utils.input_styled(utils.ByteStyle.INPUT + "Last name:")
    grad_year = utils.input_styled(utils.ByteStyle.INPUT + "Grad Year:")
    student_number = utils.input_styled(utils.ByteStyle.INPUT + "Student number:")

    subjects = ['Digital Art', 'Digital Photography', '3D Modelling & Animation', utils.input_styled((utils.ByteStyle.INPUT + "Custom subject:"))]