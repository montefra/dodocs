"""Version control system (vcs) abstraction layer

Implement git

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import dodocs.utils as dutils
from dodocs.mkdoc.vcs.base_vcs import BaseVCS


class Git(BaseVCS):
    """Implement git handler. The main complication is that git needs to act in
    the repository directory tree.
    """

    @property
    def status_cmd(self):
        """git status"""
        return [self.vcs_type, "status"]

    def is_repo(self):
        with dutils.cd_project(self.profile, self.project):
            super().is_repo()

    @property
    def update_cmd(self):
        """Command to update the repository

        Default "[vcs type] update project_dir".
        """
        return [self.vcs_type, "pull"]

    def update_repo(self):
        with dutils.cd_project(self.profile, self.project):
            super().update_repo()

    @property
    def getrepo_cmd(self):
        """Command to clone/checkout the repository

        Default "[vcs type] clone project_dir".
        """
        return [self.vcs_type, "clone", self.project_path,
                dutils.project_dir(self.profile, self.project)]
