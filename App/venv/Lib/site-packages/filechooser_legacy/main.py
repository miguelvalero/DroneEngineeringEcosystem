import math
import os
import os.path
import random
import shutil
import stat
import sys
import tempfile
import filechooser.parse_commandline as parse_commandline


def main():
    """The main function."""

    options = parse_commandline.parse_commandline()

    if options.suffix is not None:
        temp = []
        for i in options.suffix:
            temp.extend(i)
        options.suffix = temp

        for i in range(len(options.suffix)):
            options.suffix[i] = options.suffix[i].lower()

    photos = []
    for path in options.DIR:
        for root, dirs, files in os.walk(path):
            for i in files:
                if options.suffix is not None:
                    (basename, extension) = os.path.splitext(i)
                    if not extension.lower() in options.suffix:
                        continue
                photos.append(os.path.join(root, i))

    if len(photos) == 0:
        print("could not find any files to select from")
        sys.exit(0)

    selectedPhotos = []
    if len(photos) >= options.N:
        N = options.N
    else:
        N = len(photos)

    for i in range(N):
        selectedPhotos.append(photos.pop(int(math.floor(random.random() *
                                                        len(photos)))))

    if options.destination is not None:
        try:
            os.mkdir(options.destination)
        except OSError as e:
            print("destination path already exists: %s" % (e))

            if options.delete_existing:
                print("deleting existing files")
                for root, dirs, files in os.walk(options.destination):
                    for i in files:
                        os.remove(os.path.join(root, i))
            else:
                backupfolder = tempfile.mkdtemp()
                print("moving old files to %s" % (backupfolder))
                for root, dirs, files in os.walk(options.destination):
                    for i in files:
                        shutil.move(os.path.join(root, i), backupfolder)

        # Set very permissible permissions on destination directory.
        os.chmod(options.destination,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                 stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
                 stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)

    for i in selectedPhotos:
        if options.destination is not None:
            if options.verbose:
                print("copying %s" % (i))
            shutil.copy(i, options.destination)
        else:
            print("skipping %s, no destination given" % (i))

    return 0
