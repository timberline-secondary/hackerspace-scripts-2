import os
import csv

from scripts._utils import utils, ssh

from getpass import getpass

from .add_new_user import add_new_user

hostname = 'lannister'
server_username = 'hackerspace_admin'

default_csv_location = os.path.expanduser("~") + "/Downloads/StudentList.csv"


def add_new_users_csv_import():

    utils.print_warning("""
Importing new users in bulk requires a csv file with at least these two fields (extra fields are ok):

Name, Email1
"Bloggins, Jimmy", "jimmy.bloggins@stu.sd72.bc.ca"
...etc

There should be no headings row, just students.
Usernames can include @stu.sd72.bc.ca or not.  If it is included, it will be removed and only firstname.lastname will be used for their username
""")
    print("""To get this list from MyEd:
1. Go to the Students tab
2. Click the filter and choose Students in My Classes
3. Select the grid icon beside the filter and choose EMAIL STUDENT SD72...
4. Click the print icon and choose CSV
5. Save the file to your Downloads as StudentList.csv
""")

    # Get a CSV file and read it:

    while True:
        utils.print_warning(
            "If the csv file is not in the default location you'll have to tell me where it is, and what it's called, e.g:")
        utils.print_warning('"/home/myusername/Documents/students.csv"')

        student_csv_file = utils.input_plus('Where can I find the csv file?', default_csv_location)
        if student_csv_file == 'q':
            return

        if os.path.isfile(student_csv_file):
            # good, carry on with script
            break
        else:
            utils.print_error("I couldn't find this file: {} ".format(student_csv_file))

    password = getpass("Enter the admin password: ")

    # userlist = []
    # next_uid = None
    # ldif_entry = ""

    name_heading = "Name"
    email_heading = "Email1"

    ssh_connection = ssh.SSH(hostname, server_username, password)

    with open(student_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        name_column = None
        email_column = None
        for row in csv_reader:
            if name_column is None:  # then this is the header row               
                try:
                    name_column = row.index(name_heading)
                    email_column = row.index(email_heading)
                except ValueError:  # column doesn't exist
                    ssh_connection.close()
                    return False
            else:
                try:
                    username = parse_username_from_email(row[email_column])
                except IndexError:
                    # Probably blank lines at the end of the list, or missing data?  Even missing data should be a blank string
                    print("Skipping line. Blank line at end of list or missing student email field.")
                    continue

                # Check if user already exists or not
                if utils.user_exists(username):
                    utils.print_warning("This user already exists: {}".format(username))
                    continue  # go to next user

                # Name column is in format: "Lastname, Firstname"
                first_name = row[name_column].split(",")[1]
                last_name = row[name_column].split(",")[0]

                add_new_user(
                    username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    ssh_connection=ssh_connection,
                    bulk_creation=True,
                )

                # next_uid = get_next_avail_uid()
                # ldif_entry += generate_ldif_entry(username, first_name, last_name, next_uid) + "\n"

                # success = create_users_from_ldif(ldif_entry, password=password)

                # create home dir for new user
                # if success:
                #     return create_home_dirs([username], password)

    ssh_connection.close()
    print("All done!")


def parse_username_from_email(username: str) -> str:
    """ Takes a username in the format firstname.lastname or 
    firstname.lastname@stu.sd72.bc.ca and returns only firstname.lastname all lowercase
    """
    return username.split("@")[0].lower()
