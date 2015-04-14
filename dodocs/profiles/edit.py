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
    """Create a new profile and copy the configuration file in it

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = getLogger()

    log.debug("opening configuration file for profile {} for"
              " editing".format(args.name))

    profile_dir = utils.profile_dir(args.name)

    if not os.path.exists(profile_dir):
        log.warn("Profile {} does not exist. Bye".format(args.name))
        return

    config_file = os.path.join(profile_dir, dconf.CONF_FILE)

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
