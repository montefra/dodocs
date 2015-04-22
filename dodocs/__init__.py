"""Main function

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os
import sys

import colorama

from dodocs.cmdline import parse
from dodocs.logger import setLogger

__version__ = "0.0.1"

colorama.init(autoreset=True)


def main(argv=None):
    """
    Main code

    Parameters
    ----------
    argv : list of strings, optional
        command line arguments
    """
    args = parse(argv=argv)

    log = setLogger(args)

    if "func" in args:
        args.func(args)
        log.debug("Finished")
    else:
        # defaults profile to list
        if args.subparser_name == 'profile' and args.profile_cmd is None:
            main(sys.argv[1:] + ["list"])
        else:
            # in the other cases suggest to run -h
            msg = (colorama.Fore.RED + "Please provide a valid command.\n"
                   "Type\n  " + os.path.split(sys.argv[0])[1])
            if args.subparser_name is not None:
                msg += " " + args.subparser_name
            msg += ' -h'
            log.error(msg)
