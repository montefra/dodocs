"""Edit the given profile

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import subprocess as sp
import sys

import dodocs.config as dconf
import dodocs.logger as dlog
from dodocs import utils


def edit(args):
    """Edit the configuration file(s)

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = dlog.getLogger()
    if not utils.dodocs_directory().exists():
        log.critical("No dodocs directory found. Create it first with the"
                     " command 'dodoc profile create [profilename]'")
        return

    for profile in args.name:
        dlog.set_profile(profile)

        log.debug("opening configuration file for profile {} for"
                  " editing".format(args.name))

        profile_dir = utils.profile_dir(profile)

        if not profile_dir.exists():
            log.warn("Profile does not exist. Bye")
            return

        config_file = str(profile_dir / dconf.CONF_FILE)

        # this part is taken without shame from the web
        if os.name == 'posix':
            if "EDITOR" in os.environ:
                sp.call([os.environ["EDITOR"], config_file])
            else:
                sp.call(["xdg-open", config_file])
        elif sys.platform.startswith('darwin'):
            sp.call(["open", config_file])
        elif os.name == 'nt':
            os.startfile(config_file)
