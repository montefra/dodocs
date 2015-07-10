"""Install the library and the script ``dodoc``

Copyright (c) 2015 Francesco Montesano
"""
import sys
try:
    from pathlib import Path
except ImportError:
    sys.exit("This code requires ``pathlib`` which is shipped with python 3.4"
             " or older")

from setuptools import setup, find_packages
from setuptools.command.test import test

# import only dodocs.utils without relying on it to be in the package to avoid
# problems with requirements
dd = Path(__file__).parent / 'dodocs'
sys.path.insert(0, str(dd))
from utils import get_version
sys.path.pop(0)


# custom test command using py.test
class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = []

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def extras_require():
    """Deal with extra requirements

    Returns
    -------
    dictionary of requirements
    """
    req_dic = {'doc': ['sphinx', 'numpydoc', 'alabaster', ],
               }

    req_dic['livedoc'] = req_dic['doc'] + ['sphinx-autobuild>=0.5.2', ]

    req_dic['test'] = ['pytest']

    req_dic['all'] = set(sum((v for v in req_dic.values()), []))

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
        'test': PyTest,
    },

    # list of packages and data
    packages=find_packages(),
    include_package_data=True,
    # don't zip when installing
    zip_safe=False,

    # entry points
    entry_points={"console_scripts": ["dodoc = dodocs:main", ], },

    # dependences
    install_requires=['colorlog'],
    extras_require=extras_require(),

    # tests
    tests_require=extras_require()['test'],

    classifiers=classifiers,
)
