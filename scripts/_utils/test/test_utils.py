import unittest
from unittest.mock import patch

from scripts._utils.utils import *

TEST_IMAGES = [
    # transparent png
    {"url": "https://github.com/timberline-secondary/hackerspace-scripts-2/blob/master/test_media/cat-png-cat-png-hd-1500.png", "mime": "image/png", "local": False, "ext": ".png"},
    # non-transparent png
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/cat1-1661521877.png", "mime": "image/png", "local": False, "ext": ".png"},
    # non-transparent gif
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/canofasparaguspix_2GEezO4.gif", "mime": "image/gif", "local": False, "ext": ".gif"},
    # transparent gif
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/mavey_locket.gif", "mime": "image/gif", "local": False, "ext": ".gif"},
    # non-transparent svg
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/rat.svg", "mime": "image/svg+xml", "local": False, "ext": ".svg"},
    # transparent svg
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/icon.svg", "mime": "image/svg+xml", "local": False, "ext": ".svg"},
    # jpeg
    {"url": "https://raw.githubusercontent.com/timberline-secondary/hackerspace-scripts-2/master/test_media/happy_dog.jpg", "mime": "image/jpeg", "local": False, "ext": ".jpg"}
]


class TestUtils(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_styled_print(self, mock_stdout):
        print_styled("success", ByteStyle.SUCCESS)

        assert mock_stdout.getvalue() == ByteStyle.SUCCESS + "success" + ByteStyle.ENDC + "\n"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_header(self, mock_stdout):
        print_heading("UNIT test")

        assert mock_stdout.getvalue() == ByteStyle.HEADER + "#" * 60 + ByteStyle.ENDC + "\n" + ByteStyle.HEADER + "#" + "UNIT TEST".center(60 - 2, " ") + "#" + ByteStyle.ENDC + "\n" + ByteStyle.HEADER + "#" * 60 + ByteStyle.ENDC + "\n\n"

    def test_get_computers_prompt(self):
        num_list, passw = get_computers_prompt("ALL", password="test123")

        # check num_list
        assert num_list == [f"{i}" for i in range(0, 32)]

        # check if password has changed (it shouldn't)
        assert passw == "test123"

        # NOTE: don't need to check password for this, if it has been changed it would fail on previous
        num_list_specified, _ = get_computers_prompt("test 2 15 30 5", password="test123")

        # check specified num_list
        assert num_list_specified == "test 2 15 30 5".split()

        # Check quitting
        num_list_none, password_none = get_computers_prompt("q", "test123")

        assert num_list_none is None

        assert password_none is None

    def test_verify_mimetype(self):
        failure = False

        for image in TEST_IMAGES:
            if not failure:
                success = verify_mimetype(image["url"], image["mime"], image["local"])
                if success is False:
                    failure = True
                    print(f"{image['url']} ❌")
                else:
                    print(f"{image['url']} 👍")

        assert failure is False

    def test_verify_image_integrity(self):
        failure = False

        for image in TEST_IMAGES:
            if not failure:
                success, url, local, ext = verify_image_integrity(image["url"], image["mime"], image["local"], image["ext"])
                if success is False:
                    failure = True
                    print(f"{image['url']} ❌")
                else:
                    print(f"{image['url']} 👍")

        assert failure is False

    def test_get_fqdn(self):
        hostname = get_fqdn("test")

        assert hostname == "test.hackerspace.tbl"

    @patch('builtins.input', side_effect=['Q'])
    def test_input_plus(self, _):
        output = input_plus("String or quit?")

        assert output == 'q'

    @patch('builtins.input', side_effect=['Y'])
    def test_confirm(self, _):
        confirmation = confirm("Yes or no?")

        assert confirmation


if __name__ == "__main__":
    unittest.main()
