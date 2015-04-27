"""Create a virtual environment with python3 :mod:`venv`

The module is adapted from the example in :mod:`venv`.

Raises
------
ValueError
    for Python version < 3.3

Original copyright (C) 2013 Vinay Sajip. New BSD License.
Copyright 2015 Francesco Montesano.
MIT Licence
"""

import os
import shutil
import subprocess as sp
import sys
import venv

import dodocs.utils as dutils
import dodocs.logger as dlog

if sys.version_info < (3, 3) or not hasattr(sys, 'base_prefix'):
    raise ValueError('This script is only for use with Python 3.3 or later')


class VenvError(RuntimeError):
    """Error raised when something goes wrong with the virtualenv"""


def bin_dir(venv_dir):
    """Virtual environment bin directory

    Parameters
    ----------
    venv_dir : string
        name of the directory in which the virtual environment should be
        created

    Returns
    -------
    string
        bin directory
    """
    return os.path.join(venv_dir, 'bin')


def venv_bin(profile, pyversion):
    """Returns the path to the bin directory of the virtual environment for the
    given python version. Create it if necessary

    Parameters
    ----------
    profile : string
        name of the profile
    pyversion : string
        name of the python exe (e.g. ``python3``)

    Returns
    -------
    string
        bin directory
    """
    venv_dir = dutils.venv_dir(profile, pyversion)
    bindir = bin_dir(venv_dir)
    if not os.path.exists(venv_dir):
        create_venv(venv_dir)

    return bindir


@dutils.format_docstring(dutils.VENV_DIRECTORY)
def create_venv(venv_dir):
    """Create the virtual environment for the given python version and install
    sphinx in it.

    The virtual environment is located into the "{0}" subdirectory in the
    project.

    Parameters
    ----------
    venv_dir : string
        name of the directory in which the virtual environment should be
        created
    """
    log = dlog.getLogger()

    build_venv(venv_dir)
    log.debug("Virtualenv '%s' created", venv_dir)


class VenvInVenvBuilder(venv.EnvBuilder):
    """Virtual environment builder that, when instantiated from an other
    virtual environment, modifies the context to use global
    ``context.executable`` and ``context.python_dir``.

    This trick allow to install setuptools and pip also when dodocs is called
    from a virtual environment.
    """

    def ensure_directories(self, env_dir):
        """
        Create the directories for the environment.

        Returns a context object which holds paths in the environment,
        for use by subsequent logic.

        Parameters
        ----------
        env_dir : string
            directory of the virtual environment to create

        Returns
        -------
        context : Namespace
            environment paths and names
        """
        context = super(VenvInVenvBuilder, self).ensure_directories(env_dir)

        if 'VIRTUAL_ENV' in os.environ:
            original_venv = os.environ['VIRTUAL_ENV']
            path = os.environ['PATH']
            for d in path.split(":")[1:]:
                if original_venv in d:  # ignore the venv directory
                    continue
                if os.path.exists(os.path.join(d, context.python_exe)):
                    break
            else:
                raise ValueError("couldn't find any {} outside the virtual"
                                 " env, weird".format(context.python_exe))

            context.python_dir = d
            context.executable = os.path.join(d, context.python_exe)

        return context


def build_venv(venv_dir):
    """Create the virtual environments

    Parameters
    ----------
    venv_dir : string
        name of the directory of the virtual environment
    """
    log = dlog.getLogger()

    builder = VenvInVenvBuilder(with_pip=True)
    builder.create(venv_dir)
    log.debug("Installing sphinx")
    pip = os.path.join(bin_dir(venv_dir), 'pip')
    cmd = [pip, 'install', 'sphinx']
    try:
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            if stdout:
                log.debug(stdout)
            if stderr:
                log.warning(stderr)
            log.debug("Sphinx installed")
        else:
            if stdout:
                log.warning(stdout)
            if stderr:
                log.error(stderr)

            log.info("Removing '%s' to avoid future problems", venv_dir)
            shutil.rmtree(venv_dir)
            raise VenvError("The installation of sphinx failed. Are you"
                            " connected to the internet?")

    except FileNotFoundError:
        log.error("The installation of 'sphinx' failed because '%s' could not"
                  " be found ", pip)
