"""Test the profile listing and creation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import dodocs


def test_list():
    "List profiles"
    command_line = 'profile list'

    dodocs.main(command_line.split())
