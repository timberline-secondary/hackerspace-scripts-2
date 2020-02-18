import os
from urllib.parse import urlparse

from scripts._utils import utils
from scripts._utils.ssh import SSH
from scripts.User_Management._utils import get_student_name2, get_new_username, get_new_user_names, get_next_avail_uid, generate_ldif
from getpass import getpass

hostname = 'lannister'
admin_username = 'hackerspace_admin'

ldif_filename = '/home/hackerspace_admin/hs-ldap/tmp.ldif'

def add_new_user_v2(username=None, first_name=None, last_name=None, password=None, bulk_creation=False, ssh_connection=None):

    if not username:
        username = get_new_username()

    # if username is not None:
    #     if bulk_creation:
    #         utils.print_warning("An account for {}, {}, already exists, skipping... ".format(student_number, student))
    #         return
    #     else:
    #         utils.print_warning("An account for {}, {}, already exists.  Try resetting their password if they can't log in.".format(student_number, student))
    #         return
    # else:

    if not first_name:  # no name provide to function
        first_name, last_name = get_new_user_names(username)

    create = utils.input_styled("Create account for {} {} {}? y/[n] \n".format(username, first_name, last_name))

    if create.lower() == 'y':
        # generate ldif file
        uid = get_next_avail_uid()
        ldif = generate_ldif(username, first_name, last_name, uid)

        if not ssh_connection:
            if not password:
                password = getpass("Enter the admin password: ")
            ssh_connection = SSH(hostname, admin_username, password)
            
            # remove old tmp ldif file if it exists
            ssh_connection.send_cmd('rm {}'.format(ldif_filename), print_stdout=False) # don't care about error if it doesn't exists

            # save the ldif file to lannister
            ssh_connection.send_cmd('echo -e "{}" >> {}'.format(ldif, ldif_filename))

            ldap_add_cmd = "ldapadd -x -D cn=admin,dc=hackerspace,dc=tbl -W -f {}".format(ldif_filename)
            # use the ldif file to create the user

            command_response_list = [
                                (ldap_add_cmd, "Enter LDAP Password: ", None),
                                (password, "$", "adding new entry"),
            ]
            success = ssh_connection.send_interactive_commands(command_response_list)

            if success:
                make_home_dirs_cmd = 'ssh -t hackerspace_admin@tyrell "sudo /nfshome/makehomedirs.sh {}"'.format(username)

                command_response_list = [
                                (make_home_dirs_cmd, "hackerspace_admin@tyrell's password: ", None),
                                (password, "[sudo] password for hackerspace_admin: ", None),
                                (password, "$", None),
                ]
                # why are we doing this through lannister?  ssh direct to tyrell!!!
                success = ssh_connection.send_interactive_commands(command_response_list)

                if success:
                    utils.print_success("Looks like it worked!  Unless you see some nasty errors above...")
                else:
                    utils.print_error("Something went wrong but I'm not smart enough to know what...")

                

                    

                    # now create home drives
                    # # create home drives. Because we are using autofs, they won't be created when the user logs in.
                    # echo -e "Creating home directories for the new users."
                    # ssh -t hackerspace_admin@tyrell "sudo /nfshome/makehomedirs.sh ${new_user_array[*]}"


            #     if not bulk_creation:
            #         ssh_connection.close()

            #     if success:
            #         utils.print_success('Successfully created account for {} {} {}'.format(username, first_name, last_name))
            #         utils.print_success('Their default password will be "wolf"')
            #         created = True
            #     else:
            #         utils.print_error("Something went wrong there, hopefully useful info is printed above...let's try again\n")

            # else:
            #     print("Aborted that one. \n")

            #     if bulk_creation or utils.input_styled("Try again? [y]/n: ") == 'n':
            #         return





# hackerspace_admin@tyrell:/nfshome$ cat makehomedirs.sh 
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

# exit $exit_code
