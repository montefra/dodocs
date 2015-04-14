"""List the profiles

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os

import colorama

import dodocs.config as dconf
from dodocs import utils
from dodocs.logger import getLogger


def plist(args):
    """List the profiles

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = getLogger()

    log.debug("Listing profiles")
    dodocs_dir = utils.dodocs_directory()
    dirpath, dirnames = next(os.walk(dodocs_dir))[:2]
    if dirnames:
        msg = colorama.Fore.GREEN + "Available profiles:" + colorama.Fore.RESET
        for d in dirnames:
            profile_dir = os.path.join(dodocs_dir, d)
            msg += "\n  * {}".format(d)
            if os.path.islink(profile_dir):
                msg += " (-> {})".format(os.path.realpath(profile_dir))
            try:
                for project in dconf.get_projects(d):
                    msg += "\n    + {}".format(project)
            except dconf.DodocConfigError as e:
                msg += ("\n    + " + colorama.Fore.RED + "there is a problem"
                        " with the configuration file" + colorama.Fore.RESET)
                log.error(e)

        print(msg)
    else:
        print(colorama.Fore.RED + "No profile found")
