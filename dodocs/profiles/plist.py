"""List the profiles

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os

import dodocs.config as dconf
from dodocs import utils
import dodocs.logger as dlog


def plist(args):
    """List the profiles

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dlog.set_profile("")
    dlog.set_project("")
    log = dlog.getLogger()

    log.debug("Listing profiles")
    dodocs_dir = utils.dodocs_directory()

    if not dodocs_dir.exists():
        log.critical("No dodocs directory found. Create it first with the"
                     " command 'dodoc profile create [profilename]'")
        return

    dirpath, dirnames = next(os.walk(str(dodocs_dir)))[:2]
    if dirnames:
        log.info("Available profiles:")
        for d in dirnames:
            profile_dir = dodocs_dir / d
            msg = "  * {}".format(d)
            if profile_dir.is_symlink():
                msg += " (-> {})".format(profile_dir.resolve())
            log.info(msg)
            for project in dconf.get_projects(d, check_config=False):
                dlog.set_profile("")
                log.info("    + %s", project)

    else:
        log.warning("No profile found")
