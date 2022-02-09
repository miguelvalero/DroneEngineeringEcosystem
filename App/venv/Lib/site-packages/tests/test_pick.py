import os
import shutil
import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from filechooser import pick_file
import filechooser.db as db

images = [
    "collection_a/a/a_1.jpg",
    "collection_a/a/a_2.gif",
    "collection_a/b/b_1.jpg",
    "collection_a/b/b_2.txt",
    "collection_b/c/c_1.jpg",
]


class TestPick(unittest.TestCase):

    def setUp(self):
        # Create a filesystem structure in a temporary location. This
        # should eventually be replaced with something in memory, i.e.
        # using `pyfakefs`.
        self.fs_base = tempfile.mkdtemp()
        for image in images:
            path = os.path.dirname(image)
            try:
                os.makedirs(os.path.join(self.fs_base, path))
            except OSError as e:
                pass
            with open(os.path.join(self.fs_base, image), "w"):
                pass

        self.db = tempfile.NamedTemporaryFile(delete=False)
        self.db.close()
        db.database = self.db.name
        db.initialize_db()

    def tearDown(self):
        shutil.rmtree(self.fs_base)
        os.remove(self.db.name)

    def test_get_image_files(self):
        # Sort the lists so we can compare them directly.
        image_files = sorted(pick_file.get_image_files(
            [os.path.join(self.fs_base, "collection_a"),
             os.path.join(self.fs_base, "collection_b")]))
        reference_image_files = sorted(
            [os.path.join(self.fs_base, p) for p in images
             if p.split(".")[-1] != "txt"])
        self.assertEqual(image_files, reference_image_files)

    def test_get_image_files_not_exist(self):
        with self.assertRaisesRegexp(Exception, "does not exist"):
            pick_file.get_image_files(["does_not_exist"])

    def test_set_image_timestamp(self):
        with mock.patch("filechooser.db.time", return_value=1.0):
            pick_file.set_image_timestamp(
                os.path.join(self.fs_base, images[0]))
        result = db.get_timestamp(os.path.join(self.fs_base, images[0]))
        self.assertEqual(result[0]["timestamp"], 1.0)

    def test_get_image_timestamp(self):
        with mock.patch("filechooser.db.time", return_value=1.0):
            pick_file.set_image_timestamp(
                os.path.join(self.fs_base, images[0]))
        result = pick_file.get_image_timestamp(
            os.path.join(self.fs_base, images[0]))
        self.assertEqual(result, 1.0)
