import datetime
import pytz
import time

from scripts.TVs._utils import TV_ROOT, TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW
from scripts.TVs.refresh_slideshow import refresh_slideshow
from scripts.TVs.turn_tv_pi_off_and_on_again import turn_tv_pi_off_and_on_again
from scripts._utils import utils
from scripts._utils import pi

from scripts._utils.ssh import SSH


def tv_report():
    num = utils.input_styled("Enter the TV number (where # is from hostname tv-# e.g: 4) or [q]uit: ")

    if num.lower()[0] == "q":
        # quit
        return

    outputs = []

    def run_commands():
        utils.print_warning("Trying TV #{}...".format(num))
        ssh_connection = SSH(f"pi-tv{num}", pi.username, pi.password)

        for command in commands:
            outputs.append(ssh_connection.send_cmd(command, print_stdout=False).replace("\n", ""))

        ssh_connection.close()

    last_duration = "systemctl status rs | tail -2 | grep Duration | awk 'BEGIN { FS = \" \" }; { printf \"%s %s %s|%s\", $1,$2,$3,$7}'"
    last_played = "systemctl status rs | tail -2 | grep Playing | awk 'BEGIN { FS = \" \" }; { print $7 }'"

    commands = [last_duration, last_played]

    run_commands()

    if last_duration == "" or last_duration == " ":
        # the program is in-between switching media, wait a second a re-run
        utils.print_warning("TV is switching media, please wait.")
        time.sleep(2)
        run_commands()

    try:
        # IF there were outputs
        duration = outputs[0].split("|")[1]
        file_name = outputs[1].split("/")[-1][:-1]
        username = ".".join(file_name.split(".")[:2])
    except IndexError:
        # Outputs could not be indexed; therefore, no logs were present
        utils.print_warning("Unable to verify any logs (did the TV just start-up?)")
        return
    # time it should finish (+ 2 sec)
    datetime_at_finish = pytz.timezone('America/Vancouver').localize(datetime.datetime.strptime(f"{datetime.datetime.now().year} {outputs[0].split('|')[0]}", "%Y %b %d %H:%M:%S") + datetime.timedelta(0, float(duration) + 2))
    now = datetime.datetime.now(pytz.timezone('America/Vancouver'))

    # check if it has been longer than duration + 2 seconds (to account for lag, if any)
    if (datetime_at_finish - now).total_seconds() >= 0:
        read_log = utils.confirm("No issues with the program detected, would you like to view the log anyway?")

        if read_log:
            print(f"File: {file_name}\nTime at start of playing: {outputs[0].split('|')[0]}\nDuration of file: {duration}s\nExpected finish time: ±{datetime_at_finish}\nCurrent time: {now.strftime('%c')}")
        else:
            return
    else:
        delete_file = utils.confirm(f"Program has exceeded playtime, would you like to remove the file causing this? ({file_name})")

        if delete_file:
            ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)
            if file_name.split(".")[-1] == "mp4":
                file_path = f"{TV_ROOT}/tv{num}/{file_name}"
            else:
                file_path = f"{TV_ROOT}/tv{num}/{username}/{file_name}"

            cmd = f"rm {file_path}"
            ssh_connection.send_cmd(cmd, print_stdout=True)

            # confirm it's gone:
            if ssh_connection.file_exists(file_path):
                utils.print_error("\nNot sure what happened there, but the file didn't get deleted.  Sorry!")
            else:
                utils.print_success("\nThe file was successfully deleted.")

            refresh = utils.confirm("Would you like to refresh this user's slideshow?")

            if refresh:
                refresh_slideshow(username=username)

            utils.print_warning("The TV will now recover from the crash by rebooting.")
            turn_tv_pi_off_and_on_again(num)
        else:
            read_log = utils.confirm("Would you like to view the log?")

            if read_log:
                print(
                    f"File: {file_name}\nTime at start of playing: {outputs[0].split('|')[0]}\nDuration of file: {duration}s\nExpected finish time: ±{datetime_at_finish}\nCurrent time: {now.strftime('%c')}")
            else:
                return
