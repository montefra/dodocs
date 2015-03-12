"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import shutil
import sys

import colorama

import dodocs.config as dconf
import dodocs.utils as dutils


def create(args):
    """Create a new profile and copy the configuration file in it

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dodocs_dir = dutils.dodocs_directory()
    profile_dir = os.path.join(dodocs_dir, args.name)

    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)
    elif os.path.isdir(profile_dir):
        if args.force:
            print(colorama.Fore.YELLOW +
                  "Removing and recreating '{}'".format(profile_dir))
            shutil.rmtree(profile_dir)
            os.mkdir(profile_dir)
        else:
            msg = colorama.Fore.RED + "'{pd}' already exists. Aborting."
            sys.exit(msg.format(pd=profile_dir))
    else:
        msg = colorama.Fore.RED + "'{pd}' exists and is a file. I don't know what to do."
        sys.exit(msg.format(pd=profile_dir))

    cfg_file = dconf.get_sample_cfg_file()
    shutil.copy(cfg_file, profile_dir)
    print(colorama.Fore.GREEN + "profile '{}' created".format(args.name))
