"""Test the functionalities provided by dodocs/utils.py
"""

import os

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
