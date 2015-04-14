"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import shutil

import colorama

import dodocs.logger as dlog
import dodocs.utils as dutils


def remove(args):
    """Remove profile(s)

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = dlog.getLogger()

    for name in args.name:
        log.debug("Removing profile {}".format(name))
        profile_dir = dutils.profile_dir(name)

        if not os.path.exists(profile_dir):
            log.warn("Profile {} does not exist".format(name))
            continue

        try:
            if os.path.islink(profile_dir):
                realpath = os.path.realpath(profile_dir)
                os.remove(profile_dir)
                shutil.rmtree(realpath)
            else:
                shutil.rmtree(profile_dir)
        except FileNotFoundError:
            msg = "The removal of profile {} failed".format(name)
            log.error(msg, exc_info=True)

        log.info(colorama.Fore.GREEN + "profile '{}' removed".format(name))
