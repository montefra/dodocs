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

# name of the configuration file
CONF_FILE = "dodocs_setup.cfg"

# private dictionary storing configurations
_config_dic = {}


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

        check_version(conf)

        _config_dic[profile] = conf
        return conf


def check_version(conf):
    """Check that the version in the configuration files corresponds with the
    one of ``dodocs``

    Parameters
    ----------
    conf : :class:`confp.ConfigParser` instance
        configuration object
    """
    try:
        conf_version = conf.get("general", "version")
        current_version = du.get_version()
        if conf_version != current_version:
            msg = ("The current `dodocs` version {dv} is different from the"
                   " one in the configuration file {dc}. Beware that the built"
                   " might fail."
                   )
            print(colorama.Fore.YELLOW + msg.format(dv=current_version,
                                                    dc=conf_version))
    except confp.NoOptionError:
        msg = ("The configuration file doesn't have a `version` entry. Are you"
               " sure that it is a `dodocs` configuration"
               )
        print(colorama.Fore.RED + msg)
        raise
