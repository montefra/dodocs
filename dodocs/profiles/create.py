"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import shutil

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
            print("Removing and recreating '{}'".format(profile_dir))
            os.rmdir(profile_dir)
            os.mkdir(profile_dir)
        else:
            msg = "'{pd}' already exists. Aborting."
            raise ValueError(msg.format(pd=profile_dir))
    else:
        msg = "'{pd}' exists and is a file. I don't know what to do."
        raise ValueError(msg.format(pd=profile_dir))

    cfg_file = dconf.get_sample_cfg_file()
    shutil.copy(cfg_file, profile_dir)
    print("profile {} created".format(args.name))
