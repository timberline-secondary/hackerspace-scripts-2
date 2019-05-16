
from scripts._utils.ssh import SSH


def test():
    hostname = "pi-themes"
    username = "pi"
    password = "hackerberry"

    #
    # hostname = input("Hostname: ")
    # username = input("Username: ")
    # password = input("Password: ")

    ssh_connection = SSH(hostname, username, password)
    ssh_connection.connect()

    command = input("What command would you like to run with sudo?: ")

    output = ssh_connection.send_cmd(command)
    print(output)

    ssh_connection.close()

# check the hackerspace github for some example sudo scripts that do work