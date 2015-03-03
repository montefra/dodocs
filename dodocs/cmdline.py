"""Command line parser
"""

import argparse as ap

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

    description = """Fetch a repository, build the documentation and place it
    in the given place"""

    p = ap.ArgumentParser(description=description,
                          formatter_class=DEF_FORMATTER)

    p.add_argument('--version', action='version', version=utils.get_version())
    # p.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    # add subparsers
    subparser = p.add_subparsers(dest='subparser_name')

    # create virtual environment and place there the configuration file
    venv = subparser.add_parser("create", description="""Create the virtual
                                environment""", formatter_class=DEF_FORMATTER)

    venv.add_argument("name", help="Name of the virtual environment")

    return p.parse_args(args=argv)
