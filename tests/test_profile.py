"""Test the profile listing and creation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""
import pytest

import dodocs


# fixtures
@pytest.fixture
def profile_list():
    """Execute the command profile list"""
    command_line = 'profile list'
    dodocs.main(command_line.split())


# profile listing
def test_list_no_exist(tmp_homedir, profile_list, caplog):
    """Test that listing without a dodocs directory fails"""
    for record in caplog.records():
        assert record.levelname == "CRITICAL"
    assert "No dodocs directory found" in caplog.text()


@pytest.mark.skipif("True")
def test_list():
    "List profiles"
    command_line = 'profile list'
    dodocs.main(command_line.split())


@pytest.mark.skipif("True")
def test_create():
    "List profiles"
    command_line = 'profile create'
    # dodocs.main(command_line.split())
