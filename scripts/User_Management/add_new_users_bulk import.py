import os
import csv

from scripts._utils import utils

from getpass import getpass
from scripts.User_Management._utils import generate_ldif_entry, get_next_avail_uid, create_users_from_ldif, create_home_dirs

from .add_new_user import add_new_user

hostname = 'lannister'
username = 'hackerspace_admin'

default_csv_location = os.path.expanduser("~") + "/Downloads/StudentList.csv"

# TODO FIX ME TO WORK WITH add_new_user!!!

def import_new_users():

    utils.print_warning("\nImporting new users in bulk requires a csv file with data like this:")
    utils.print_warning("FIRST NAME, LAST NAME, USERNAME")
    utils.print_warning("JIMMY, BLOGGINS, jimmy.bloggins@stu.sd72.bc.ca")
    utils.print_warning("...etc\n\n")
    utils.print_warning("There should be no headings row, just students.\n")
    utils.print_warning("Usernames can include @stu.sd72.bc.ca or not.  If it is included, it will be removed and " +
                        "only firstname.lastname will be used for their username")

    # Get a CSV file and read it:

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

    userlist = []
    next_uid = None
    ldif_entry = ""

    with open(student_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == 'col1':
                continue
            if row[0] == 'UNIVERSAL ID':
                continue

            #Add a tuple for each account to create
            # row[0] = first name
            # row[1] = last name
            # row[2] = username (firstname.lastname[@stu.sd72.bc.ca])

            username = parse_username(row[2])

            # Check if user already exists or not
            if utils.user_exists(username):
                utils.print_warning("This user already exists: {}".format(username))
                continue # go to next user

            userlist.append(username)

            next_uid = get_next_avail_uid()
            ldif_entry += generate_ldif_entry(username, row[0], row[2], next_uid) + "\n"

            success = create_users_from_ldif(ldif_entry, password=password)
    
            # create home dir for new user
            if success:
                return create_home_dirs([username], password)

            # add_new_user(
            #     username=row[0],
            #     first_name=row[1],
            #     last_name=row[2],
            #     password=password,
            #     bulk_creation=True,
            #     ssh_connection=ssh_connection
            # )

    print("All done!")


def parse_username_from_email(username: str) -> str:
    """ Takes a username in the format firstname.lastname or 
    firstname.lastname@stu.sd72.bc.ca and returns only firstname.lastname 
    """
    return username.split("@")[0]






