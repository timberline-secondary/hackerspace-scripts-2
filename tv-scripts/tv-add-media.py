import asyncio
import asyncssh
import sys
import subprocess
from urllib.request import urlopen
from urllib.parse import urlparse
import os


class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def run_client2():
    # logged in user, default SSH client keys or certificates
    async with asyncssh.connect('pi-themes', username='pi') as conn:
        async with conn.create_process('bc') as process:
            for op in ['2+2', '1*2*3*4', '2^32']:
                process.stdin.write(op + '\n')
                result = await process.stdout.readline()
                print(op, '=', result, end='')

async def run_client3():
    async with asyncssh.connect('pi-themes', username='pi') as conn:
        await conn.run('tail', input='1\n2\n3\n', stdout='/tmp/stdout')


async def run_client():
    async with asyncssh.connect('pi-themes', username='pi') as conn:
        local_proc = subprocess.Popen(r'echo "1\n2\n3"', shell=True,
                                      stdout=subprocess.PIPE)
        remote_result = await conn.run('tail', stdin=local_proc.stdout)
        print(remote_result)
        #print(remote_result.stdout, end='')


print("#### ADDING ENTRANCE THEMES ####\n")


# get and check the url
have_good_input = False
mp3_url = ""
while not have_good_input:
    mp3_url = input("Paste the url to the mp3 file you want to add or [q]uit: ")

    if mp3_url == 'q':
        break

    # check content to ensure proper mp3 content type.
    try:
        with urlopen(mp3_url) as response:
            ct = response.info().get_content_type()
            if ct == "audio/mpeg":
                print("File looks good.")
                have_good_input = True
            else:
                print("\n* Something is funky about this file.  I expected type 'audio/mpeg' but got '{}'.  "
                      "Make sure it was properly exported to an mp3.".format(ct))

    except ValueError as e:
        print(e)

if have_good_input:

    have_good_input = False
    while not have_good_input:
        filename = os.path.basename(urlparse(mp3_url).path)
        name, ext = os.path.splitext(filename)

        print("test")

        # check if the filename is already a number, and offer to use it
        try:
            name = int(name)
            good_name_already = True
        except ValueError:
            good_name_already = False

        mp3_number = "What number do you want to give it? " + ("[Enter] = {}".format(name) if good_name_already else "")

        try:
            if good_name_already and mp3_number:
                mp3_number = name
            else:
                mp3_number = int(mp3_number)
            have_good_input = True
        except ValueError:
            print("Dude, that wasn't a number! ")
            have_good_input = False


    #mp3_name = input(prompt)

    print("test: {}".format(mp3_url))

    # try:
    #     asyncio.get_event_loop().run_until_complete(run_client())
    # except (OSError, asyncssh.Error) as exc:
    #     sys.exit('SSH connection failed: ' + str(exc))

else:
    print("Quitting...")


