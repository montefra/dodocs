"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import shutil

import colorama

import dodocs.utils as dutils


def remove(args):
    """Remove profile(s)

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dodocs_dir = dutils.dodocs_directory()

    for name in args.name:
        profile_dir = os.path.join(dodocs_dir, name)

        if os.path.islink(profile_dir):
            realpath = os.path.realpath(profile_dir)
            os.remove(profile_dir)
            shutil.rmtree(realpath)
        else:
            shutil.rmtree(profile_dir)
        print(colorama.Fore.GREEN + "profile '{}' removed".format(name))
