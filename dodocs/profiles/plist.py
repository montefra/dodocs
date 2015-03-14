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
    dodocs_dir = utils.dodocs_directory()
    dirpath, dirnames = next(os.walk(dodocs_dir))[:2]
    if dirnames:
        print(colorama.Fore.GREEN + "Available profiles:")
        for d in dirnames:
            profile_dir = os.path.join(dodocs_dir, d)
            msg = "  * {}".format(d)
            if os.path.islink(profile_dir):
                msg += " (-> {})".format(os.path.realpath(profile_dir))
            print(msg)
    else:
        print(colorama.Fore.RED + "No profile found")
