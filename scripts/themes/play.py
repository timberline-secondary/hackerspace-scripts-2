
from scripts._utils.ssh import SSH
from scripts._utils import pi

hostname = "pi-themes"
#this code worked on by Nicholas (Tseilorin) Hopkins

def play():
    # connect to pi-themes
    ssh_connection = SSH(hostname, pi.username, pi.password)
    ssh_connection.connect()
    transport = ssh_connection.ssh_client.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()

    session.exec_command("sudo bash startthemes.sh")
    stdin = session.makefile("wb", -1)
    quitting = False
    while not quitting:
        #gets user input for whatever song they want to play
        song_number = input("Give me a song number. (q to quit): ")
        if song_number == 'q':
            quitting = True

        else:

            stdin.write(song_number + "\n")
            stdin.flush()

    ssh_connection.close()