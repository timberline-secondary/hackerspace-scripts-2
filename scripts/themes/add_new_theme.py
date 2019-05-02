# import os
# import subprocess
# from urllib.parse import urlparse
# from urllib.request import urlopen
#
# import asyncssh
#
# from scripts._utils import utils
#
#
# async def run_client2():
#     # logged in user, default SSH client keys or certificates
#     async with asyncssh.connect('pi-themes', username='pi') as conn:
#         async with conn.create_process('bc') as process:
#             for op in ['2+2', '1*2*3*4', '2^32']:
#                 process.stdin.write(op + '\n')
#                 result = await process.stdout.readline()
#                 print(op, '=', result, end='')
#
# async def run_client3():
#     async with asyncssh.connect('pi-themes', username='pi') as conn:
#         await conn.run('tail', input='1\n2\n3\n', stdout='/tmp/stdout')
#
#
# async def run_client():
#     async with asyncssh.connect('pi-themes', username='pi') as conn:
#         local_proc = subprocess.Popen(r'echo "1\n2\n3"', shell=True,
#                                       stdout=subprocess.PIPE)
#         remote_result = await conn.run('tail', stdin=local_proc.stdout)
#         print(remote_result)
#         #print(remote_result.stdout, end='')
#
#
# def add_new_theme():
#     # get and check the url of the file
#     have_good_input = False
#     mp3_url = ""
#     while not have_good_input:
#         mp3_url = input("Paste the url to the mp3 file you want to add or [q]uit: ")
#
#         if mp3_url == 'q':
#             break
#
#         # check content to ensure proper mp3 content type.
#         try:
#             with urlopen(mp3_url) as response:
#                 ct = response.info().get_content_type()
#                 if ct == "audio/mpeg":
#                     utils.print_styled(utils.ByteStyle.SUCCESS, "File looks good.")
#                     have_good_input = True
#                 else:
#                     utils.print_styled(utils.ByteStyle.FAIL,
#                                        "Something is funky about this file.  I expected type 'audio/mpeg' but got '{}'."
#                                        " Make sure it was properly exported to an mp3.".format(ct))
#
#         except ValueError as e:
#             utils.print_styled(utils.ByteStyle.FAIL, str(e))
#
#     if have_good_input:  # then get the file number
#
#         have_good_input = False
#         while not have_good_input:
#             filename = os.path.basename(urlparse(mp3_url).path)
#             name, ext = os.path.splitext(filename)
#
#             # check if the filename is already a number, and offer to use it
#             try:
#                 name = int(name)
#                 good_name_already = True
#             except ValueError:
#                 good_name_already = False
#
#             prompt = "What number (integers only) do you want to give it? " + ("[Enter] = {}".format(name) if good_name_already else "")
#             mp3_number = input(prompt)
#
#             try:
#                 if good_name_already and mp3_number:
#                     mp3_number = name
#                 else:
#                     mp3_number = int(mp3_number)
#                 have_good_input = True
#             except ValueError:
#                 utils.print_styled(utils.ByteStyle.FAIL, "Dude, that wasn't an integer! ")
#                 have_good_input = False
#
#         filename = "{}.mp3".format(mp3_number)
#
#         print("test: {}".format(filename))
#
#         # try:
#         #     asyncio.get_event_loop().run_until_complete(run_client())
#         # except (OSError, asyncssh.Error) as exc:
#         #     sys.exit('SSH connection failed: ' + str(exc))
#
#     else:
#         print("Quitting...")
#
