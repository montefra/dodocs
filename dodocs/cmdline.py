"""Command line parser

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import argparse as ap

from dodocs import profiles
from dodocs import utils

DEF_FORMATTER = ap.ArgumentDefaultsHelpFormatter


def parse(argv=None):
    """Define the command line and returns the namespace

    Parameters
    ----------
    argv: list of strings, optional
        command line

    Returns
    -------
    namespace
        parsed command line
    """

    description = """Build and deploy code documentation."""

    p = ap.ArgumentParser(description=description,
                          formatter_class=DEF_FORMATTER)

    p.add_argument('--version', action='version', version=utils.get_version())
    # p.add_argument("-v", "--verbose", action="store_true", help="Verbose
    # mode")

    # add subparsers
    subparser = p.add_subparsers(title='Subcommands', dest='subparser_name',
                                 description="""Type '%(prog)s cmd -h' for
                                 detailed information about the subcommands"""
                                 )

    # create profile
    subparser = profiles.profiles_cmd_arguments(subparser, DEF_FORMATTER)

    # build the whole thing
    # build = subparser.add_parser("build", description="""Create the
    #                             documentation""",
    #                             formatter_class=DEF_FORMATTER)
    return p.parse_args(args=argv)
