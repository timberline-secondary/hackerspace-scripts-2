from scripts._utils import utils
from scripts._utils.ssh import SSH

from scripts.TVs._utils import TV_FILE_SERVER, TV_FILE_SERVER_PW, TV_FILE_SERVER_USER, TV_ROOT


def refresh_slideshow(username=None):

    if not username:
        username = utils.input_styled("Enter username: \n")

    # connects and checks to see if file with the same name already exisits
    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    print("Updating movie maker script...")
    copy_movie_maker_to_host(ssh_connection)

    # Cycle through TV directories to find student folder
    for tv in range(1, 5):
        filepath = "{}/tv{}/".format(TV_ROOT, tv)
        command = 'ls {}'.format(filepath)
        dir_contents = ssh_connection.send_cmd(command, print_stdout=False).split()
        if username in dir_contents:
            utils.print_success("Found art for {} on TV# {}".format(username, tv))

            # refresh the video
            utils.print_warning("\nGonna regenerate video slideshow now, THIS MIGHT TAKE A WHILE!")
            generate_new_movie_file(ssh_connection, username, tv)
            return True

    utils.print_error("\nSorry, I could find art for {}.  Are you sure they have art uploaded to the server?".format(username))
    return None


def copy_movie_maker_to_host(ssh_connection):
    # overwrite if it already exists in case it has been updated.
    ssh_connection.copy_file('scripts/_utils/movie_maker_fade.py', '{}/movie_maker.py'.format(TV_ROOT))


def generate_new_movie_file(ssh_connection, username, tv, silent=False):

    output = '/tmp/slideshow.mp4'
    # remove existing file
    ssh_connection.send_cmd('rm {}'.format(output), print_stdout=False)  # don't care about error if it doesn't exists

    # create video in defaul location
    cmd = 'python3 movie_maker.py --images tv{}/{} --output {}'.format(tv, username, output)
    ssh_connection.send_cmd(cmd)

    # move the file into the proper location
    success = ssh_connection.send_cmd('cp {} {}/tv{}/{}.a.mp4'.format(output, TV_ROOT, tv, username))

    if success == '':
        if not silent:
            # copy so still avail for tv 4 move
            utils.print_success(f"Video created and placed on tv {tv}.")

        # also place on tv4
        if tv != 4:
            success = ssh_connection.send_cmd('cp {} {}/tv4/{}.a.mp4'.format(output, TV_ROOT, username))
            if success == '':
                if not silent:
                    utils.print_success("Also placed on tv 4.")
            else:
                utils.print_error("Something went wrong sending to tv 4.")

    else:
        utils.print_error(f"Something went wrong sending to tv {tv}.")
