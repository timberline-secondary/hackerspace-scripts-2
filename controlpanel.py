import os
import sys
from importlib import import_module

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

    return module_dict


def load_scripts(module):
    scripts_dir = SCRIPTS_DIR + os.sep + module
    scripts = os.listdir(scripts_dir)
    scripts = [s for s in scripts if s[0] not in "_."]  # remove hidden files
    scripts = [s[:-3] for s in scripts]  # remove '.py'

    script_dict = {}
    module_dir = SCRIPTS_DIR

    for s in scripts:
        script_dict[s] = __import__(module_dir + "." + module + "." + s, fromlist=["*"])
    return script_dict


def print_menu(menu_items, title):
    os.system('clear')
    utils.print_heading(title)

    for i, item in enumerate(menu_items):
        print("{}. {}".format(i, item))
    print("Ctrl+C to quit")

    choice = input("\nChoose an item: ")

    return menu_items[int(choice)]


def control_panel():

    try:
        # get modules
        module_dict = load_modules()
        module_choice = print_menu(list(module_dict.keys()), "Hackerspace Control Panel")

        # get scripts from chosen module
        sub_module_dict = load_scripts(module_choice)
        sub_module_choice_str = print_menu(list(sub_module_dict.keys()), module_choice)
        sub_module = sub_module_dict[sub_module_choice_str]

        print(sub_module)
        method = getattr(sub_module, sub_module_choice_str)
        utils.print_heading(sub_module_choice_str)
        method()

        # import the package module
        # print(control_panel.current_module)
        # control_panel.current_module = import_module('scripts.'+module_name)
        # print("current module: {}".format(control_panel.current_module))

    except KeyboardInterrupt:
        print("\nGoodbye")
        sys.exit(0)


control_panel.current_module = 'scripts'


if __name__ == '__main__':
    control_panel()
