"""Configuration file manager

Tasks:
* creates the example configuration file when creating the virtual environment;
* reads and parse the configuration file otherwise

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import configparser as confp
import os


def get_sample_cfg_file():
    """Get the name of the sample configuration file

    Returns
    -------
    cfg_file: string
        absolute path of the sample configuration file
    """
    path = os.path.split(os.path.abspath(__file__))[0]
    cfg_file = os.path.join(path, "dodocs_data", "dodocs_setup.cfg")
    return cfg_file
