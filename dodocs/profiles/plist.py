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
    dirpath, dirnames = next(os.walk(str(dodocs_dir)))[:2]
    if dirnames:
        msg = colorama.Fore.GREEN + "Available profiles:" + colorama.Fore.RESET
        for d in dirnames:
            profile_dir = dodocs_dir / d
            msg += "\n  * {}".format(d)
            if profile_dir.is_symlink():
                msg += " (-> {})".format(profile_dir.resolve())
            try:
                for project in dconf.get_projects(d):
                    msg += "\n    + {}".format(project)
            except dconf.DodocConfigError as e:
                msg += ("\n    + " + colorama.Fore.RED + "there is a problem"
                        " with the configuration file. See the above error"
                        " log." + colorama.Fore.RESET)
                log.error(e)

        print(msg)
    else:
        print(colorama.Fore.RED + "No profile found")
