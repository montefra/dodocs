"""Python3 builder.

Create a virtual environment if necessary, install the project if required and
run sphinx to build the documentation.

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import subprocess as sp

import dodocs.mkdoc.builders.base_builder as bb
from dodocs.mkdoc.builders import register_builder
from dodocs.mkdoc.builders import pyvenvex


class Py3BuilderError(RuntimeError):
    """Error in python 3 builder"""
    pass


class Python3Builder(bb.BaseBuilder):
    """Python

    Parameters
    ----------
    same as :class:`bb.BaseBuilder`
    """
    def __init__(self, *args, **kwargs):
        super(Python3Builder, self).__init__(*args, **kwargs)
        self._prepare_venv()

        py_install = self.conf.get(self.project, "py-install")
        if py_install.lower() not in ['no', 'none']:
            self.log.debug("install %s? %s", self.project, py_install)
            self._install_pkg(py_install)

    def _prepare_venv(self):
        """Prepare the virtual environment if necessary"""
        self._venv_bin = pyvenvex.venv_bin(self.profile, self.language)
        self.log.debug("virtualenv bin directory '%s'", self._venv_bin)

    def _install_pkg(self, what_install):
        """Install it in developer mode

        Parameters
        ----------
        what_install : string
            what to install; if ``yes`` just install, if any other string
            interpret it as optional dependences
        """
        pip = self._venv_bin / 'pip'
        cmd = [str(pip), 'install', '-e']
        if what_install.lower() == 'yes':
            cmd += ['.']
        else:
            cmd += ['.[{}]'.format(what_install)]
        self.log.debug("running '%s'", " ".join(cmd))

        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                     universal_newlines=True)
        stdout, stderr = p.communicate()
        if p.returncode < 0:
            if stdout:
                self.log.debug(str(stdout).replace('\n\n', '\n'))
        else:
            if stdout:
                self.log.error(str(stdout).replace('\n\n', '\n'))
        if stderr:
            self.log.error(stderr)
        if p.returncode > 0:
            self.log.error("'%s' return code: %d", " ".join(cmd), p.returncode)
            raise Py3BuilderError("pip failed")

    @property
    def build_cmd(self):
        cmd = ['ls']  # ['sphinx-build']
        return cmd


register_builder('python3', Python3Builder)
