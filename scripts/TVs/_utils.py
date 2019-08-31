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



