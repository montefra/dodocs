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
from threading import Thread
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlretrieve
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

    try:
        build_venv(venv_dir)
        log.debug("Virtualenv '%s' created", venv_dir)
    except URLError as e:
        log.warning("The Virtualenv has been created but it couldn't fetch"
                    " pip and setuptools from the network. As pip is"
                    " needed for the installation of python packages, it"
                    " gets removed")
        # shutil.rmtree(venv_dir)
        raise VenvError("Virtual environment creation failed") from e


class ExtendedEnvBuilder(venv.EnvBuilder):
    """
    This builder installs setuptools and pip so that you can pip or
    easy_install other packages into the created environment.

    Parameters
    ----------
    nodist : bool, optional
        If True, ``setuptools`` and ``pip`` are not installed into the created
        environment.
    nopip : bool, optional
        If True, ``pip`` is not installed into the created environment.
    progress: callable, optional
        If setuptools or pip are installed, the progress of the installation
        can be monitored by passing a progress callable. If specified, it is
        called with two arguments: a string indicating some progress, and a
        context indicating where the string is coming from. The context
        argument can have one of three values: 'main', indicating that it is
        called from virtualize() itself, and 'stdout' and 'stderr', which are
        obtained by reading lines from the output streams of a subprocess which
        is used to install the app.

        If a callable is not specified, default progress information is output
        to sys.stderr.
    verbose : bool, optional
        verbose mode
    """

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop('nodist', False)
        self.nopip = kwargs.pop('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verbose = kwargs.pop('verbose', False)
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the environment
        being created.

        Parameters
        ----------
        context : context object
            The information for the environment creation request being
            processed.
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir
        if not self.nodist:
            self.install_setuptools(context)
        # Can't install pip without setuptools
        if not self.nopip and not self.nodist:
            self.install_pip(context)

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a
        progress callable (if specified) or write progress information to
        sys.stderr.

        Parameters
        ----------
        stream : file object like instance
            subprocess output stream
        context : context object
            The information for the environment creation request being
            processed.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, url):
        """Install the script ``name`` fetching its source from ``url`

        Parameters
        ----------
        context : context object
            The information for the environment creation request being
            processed.
        name : string
            name of the script to install
        url : string
            url there to find the script
        """
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the env's binaries folder
        urlretrieve(url, distpath)
        progress = self.progress
        if self.verbose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress('Installing %s ...%s' % (name, term), 'main')
        else:
            sys.stderr.write('Installing %s ...%s' % (name, term))
            sys.stderr.flush()
        # Install in the env
        args = [context.env_exe, fn]
        p = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done.', 'main')
        else:
            sys.stderr.write('done.\n')
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the environment.

        Parameters
        ----------
        context : context object
            The information for the environment creation request being
            processed.
        """
        url = 'https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py'
        self.install_script(context, 'setuptools', url)
        # clear up the setuptools archive which gets downloaded
        pred = lambda o: o.startswith('setuptools-') and o.endswith('.tar.gz')
        files = filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the environment.

        Parameters
        ----------
        context : context object
            The information for the environment creation request being
            processed.
        """
        url = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'
        self.install_script(context, 'pip', url)


def build_venv(venv_dir):
    """Create the virtual environments

    Parameters
    ----------
    venv_dir : string
        name of the directory of the virtual environment
    """
    log = dlog.getLogger()

    builder = ExtendedEnvBuilder(system_site_packages=False, clear=False,
                                 symlinks=False, upgrade=False, nodist=False,
                                 nopip=False, verbose=True)
    builder.create(venv_dir)
    log.debug("Installing sphinx")
    pip = os.path.join(bin_dir(venv_dir), 'pip')
    cmd = [pip, 'install', 'sphinx']
    try:
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            log.debug(stdout)
        if stderr:
            log.error(stderr)
        else:
            log.debug("Sphinx installed")
    except FileNotFoundError:
        log.error("The installation of 'sphinx' failed because '%s' could not"
                  " be found ", pip)
