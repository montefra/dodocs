"""List the profiles

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os

import colorama

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
        print(colorama.Fore.GREEN + "Available profiles:")
        for d in dirnames:
            print("  * {}".format(d))
    else:
        print(colorama.Fore.RED + "No profile found")
