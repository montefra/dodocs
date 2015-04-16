"""Deal with one profile documentation

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import os

import dodocs.config as dconf
import dodocs.logger as dlog
import dodocs.utils as dutils

from dodocs.mkdoc import vcs
from dodocs.mkdoc import pyvenvex


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
        try:
            build_project(profile, s, args)
        except Exception:
            msg = "something bad happened"
            log.exception(msg)
            continue


def build_project(profile, project, args):
    """Build the project documentation.

    * Fetch the code
    * if it's python:
        * make a virtualenv, if it does not exists already
        * pip install -e
    * build the documentation
    * if it's python:
        * deactivate the virtualenv

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the project
    args : namespace
        parsed command line arguments
    """
    conf = dconf.get_config(profile)
    log = dlog.getLogger()

    # create the directory
    dutils.mk_project(profile, project)

    # cd into it
    with dutils.cd_project(profile, project):
        log.debug("cd'ed into the project '%s' directory", project)
        vcs_type = conf.get(project, "vcs")
        project_path = conf.get(project, "project_path")

        vcs.get_or_update_source(vcs_type, project_path)
        log.debug("%s repository updated", vcs_type)

        # if the project is python deal with virtual environment
        language = conf.get(project, "language").lower()
        if language == "python3":
            venv_bin = pyvenvex.venv_bin(profile, language)
        else:
            raise ValueError("for now I don't know with language"
                             " {}".format(language))

        # if it's any python, install it in developer mode
        if language.find("python"):
            pip = os.path.join(venv_bin, 'pip')

        # build the documentation
