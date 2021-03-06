"""Configuration file manager

Tasks:
* creates the example configuration file when creating the virtual environment;
* reads and parse the configuration file otherwise

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import configparser as confp
from pathlib import Path

import dodocs.logger as dlog
import dodocs.utils as du

CONF_FILE = "dodocs_setup.cfg"
"name of the configuration file"

EXPECTED_SECTIONS = ['general']
"""Name of the sections that must be always present in the configuration file
and that are ignored when searching for projects"""

# private dictionary storing configurations
_config_dic = {}


class DodocConfigError(confp.Error):
    """Error with the configuration"""
    pass


def get_sample_cfg_file():
    """Get the name of the sample configuration file.

    Returns
    -------
    cfg_file: string
        absolute path of the sample configuration file
    """
    this_file_path = Path(__file__).parent
    cfg_file = this_file_path / "dodocs_data" / CONF_FILE
    return cfg_file


def defaults():
    """Default settings for the projects

    Returns
    -------
    dictionary
    """
    default_dict = {"vcs": "git",
                    "language": "python3",
                    "py-install": "no",
                    }
    return default_dict


@du.format_docstring(CONF_FILE)
def get_config(profile, check_config=True):
    """Returns the configuration for the given profile. If it doesn't exists,
    first create it.

    It is assumed the existence of the file {} under the ``profile`` directory.

    Parameters
    ----------
    profile : string
        name of the profile
    check_config : bool, optional
        if ``False``, do no check if the configuration file is correct

    Returns
    -------
    conf : :class:`confp.ConfigParser` instance

   Raises
    ------
    DodocConfigError
        if the configuration file does not exist
    """
    try:
        return _config_dic[profile]
    except KeyError:
        dlog.set_profile(profile)
        conf = confp.ConfigParser(defaults=defaults())
        fname = du.profile_dir(profile) / CONF_FILE
        if not fname.exists():
            raise DodocConfigError("The configuration file for profile {} does"
                                   " not exist".format(profile))
        conf.read(str(fname))
        dlog.set_profile(profile)
        dlog.getLogger().debug("Configuration file loaded")

        if check_config:
            check_edited(conf, profile)
            check_version(conf, profile)

        _config_dic[profile] = conf
        return conf


def check_version(conf, profile):
    """Check that the version in the configuration files corresponds with the
    one of ``dodocs``

    Parameters
    ----------
    conf : :class:`confp.ConfigParser` instance
        configuration object
    profile : string
        name of the profile

    Raises
    ------
    DodocConfigError
        if the configuration file doesn't have the version option
    """
    dlog.set_profile(profile)
    log = dlog.getLogger()
    try:
        conf_version = conf.get("general", "version")
        current_version = du.get_version()
        if conf_version != current_version:
            msg = ("The current `dodocs` version %s is different from"
                   " the one in the configuration file %s. Something bad might"
                   " happen")
            log.warn(msg, current_version, conf_version)
    except confp.NoOptionError:
        msg = ("[{p}] The configuration file doesn't have a `version` option."
               " Are you sure that it is a `dodocs` configuration"
               )
        raise DodocConfigError(msg.format(p=profile))


def check_edited(conf, profile):
    """Check if the configuration file has been edited.

    Parameters
    ----------
    conf : :class:`confp.ConfigParser` instance
        configuration object
    profile : string
        name of the profile

    Raises
    ------
    DodocConfigError
        if the configuration file has never been edited
    """
    try:
        if conf.getboolean('general', 'is_edited'):
            msg = ("[{p}] The configuration file has not been edited."
                   " Aborting")
            raise DodocConfigError(msg.format(p=profile))
    except confp.NoOptionError:
        pass


def check_sections(conf, profile):
    """Check that the expected sections are present in the configuration file

    Parameters
    ----------
    conf : :class:`confp.ConfigParser` instance
        configuration object
    profile : string
        name of the profile

    Raises
    ------
    DodocConfigError
        if the configuration file does not contain the required sections
    """
    for es in EXPECTED_SECTIONS:
        if es not in conf.sections:
            msg = "[{p}] Mandatory section '{s}' is missing"
            raise DodocConfigError(msg.format(p=profile, s=es))


def get_projects(profile, check_config=True):
    """Get the list of projects for the given profile

    Parameters
    ----------
    profile : string
        name of the profile
    check_config : bool, optional
        if ``False``, do no check if the configuration file is correct

    Returns
    -------
    projects : list of strings
        name of the projects
    """
    conf = get_config(profile, check_config=check_config)
    projects = conf.sections()
    # remove the expected sections
    for es in EXPECTED_SECTIONS:
        projects.remove(es)

    return projects
