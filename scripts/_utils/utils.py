import io
import pwd
from getpass import getpass
from typing import Union, Tuple

import PIL
import magic
import imageio.v2 as imageio
from urllib.error import URLError
from urllib.request import urlopen
import subprocess
from PIL import Image
import moviepy.editor as mp
import urllib.request

# from getpass import getpass

LOCALDOMAIN = "hackerspace.tbl"


class ByteStyle:
    HEADER = '\033[95m'  # intense purple
    SUCCESS = '\033[92m'  # intense green
    WARNING = '\033[93m'  # intense yellow
    ERROR = '\033[91m'  # intense red
    ENDC = '\033[0m'  # resets
    BOLD = '\033[1m'  # makes it bold
    UNDERLINE = '\033[4m'  # underlines
    INPUT = '\033[1;33m'  # bold yellow
    # Y_N = '\033[0;33m'  # dark yellow (brown)
    Y_N = '\033[36m'  # cyan


def print_styled(text, color):
    print(color + text + ByteStyle.ENDC)


def print_success(text):
    print_styled(text, color=ByteStyle.SUCCESS)


def print_warning(text):
    print_styled(text, color=ByteStyle.WARNING)


def print_error(text):
    print_styled(text, color=ByteStyle.ERROR)


def input_styled(text, color=ByteStyle.INPUT):
    return input(color + text + ByteStyle.ENDC).strip()


def print_heading(title):
    width = 60
    title = title.upper()
    if len(title) > width - 4:
        title = title[:width - 7] + "..."
    print_styled("#" * width, color=ByteStyle.HEADER)
    print_styled("#" + title.center(width - 2, " ") + "#", color=ByteStyle.HEADER)
    print_styled("#" * width, color=ByteStyle.HEADER)
    print()


# simple wrapper over common method
def get_computers_prompt(hostname=None, password=None):
    if password is None:
        password = getpass("Enter the admin password: ")

    if hostname is None:
        hostname = input_styled("Enter the computer numbers or name, seperated by spaces \n"
                                "(where # is from hostname tbl-h10-#-s e.g: test 2 15 30)\n"
                                " or 'all' to run on all computers or [q]uit: ")

        if hostname == "q":
            print("Quitting this.")
            return None, None

        num_list = hostname.split()

        if num_list == "":
            return

        if num_list[0].lower() == "all":
            num_list = [f"{i}" for i in range(0, 32)]  # list of strings.  0 will cause problem if int instead of str

        return num_list, password


def verify_mimetype(file_url, mimetype_string, local=False):
    mt = ''

    if mimetype_string is None:
        print_error(" This media type is not supported.")
        return False

    file_url = file_url.strip()

    if local:
        try:
            mt = magic.from_file(file_url, mime=True)
        except FileNotFoundError as e:
            print("Can't find this file.")
            print_error(str(e))
    else:  # web url
        try:
            with urlopen(file_url) as response:
                mt = response.info().get_content_type()
        except ValueError as e:
            print_error(str(e))
        except URLError as e:
            print("That is a bad URL.")
            print_error(str(e))

    if mt == mimetype_string:
        print_success(f"File looks good: {mt}")
        return True
    else:
        print_error(f"Something is funky about this file. I expected type '{mimetype_string}' but got '{mt}'.")
        return False


def is_ffmpeg_compatible(file_url) -> bool:
    """
    Checks to see if the file (local and non-local) is compatible with ffmpeg.
    :returns: success
    """
    command = "ffmpeg -y -v error -i " + file_url + " /tmp/verify-ffmpeg.mp4"
    err = subprocess.run(command.split(" "), capture_output=True).stderr
    return err == b''


def find_gif_duration(img_obj) -> float:
    """
    Returns duration of gif in seconds
    """
    return img_obj.info["duration"] / 1000


def remove_gif_transparency(image, file_url) -> str:
    """
    Removes the transparent background of a gif and replaces it with black
    :returns: file_url
    """

    # Set the transparent pixels to black
    image.info['transparency'] = 0

    try:
        image.save('/tmp/corrected.gif', **image.info)
        return '/tmp/corrected.gif'
    except PIL.UnidentifiedImageError:
        return file_url


