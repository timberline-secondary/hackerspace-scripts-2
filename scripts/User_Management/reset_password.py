import os, socket
from getpass import getpass

print(os.getcwd())
from scripts._utils import utils
from scripts._utils.ssh import SSH

hostname = socket.gethostname() # can use the local computer
username = 'hackerspace_admin'

def reset_password():
    sn = utils.input_styled(
        "Enter the student number of the student whose password you want to reset to 'wolf': ")

    pw = getpass("You'll have to enter the Hackerspace's admin password twice. Password: ")
    
    cmd = 'su -c "echo -e \\"{}\nwolf\nwolf\\" | sudo -S passwd {}" -m hackerspace_admin'.format(pw, sn)
    os.system(cmd)

# def reset_password():
#     sn = utils.input_styled(
#         "Enter the student number of the student whose password you want to reset to 'wolf': ") 
#     pw = getpass("Password: ")

#     ssh_connection = SSH(hostname, username, pw)

#     # https://www.youtube.com/watch?v=lLKdxIu3-A4
#     channel = ssh.invoke_shell()

#     stdin, stdout, stderr = ssh_connection.client.exec_command("sudo passwd {}".format(sn))

#     stdin.write(pw)
#     stdin.write('\n')
#     stdin.flush()
#     stdin.write('wolf')
#     stdin.write('\n')
#     stdin.flush()
#     stdin.write('wolf')
#     stdin.write('\n')
    
#     output = stdout.readlines()
#     print('\n'.join(output))

#     # output = str(stdout.read(), 'utf8') # convert from bytestring for newlines to work
#     # print (output)

#     ssh_connection.close()



    # session = ssh_connection.get_open_session()

    # session.exec_command("sudo passwd {}".format(sn))
    # stdin.write(pw + "\n") # sudo
    # stdin.flush()
    # stdin.write('wolf\n')
    # stdin.flush()
    # stdin.write('wolf\n')
    # stdin.flush()
    
    # stdout = session.makefile("rb", -1)
    # output = str(stdout.read(), 'utf8')
    # print(output)

