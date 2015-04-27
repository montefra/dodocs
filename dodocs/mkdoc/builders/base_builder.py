"""Base class for the documentation builders.

All the builders should be derived from this base builder, and if necessary
reimplement its interface, defined in :class:`BaseBuilder`

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import abc
import subprocess as sp

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
        vcs_type = conf.get(project, "vcs")
        vcs.get_or_update_source(vcs_type, self.project_path)
        log.debug("%s repository updated", vcs_type)

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

    def move_doc(self, destination):
        """Move the documentation to the correct place
        """
        raise NotImplementedError("The method must be implemented")
