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


@pytest.fixture
def profile_rm():
    """Execute the command profile remove"""
    command_line = 'profile remove dodocs_pytest'
    dodocs.main(command_line.split())


@pytest.fixture
def profile_edit():
    """Execute the command profile edit"""
    command_line = 'profile edit dodocs_pytest'
    dodocs.main(command_line.split())


# profile listing
def test_list_no_exist_home(tmp_and_clear, profile_list, caplog):
    """Test that listing without a dodocs directory fails"""
    record = caplog.records()[0]
    assert record.levelname == "CRITICAL"
    assert "No dodocs directory found" in record.message


def test_list_no_exist_profile(mkdodocs_dir, profile_list, clear_conf_log, caplog):
    """Test that listing without a dodocs directory fails"""
    record = caplog.records()[1]
    assert record.levelname == "WARNING"
    assert "No profile found" in record.message


def test_list(create_and_clear, profile_list, caplog):
    "List profiles"
    list_record = [r.levelname == "INFO" for r in caplog.records() if
                   'profile.list' in r.subc]
    assert all(list_record)
    assert len(list_record) == 3


def test_list_link(create_symlink_and_clear, profile_list, caplog):
    """Test the linking of the profile"""
    list_record = [r.levelname == "INFO" for r in caplog.records() if
                   'profile.list' in r.subc]
    assert all(list_record)
    assert len(list_record) == 3
    assert ("(-> " + create_symlink_and_clear[1] + ")") in caplog.text()


# profile removal
def test_rm_no_exists(tmp_and_clear, profile_rm, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[0]
    assert record.levelname == "WARNING"
    assert "Profile does not exist" in record.message


# profile editing
def test_edit_no_exists(tmp_and_clear, profile_edit, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[0]
    assert record.levelname == "CRITICAL"
    assert "No dodocs directory found" in record.message


@pytest.mark.skipif("True")
def test_create():
    "List profiles"
    command_line = 'profile create'
    # dodocs.main(command_line.split())
