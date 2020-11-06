import unittest

from textgridtofolia.helpers import begin_end_time


class TestHelperMethods(unittest.TestCase):
    def test_begin_end_time(self):
        self.assertEqual(begin_end_time(1234.563451), (0, 20, 34, 563))
