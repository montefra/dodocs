"""Test the profile listing and creation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""
import pytest

import dodocs


def test_list():
    "List profiles"
    command_line = 'profile list'
    dodocs.main(command_line.split())


@pytest.mark.skipif("True")
def test_create():
    "List profiles"
    command_line = 'profile create'
    # dodocs.main(command_line.split())
