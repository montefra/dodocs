"""Create a logger instance

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import logging

import colorlog


_def_extras = {'subc': '', 'profile': '', 'project': ''}
_extra = {}


def _colorformatter():
    """Returns the color formatter"""
    formatter = colorlog.ColoredFormatter(
        fmt=("%(log_color)s%(levelname)-8s [%(subc)s - %(project)s -"
             " %(profile)s]%(reset)s: %(message)s"),
        datefmt=None,
        reset=True,
        log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
        )
    return formatter


def setLogger(args, name=None):
    """Create the logger instance and save the extra dictionary used to create
    a :class:`logging.LoggerAdapter` instance.

    Of the command line arguments are used:

    * ``verbose``: if true the logger level is set to DEBUT, otherwise to INFO
    * ``subparser_name``: to get the name of the branch we're working
    * any further subparser

    Parameters
    ----------
    args : Namespace
        parsed command line options
    name : string or None
        name of the logger to use. ``None`` is the root logger
    """
    # if extra already exists, then the logger has also already initialised
    try:
        extra = _extra[name]
    except KeyError:  # initialise the logger
        log = logging.getLogger(name=name)

        # set level
        if args.verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        log.setLevel(level)

        # create the stdout handler and set the formatter
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(_colorformatter())
        log.addHandler(handler)

        # create the extra entry
        extra = _def_extras.copy()

    # name of the asked command
    subc = _get_subc(args)
    extra['subc'] = subc
    _extra[name] = extra


def _get_subc(args):
    """create the string used by the "subc" format string

    Parameters
    ----------
    args : Namespace
        parsed command line options

    Returns
    -------
    string
    """
    subc = args.subparser_name
    if args.subparser_name == 'profile' and args.profile_cmd is not None:
        subc += "." + args.profile_cmd
    return subc


def getLogger(name=None):
    """Returns the adapted logger based on the logger called ``name``

    Returns
    -------
    :class:`~logging.LoggerAdapter`
    """
    try:
        extra = _extra[name]
    except KeyError:
        extra = _def_extras.copy()
    return logging.LoggerAdapter(logging.getLogger(name), extra)


def set_subcommand(args, name=None):
    """Set the subcommand name in the logger adapter extra dictionary

    Parameters
    ----------
    Parameters
    ----------
    args : Namespace
        parsed command line options
    name : string or None
        name of the logger to use. ``None`` is the root logger
    """
    _extra[name]['subc'] = _get_subc(args)


def set_project(project: str, name=None):
    """Set the name of the project in the logger adapter extra dictionary

    Parameters
    ----------
    project : string
        name of the project
    name : string or None
        name of the logger to use. ``None`` is the root logger
    """
    _extra[name]['project'] = project


def set_profile(profile: str, name=None):
    """Set the name of the profile in the logger adapter extra dictionary

    Parameters
    ----------
    profile : string
        name of the profile
    name : string or None
        name of the logger to use. ``None`` is the root logger
    """
    _extra[name]['profile'] = profile
