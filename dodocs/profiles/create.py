"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import shutil
import string
import warnings

import colorama

import dodocs.config as dconf
import dodocs.logger as dlog
import dodocs.utils as dutils


def create(args):
    """Create a new profile and copy the configuration file in it

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dodocs_dir = dutils.dodocs_directory()
    log = dlog.getLogger()

    for name in args.name:
        log.info("Creating profile {}".format(name))
        profile_dir = os.path.join(dodocs_dir, name)
        log.debug("Profile directory: {}".format(profile_dir))

        # deal with existing profile
        if os.path.exists(profile_dir):
            if args.force and (os.path.isdir(profile_dir) or
                               os.path.isfile(profile_dir)):
                log.warning(colorama.Fore.YELLOW +
                            "Removing '{}'".format(name))
                shutil.rmtree(profile_dir)
            elif args.force and os.path.islink(profile_dir):
                log.warning(colorama.Fore.YELLOW +
                            "Unlinking and Removing '{}'".format(name))
                realpath = os.path.realpath(profile_dir)
                os.remove(profile_dir)
                shutil.rmtree(realpath)
            else:
                msg = colorama.Fore.RED + "Profile '{pd}' already exists. Aborting."
                log.error(msg.format(pd=name))
                continue

        # create new profiles
        if args.link:
            link_dir = profile_dir
            profile_dir = os.path.join(args.link, name)
            log.debug("Profile linked to {}".format(profile_dir))
        try:
            os.mkdir(profile_dir)
        except FileExistsError:
            log.error(colorama.Fore.RED +
                      "'{pd}' already exists. Aborting.")
            continue

        copy_config(profile_dir)
        if args.link:
            os.symlink(profile_dir, link_dir)
        log.info(colorama.Fore.GREEN + "profile '{}' created".format(name))


def copy_config(profile_dir):
    """Copy the configuration file into ``profile_dir``.

    Substitute the version into the file.

    Parameters
    ----------
    profile_dir : string
        name of the profile directory
    """
    log = dlog.getLogger()
    cfg_file = dconf.get_sample_cfg_file()
    log.debug("Copy file '{}' into directory '{}'".format(cfg_file,
                                                          profile_dir))
    with open(cfg_file, 'r') as inf,\
                open(os.path.join(profile_dir, dconf.CONF_FILE), 'w') as outf:
        conf = string.Template(inf.read())
        conf = conf.safe_substitute(version=dutils.get_version())
        outf.write(conf)
