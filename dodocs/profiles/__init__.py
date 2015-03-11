"""Profile creation and management

This module provides the command line and the entry point for the sub-package

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

from dodocs import utils


def profiles_cmd_arguments(subparser, formatter_class):
    """Create the ``profiles`` parser and fill it with the relevant options.

    Parameters
    ----------
    subparser : instances of :class:`argparse._SubParsersAction`
    formatter_class : argparse formatter
        formatter to use when creating the subparser

    Returns
    -------
    parser
    """
    profile = subparser.add_parser("profile", description="""List and create
                                   profiles.""",
                                   formatter_class=formatter_class,
                                   help="Profiles management")

    # create sub commands for the profile subparser
    profile_cmd = profile.add_subparsers(title="Actions", dest='profile_cmd',
                                         description="""Type '%(prog)s cmd -h'
                                         for detailed information about the
                                         subcommands""")

    # list the profiles
    description = "List the available profiles."
    profile_list = profile_cmd.add_parser("list", description=description,
                                          help=description + " Default action")
    # profile_list.add_argument("-v", "--verbose", action="store_true")

    # create the profiles
    description = """Create a new profile in the '{home}' directory. A profile
                     is a subdirectory and at creation contains a
                     configuration. The user should edit the relevant parts of
                     the configuration file before creating the documentation.
                     """
    description = description.format(home=utils.dodocs_directory())
    profile_create = profile_cmd.add_parser("create", description=description,
                                            help="""Create a new profile""")

    profile_create.add_argument('name', help='''Name of the profile to
                                create''')
    profile_create.add_argument('-c', '--clean', action='store_true',
                                help='''If the profile already exists, remove it
                                and recreate new. Do it at your own risk''')
    return subparser


def main(args):
    """Manage the profiles

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    if args.profile_cmd == "list":
        from dodocs.profiles.plist import plist
        plist(args)
    elif args.profile_cmd == "create":
        print("create a profile")
    else:
        raise ValueError("Command {} is not valid".format(args.profile_cmd))