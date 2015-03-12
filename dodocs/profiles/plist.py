"""List the profiles

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os

from dodocs import utils


def plist(args):
    """List the profiles

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dirnames = next(os.walk(utils.dodocs_directory()))[1]
    if dirnames:
        print("Available profiles:")
        for d in dirnames:
            print("  * {}".format(d))
    else:
        print("No profile found")
