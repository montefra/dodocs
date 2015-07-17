"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import shutil

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
        dlog.set_profile(name)
        log.debug("Removing profile")
        profile_dir = dutils.profile_dir(name)

        if not profile_dir.exists():
            log.warn("Profile does not exist")
            continue

        try:
            if profile_dir.is_symlink():
                realpath = profile_dir.resolve()
                profile_dir.unlink()
                shutil.rmtree(str(realpath))
            else:
                shutil.rmtree(str(profile_dir))
        except FileNotFoundError:
            log.error("The removal of profile failed", exc_info=True)

        log.info("profile removed")
