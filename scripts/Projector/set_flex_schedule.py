import json
import re

from sty import fg

from scripts._utils import ssh, pi, utils

hostname = "pi-projector"


def print_schedule(data, index, i=0):
    for block in data["schedule"][index]["values"]:
        i += 1
        rgb = re.findall(r'\d+', block['colour'])
        print(
            f"{i}: {block['text']}, {block['start']} - {block['end']} & {fg(rgb[0], rgb[1], rgb[2]) if rgb else fg(128, 128, 128)}{block['colour']}{fg.rs}")


def set_flex_schedule():
    # Connect to the clock
    ssh_connection = ssh.SSH(hostname, pi.username, pi.password)
    ssh_connection.connect_sftp()
    ssh_connection.get_file("/home/pi/clock/components/schedule.json", "/tmp/schedule.json")  # download the schedule file locally

    def select_schedule():
        # open the schedule.json file
        f = open("/tmp/schedule.json", "r")
        data = json.loads(f.read())

        # onyl used for listing the options, tracks iterations of loop
        i = 0

        for sched in data["schedule"]:
            # print list of descriptions for schedules
            print(f'{i}. {sched["description"]}')
            i += 1

        # get user input on the flex index, this will preview and then prompt a confirmation afterwards
        flex_input = utils.input_styled("Which schedule do you want to preview? (int) (q to quit) > ")
        if flex_input.lower() == 'q':  # q chosen as option; quit.
            return True
        elif not flex_input.isdigit():  # Flex input was not a number.
            print("Not valid index")
            return False

        # get only number if number in string
        index = [int(s) for s in flex_input.split() if s.isdigit()][0]

        try:
            print("\n" + data["schedule"][index]["description"] + "\n")  # Print the description of the schedule
        except IndexError:
            print("Index out of range.")  # The flex inout number is out of range in teh schedule file
            return False

        # Print the blocks & times in the schedule
        print_schedule(data, index)

        confirmation = utils.input_styled("\nIs this the correct schedule? [y/N] (q to quit): \n")
        if confirmation and confirmation[0].lower() == "y":  # update clock file & exit loop
            ssh_connection.send_cmd("touch /home/pi/clock/public/flex-index >> echo '1' > /home/pi/clock/public/flex-index")
            # prompt reboot
            if utils.confirm("Clock requires a reboot to update; would you like to reboot now?"):
                pi.reboot_pi(hostname)
            return True
        elif confirmation == "q":  # Quit loop
            return True
        else:  # Continue while loop
            return False

    # make sure a schedule is chosen or quit is called; do not exit on incorrect input
    while True:
        if select_schedule():
            break

    print("\nDone.")
    ssh_connection.close()
