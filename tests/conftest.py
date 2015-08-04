"""Global settings and fixtures
"""
from pathlib import Path
import os
import shutil

import pytest

import dodocs


@pytest.fixture(scope='session')
def dodocs_homedir():
    """Return the home directory to use during the tests

    Returns
    -------
    :class:`pathlib.Path` instance
    """
    _path = Path(__file__).parent / 'data' / '.dodocs'
    return _path


@pytest.fixture()
def default_profile_name():
    """Return the default profile name: 'test_suite'"""
    return "test_suite"


def _create_project(pname=[default_profile_name()]):
    """Create a new project"""
    create_command = "profile create".split() + pname
    dodocs.main(create_command)


@pytest.yield_fixture(scope='session')
def homedir(dodocs_homedir):
    """Set the environment variable for the ``dodocs`` home directory and set up
    all the necessary things for running the tests. At the end of the test
    session, remove the ``dodocs`` home directory

    Yields
    ------
    :class:`pathlib.Path` instance
        home directory name
    """
    # set the dodocs home in the environment
    os.environ['DODOCSHOME'] = str(dodocs_homedir)
    # create a new project
    _create_project()
    yield dodocs_homedir
    if dodocs_homedir.exists():
        shutil.rmtree(str(dodocs_homedir))
    del os.environ['DODOCSHOME']


@pytest.yield_fixture
def tmp_homedir(monkeypatch, tmpdir):
    """Override ``homedir`` fixture temporarily unsetting the ``DODOCSHOME``
    environment variable and expanding user directory to a temporary one

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
