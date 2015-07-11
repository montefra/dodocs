"""Global settings and fixtures
"""
import os

import pytest


# monkey patch the expand user to test directory
@pytest.yield_fixture(scope='session', autouse=True)
def homedir():
    """Set the home directory"""
    print("setting the home directory")
    yield
    print("tear down the home directory")


@pytest.yield_fixture
def tmp_homedir(monkeypatch, tmpdir):
    "Set homedir to a tmp one"
    def mockreturn(path):
        return tmpdir
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    print("setting up the temp directory '{}'".format(tmpdir))
    yield
    print("tearing down the temp directory '{}'".format(tmpdir))
