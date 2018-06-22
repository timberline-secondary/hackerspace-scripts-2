import os
import sys

from scripts._utils import utils

SCRIPTS_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")


def get_menu_items(directory=None):
    directory = os.path.join(SCRIPTS_ROOT, directory)
    dir_contents = os.listdir(directory)
    # remove "hidden" items beginning with _ or .
    # https://stackoverflow.com/questions/36268749/remove-multiple-items-from-a-python-list-in-just-one-statement
    dir_contents = [s for s in dir_contents if s[0] not in "_."]
    return dir_contents


def print_menu(menu_items, title):
    os.system('clear')
    utils.print_heading(title)

    for i, item in enumerate(menu_items):
        print("{}. {}".format(i, item))
    print("Ctrl+C to quit")

    return input("\nChoose an item: ")


def control_panel(directory=SCRIPTS_ROOT, title="Hackerspace Control Panel"):
    try:
        menu_items = get_menu_items(directory)
        choice = int(print_menu(menu_items, title))
        # try to dynamically import the choice as a package
        module_name = menu_items[choice]
        try:
            control_panel.current_module = globals()[module_name]
            print(control_panel.current_module)
            control_panel(module_name, module_name)
        except ImportError:  # not a package!
            method = getattr(control_panel.current_module, module_name)
            print(method)
            print("ImportError")

    except KeyboardInterrupt:
        print("\nGoodbye")
        sys.exit(0)

control_panel.current_module = None

if __name__ == '__main__':
    # print(globals())
    control_panel()
