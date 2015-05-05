"""Version control system (vcs) abstraction layer

Initialise and return the appropriate version control handler

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import subprocess as sp

import importlib
from pathlib import Path


# key: vcs; value: vcs class
_vcs = {}
"Map of known version control system names to executables"


class VCSTypeError(KeyError):
    """Unknown vcs type"""
    pass


def init():
    """Import all the modules in the vcs directory to register the available
    vcs handlers.

    Must be called before using any of the handlers, e.g. in
    :func:`dodocs.mkdocs.build_doc`
    """
    vcs_dir = Path(__file__).parent
    for to_register in vcs_dir.glob('*py'):
        if to_register.name not in ['__init__.py', 'base_vcs.py']:
            importlib.import_module(__name__ + '.' + to_register.stem)


def register_vcs(vcs, VCSClass):
    """Register ``VCSClass`` for ``language``

    Parameters
    ----------
    vcs : string
        type of vcs
    VCSClass : child of :class:`~dodocs.mkdoc.vcs.base_vcs.BaseVCS`
        vcs class to associate with the ``vcs`` type
    """
    _vcs[vcs] = VCSClass


def picker(profile, project, conf, log):
    """Pick and initialise the vcs

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the string
    conf : :class:`configparser.ConfigParser` instance
        configuration object
    log : :class:`~logging.LoggerAdapter` or :class:`~logging.Logger`
        logger

    Returns
    -------
    VCSClass : child of :class:`~dodocs.mkdoc.vcs.base_vcs.BaseVCS`
    """
    vcs_type = conf.get(project, "vcs")

    try:
        VCSClass = _vcs[vcs_type]
    except KeyError:
        raise VCSTypeError("The required version control system '{}'"
                           " is not implemented yet, sorry".format(vcs_type))

    return VCSClass(profile, project, conf, log)


# === Anything below here must be rewritten ===#
def get_or_update_source(vcs_name, from_where):
    """Get or update the source code

    Parameters
    ----------
    vcs_name: string
        kind of version control system
    from_where: string
        path or url of the repository/source code

    Raises
    ------
    VCSError
        if the vcs type is unknown or something happened when creating/updating
        the repository
    """
    # convert the vcs name to executable
    try:
        vcs_exe = _vcs[vcs_name]
    except KeyError as e:
        raise VCSTypeError from e

    if is_repo(vcs_exe):
        update_repo(vcs_exe)
    else:
        clone_repo(vcs_exe, from_where)


def is_repo(vcs_exe):
    """check if current working directory is under version control

    Parameters
    ----------
    vcs_exe: string
        name of the vsc command to execute

    Returns
    -------
    bool
        whether it's are repository or not
    """
    cmd = [vcs_exe, "status"]
    try:
        stdout = sp.check_output(cmd, stderr=sp.STDOUT)
        if vcs_exe != "svn":
            return True
        else:
            if "warning: W155007:" in stdout:
                return False
    except sp.CalledProcessError:
        return False


def update_repo(vcs_exe):
    """Update the repository in the current directory

    Parameters
    ----------
    vcs_exe: string
        name of the vsc command to execute

    Raises
    ------
    VCSError
        if the repository update fails
    """
    cmd = [vcs_exe, "pull"]
    try:
        sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        raise VCSTypeError from e


def clone_repo(vcs_exe, from_where):
    """Create the new repository

    Parameters
    ----------
    vcs_exe: string
        name of the vsc command to execute
    from_where: string
        path or url of the repository/source code

    Raises
    ------
    VCSError
        if the vcs type is unknown or something happened when creating/updating
        the repository
    """
    cmd = [vcs_exe, "clone", from_where, '.']
    try:
        sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        raise VCSTypeError from e
