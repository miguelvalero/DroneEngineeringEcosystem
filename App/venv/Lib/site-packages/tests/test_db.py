import os
import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import filechooser.db as db
from filechooser.logger import logger


class TestDB(unittest.TestCase):

    def setUp(self):
        from logging import DEBUG
        logger.setLevel(DEBUG)
        self.db = tempfile.NamedTemporaryFile(delete=False)
        self.db.close()
        db.database = self.db.name
        db.initialize_db()

    def tearDown(self):
        os.remove(self.db.name)

    def test_set_timestamp(self):
        with mock.patch("filechooser.db.time", return_value=1.0):
            db.set_timestamp("a.gif")
        result = db.get_timestamp("a.gif")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['filename'], "a.gif")
        self.assertEqual(result[0]['timestamp'], 1.0)

    def test_update_timestamp(self):
        with mock.patch("filechooser.db.time", return_value=1.0):
            db.set_timestamp("b.gif")
        with mock.patch("filechooser.db.time", return_value=2.0):
            db.set_timestamp("b.gif")
        result = db.get_timestamp("b.gif")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['timestamp'], 2.0)
