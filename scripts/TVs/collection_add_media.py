import inquirer

from scripts.TVs.add_new_media import add_new_media
from scripts._utils.ssh import SSH
from scripts.TVs._utils import TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW


def collection_add_media():
    # connect to hightower
    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)
    # get all collections in tv3
    collections = ssh_connection.send_cmd("find tv3 -type d", print_stdout=False)
    # format the collection names from /tv3/<collection_name>/r/n -> <collection_name>
    collection_list = [c[4:-1] for c in collections.split('\n')[1:-1]]

    questions = [
        inquirer.List('dir',
                      message="What collection would you like to add to?",
                      choices=[*collection_list, "[Quit]"],
                      ),
    ]

    collection = inquirer.prompt(questions)["dir"]
    ssh_connection.close()

    if collection == "[Quit]":
        return False

    add_new_media(collection, '3')


