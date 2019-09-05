import os
import csv

from scripts._utils import utils
from scripts._utils.ssh import SSH
from getpass import getpass

from .add_new_user import add_new_user

hostname = 'lannister'
username = 'hackerspace_admin'

default_csv_location = os.path.expanduser("~") + "/Downloads/StudentList.csv"

def import_new_users():

    print("\nImporting new users in bulk requires a csv file with data like this(Universal ID is student number):")
    print("col1, col2, col3,,,etc")
    print("UNIVERSAL ID, FIRST NAME, LAST NAME,,,etc")
    print("9999999, JIMMY, BLOGGINS,,,etc")
    print("...etc\n")
    print("The \"col1, col2, \" headings can be there or not, doesn't matter.\n")

    # Get a CSV file and read it:

    while True:
        print("If the csv file is not in the default location you'll have to tell me where it is, and what it's called, e.g:")
        print("\"/home/myusername/Documents/students.csv\"\n")

        student_csv_file = utils.input_styled("Where can I find the csv file?  (default = \"{}\", [q]uit) ".format(default_csv_location))

        if student_csv_file == 'q':
            return

        if not student_csv_file:
            student_csv_file = default_csv_location

        if os.path.isfile(student_csv_file):
            break
        else:
            utils.print_error("I couldn't find this file: {} ".format(student_csv_file))


    password = getpass("Enter the admin password: ")

    ssh_connection = SSH(hostname, username, password, verbose=False)

    with open(student_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == 'col1':
                continue
            if row[0] == 'UNIVERSAL ID':
                continue

            # row[0] = student number
            # row[1] = first name
            # row[2] = last name

            add_new_user(
                student_number=row[0],
                first_name=row[1],
                last_name=row[2],
                password=password,
                bulk_creation=True,
                ssh_connection=ssh_connection
            )
    
    ssh_connection.close()

    print("All done!")










