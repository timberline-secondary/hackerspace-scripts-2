from getpass import getpass

from scripts._utils import utils

from scripts.Workstation_Management.run_command_on_computers import run_command


def lab_report(print_stdout=True):
    num_list, password = utils.get_computers_prompt()

    cpu_command = "top -bn2 | grep '%Cpu' | tail -1 | grep -P '(....|...) id,'|awk '{print 100-$8 \"%\"}'"
    last_boot = "last reboot | head -1 | awk 'BEGIN { FS = \" \" }; { print $5,$6,$7,$8 }'"
    avail_space = "df /dev/nvme0n1p2 -h --total | grep total | head -c-3 | awk '{ printf \"%s% (%s / %s)\", 100 - $NF, $3, $2}'"

    commands = ["hostname -I", "awk -F: 'BEGIN { FS = \"Last run: \" }; { print $2 }' /etc/motd",
                last_boot, avail_space, "uname -r", cpu_command]

    # options was quit
    if num_list is None and password is None:
        return False

    outputs = []

    for num in num_list:
        utils.print_warning("Trying computer #{}...".format(num))
        output, computer = run_command(num, password, commands, sudo=False)
        output = [out.replace("\n", "") for out in output] if output else [""] * len(commands)
        if print_stdout:
            outputs.append({"name": computer, "outputs": output})

    if print_stdout:
        for com in outputs:
            utils.print_success(f"\nRan command with output of:\n")
            print("-" * 10 + f" {com['name']} " + "-" * 10)
            print(f"Connection status: {'true' if com['outputs'][0] else 'false'}")
            print(f"Local IP: {com['outputs'][0] if com['outputs'][0] else 'N/A'}")
            print(f"Last puppet run: {com['outputs'][1] if com['outputs'][1] else 'N/A'}")
            print(f"Last boot: {com['outputs'][2] if com['outputs'][2] else 'N/A'}")
            print(f"Available Space: {com['outputs'][3] if com['outputs'][3] else 'N/A'}")
            print(f"Kernel: {com['outputs'][4] if com['outputs'][4] else 'N/A'}")
            print(f"CPU Usage: {com['outputs'][5] if com['outputs'][5] else 'N/A'}")
            print("-" * 32 + "\n")
