
import os
import sys
from collections import OrderedDict
from importlib import import_module
from pip._internal import main as pipmain

from scripts._utils import utils
# from scripts import themes

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPTS_DIR = "scripts"


def load_modules():
    # https://stackoverflow.com/a/951678/2700631
    module_dir = SCRIPTS_DIR
    # scripts_dir += (os.sep + module_name) if module_name else ''
    module_dict = {}
    # check subfolders
    lst = os.listdir(module_dir)
    directories = []
    lst = [s for s in lst if s[0] not in "_."]  # remove hidden modules
    for d in lst:
        s = os.path.abspath(module_dir) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            directories.append(d)
    # load the modules
    for d in directories:
        module_dict[d] = __import__(module_dir + "." + d, fromlist=["*"])

    # sort by key
    return OrderedDict(sorted(module_dict.items()))


def load_scripts(module):
    scripts_dir = SCRIPTS_DIR + os.sep + module
    scripts = os.listdir(scripts_dir)
    scripts = [s for s in scripts if s[0] not in "_."]  # remove hidden files
    scripts = [s[:-3] for s in scripts]  # remove '.py'
    script_dict = {}
    module_dir = SCRIPTS_DIR

    for s in scripts:
        script_dict[s] = __import__(module_dir + "." + module + "." + s, fromlist=["*"])

    # sort by key
    return OrderedDict(sorted(script_dict.items()))


def print_menu(menu_items, title, quit_option=True, back_option=False):
    os.system('clear')
    utils.print_heading(title)

    for i, item in enumerate(menu_items):
        print("{}. {}".format(i, item))

    if back_option:
        print("[b]ack")

    if quit_option:
        print("[q]uit")

    choice = input("\nChoose an item: ")

    return choice

def pip_install():
    utils.print_warning("Checking to see if all necassary pip modules are installed. \n")
    pipmain(['install', 'paramiko'])
    pipmain(['install', 'inquirer'])
    utils.print_success("Everything is installed!")
    os.system('clear')

def control_panel():

    try:
        # get modules
        module_dict = load_modules()

        pip_install()

        while True:
            menu_items = list(module_dict.keys())
            menu_choice = print_menu(menu_items, "Hackerspace Control Panel")

            if menu_choice == 'q':
                break
            module_choice = menu_items[int(menu_choice)]

            # add b as a menu option so you can go back to the previous menu / when done with a certain menu have it go back to the same menu it came from (C said while loop)

            # get scripts from chosen module
            sub_module_dict = load_scripts(module_choice)
            menu_items = list(sub_module_dict.keys())
            sub_module_choice_str = print_menu(menu_items, module_choice, back_option=True)

            if sub_module_choice_str == 'q':
                break

            if sub_module_choice_str == 'b':
                continue

            sub_module_key = menu_items[int(sub_module_choice_str)]

            sub_module = sub_module_dict[sub_module_key]

            method = getattr(sub_module, sub_module_key)
            utils.print_heading(sub_module_key)
            method()

    except KeyboardInterrupt:
        print("\nGoodbye")
        sys.exit(0)
    finally:
        print("\nGoodbye")


control_panel.current_module = 'scripts'


if __name__ == '__main__':
    control_panel()
