"""Global settings and fixtures
"""
from pathlib import Path
import os

import pytest


@pytest.fixture(scope='session')
def dodocs_homedir():
    """Return the home directory to use during the tests

    Returns
    -------
    :class:`pathlib.Path` instance
    """
    _path = Path(__file__).parent / 'data' / '.dodocs'
    return _path


@pytest.yield_fixture(scope='session', autouse=True)
def homedir(dodocs_homedir):
    """Set the environment variable for the ``dodocs`` home directory and set up
    all the necessary things for running the tests. At the end of the test
    session, remove the ``dodocs`` home directory

    This fixture is auto used and in the session scope
    """
    test_homedir = dodocs_homedir
    os.environ['DODOCSHOME'] = str(test_homedir)
    yield test_homedir
    print("tear down global fixture")


@pytest.yield_fixture
def tmp_homedir(monkeypatch, tmpdir):
    """Override ``homedir`` fixture temporarily unsetting the ``DODOCSHOME``
    environment variable and expanding user directory to a temporary one"""
    monkeypatch.delitem(os.environ, "DODOCSHOME")

    def mockreturn(path):
        return str(tmpdir)
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    print("setting up the temp directory '{}'".format(tmpdir))
    yield Path(str(tmpdir))
    print("tearing down the temp directory '{}'".format(tmpdir))
