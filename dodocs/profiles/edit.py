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

    dodocs_dir = utils.dodocs_directory()
    config_file = os.path.join(dodocs_dir, args.name, dconf.CONF_FILE)

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
