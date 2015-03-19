"""Configuration file manager

Tasks:
* creates the example configuration file when creating the virtual environment;
* reads and parse the configuration file otherwise

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import configparser as confp
import os

import colorama

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
    path = os.path.split(os.path.abspath(__file__))[0]
    cfg_file = os.path.join(path, "dodocs_data", CONF_FILE)
    return cfg_file


@du.format_docstring(CONF_FILE)
def get_config(profile):
    """Returns the configuration for the given profile. If it doesn't exists,
    first create it.

    It is assumed the existence of the file {} under the ``profile`` directory.

    Parameters
    ----------
    profile : string
        name of the profile

    Returns
    -------
    conf : :class:`confp.ConfigParser` instance
    """
    try:
        return _config_dic[profile]
    except KeyError:
        conf = confp.ConfigParser()
        fname = os.path.join(du.dodocs_directory(), profile, CONF_FILE)
        conf.read(fname)

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
    """
    try:
        conf_version = conf.get("general", "version")
        current_version = du.get_version()
        if conf_version != current_version:
            msg = ("[{p}] The current `dodocs` version {dv} is different from"
                   " the one in the configuration file {dc}. Beware that the"
                   " built might fail."
                   )
            print(colorama.Fore.YELLOW + msg.format(dv=current_version,
                                                    dc=conf_version,
                                                    p=profile))
    except confp.NoOptionError:
        msg = ("[{p}] The configuration file doesn't have a `version` entry."
               " Are you sure that it is a `dodocs` configuration"
               )
        print(colorama.Fore.RED + msg.format(p=profile))
        raise


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
            msg = ("[{p}] The configuration file has likely not been edited."
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
