from scripts._utils import utils
from scripts._utils.ssh import SSH

mime_types = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg":"image/jpeg", 
    ".avi": "video/x-msvideo",
    ".mpeg":"video/mpeg",
    ".mp4": "video/mp4",
    ".ogv": "video/ogg",
    ".webm":"video/webm",
    ".mkv": "video/x-matroska",
    ".svg": "image/svg+xml",
}

TV_FILE_SERVER = "hightower"
TV_FILE_SERVER_USER = "pi-slideshow"
TV_FILE_SERVER_PW = "hackerberry" # not secure, obvs.

TV_ROOT = "/home/{}".format(TV_FILE_SERVER_USER)  

def get_tv_containing_student(student_number):
    """ Search all pi-slideshow TV directories until directory with same number is found, return the TV # """
    ssh_connection = SSH(TV_FILE_SERVER, TV_FILE_SERVER_USER, TV_FILE_SERVER_PW)

    for tv in range(1,5):
            filepath = "{}/tv{}/".format(TV_ROOT, tv)
            command = 'ls {}'.format(filepath)
            dir_contents = ssh_connection.send_cmd(command, print_stdout=False).split()
            if student_number in dir_contents:
                utils.print_success("Found art for {} on TV# {}".format(student_number, tv))
                ssh_connection.close()
                return tv
    
    
    ssh_connection.close()
    return None

