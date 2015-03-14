"""Main function

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import sys

import colorama

from dodocs.cmdline import parse

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

    try:
        args.func(args)
    except AttributeError:
        # defaults profile to list
        if args.subparser_name == 'profile' and args.profile_cmd is None:
            main([args.subparser_name, 'list'])
        else:
            # in the other cases suggest to run -h
            msg = colorama.Fore.RED + "Please provide a valid command."
            print(msg)
            msg = "Type\n  " + sys.argv[0]
            if args.subparser_name is not None:
                msg += " " + args.subparser_name
            msg += ' -h'
            print(msg)
