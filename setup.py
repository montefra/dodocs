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

# import only dodocs.utils without relying on it to be in the package to avoid
# problems with requirements
dd = Path(__file__).parent / 'dodocs'
sys.path.insert(0, str(dd))
from utils import get_version
sys.path.pop(0)


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
