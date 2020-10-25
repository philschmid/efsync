import os
import shutil
# define the name of the directory to be created


def create_dir(path='.efsync'):
    try:
        os.mkdir(path)
    except OSError:
        # print("Creation of the directory %s failed" % path)
        return False
    else:
        # print("Successfully created the directory %s " % path)
        return True


def delete_dir(path='.efsync'):
    try:
        shutil.rmtree(path)
    except OSError:
        # print("Deletion of the directory %s failed" % path)
        return False
    else:
        # print("Successfully deleted the directory %s" % path)
        return True
