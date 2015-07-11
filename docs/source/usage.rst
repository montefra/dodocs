Usage
*****

``dodocs`` allows to group project under multiple profiles. All the projects
belonging to the same profile are treated together and copied to the same target
directory (see ``target_dir`` option in the ``[general]`` section in the
:ref:`configuration file example <conf_example>`).

The home directory is either ``~/.dodocs`` or, if the variable is defined in
the environment, ``$DODOCSHOME``.

Each of the profiles is a directory under ``~/.dodocs``. The most important file
in each profile directory is ``dodocs_setup.cfg`` and it contains all the
information needed by ``dodocs`` to build the documentation. The configuration
file is described in :doc:`config`.

``dodocs`` provides two subcommands:

* :ref:`profile <profile>`: manages profiles
* :ref:`mkdocs <mkdocs>`: creates the documentation for the desired profiles

.. _profile:

Profiles
========

Manage profiles:

* list the available profiles:
    + ``dodocs profile``
    + ``dodocs profile {list, ls}``
* create new profiles:
    + ``dodocs {create, new} name [name ...]``
    + if a profile already exists, its creation is skipped; the option ``-f``
      forces removing and recreating the profile;
    + the option ``-l LINK`` (``--link LINK``) allows to create the profile
      outside the ``.dodocs`` directory and to link it;
* remove existing profiles:
    + ``dodocs {remove, rm} name [name ...]``

.. _mkdocs:

Build the documentation
=======================

To build the documentation is as easy as issuing the following command:

* ``dodocs {mkdocs, build, make}``
