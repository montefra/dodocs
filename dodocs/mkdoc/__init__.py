"""Build the documentation
"""


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

    # build.set_defaults(func=plist)
    build.add_argument('name', nargs="+", help="""Name(s) of the
                       profile(s) to process""")

    return subparser
