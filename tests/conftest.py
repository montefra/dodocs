"""Global settings and fixtures
"""
from pathlib import Path
import os
import shutil

import pytest

import dodocs
import dodocs.config as dconfig
import dodocs.logger as dlog


def create_profile(pname):
    """Create a new profile with name ``pname``"""
    create_command = "profile create " + pname
    dodocs.main(create_command.split())


@pytest.fixture
def dodocs_homedir(monkeypatch):
    """Set in ``DODOCSHOME`` and return the home directory to use during the
    tests

    Returns
    -------
    :class:`pathlib.Path` instance
    """
    _path = Path(__file__).parent / 'data' / '.dodocs'
    # set the dodocs home in the environment
    monkeypatch.setitem(os.environ, "DODOCSHOME", str(_path))
    return _path


@pytest.yield_fixture
def tmp_homedir(monkeypatch, tmpdir):
    """Override ``dodocs_homedir`` fixture temporarily unsetting the
    ``DODOCSHOME`` environment variable and expanding user directory to a
    temporary one

    Yields
    ------
    :class:`pathlib.Path` instance
        temporary directory name
    """
    monkeypatch.delitem(os.environ, "DODOCSHOME", raising=False)

    _tmpdir = Path(str(tmpdir))

    def mockreturn(path):
        return str(_tmpdir)
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    yield _tmpdir

    if _tmpdir.exists():
        shutil.rmtree(str(_tmpdir))


@pytest.fixture
def default_profile_name():
    """Return the default profile name: 'test_suite'"""
    return "test_suite"


@pytest.yield_fixture
def set_dodocs(dodocs_homedir, default_profile_name):
    """Create the project and returns the directory and the name of the
    project. Removes the directory afterwards.

    Yields
    ------
    :class:`pathlib.Path` instance
        home directory name
    """
    # create a new profile
    create_profile(default_profile_name)
    yield dodocs_homedir, default_profile_name
    if dodocs_homedir.exists():
        shutil.rmtree(str(dodocs_homedir))


@pytest.yield_fixture
def set_dodocs_link(dodocs_homedir, default_profile_name, tmpdir):
    """Create the project symlinked to something else and returns the directory
    and the name of the project. Removes the directory afterwards.

    Yields
    ------
    :class:`pathlib.Path` instance
        home directory name
    string
        profile directory at which the link points
    """
    # create a new profile
    print(tmpdir.exists())
    link_to = " -l {}".format(str(tmpdir))
    create_profile(default_profile_name + link_to)
    yield dodocs_homedir, os.path.join(str(tmpdir), default_profile_name)
    if dodocs_homedir.exists():
        shutil.rmtree(str(dodocs_homedir))
    if tmpdir.exists():
        shutil.rmtree(str(tmpdir))


@pytest.yield_fixture
def mkdodocs_dir(dodocs_homedir):
    """Create the dodocs home directory without adding any profile"""
    create_profile("")
    yield dodocs_homedir
    if dodocs_homedir.exists():
        shutil.rmtree(str(dodocs_homedir))


@pytest.yield_fixture
def clear_conf_log():
    """After yielding nothing, clear the dictionaries containing the
    configuration and the logger"""
    yield
    # clear logging and configuration stuff
    dconfig._config_dic.clear()
    # get the underlying logger
    log = dlog.getLogger().logger
    for h in log.handlers:
        log.removeHandler(h)
    dlog._extra.clear()


@pytest.yield_fixture
def create_and_clear(set_dodocs, clear_conf_log):
    """Combine the creation and cleanup of the default dodocs project

    Returns the directory and the name of the
    project. Removes the directory afterwards."""
    yield set_dodocs


@pytest.yield_fixture
def create_symlink_and_clear(set_dodocs_link, clear_conf_log):
    """Combine the creation and cleanup of the symlinked dodocs project

    Returns the directory and the name of the
    project. Removes the directory afterwards."""
    yield set_dodocs_link


@pytest.yield_fixture
def tmp_and_clear(tmp_homedir, clear_conf_log):
    """Combine the creation of the temporary directory and cleanup.

    Returns the home directory"""
    yield tmp_homedir
