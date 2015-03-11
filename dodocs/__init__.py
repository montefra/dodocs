"""Main function

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

from dodocs.cmdline import parse

__version__ = "0.0.1"


def main():
    """
    Main code
    """
    args = parse()

    if args.subparser_name is None:
        raise ValueError("No command provided")
    elif args.subparser_name == "profile":
        from dodocs.profiles import main
        main(args)
    elif args.subparser_name == "mkvenv":
        from dodocs.venvs import create
        create(args)
    elif args.subparser_name == "build":
        print("building")
    else:
        raise ValueError("Command {} is not valid".format(args.subparser_name))
