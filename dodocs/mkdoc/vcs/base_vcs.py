"""Version control system (vcs) abstraction layer

Base class. All classes implementing vcs should derive from this.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import subprocess as sp

import dodocs.utils as dutils


class VCSUpdateError(sp.CalledProcessError):
    """Raised when the update fails"""
    pass


class VCSCloneError(sp.CalledProcessError):
    """Raised when the update fails"""
    pass


class BaseVCS(object):
    """Base class for dealing with the version control systems.

    It defines as "do-nothing" interface that any vcs should implement.

    Parameters
    ----------
    profile : string
        name of the profile
    project : string
        name of the string
    conf : :class:`configparser.ConfigParser` instance
        configuration object
    log : :class:`~logging.LoggerAdapter` or :class:`~logging.Logger`
        logger

    Attributes
    ----------
    profile, project, conf, log : as above
    vcs_type : string
        type of the version control system
    project_path : string
        path where to grab the project
    """
    def __init__(self, profile, project, conf, log):
        self.profile = profile
        self.project = project
        self.conf = conf
        self.log = log

        self.vcs_type = conf.get(project, "vcs")
        self.project_path = conf.get(project, "project_path")

        if self.is_repo():
            self.update_repo()
        else:
            self.get_repo()

    def run_cmd(self, cmd):
        """Run command ``cmd`` in a subprocess, log and return stdout, stderr
        and return code

        Parameters
        ----------
        cmd : list of strings
            command to run

        Returns
        -------
        stdout, stderr : string
            standard output and error of the command
        returncode : int
            return code of the command
        """
        p = sp.Popen(self.status_cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                     universal_newlines=True)
        stdout, stderr = p.communicate()
        if stdout:
            self.log.debug(stdout)
        if stderr:
            self.log.error(stdout)
        if p.returncode != 0:
            self.log.error("'%s' returned %d", ' '.join(self.status_cmd),
                           p.returncode)
        return stdout, stderr, p.returncode

    @property
    def status_cmd(self):
        """Command to check the status.

        Default "[vcs type] status project_dir".
        """
        return [self.vcs_type, "status",
                dutils.project_dir(self.profile, self.project)]

    def is_repo(self):
        """Run command :attr:``status_cmd`` to check whether the directory is
        already under version control

        Returns
        -------
        bool
            is a repository of the given kind or not
        """
        _, _, returncode = self.run_cmd(self.status_cmd)
        if returncode == 0:
            return True
        else:
            return False

    @property
    def update_cmd(self):
        """Command to update the repository

        Default "[vcs type] update project_dir".
        """
        return [self.vcs_type, "update",
                dutils.project_dir(self.profile, self.project)]

    def update_repo(self):
        """Update the repository.

        Raises
        ------
        VCSUpdateError
            if the repository update fails
        """
        _, _, returncode = self.run_cmd(self.update_cmd)
        if returncode != 0:
            raise VCSUpdateError("Could not update the repository of project"
                                 " '{}'".format(self.project))

    @property
    def getrepo_cmd(self):
        """Command to clone/checkout the repository

        Default "[vcs type] clone project_path".
        """
        return [self.vcs_type, "clone", self.project_path]

    def get_repo(self):
        """Update the repository.

        Raises
        ------
        VCSCloneError
            if the repository update fails
        """
        _, _, returncode = self.run_cmd(self.update_cmd)
        if returncode != 0:
            raise VCSCloneError("Could not clone the repository of project"
                                " '{}'".format(self.project))
