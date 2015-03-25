"""Build the documentation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import colorama

import dodocs.config as dconf
import dodocs.logger as dlog
import dodocs.utils as dutils

from dodocs.mkdoc import mkprofile as mkp


def build_cmd_arguments(subparser, formatter_class):
    """Create the ``build`` parser and fill it with the relevant options.

    Parameters
    ----------
    subparser : instances of :class:`argparse._SubParsersAction`
    formatter_class : argparse formatter
        formatter to use when creating the subparser

    Returns
    -------
    parser
    """
    build = subparser.add_parser("mkdocs", description="""Build the
                                 documentation following the directives in the
                                 configuration file.""",
                                 formatter_class=formatter_class,
                                 help="Documentation builder",
                                 aliases=['build', 'make'])

    build.set_defaults(func=build_doc)
    build.add_argument('name', nargs="+", help="""Name(s) of the
                       profile(s) to process""")

    return subparser


def build_doc(args):
    """Build the documentation for the given profiles.

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    dodocs_dir = dutils.dodocs_directory()
    log = dlog.getLogger()

    for name in args.name:
        log.info(colorama.Fore.GREEN + "Building documentation for profile"
                 " '{}'".format(name))
        try:
            dconf.get_config(name)
        except dconf.DodocConfigError as e:
            log.error("Profile {} won't be built because \n" +
                          str(e))
            continue

    mkp.main(name, args)
