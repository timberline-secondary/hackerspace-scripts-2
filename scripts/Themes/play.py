
from scripts._utils.ssh import SSH
from scripts._utils import pi
from scripts._utils import utils


hostname = "pi-themes"
# this code worked on by Nicholas (Tseilorin) Hopkins

def play():
    # connect to pi-themes
    ssh_connection = SSH(hostname, pi.username, pi.password)
    session = ssh_connection.get_open_session()

    session.exec_command("cd /home/pi/themes && python themes.py silent")
    stdin = session.makefile("wb", -1)
    quitting = False
    while not quitting:
        # gets user input for whatever song they want to play
        song_number = utils.input_styled("Give me a song number. (q to quit): \n")
        if song_number == 'q':
            quitting = True
        else:
            stdin.write(song_number + "\n")
            stdin.flush()

    ssh_connection.close()
