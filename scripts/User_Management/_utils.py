import os, socket, pwd, re
from getpass import getpass
from datetime import date

from scripts._utils import utils
from scripts._utils.ssh import SSH

STUDENT_GID = 5000
TEACHER_GID = 10004

LDIF_FILENAME = '/home/hackerspace_admin/hs-ldap/tmp.ldif'

AUTH_SERVER_HOSTNAME = 'lannister'
FILE_SERVER_HOSTNAME = 'tyrell'
USERNAME = 'hackerspace_admin'


def create_home_dirs(username_list: list, password: str = None):
    """Sends the list of users to the file server and runs this script 

    Arguments:
        username_list {list} -- [description]

    Keyword Arguments:
        password {str} -- [description] (default: {None})
    """
    username_list_as_string = " ".join(username_list)

    make_home_dirs_cmd = 'ssh -t hackerspace_admin@tyrell "sudo /nfshome/makehomedirs.sh {}"'.format(username_list_as_string)

    command_response_list = [
        (make_home_dirs_cmd, "hackerspace_admin@tyrell's password: ", None),
        (password, "[sudo] password for hackerspace_admin: ", None),
        (password, "$", None),
    ]

    if not password:
        password = getpass("Enter the admin password: ")

    ssh_connection = SSH(FILE_SERVER_HOSTNAME, USERNAME, password)

    # why are we doing this through lannister?  ssh direct to tyrell!!!
    success = ssh_connection.send_interactive_commands(command_response_list)

    if success:
        utils.print_success("Looks like it worked!  Unless you see some nasty errors above...")
        return success
    else:
        utils.print_error("Something went wrong but I'm not smart enough to know what...")
        return False


def create_users_from_ldif(ldif_content: str, ssh_connection=None, password=None):
    """Save an ldif file on the authenticationserver and run ldapadd command to create new users with it.
    Use the provided ssh connect if supplied, otherwise create one.

    Arguments:
        ldif_content {str} -- string containing all the ldif entry to create the new users via `ldapadd`
        ssh_connection {[type]} -- [description]
        password {str} -- if user has already entered PW this prevent re-entering it.
    """

    # if we were passed an ssh connection, leave it open, otherwise  we need to create it and close it at the end.
    close_connection = False if ssh_connection else True

    if not ssh_connection:
        if not password:
            password = getpass("Enter the admin password: ")

        ssh_connection = SSH(AUTH_SERVER_HOSTNAME, USERNAME, password)

    # remove old tmp ldif file if it exists
    ssh_connection.send_cmd('rm {}'.format(LDIF_FILENAME), print_stdout=False) # don't care about error if it doesn't exists

    # save the ldif file to lannister
    ssh_connection.send_cmd('echo -e "{}" >> {}'.format(ldif_content, LDIF_FILENAME))


    # use the ldif file to create the user with `ldapadd`
    # https://linux.die.net/man/1/ldapadd
    # -x Use simple authentiction instead of SASL.
    # -D Use the Distinguished Name binddn to bind to the LDAP directory.
    # -W Prompt for simple authentication. This is used instead of specifying the password on the command line. 
    # -f Read the entry modification information from file instead of from standard input. 
    ldap_add_cmd = "ldapadd -x -D cn=admin,dc=hackerspace,dc=tbl -W -f {}".format(LDIF_FILENAME)
    command_response_list = [
                        (ldap_add_cmd, "Enter LDAP Password: ", None),
                        (password, "$", "adding new entry"),
    ]
    success = ssh_connection.send_interactive_commands(command_response_list)

    # if we were passed an ssh connection, leave it open, otherwise close it.
    if close_connection:
        ssh_connection.close()

    return success


def generate_ldif_entry(username, firstname, lastname, uid=None, gid=STUDENT_GID) -> str:

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
        str -- the username if it's new, or {None} if it already exists or bad username
    """

    username = utils.input_styled("What is the new username? (must start with a letter, then any combo of letters, numbers, or _-.) ")
    username = username.lower().strip()
    # make sure it's valid
    if not re.match(r'^[a-zA-Z][\w\-._]+$', username):
        utils.print_error("Invalid username {}".format(username))
        return None

    # does user exist already?
    if utils.user_exists(username):
        fullname = utils.get_users_name(username)
        utils.print_warning("The username {} already exists for {}.".format(username, fullname))
        return None
    else:
        return username


def get_new_users_names(username: str = None) -> tuple:
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

    return firstname.upper().strip(), lastname.upper().strip()


def get_and_confirm_user():
    """ Ask for a username and checks if it exists. If it does, returns a tuple of
    (username, fullname)
    """
    username = utils.input_styled("Enter username: \n")
    # password = getpass("Enter the admin password: ")

    fullname = utils.get_users_name(username)

    if fullname is None:
        utils.print_warning("I couldn't find an account for {}.  Sorry!".format(username))
        return None, None
    else:
        utils.print_success("Found {}: {}.".format(username, fullname))
        is_correct_user = utils.input_styled("Is this the correct student? y/[n] ")

        if is_correct_user.lower() != 'y':
            print("Bailing...")
            return None, None
        else:
            return username, fullname


def modify_user(username, ldif_changes_dict, password=None):
    """[summary]

    Args:
        username: ldap username
        ldif_changes_dict: a dictionary of ldif keys and their new values, e.g {'sn': 'COUTURE', 'givenName': 'TYLERE'}
        password: admin password
    """
    if not password:
        password = getpass("Enter the admin password: ")

    ssh_connection = SSH(AUTH_SERVER_HOSTNAME, USERNAME, password)
    main_command = "sudo ldapmodifyuser {}".format(username)
    EOF = '\x04'  # Ctrl + D

    command_response_list = []

    first = True
    for key, value in ldif_changes_dict.items():
        if first:
            command_response_list.append((main_command, "[sudo] password for hackerspace_admin: ", None))
            command_response_list.append((password, "dc=tbl", None))
            first = False
        else:
            command_response_list.append((main_command, "dc=tbl", None))

        change_tuple = (f"replace: {key}\n{key}: {value}\n{EOF}", '$', None)
        command_response_list.append(change_tuple)

    success = ssh_connection.send_interactive_commands(command_response_list)

    if success:
        utils.print_success("Looks like it worked to me?")
        return True

    else:
        utils.print_error("Something appears to have gone wrong. Hopefully there's a useful error message somewhere up there.")
        return False
