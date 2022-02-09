import argparse


def parse_commandline():
    """Parse the command line."""

    parser = argparse.ArgumentParser(description="""This script
randomly picks a chosen numer of files from a set of folders and
copies those files to a single destination folder. The files to be
considered can be filtered by suffix.""")

    parser.add_argument(
        "DIR",
        help="The directory to consider (scanned recursively)",
        nargs="+")

    parser.add_argument(
        "-N",
        help="Choose N files randomly",
        type=int,
        default=10)

    parser.add_argument(
        "--destination",
        metavar="DIR",
        help="Copy files to DIR")

    parser.add_argument(
        "--delete-existing",
        help="""Delete existing files in the destionation folder
instead of moving those files to a new location.""",
        action="store_true",
        default=False)

    parser.add_argument(
        "--suffix",
        help="""Only consider files with this SUFFIX. For instance, to
only load jpeg files you would specify either 'jpg' or '.jpg'. By
default, all files are be considered. The suffix is case
insensitive.""",
        action="append",
        nargs="+")

    parser.add_argument(
        "--verbose",
        help="Print a lot of stuff",
        action="store_true",
        default=False)

    return parser.parse_args()
