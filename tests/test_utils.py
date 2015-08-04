"""Test the functionalities provided by dodocs/utils.py
"""
import pathlib

import pytest

import dodocs
import dodocs.utils as du

_test_version_p = [(None, dodocs.__version__),
                   (dodocs.__file__, dodocs.__version__),
                   pytest.mark.xfail(raises=UnboundLocalError)((__file__, 0.)),
                   pytest.mark.xfail(raises=FileNotFoundError)(("random", 0.)),
                   ]


@pytest.mark.parametrize("fname,expected", _test_version_p)
def test_version(fname, expected):
    assert du.get_version(from_file=fname) == expected


def test_tmp_homedir(tmp_homedir):
    """Correct monkey patched home directory"""
    assert du.dodocs_directory() == tmp_homedir / '.dodocs'


def test_homedir(homedir):
    """Correct default testing home directory"""
    assert du.dodocs_directory() == homedir


def test_profile_dir(dodocs_homedir):
    """Correct profile directory"""
    profile_dir = du.profile_dir("profile")
    assert dodocs_homedir == profile_dir.parent
    assert profile_dir.name == "profile"


def test_project_dir(dodocs_homedir):
    """Correct project directory"""
    project_dir = du.project_dir("profile", "project")
    assert project_dir.name == "project"
    profdir = project_dir.parent
    assert profdir.name == du.SRC_DIRECTORY
    profdir = profdir.parent
    assert profdir.name == "profile"
    assert dodocs_homedir == profdir.parent


def test_venv_dir(dodocs_homedir):
    """Correct virtual environment dir"""
    venv_dir = du.venv_dir("profile", "python3")
    assert venv_dir.name == "python3"
    vdir = venv_dir.parent
    assert vdir.name == du.VENV_DIRECTORY
    vdir = vdir.parent
    assert vdir.name == "profile"
    assert dodocs_homedir == vdir.parent


def test_build_dir(dodocs_homedir):
    """Correct build directory directory"""
    project_dir = du.build_dir("profile", "project")
    assert project_dir.name == "project"
    profdir = project_dir.parent
    assert profdir.name == du.BUILD_DIRECTORY
    profdir = profdir.parent
    assert profdir.name == "profile"
    assert dodocs_homedir == profdir.parent


def test_project_creation(tmp_homedir):
    """Test that the directory is correctly created"""
    du.mk_project("profile", "project")
    assert du.project_dir("profile", "project").exists()


def test_project_creation_again(tmp_homedir):
    """Test that the directory is correctly only once"""
    for i in range(4):
        du.mk_project("profile", "project")
    assert du.project_dir("profile", "project").exists()


def test_project_creation_fail(tmp_homedir):
    pass


def test_cd_profile(tmp_homedir):
    """Test that we do cd into the project directory"""
    du.mk_project("profile", "project")
    with du.cd_project("profile", "project"):
        assert pathlib.Path.cwd() == du.project_dir("profile", "project")
