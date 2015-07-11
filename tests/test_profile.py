"""Test the profile listing and creation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""
import os

# import dodocs


def test_list():
    "List profiles"
    command_line = 'profile list'
    print(command_line)
    print(os.path.expanduser('~'))
    # dodocs.main(command_line.split())


def test_tmp(tmp_homedir):
    print(os.path.expanduser('~'))


def test_create():
    "List profiles"
    command_line = 'profile create'
    print(command_line)
    print(os.path.expanduser('~'))
    # dodocs.main(command_line.split())
