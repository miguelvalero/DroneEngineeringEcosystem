import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import sys

from filechooser import parse_commandline


class TestParseCommandline(unittest.TestCase):

    def test_empty_dirs(self):
        with mock.patch.object(sys, "argv", ["/script"]):
            with self.assertRaises(SystemExit):
                parse_commandline.parse_commandline()

    def test_dirs(self):
        testdirs = ["/images-1", "/images-2"]
        with mock.patch.object(sys, "argv", ["/scriptpath"] + testdirs):
            options = parse_commandline.parse_commandline()
        self.assertTrue(isinstance(options.DIR, list))
        self.assertTrue(len(options.DIR) == 2)
        self.assertEqual(options.DIR, testdirs)

    def test_N(self):
        with mock.patch.object(sys, "argv",
                               ["/scriptpath", "-N", "10", "/images"]):
            options = parse_commandline.parse_commandline()
        self.assertEqual(options.N, 10)

    def test_illegal_N(self):
        with mock.patch.object(sys, "argv",
                               ["/scriptpath", "-N", "a", "/images"]):
            with self.assertRaises(SystemExit):
                parse_commandline.parse_commandline()

    def test_negative_N(self):
        with mock.patch.object(sys, "argv",
                               ["/scriptpath", "-N", "-10", "/images"]):
            with self.assertRaisesRegexp(Exception, "can not be less than"):
                parse_commandline.parse_commandline()
