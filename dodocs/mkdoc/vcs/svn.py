"""Version control system (vcs) abstraction layer

Implement subversion

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import re

import dodocs.utils as dutils
from dodocs.mkdoc.vcs.base_vcs import BaseVCS
from dodocs.mkdoc.vcs import register_vcs


class Svn(BaseVCS):
    """Implement svn handler.
    """

    def __init__(self, profile, project, conf, log):
        super(Svn, self).__init__(profile, project, conf, log)
        self.branch = "trunk"

    def run_cmd(self, cmd):
        """Run command ``cmd`` in a subprocess, log and return stdout, stderr
        and return code. Subversion doesn't set a return code, but gives it in
        the stderr. Find it an replace the returncode with it

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
        stdout, stderr, returncode = super().run_cmd(cmd)

        if returncode == 0:
            # look for warning codes and if any treat it as an error and set
            # ``returncode`` to 2
            if re.findall(r"W\d{6}", stderr):
                returncode = 2
        return stdout, stderr, returncode

    @property
    def getrepo_cmd(self):
        """Command to checkout the repository

        "[vcs type] checkout project_path project_dir".
        """
        return [self.vcs_type, "checkout", self.project_path,
                dutils.project_dir(self.profile, self.project)]

    @property
    def source_dir(self):
        """Directory where the source code is found.

        For now it's just trunk
        """
        return super(Svn, self).source_dir() / self.branch


register_vcs("svn", Svn)
register_vcs("subversion", Svn)
