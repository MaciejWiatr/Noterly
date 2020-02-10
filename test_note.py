import unittest
from note import Note

Noter = Note()


class TestNoter(unittest.TestCase):

    def test_create(self):
        Noter.DEFAULT_EDITOR = "copy NUL"
        self.assertEqual(Noter.create(['test.test']), 'created')


if __name__ == "__main__":
    unittest.main()
