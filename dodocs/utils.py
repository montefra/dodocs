"""Generic utilities"""


def get_version(from_file=None):
    """
    Returns the version number.

    Inspired by from :mod:`matplotlib.setupext`

    Parameters
    ----------
    from_file: string, optional
        scan from the string ``__version__`` in the given file
    """
    if from_file is None:
        import dodoc
        version = dodoc.__version__
    else:
        with open('lib/__init__.py') as fd:
            for line in fd:
                if (line.startswith('__version__')):
                    version = line.split('=')[1].strip().strip('"')
                    break
    return version
