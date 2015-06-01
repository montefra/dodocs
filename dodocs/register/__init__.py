"""Add ``dodocs register profile`` to the user crontab.

This module provides the command line and the entry point for the sub-package

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

from dodocs.register.rlist import rlist


def register_cmd_arguments(subparser, formatter_class):
    """Create the ``register`` parser and fill it with the relevant options.

    Parameters
    ----------
    subparser : instances of :class:`argparse._SubParsersAction`
    formatter_class : argparse formatter
        formatter to use when creating the subparser

    Returns
    -------
    parser
    """
    register = subparser.add_parser("register", description="""Add to and
                                    remove from ``crontab``, list registered
                                    jobs""", formatter_class=formatter_class,
                                    help="Cron jobs management")

    # create sub commands for the registration subparser
    register_cmd = register.add_subparsers(title="Actions",
                                           dest='register_cmd',
                                           description="""Type '%(prog)s cmd
                                           -h' for detailed information about
                                           the subcommands""")

    # list the registered profiles
    description = "List the registered profiles."
    register_list = register_cmd.add_parser("list", description=description,
                                            help=description + """ Default
                                            action""", aliases=['ls'])
    register_list.set_defaults(func=rlist)

    return subparser
