"""Deal with one profile documentation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import dodocs.config as dconf
import dodocs.logger as dlog
import dodocs.utils as dutils


def main(profile, args):
    """Make the documentation for on project

    Parameters
    ----------
    profile : string
        name of the profile
    args : namespace
        parsed command line arguments
    """
    log = dlog.getLogger()

    for s in dconf.get_projects(profile):
        log.debug("building project %s", s)
        build_project(profile, s, args)


def build_project(profile, project, args):
    """Build the project documentation.

    * Fetch the code
    * if it's python:
        * make a virtualenv, if it does not exists already
        * pip install -e
    * build the documentation

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the project
    args : namespace
        parsed command line arguments
    """
    # create the directory
    with dutils.cd_project(profile, project):
        pass
