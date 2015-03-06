"""Create the virtual environment

Copyright (c) 2015 Francesco Montesano
MIT Licence

The implementation of :func:`venv_cmd_arguments` is taken from :mod:`venv`
Original copyright (C) 2013 Vinay Sajip. New BSD License.
"""

import shutil
import os

import dodocs.config as dconf


def venv_cmd_arguments(parser):
    """Add to ``parser`` the command line arguments needed to create the
    virtual environment.

    Parameters
    ----------
    parser : instances of :class:`argparse.ArgumentParser`
        parser to which the arguments are added

    Returns
    -------
    parser
    """
    parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                        help='A directory to create the environment in.')
    parser.add_argument('--no-setuptools', default=False,
                        action='store_true', dest='nodist',
                        help="""Don't install setuptools or pip in the virtual
                        environment.""")
    parser.add_argument('--no-pip', default=False,
                        action='store_true', dest='nopip',
                        help="Don't install pip in the virtual environment.")
    parser.add_argument('--system-site-packages', default=False,
                        action='store_true', dest='system_site',
                        help='''Give the virtual environment access to the
                        system site-packages dir.''')
    if os.name == 'nt':
        use_symlinks = False
    else:
        use_symlinks = True
    parser.add_argument('--symlinks', default=use_symlinks,
                        action='store_true', dest='symlinks',
                        help='''Try to use symlinks rather than copies, when
                        symlinks are not the default for the platform.''')
    parser.add_argument('--clear', default=False, action='store_true',
                        dest='clear', help='''Delete the contents of the
                        environment directory if it already exists, before
                        environment creation.''')
    parser.add_argument('--upgrade', default=False, action='store_true',
                        dest='upgrade', help='''Upgrade the environment
                        directory to use this version of Python, assuming
                        Python has been upgraded in-place.''')
    parser.add_argument('--verbose', default=False, action='store_true',
                        dest='verbose', help='''Display the output from the
                        scripts which install setuptools and pip.''')
    return parser


def create(args):
    """Create the virtual environments and copy the sample configuration file

    Parameters
    ----------
    options : namespace
        options to use when creating the virtual environment
    """
    import dodocs.venvs.pyvenvex as pyenv
    pyenv.build_venv(args)

    cfg_file = dconf.get_sample_cfg_file()
    for d in args.dirs:
        shutil.copy(cfg_file, d)
    
        
