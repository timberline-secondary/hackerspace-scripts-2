import os
import csv

from getpass import getpass

from scripts._utils import utils
from scripts.User_Management import _utils as user_utils
from scripts.User_Management.change_username import change_username


def rename_all_users():

    # load all usernames into dict with studentnumber and first.last, from csv file
    default_csv_location = os.path.expanduser("~") + "/Downloads/HomeRoomRoster.csv"
    # loop through to change usernames\

    while True:
        utils.print_warning("If the csv file is not in the default location you'll have to tell me where it is, and what it's called, e.g:")
        utils.print_warning('"/home/myusername/Documents/students.csv"')

        student_csv_file = utils.input_styled('Where can I find the csv file?  (default = "{}", [q]uit) '.format(default_csv_location))

        if student_csv_file == 'q':
            return

        if not student_csv_file:
            student_csv_file = default_csv_location

        if os.path.isfile(student_csv_file):
            break
        else:
            utils.print_error("I couldn't find this file: {} ".format(student_csv_file))

    password = getpass("Enter the admin password: ")

    user_list = []

    print("GENERATING USERNAME CROSS REFERENCE\n")

    with open(student_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == 'MyEd Student number':
                continue

            student_number = row[1]  # "Login Student Number" heading

            if not utils.user_exists(student_number):
                utils.print_warning("This user doesn't exist, skipping {}".format(student_number))
                continue  # go to next user

            new_username = user_utils.parse_username_from_email(row[4])
            print(student_number, new_username)

            # Check if user already exists or not
            user_list.append((student_number, new_username))

    for sn, new_username in user_list:
        change_username(current_username=sn, new_username=new_username, auto=True, password=password)

    print("All done!")
