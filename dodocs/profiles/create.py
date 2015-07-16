"""Create the profile.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

from pathlib import Path
import shutil
import string

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
    log = dlog.getLogger()

    if not args.name:
        if not dutils.dodocs_directory().exists():
            dutils.dodocs_directory().mkdir(parents=True)
            log.info("Home directory created")
        else:
            log.info("Home directory already exists")

    for name in args.name:
        dlog.set_profile(name)
        log.info("Creating profile")
        profile_dir = dutils.profile_dir(name)
        log.debug("Profile directory: %s", profile_dir)

        # deal with existing profile
        if profile_dir.exists():
            if args.force and profile_dir.is_symlink():
                log.warning("Unlinking and removing existing profile")
                realpath = profile_dir.resolve()
                profile_dir.unlink()
                shutil.rmtree(str(realpath))
            elif args.force and (profile_dir.is_dir() or
                                 profile_dir.is_file()):
                log.warning("Removing existing profile".format(name))
                shutil.rmtree(str(profile_dir))
            else:
                log.error("Profile already exists. Aborting.")
                continue

        # create new profiles
        if args.link:
            link_dir = profile_dir
            profile_dir = Path(args.link).resolve() / name
            log.debug("Profile linked to {}".format(profile_dir))
        try:
            profile_dir.mkdir(parents=True)
        except FileExistsError:
            log.error("Profile already exists. Aborting.")
            continue

        copy_config(profile_dir)
        if args.link:
            link_dir.symlink_to(profile_dir, target_is_directory=True)
        log.info("profile created")


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
    with cfg_file.open('r') as inf, \
            (profile_dir / dconf.CONF_FILE).open('w') as outf:
        conf = string.Template(inf.read())
        conf = conf.safe_substitute(version=dutils.get_version())
        outf.write(conf)
