"""Generic utilities

Notes
-----

Make sure that this module imports only standard library modules, as it is used
during the setup. It is possible to test it?

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import contextlib
import errno
import os

src_directory = "src"
"The sources of the projects goes here"


class DodocsOSError(OSError):
    """Rename :class:`OSError`"""
    pass


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
        import dodocs
        version = dodocs.__version__
    else:
        with open(from_file) as fd:
            for line in fd:
                if (line.startswith('__version__')):
                    version = line.split('=')[1].strip().strip('"')
                    break
    return version


def dodocs_directory():
    """Returns the default ``dodocs`` directory

    Returns
    -------
    dodocs_dir: string
        dodocs directory
    """
    home = os.path.expanduser('~')
    dodocs_dir = os.path.join(home, '.dodocs')
    return dodocs_dir


def format_docstring(*args, **kwargs):
    """Decorator to format the docstring using :func:`string.format` syntax
    """
    def wrapper(func):
        doc = func.__doc__
        doc = doc.format(*args, **kwargs)
        func.__doc__ = doc
        return func
    return wrapper


def mkdir(profile, project):
    """Create the project directory for the profile

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the project

    Raises
    ------
    DodocsOSError
        if the directory(ies) could not be created
    """
    project_dir = os.path.join(dodocs_directory(), profile, src_directory,
                               project)

    # if the directory does not exist create it
    try:
        os.makedirs(project_dir)
        is_new = True
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(project_dir):
            pass
        else:
            raise DodocsOSError from e


@contextlib.contextmanager
def cd_project(profile, project):
    """Context manager to ``cd`` into a project of a profile and return to the
    original directory when finishing or upon error.

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the project
    """
    cwd = os.getcwd()

    project_dir = os.path.join(dodocs_directory(), profile, src_directory,
                               project)

    os.chdir(project_dir)
    try:
        yield
    finally:
        os.chdir(cwd)
