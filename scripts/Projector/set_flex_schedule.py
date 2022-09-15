import json
import re

from sty import fg

from scripts._utils import ssh, pi, utils

hostname = "pi-projector"


def set_flex_schedule():
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)
    ssh_connection.connect_sftp()
    ssh_connection.get_file("/home/pi/clock/components/schedule.json", "/tmp/schedule.json")

    def select_schedule():
        flex_input = utils.input_styled("Which index should the flex schedule be? (int) > ")
        if flex_input.lower() == 'q':
            return True
        elif not flex_input.isdigit():
            print("Not valid index")
            return False

        index = [int(s) for s in flex_input.split() if s.isdigit()]
        index = index[0]

        f = open("/tmp/schedule.json", "r")
        data = json.loads(f.read())
        try:
            print("\n" + data["schedule"][index]["description"] + "\n")
        except IndexError:
            print("Index out of range.")
            return False
        i = 0
        for block in data["schedule"][index]["values"]:
            i += 1
            rgb = re.findall(r'\d+', block['colour'])
            print(
                f"{i}: {block['text']}, {block['start']} - {block['end']} & {fg(rgb[0], rgb[1], rgb[2]) if rgb else fg(128, 128, 128)}{block['colour']}{fg.rs}")

        confirmation = utils.input_styled("\nIs this the correct schedule? [y/N] (q to quit): \n")
        if confirmation and confirmation[0].lower() == "y":
            ssh_connection.send_cmd("touch /home/pi/clock/public/flex-index >> echo '1' > /home/pi/clock/public/flex-index")
            return True
        elif confirmation == "q":
            return True
        else:
            return False

    while True:
        if select_schedule():
            break

    print("\nDone.")
    ssh_connection.close()
