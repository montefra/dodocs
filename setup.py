"""Install the library and the script ``dodoc``

Copyright (c) 2015 Francesco Montesano
"""
import os
import sys

if sys.version_info < (3, 3):
    sys.exit("This code requires python 3.3 or older")

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

# import only dodocs.utils without relying on it to be in the package to avoid
# problems with requirements
dd = os.path.join(os.path.split(__file__)[0], 'dodocs')
sys.path.insert(0, dd)
from utils import get_version, dodocs_directory
sys.path.pop(0)


if sys.version_info < (3, 4):
    msg = ('This code relies on the venv module as implemented in python >='
           ' 3.4. If there is interest, should be possible to add support for'
           ' the ``virtualenv`` package in order to create virtual'
           ' environments using older versions of python\n'
           'Anyway remember that the code itself runs on python 3 only')
    sys.exit(msg)


# Custom install and develop. Create the directory ``.dodocs`` after
# installation is done
# inspired by
# http://www.niteoweb.com/blog/setuptools-run-custom-code-during-install
def wrap_run(command_subclass):
    """A decorator to modify the ``run`` command from `setuptools` to create a
    ``$HOME/.dodocs`` directory, if it doesn't exist.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        # check if the dodocs_dir exists or not
        dodocs_dir = dodocs_directory()
        is_new, is_dir = False, False
        if not os.path.exists(dodocs_dir):
            is_new = True
        elif os.path.isdir(dodocs_dir):
            is_dir = True
        else:
            msg = "'{n}' already exists and it's not a directory. 'dodocs'"
            msg += " uses it as the home directory. If you can,"
            msg += " rename/remove/... '{n}', otherwise open an issue on"
            msg += " github and we will try to solve the problem. Installation"
            msg += " aborted."
            sys.exit(msg.format(n=dodocs_dir))

        # run the original run
        orig_run(self)

        # create the directory or use the old one
        if is_new:
            os.mkdir(dodocs_dir)
            print("\n'{}' directory created\n".format(dodocs_dir))
        elif is_dir:
            print("\n'{}' already exists: I'm going to use it,"
                  " then\n".format(dodocs_dir))

    command_subclass.run = modified_run
    return command_subclass


@wrap_run
class CustomDevelopCommand(develop):
    pass


@wrap_run
class CustomInstallCommand(install):
    pass


def extras_require():
    """Deal with extra requirements

    Returns
    -------
    dictionary of requirements
    """
    req_dic = {'doc': ['sphinx', 'numpydoc', 'alabaster', ],
               }

    req_dic['livedoc'] = req_dic['doc'] + ['sphinx-autobuild>=0.5.2', ]

    return req_dic

classifiers = ["Development Status :: 1 - Planning",
               "Environment :: Console",
               "Intended Audience :: Developers",
               "Intended Audience :: Other Audience",
               "Programming Language :: Python :: 3.3",
               "Programming Language :: Python :: 3.4",
               "Topic :: Documentation",
               "Topic :: Documentation :: Sphinx",
               ]

setup(
    # package description and version
    name="dodocs",
    version=get_version(from_file='dodocs/__init__.py'),
    author="Francesco Montesano",
    author_email="franz.bergesund@gmail.com",
    description="Heterogeneous collection of HETDEX-related functionalities",
    long_description=open("README.md").read(),
    license="The MIT License (MIT)\n Copyright (c) 2015 Francesco Montesano",

    # custom install and build
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },

    # list of packages and data
    packages=find_packages(),
    include_package_data=True,
    # don't zip when installing
    zip_safe=False,

    # entry points
    entry_points={"console_scripts": ["dodoc = dodocs:main", ], },

    # dependences
    install_requires=['colorama'],
    extras_require=extras_require(),
    # bootstrap nose to make `nosetests` available to setup.py
    setup_requires=['nose>=1', ],

    # tests
    tests_require=['nose>=1', 'coverage'],
    test_suite='nose.collector',

    classifiers=classifiers,
)
