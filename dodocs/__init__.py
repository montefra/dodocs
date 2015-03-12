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

    if args.subparser_name == "profile":
        from dodocs.profiles import main
        main(args)
    # elif args.subparser_name == "mkvenv":
    #     from dodocs.venvs import create
    #     create(args)
    # elif args.subparser_name == "build":
    #     print("building")
    else:
        msg = colorama.Fore.RED + "Please provide a command."
        msg += " Valid commands are:\n * profile"  # \n * create"
        sys.exit(msg)
