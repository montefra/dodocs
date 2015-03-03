from setuptools import setup, find_packages
import os

from dodocs import utils

setup(
    # package description and version
    name="dodocs",
    version=utils.get_version(from_file='dodocs/__init__.py'),
    author="Francesco Montesano",
    author_email="franz.bergesund@gmail.com",
    description="Heterogeneous collection of HETDEX-related functionalities",
    long_description=open("README.md").read(),

    # list of packages and data
    packages=find_packages(),
    # don't zip when installing
    zip_safe=False,

    # entry points
    entry_points={"console_scripts": ["dodoc = dodocs.main:main", ],},

    # dependences
    install_requires=[],
    extras_require={'doc': ['sphinx', 'numpydoc']},

    # tests
    tests_require=['nose>=1', 'coverage'],
    test_suite='nose.collector',
)
