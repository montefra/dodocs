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
import dodocs.utils as dutils


class ProfileWarning(UserWarning):
    """Warning raised when creating profiles"""
    pass


def create(args):
    """Create a new profile and copy the configuration file in it

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dodocs_dir = dutils.dodocs_directory()

    for name in args.name:
        profile_dir = os.path.join(dodocs_dir, name)

        # deal with existing profile
        if os.path.exists(profile_dir):
            if args.force and (os.path.isdir(profile_dir) or
                               os.path.isfile(profile_dir)):
                print(colorama.Fore.YELLOW + "Removing '{}'".format(name))
                shutil.rmtree(profile_dir)
            elif args.force and os.path.islink(profile_dir):
                print(colorama.Fore.YELLOW +
                      "Unlinking and Removing '{}'".format(name))
                realpath = os.path.realpath(profile_dir)
                os.remove(profile_dir)
                shutil.rmtree(realpath)
            else:
                msg = colorama.Fore.RED + "'{pd}' already exists. Aborting."
                warnings.warn(msg.format(pd=name), ProfileWarning)
                continue

        # create new profiles
        if args.link:
            profile_dir = os.path.join(args.link, name)
            link_dir = os.path.join(dodocs_dir, name)
        try:
            os.mkdir(profile_dir)
        except FileExistsError:
            msg = colorama.Fore.RED + "'{pd}' already exists. Aborting."
            warnings.warn(msg.format(pd=profile_dir), ProfileWarning)
            continue

        copy_config(profile_dir)
        if args.link:
            os.symlink(profile_dir, link_dir)
        print(colorama.Fore.GREEN + "profile '{}' created".format(name))


def copy_config(profile_dir):
    """Copy the configuration file into ``profile_dir``.

    Substitute the version into the file.

    Parameters
    ----------
    profile_dir : string
        name of the profile directory
    """
    cfg_file = dconf.get_sample_cfg_file()
    with open(cfg_file, 'r') as inf,\
                open(os.path.join(profile_dir, dconf.CONF_FILE), 'w') as outf:
        conf = string.Template(inf.read())
        conf = conf.safe_substitute(version=dutils.get_version())
        outf.write(conf)
