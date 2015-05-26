"""Version control system (vcs) abstraction layer

Initialise and return the appropriate version control handler

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

import importlib
from pathlib import Path

# key: vcs; value: vcs class
_vcs = {}
"Map of known version control system names to executables"


class VCSTypeError(KeyError):
    """Unknown vcs type"""
    pass


def init():
    """Import all the modules in the vcs directory to register the available
    vcs handlers.

    Must be called before using any of the handlers, e.g. in
    :func:`dodocs.mkdocs.build_doc`
    """
    vcs_dir = Path(__file__).parent
    for to_register in vcs_dir.glob('*py'):
        if to_register.name not in ['__init__.py', 'base_vcs.py']:
            importlib.import_module(__name__ + '.' + to_register.stem)


def register_vcs(vcs, VCSClass):
    """Register ``VCSClass`` for ``language``

    Parameters
    ----------
    vcs : string
        type of vcs
    VCSClass : child of :class:`~dodocs.mkdoc.vcs.base_vcs.BaseVCS`
        vcs class to associate with the ``vcs`` type
    """
    _vcs[vcs] = VCSClass


def picker(profile, project, conf, log):
    """Pick and initialise the vcs

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

    Returns
    -------
    VCSClass : child of :class:`~dodocs.mkdoc.vcs.base_vcs.BaseVCS`
    """
    vcs_type = conf.get(project, "vcs")

    try:
        VCSClass = _vcs[vcs_type]
    except KeyError:
        raise VCSTypeError("The required version control system '{}'"
                           " is not implemented yet, sorry".format(vcs_type))

    return VCSClass(profile, project, conf, log)
