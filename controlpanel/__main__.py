import os

# https://stackoverflow.com/questions/8299270/ultimate-answer-to-relative-python-imports
import os, sys
# get an absolute path to the directory that contains mypackage
foo_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.normpath(os.path.join(foo_dir, '..', '..')))

from _utils import utils

utils.print_heading("Hackerspace Control Panel")

scripts_root = os.path.dirname(os.path.realpath(__file__))

options = os.listdir(scripts_root)
i = 1

for option in options:
    if option[0] is not '_':
        print("{}. {}".format(i, option))
        i += 1

choice = input("Choose a script or directory: ")




