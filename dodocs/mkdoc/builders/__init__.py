"""Builder picker.

Initialise and return the appropriate builder for the given language.

"""

import importlib
from pathlib import Path
import sys

# a builder for every language; key: language; value: builder class
_builders = {}


def init():
    # import all the modules in the builders directory to register them
    builders_dir = Path(__file__).parent
    for to_register in builders_dir.glob('*py'):
        if to_register.name not in ['__init__.py', 'base_builder.py']:
            importlib.import_module(__name__ + '.' + to_register.stem)


def register_builder(language, BuilderClass):
    """Register ``BuilderClass`` for ``language``

    Parameters
    ----------
    language : string
        language to register
    BuilderClass : :class:`~dodocs.mkdoc.builders.base_builder.BaseBuilder`
        builder class to associate with the ``language``
    """
    _builders[language] = BuilderClass


def picker(profile, project, conf, log):
    """Pick and initialise the builder

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
    :class:`~dodocs.mkdoc.builders.BaseBuilder
    """
    language = conf.get(project, "language").lower()

    try:
        BuilderClass = _builders[language]
    except KeyError:
        raise ValueError("The documentation builder for the language '{}'"
                         " is not implemented yet, sorry".format(language))

    return BuilderClass(profile, project, conf, log)
