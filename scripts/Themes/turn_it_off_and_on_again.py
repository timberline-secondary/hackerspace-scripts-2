from scripts._utils.pi import reboot_pi

hostname = "pi-themes"


def turn_it_off_and_on_again():
    reboot_pi(hostname)
