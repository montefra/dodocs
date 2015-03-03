from setuptools import setup, find_packages
import os

import dodoc


setup(
    # package description and version
    name="dodoc",
    version=dodoc.utils.extract_version()
    author="Francesco Montesano",
    author_email="franz.bergesund@gmail.com",
    description="Heterogeneous collection of HETDEX-related functionalities",
    long_description=open("README.md").read(),

    # list of packages and data
    packages=find_packages(),
    # don't zip when installing
    zip_safe=False,

    # entry points
    entry_points={"dodoc": "dodoc.main:main"}

    # dependences
    install_requires=[],
    extras_require={'doc': ['sphinx', 'numpydoc']},

    # tests
    tests_requires=['nose>=1', 'coverage']
    test_suite='nose.collector',
)
