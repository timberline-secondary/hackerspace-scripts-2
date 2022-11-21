from scripts.TVs.add_new_media import add_new_media
from scripts._utils.ssh import SSH
from scripts._utils import utils
from scripts.TVs._utils import TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW


def collection_create_new():
    collection_name = utils.input_styled("Name of new collection: \n")

    server_filepath = "tv3/{}/".format(collection_name)

    # connect to hightower
    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    if not ssh_connection.dir_exists(server_filepath):
        ssh_connection.send_cmd('mkdir {}'.format(server_filepath))
        utils.print_success(f"New collection \"{collection_name}\" was created successfully!")
    else:
        utils.print_error("Collection already exists")

    ssh_connection.close()
    add_to_collection = utils.confirm("Would you like to add to this collection?", yes_is_default=True)
    if add_to_collection:
        add_new_media(collection_name, '3')



