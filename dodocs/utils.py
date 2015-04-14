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

SRC_DIRECTORY = "src"
"The sources of the projects goes here"
VENV_DIRECTORY = "src"
"The virtual environments of the profiles go here"


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


def profile_dir(profile):
    """Name of the profile directory

    Parameters
    ----------
    profile : string
        name of the profile

    Returns
    -------
    string
        the name of the directory of the project
    """
    return os.path.join(dodocs_directory(), profile)


def project_dir(profile, project):
    """Name of the project directory

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the project

    Returns
    -------
    string
        the name of the directory where the source of the project lives
    """
    return os.path.join(profile_dir(profile), SRC_DIRECTORY, project)


def venv_dir(profile, language):
    """Name of the virtual environment

    Parameters
    ----------
    profile : string
        name of the profile
    language : string
        name of python version to use (e.g. ``python3``)

    Returns
    -------
    string
        the name of the directory where the venv is created
    """
    return os.path.join(profile_dir(profile), VENV_DIRECTORY, language)


def mk_project(profile, project):
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
    project_d = project_dir(profile, project)

    # if the directory does not exist create it
    try:
        os.makedirs(project_d)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(project_d):
            pass
        else:
            raise DodocsOSError from e


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
    project_d = project_dir(profile, project)
    return cd(project_d)


@contextlib.contextmanager
def cd(path):
    """Context manager to ``cd`` into the given path

    Parameters
    ----------
    path : string
        directory where to cd to
    """
    cwd = os.getcwd()

    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)
