"""Version control system abstraction layer

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import subprocess as sp

known_vcs = {"git": "git",
             }
"Map of known version control system names to executables"


class VCSError(KeyError):
    """Unknown vcs type"""
    pass


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
        vcs_exe = known_vcs[vcs_name]
    except KeyError as e:
        raise VCSError from e

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
        stdout = sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        raise VCSError from e


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
        stdout = sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        raise VCSError from e
