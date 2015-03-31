Configuration options
*********************

Configuration file options

.. _conf_example:

Example
=======

.. literalinclude:: ../../dodocs/dodocs_data/dodocs_setup.cfg
    :language: ini

..    :linenos:

Available options
=================

General
-------

There are few options common to all projects:

* ``target_dir``: directory where the documentation is moved after creation.
* ``is_edited``: dummy variable to check if the configuration has ever been
  edited; it should be removed or set to ``off``.
* ``version``: automatically filled when created a new profile; used to warn
  the user if the configuration and ``dodocs`` version do not agree.

Project
-------
