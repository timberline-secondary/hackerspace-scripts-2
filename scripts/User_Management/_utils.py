import os, socket, pwd
from getpass import getpass
from datetime import date

from scripts._utils import utils
from scripts._utils.ssh import SSH

STUDENT_GID = 5000
TEACHER_GID = 10004

def generate_ldif(username, firstname, lastname, uid, gid=STUDENT_GID) -> str:

    if not uid:
        uid = get_next_avail_uid()

    ldif_content = """dn: uid={username},ou=Users,dc=hackerspace,dc=tbl
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: {username}
sn: {lastname}
givenName: {firstname}
cn: {firstname} {lastname}
displayName: {firstname} {lastname}
uidNumber: {uid}
gidNumber: {gid}
userPassword: wolf
gecos: {firstname} {lastname}
loginShell: /bin/bash
homeDirectory: /home/{username}
""".format(
        username=username, 
        uid=uid,
        gid=gid,
        firstname=firstname,
        lastname=lastname
    )

    return ldif_content


def get_next_avail_uid(start: int = None) -> int:
    """Check if {start} is available as a uid, then increase by one untill
    an available uid is found.  If no {start} is provided, then the first number will 
    be the two-digit year followed by three zeros.  E.g. in 2022 -> start = 22000
    
    Keyword Arguments:
        start {int} -- The uid to check first (default: {None})
    """
    if start is None or start < 1000:
        # last two digits of current year x 1000, e.g. 2021 -> 21000
        start = int(date.today().strftime('%y')) * 1000

        if start < 1000:
            utils.print_warning("uid should be > 1000, using the default instead: {}".format(start))

    # get list of all users
    next_uid = start
    while True:
        try:
            next_uid = pwd.getpwuid(next_uid).pw_uid
            # print(next_uid)
            next_uid += 1
        except KeyError:  # new uid found!
            break

    return next_uid


def get_new_username() -> str:
    """Asks for a new username and checks if it already exists or not
    
    Returns:
        str -- the username if it's new, or {None} if it already exists
    """

    username = utils.input_styled("Enter new username (please match with school username, e.g. firstname.lastname or 99#####): ")
    username = username.lower().strip()

    # does user exist already?
    try:
        user = pwd.getpwnam(username) # will throw an exception if doesn't exist already
        utils.print_warning("This user already exists: {}".format(user))
        return None
    except KeyError:  # it's a new username because doesn't exist
        return username

def get_new_user_names(username: str = None) -> tuple:
    """Primpts for a new user's first and last name
    
    Arguments:
        username {str} -- the user's username.  If there is a dot, it will provide  default names assuming
        the username is firstname.lastname
    
    Returns:
        tuple -- (firstname, lastname)
    """

    firstprompt = "First name: "
    lastprompt = "Last name: "
    if username and '.' in username:
        name_guess = username.split(sep='.')
        firstprompt += "[Enter = {}]".format(name_guess[0].upper().strip())
        lastprompt += "[Enter = {}]".format(name_guess[1].upper().strip())
    else:
        name_guess = None

    firstname = None
    lastname = None
    while not firstname:
        firstname = utils.input_styled(firstprompt).upper().strip() or (name_guess[0] if name_guess else "")  # noqa
        if not firstname:
            utils.print_error("Come on, I'm sure they have a name.  I need a name or I can't continue")
    while not lastname:
        lastname = utils.input_styled(lastprompt).upper().strip() or (name_guess[1] if name_guess else "")  # noqa
        if not lastname:
            utils.print_error("They need a last name too buds.")


    # print(username, firstname or "(No first name provided)", lastname or "(No last name provided)")

    return firstname, lastname


def get_student_name2(username) -> str:
    """Iff the user exists, get their first and last name from the gecos field
    
    Arguments:
        username {[type]} -- [description]
    
    Returns:
        str -- The user's first and last name in a single string, else None if user doesn't exist
    """
    try:
        user = pwd.getpwnam(str(username)) # will throw an exception if doesn't exist already
        return user.pw_gecos
    except KeyError:  # username doesn't exist
        return None


def get_student_name(student_number, password=None):
    """Get a student's full name from their student number.  Return None if account doesn't exist.

    # TODO redo this with pwd: https://docs.python.org/3.7/library/pwd.html
    
    Arguments:
        student_number {str} -- username
    
    Keyword Arguments:
        password {str} -- admin password
    
    Returns:
        str -- student's full name, or None is student doesn't exist.
    """

    hostname = socket.gethostname() # can use the local computer
    username = 'hackerspace_admin'
    if not password:
        password = getpass("Enter the admin password: ")

    ssh_connection = SSH(hostname, username, password, verbose=False)

    # the ^ is regex for "starting with", and after the username should be a colon :
    # this ensures unique results
    command = "getent passwd | grep ^{}:".format(student_number)
    result = ssh_connection.send_cmd(command, sudo=True, print_stdout=False)

    ssh_connection.close()
    
    # results example, split on colons
    #  *****
    #  [sudo] password for hackerspace_admin: 
    #  9912345:x:16000:16000:John Doe:/home/9912345:/bin/bash

    user_info_list = result.split(':')

    # no user info returned, doesn't exist
    if len(user_info_list) == 2:
        return None
    else:
        return user_info_list[5]

def get_and_confirm_user(password=None):
    # TODO redo this with pwd: https://docs.python.org/3.7/library/pwd.html
    student = None
    while student is None:
        student_number = utils.input_styled("Enter student number: \n")
        if password is None:
            password = getpass("Enter the admin password: ")
        
        student = get_student_name(student_number, password)

        if student is not None:
            confirm = utils.input_styled("Confirm account: {}, {}? [y]/n".format(student_number, student))
            if confirm == 'n':
                student = None
            else:
                return student_number
        
            
#####################################
# /nfshome/makehomedirs.sh
# #!/bin/bash
# if [ $# -lt 1 ]; then
#     echo "Syntax: $_ USER[ USER[ ...]]" >&2
#     exit 1
# fi

# exit_code=0

# for user in "$@"; do
#     home="/nfshome/$user"
    
#     # Check whether user account exists first
#     USEREXISTS=$(getent passwd | grep ^$user:)
#     if [ ! "$USEREXISTS" ]; then
# 	echo $'\e[31m'"User does not exist: $user"$'\e[m'
#     elif [ -d "$home" ]; then
# 	echo $'\e[31m'"Home drive already exists: $home"$'\e[m'
#     else
# 	group="students"
#         cp -R /etc/skel "$home" && echo $'\e[32m'"Copied skeleton to: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to create: $home"$'\e[m' ) >&2
#         chown -R "$user:$group" "$home" && echo $'\e[32m'"Set owner on: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to set owner on: $home"$'\e[m' ) >&2
#     fi
# done
