Usage
*****

``dodocs`` allows to group project under multiple profiles. All the projects
belonging to the same project are treated together and deployed into the same
target directory (see ``target_dir`` option in the ``[general]`` section in the
:ref:`configuration file example <conf_example>`).

Each of the profiles is a directory under ``~/.dodocs``. The most important file
in each profile directory is ``dodocs_setup.cfg`` and it contains all the
options needed by ``dodocs`` to build the documentation. The configuration file
is described in :doc:`config`.

To deal with the profiles and build the documentation, ``dodocs`` provide two
subcommands:

* :ref:`profile <profile>`: list, create and remove profiles
* :ref:`mkdocs <mkdocs>`: create the documentation for the desired profiles

.. _profile:

Profiles
========

Manage profiles:

* list the available profiles
    + ``dodocs profile``
    + ``dodocs profile {list, ls}``
* create new profiles
    + ``dodocs {create, new} name [name ...]``
    + if a profile already exists, its creation is skipped; the option ``-f``
      forces removing and recreating the profile
    + the option ``-l`` (``--link``) allows to create the profile into a given
      directory and to link it into the ``.dodocs`` directory


.. _mkdocs:

Build the documentation
=======================
