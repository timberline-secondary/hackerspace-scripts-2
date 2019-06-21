import paramiko
import os
import sys
from time import time
from getpass import getpass


def read_data(channel, response_expected, response_contains=None, timeout=5.0):
    """Read channel output until expected_reponse is found, or timeout, whichever comes first. 
    
    Keyword Arguments:
        expected_response {str} -- a string to look for at the END of the output data (default: {None})
        response_contains {str} -- a string to look for WITHIN the output data (default: {None})
        timeout {float} -- in seconds (default: {5.0})

    Returns:
        str -- the output data, None if timeout occurs
    """

    channel_data = ""
    start_time = time()
    response_found = False
    while True:
        elapsed_time = time() - start_time
        if channel.recv_ready():  # if there is data ready to receive
            # Get the data
            channel_data += str(channel.recv(9999), 'utf8') # receive max # of bytes

            # New data received, check if we got the expected output yet:
            if response_expected and channel_data.endswith(response_expected):
                # if we also need to look for content within the output, cehck that too
                if response_contains is not None:
                    if response_contains in channel_data:
                        response_found = True
                else:
                    response_found = True

            if response_found:
                return channel_data
                
        elif timeout < elapsed_time:
            print("Command timed out or unexpected response.")
            print("Got response: ")
            print(channel_data)
            print("Expecetd response: ")
            print(response_expected)
            print("ABORTING...\n")
            return None 


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
username = "hackerspace_admin"
hostname = "tbl-hackerspace-13-s"
password = getpass("password for hackerspace_admin: ")
ssh.connect(hostname, username="hackerspace_admin", password=password)

cmd_list = [
                ("sudo passwd teststu", "[sudo] password for {}: ".format(username), None),
                (password, "New password: ", None),
                ("wolf", "Re-enter new password: ", None),
                ("wolf", "hackerspace_admin@tbl-hackerspace-13-s:~$ ", "password updated successfully"),
            ]

# e.g. "hackerspace_admin@tbl-hackerspace-13-s:~$ " <-- trailing space!
prompt_string = "{}@{}:~$ ".format(username, hostname)

channel = ssh.invoke_shell()

channel.send(prompt_string + '\n')
# wait for the prompt
output = read_data(channel, prompt_string)
print(prompt_string)

if output is not None:

    # send commands/input
    for cmd, response, contains in cmd_list:
        # print("Sending command: ########  {} ##############".format(cmd))
        channel.send(cmd + '\n')
        output = read_data(channel, response, contains)
        
        if output is None:
            # print('Output expected: "{}"'.format(response) )
            # print('Got: {}'.format(output) )
            break
        else:
            print(output)

# while True:

    
#     if channel.recv_ready():  # if there is data ready to receive
#         channel_data += str(channel.recv(9999), 'utf8') # receive max # of bytes
#     else:
#         continue


#     if channel_data.endswith(prompt_string):
#         print(channel_data)
#         channel.send(cmd)
#         channel.send('\n')
#         channel_data = ""
#     elif channel_data.endswith("[sudo] password for hackerspace_admin: "):
#         print(channel_data)
#         channel.send(password + '\n')
#         channel_data = ""
#     elif channel_data.endswith("New password: "):
#         print(channel_data)
#         channel.send("wolf\n")
#         channel_data = ""
#     elif channel_data.endswith("Re-enter new password: "):
#         print(channel_data)
#         channel.send("wolf\n")
#         channel_data = ""
#     elif "passwd: password updated successfully" in channel_data:
#         print(channel_data)
#         break
    



        

