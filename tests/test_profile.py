"""Test the profile listing and creation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""
import shutil
import subprocess

import pytest

import dodocs

import conftest


# fixtures
@pytest.fixture
def profile_list():
    """Execute the command profile list"""
    command_line = 'profile list'
    dodocs.main(command_line.split())


@pytest.fixture
def profile_rm(default_profile_name):
    """Execute the command profile remove"""
    command_line = 'profile remove ' + default_profile_name
    dodocs.main(command_line.split())


@pytest.fixture
def profile_edit(default_profile_name, monkeypatch):
    """Execute the command profile edit
    To avoid user interaction mocks ``subprocess.call`` simply registering the
    calls to it.

    Returns: list of calls
    """
    calls = []

    def mock_call(*args, **kwargs):
        calls.append([args, kwargs])

    monkeypatch.setattr(subprocess, 'call', mock_call)

    command_line = 'profile edit ' + default_profile_name
    dodocs.main(command_line.split())

    return calls


# profile listing
def test_list_no_exist_home(tmp_and_clear, profile_list, caplog):
    """Test that listing without a dodocs directory fails"""
    record = caplog.records()[0]
    assert record.levelname == "CRITICAL"
    assert "No dodocs directory found" in record.message


def test_list_no_exist_profile(mkdodocs_dir, profile_list, clear_conf_log,
                               caplog):
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


# profile creation

def test_create_create_link(create_and_clear, create_symlink_and_clear,
                            caplog):
    """Try to create the profile twice, once normal and once symlinking"""
    # the last record is a failure
    last_record = caplog.records()[-1]
    assert last_record.levelname == 'ERROR'
    assert "Profile already exists" in last_record.message


@pytest.mark.parametrize('force, level, msg',
                         ([' -f', 'WARNING', "Removing existing profile"],
                          ["", "ERROR", "Profile already exists. Aborting."]))
def test_recreate(create_and_clear, default_profile_name, caplog, force, level,
                  msg):
    """Test forcing a profile creation"""
    conftest.create_profile(default_profile_name + force)
    levels = [r.levelname for r in caplog.records()]
    assert level in levels
    levels = [r.message for r in caplog.records() if r.levelname == level]
    assert msg in levels
    assert sum(l == 'INFO' for l in levels) == len(levels) - 1


@pytest.mark.parametrize('force, level, msg',
                         ([' -f', 'WARNING',
                           "Unlinking and removing existing profile"],
                          ["", "ERROR", "Profile already exists. Aborting."]))
def test_recreate_force_link(create_symlink_and_clear, default_profile_name,
                             caplog, tmpdir, force, level, msg):
    """Test forcing a profile creation with a link"""
    args = "{} -l {}".format(force, tmpdir)
    conftest.create_profile(default_profile_name + args)
    levels = [r.levelname for r in caplog.records()]
    assert level in levels
    levels = [r.message for r in caplog.records() if r.levelname == level]
    assert msg in levels
    assert sum(l == 'INFO' for l in levels) == len(levels) - 1
    if tmpdir.exists():
        shutil.rmtree(str(tmpdir))


def test_recreate_link_force(create_symlink_and_clear, default_profile_name,
                             caplog):
    """Test forcing a profile creation, with the original as a link"""
    args = " -f"
    conftest.create_profile(default_profile_name + args)
    levels = [r.levelname for r in caplog.records()]
    assert "WARNING" in levels
    assert sum(l == 'INFO' for l in levels) == len(levels) - 1


def test_recreate_with_link_force(create_and_clear, default_profile_name,
                                  caplog, tmpdir):
    """Test forcing a link profile creation, with the original as real path"""
    args = " -f -l {}".format(tmpdir)
    conftest.create_profile(default_profile_name + args)
    levels = [r.levelname for r in caplog.records()]
    assert "WARNING" in levels
    assert sum(l == 'INFO' for l in levels) == len(levels) - 1


# profile removal

def test_rm_no_exists(tmp_and_clear, profile_rm, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[0]
    assert record.levelname == "WARNING"
    assert "Profile does not exist" in record.message


def test_rm(create_and_clear, profile_rm, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[-1]
    assert record.levelname == "INFO"
    assert "profile removed" in record.message


def test_rm_link(create_symlink_and_clear, profile_rm, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[-1]
    assert record.levelname == "INFO"
    assert "profile removed" in record.message


# profile editing

def test_edit_no_dodoc_dir(tmp_and_clear, profile_edit, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    record = caplog.records()[-1]
    assert record.levelname == "CRITICAL"
    assert "No dodocs directory found" in record.message
    assert len(profile_edit) == 0


def test_edit_no_exists(create_and_clear, caplog):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    command_line = 'profile edit no_exist'
    dodocs.main(command_line.split())
    record = caplog.records()[-1]
    assert record.levelname == "WARNING"
    assert "Profile does not exist" in record.message


def test_edit(create_and_clear, profile_edit):
    """Test that removing without a dodocs directory print a warning as first
    message"""
    assert len(profile_edit) == 1
