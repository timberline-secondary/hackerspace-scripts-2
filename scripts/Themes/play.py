
from scripts._utils.ssh import SSH
from scripts._utils import pi
from scripts._utils import utils


hostname = "pi-themes"
#this code worked on by Nicholas (Tseilorin) Hopkins

def play():
    # connect to pi-themes
    ssh_connection = SSH(hostname, pi.username, pi.password)
    transport = ssh_connection.client.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()

    session.exec_command("sudo bash startthemes.sh")
    stdin = session.makefile("wb", -1)
    quitting = False
    while not quitting:
        #gets user input for whatever song they want to play
        song_number = utils.input_styled(utils.ByteStyle.INPUT, "Give me a song number. (q to quit): \n")
        if song_number == 'q':
            quitting = True

        else:

            stdin.write(song_number + "\n")
            stdin.flush()

    ssh_connection.close()