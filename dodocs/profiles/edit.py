"""Edit the given profile

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import subprocess as sp
import sys

import dodocs.config as dconf
from dodocs.logger import getLogger
from dodocs import utils


def edit(args):
    """Edit the configuration file(s)

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = getLogger()

    log.debug("opening configuration file for profile {} for"
              " editing".format(args.name))

    for profile in args.name:
        profile_dir = utils.profile_dir(profile)

        if not profile_dir.exists():
            log.warn("Profile '{}' does not exist. Bye".format(profile))
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
