"""Base class for the documentation builders.

All the builders should be derived from this base builder, and if necessary
reimplement its interface, defined in :class:`BaseBuilder`

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import abc
from pathlib import Path
import shutil
import subprocess as sp

import dodocs.utils as dutils

from dodocs.mkdoc import vcs


class BaseBuilder(metaclass=abc.ABCMeta):
    """Base class documentation builder.

    It defines the interface that any builder should implement.

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
    project_path : string
        path where to grab the project
    language : string
        language of the project
    """
    def __init__(self, profile, project, conf, log):
        self.profile = profile
        self.project = project
        self.conf = conf
        self.log = log

        self.project_path = conf.get(project, "project_path")

        # get or update the source
        self.vcs_ = vcs.picker(profile, project, conf, log)

        # save the language
        self.language = conf.get(project, "language").lower()

    @property
    @abc.abstractmethod
    def build_cmd(self):
        """Command used to build the documentation.

        If the documentation builder is a simple command line call, it's enough
        to override this property and define the correct command.

        Returns
        -------
        cmd : list of strings
            command to execute to build the documentation
        """
        cmd = []
        return cmd

    def build_doc(self):
        """Build the documentation.

        Execute the :attr:`build_cmd` in a shell and log the output
        """
        self.log.debug("running '%s'", " ".join(self.build_cmd))
        p = sp.Popen(self.build_cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                     universal_newlines=True)
        stdout, stderr = p.communicate()
        if stdout:
            self.log.debug(stdout)
        if stderr:
            self.log.error(stderr)
        if p.returncode > 0:
            self.log.critical("'%s' return code is '%d'",
                              " ".join(self.build_cmd), p.returncode)

    @property
    def html_dir(self):
        """Directory where the documentation has been built.

        If the documentation builder, doesn't allow to decide the output
        directory, override this property.

        Returns
        -------
        :class:`pathlib.Path`
            directory contating the html files
        """
        return dutils.build_dir(self.profile, self.project) / 'html'

    @property
    def target_dir(self):
        """Directory where the documentation is going to be moved.

        Returns
        -------
        :class:`pathlib.Path`
            directory where to move the html files
        """
        _target_dir = Path(self.conf.get('general', 'target_dir'))
        return _target_dir / self.profile / self.project

    def move_doc(self):
        """Move the documentation to the ``target_dir`` defined in the
        configuration file.
        """
        # Remove the target directory. This way it avoids having spurious stuff
        # for older builds
        target_dir = str(self.target_dir)
        try:
            shutil.rmtree(target_dir)
        except FileNotFoundError:
            pass  # the directory does not exist
        # move the hml
        shutil.move(str(self.html_dir), target_dir)

    @abc.abstractmethod
    def clear_tmp(self):
        """Clear the temporary directory.

        Left to be implemented to the various builders
        """
        pass
