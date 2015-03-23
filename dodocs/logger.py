"""Create a logger instance

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import logging


_logadapt = {}


def setLogger(args, name=None):
    """Create the logger instance and save a :class:`logging.LoggerAdapter`
    instance to enable the creation of custom format line.

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

    Returns
    -------
    :class:`~logging.LoggerAdapter`
    """
    # name of the asked command
    subc = _get_subc(args)
    subcd = {'subc': subc}
    try:
        logadapt = _logadapt[name]
        logadapt.extra = subcd
    except KeyError:
        log = logging.getLogger(name=name)

        # set level
        if args.verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        log.setLevel(level)

        # create the stdout handler and set the formatter
        fmt = "[%(subc)s - %(levelname)s]: %(message)s"
        formatter = logging.Formatter(fmt=fmt)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        log.addHandler(handler)

        # create the subc string
        logadapt = logging.LoggerAdapter(log, subcd)

    _logadapt[name] = logadapt
    return logadapt


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
    """Returns the adapted logger with called ``name`` or a standard logger as
    fallback

    Returns
    -------
    :class:`~logging.LoggerAdapter` or :class:`~logging.Logger`
    """
    try:
        return _logadapt[name]
    except KeyError:
        return logging.getLogger(name)