def process_gif(image, file_url) -> Tuple[bool, Union[str, None], bool, str]:
    """
    Processes gif to static image or mp4
    (If the gif has 1 frame it will be converted to a png and transparency removed,
     if it has duration of <5s it will loop over the gif to reach the target of >=5s and convert to mp4,
     if it's already >=5s it will be converted directly)
    :returns: success, media_url, and local (if media_url is local path)
    """
    if not image.is_animated:  # gif with 1 frame -> png
        image.seek(1)  # go to 1st frame
        image.save('/tmp/verified.png', **image.info)  # save the first frame to a png img
        new_image = Image.open('/tmp/verified.png')
        return remove_transparency(new_image, '/tmp/verified.png', ".png")
    else:  # animated gif -> mp4
        duration = find_gif_duration(image)
        if duration > 5:
            # FFMPEG command (without looping)
            command = f"ffmpeg -i {file_url} -c:v libx264 -movflags faststart -pix_fmt yuv420p -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" /tmp/verified.mp4"
            err = subprocess.run(command.split(" "), capture_output=True).stderr
            if err == b'':
                return True, '/tmp/verified.mp4', True, ".mp4"
            else:
                return False, file_url, False, ".gif"
        else:
            # Calculate the number of times the GIF needs to be looped to reach the target duration
            n_loops = int((5 // duration) + 1)
            # FFMPEG command
            command = f"ffmpeg -stream_loop {n_loops} -i {file_url} -c:v libx264 -movflags faststart -pix_fmt yuv420p -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" /tmp/verified.mp4"
            err = subprocess.run(command.split(" "), capture_output=True).stderr
            if err == b'':
                return True, '/tmp/verified.mp4', True, ".mp4"
            else:
                return False, file_url, False, ".gif"


def process_svg(svg_url) -> Tuple[bool, Union[str, None], bool, str]:
    """
    Processes svg to png
    :returns: success, media_url, and local (if svg_url is local path)
    """
    command = 'inkscape -z -e {} -w 1920 -h 1080 {}'.format('/tmp/verified-svg.png', svg_url)
    err = subprocess.run(command.split(" "), capture_output=True).stderr
    if err == b'':
        return True, '/tmp/verified-svg.png', True, ".png"
    else:
        return False, svg_url, False, ".svg"


def remove_transparency(image, file_url, extension) -> Tuple[bool, Union[str, None], bool, str]:
    """
    Removes transparent background from png to opt for a black background
    :returns: success, media_url, local (if svg_url is local path), and extension
    """

    # convert alpha channel colors back to their respective color without any transparency
    image.convert('RGB')

    try:
        image.save('/tmp/corrected.png', **image.info)
        return True, '/tmp/corrected.png', True, ".png"
    except PIL.UnidentifiedImageError:
        return False, file_url, False, extension


def verify_image_integrity(file_url: str, mime: str, local: bool, extension: str) -> Tuple[
    bool, Union[str, None], bool, str]:
    """
    Verifies image media integrity (i.e. png, jpg, gif, etc.)
    :returns: success, media_url, local (if media_url is local path), and extension
    """
    valid_types = [
        "image/png",
        "image/jpeg",
        "image/svg+xml",
        "image/gif"
    ]

    # this function is only for image media integrity :)
    if mime not in valid_types:
        return True, file_url, local, extension

    try:  # test if input is image
        if local:
            im = Image.open(file_url)
        else:
            try:
                path = io.BytesIO(urllib.request.urlopen(file_url).read())
                im = Image.open(path)
            except (URLError, ValueError):
                print_error("Bad URL")
                return False, file_url, local, extension
    except PIL.UnidentifiedImageError:  # input is not image
        print_error("Bad path")
        return False, file_url, local, extension

    if mime == 'image/svg+xml':
        success, path, _, _ = process_svg(file_url)
        if success:
            try:
                image = Image.open(path)
                return remove_transparency(image, path, extension)
            except PIL.UnidentifiedImageError:
                print_error("Something went wrong")
                return False, file_url, local, extension
        else:
            return False, file_url, local, extension
    elif mime == 'image/png':
        return remove_transparency(im, file_url, extension)
    elif mime == 'image/gif':
        return process_gif(im, file_url)
    else:  # if image is not a gif
        try:
            if not is_ffmpeg_compatible(file_url):  # Check if not compatible
                im.save("/tmp/verified-ffmpeg.png")  # If not compatible re-save image
                if is_ffmpeg_compatible("/tmp/verified-ffmpeg.png"):  # Check compatibility again
                    # File converted to compatible image format
                    return True, '/tmp/verified-ffmpeg.png', True, ".png"
                else:
                    print_error("Image cannot be verified nor converted.")  # File is corrupt
                    return False, None, local, extension
            else:
                # file is already ffmpeg compatible
                return True, file_url, local, extension
        except Exception as e:
            # subprocess error, or pillow saving error; file could not be verified
            print_error(f'File could not be verified with mime: {mime}; {e}')
            return False, None, local, extension


def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def get_valid_hostname(computer_number=None):
    good_host = False
    while not good_host:
        if computer_number:
            computer_host = "tbl-h10-{}".format(computer_number)
        else:
            computer_host = input_styled("Which computer? (e.g. 'tbl-h10-12', or '192.168.3.125' or [q]uit) ")

        if computer_host == 'q':
            print("Quitting this.")
            return None

        good_host = host_exists(computer_host)

        if computer_number and not good_host:  # this computer # doesn't exist or can't connect
            return None

        if good_host:
            return computer_host


def host_exists(hostname, verbose=True, use_fqdn=True):
    if use_fqdn:
        hostname_2 = get_fqdn(hostname)
    else:
        hostname_2 = hostname

    ping_cmd = ['ping', '-c 1', '-W 1', hostname_2]  # ping once with 1 second wait/time out
    if verbose:
        print_warning("Checking to see if {} is connected to the network.".format(hostname_2))

    compeleted = subprocess.run(ping_cmd)

    if compeleted.returncode != 0:  # not success
        # Try again without fqdn, just in case
        if use_fqdn:
            return host_exists(hostname, verbose=True, use_fqdn=False)

        if verbose:
            print_error("{} was not found on the network.  Is there a typo? Is the computer on?".format(hostname))
        return False
    else:
        if verbose:
            print_success("{} found on the network.".format(hostname))
        return True


def get_fqdn(hostname):
    """ Appends the local domain "hackerspace.tbl" if it isn't already there """
    if LOCALDOMAIN not in hostname:
        hostname = f"{hostname}.{LOCALDOMAIN}"
    return hostname


def input_plus(prompt, default=None, validation_method=None):
    """ Gets styled user input with a defualt value and option to quit.  Returns 'q' if quitting.
    Validation_method is not yet implemented.
    """
    hints_str = "[q]uit"

    if default:
        hints_str += f" | [Enter] = {default}"

    prompt = prompt + " (" + hints_str + "): "
    response = input_styled(prompt).strip()
    if response == "":  # they just hit enter for default, or None
        return default
    elif response == "q":
        print("quitting...")
        return response
    else:
        return response


def confirm(prompt, yes_is_default=True):
    """Ask the use to confirm an action (the prompt) with y or n."""

    if yes_is_default:
        yn_prompt = " [y]/n "
    else:
        yn_prompt = " y/[n] "

    do_it = input_styled(prompt + yn_prompt, color=ByteStyle.Y_N)

    if yes_is_default:
        if do_it == "" or do_it[0].lower() != 'n':
            return True
        else:
            return False
    else:
        if do_it == "" or do_it[0].lower() != 'y':
            return False
        else:
            return True

# def get_admin_pw():
#     # ask for admin password
#     while True:
#         password = getpass("Enter admin password: ")
#         print("Give me a moment to check the password...")
#         completed_process = subprocess.run(
#             ["su", "hackerspace_admin", ">", "/dev/null"], 
#             text=True,
#             input=password,
#             capture_output=False)
#         if completed_process.returncode == 0:
#             # it's good
#             return password
#         else:
#             # bad password
#             print_error("Incorrect Password. Try again.")
