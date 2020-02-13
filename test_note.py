import unittest
from note import Note
import platform
import os


Noter = Note()


class TestNoter(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNoter, self).__init__(*args, **kwargs)
        self.change_default_editor()
        self.clear_test_files()

    @staticmethod
    def clear_test_files():
        test_file = f'{Noter.DEFAULT_NOTE_FOLDER}/test.test'
        if os.path.exists(test_file):
            os.remove(test_file)

    @staticmethod
    def change_default_editor():
        if platform.system() == "Windows":
            Noter.DEFAULT_EDITOR = "copy NUL"
        elif platform.system() == "Linux":
            Noter.DEFAULT_EDITOR = "touch"

    def test_create(self):
        Noter.DEFAULT_EDITOR = "copy NUL"
        self.assertEqual(Noter.create(['test.test']), 'ok')

    def test_aliases(self):
        self.assertEqual(Noter.handle_aliases('c'), 'create')


if __name__ == "__main__":
    unittest.main()
