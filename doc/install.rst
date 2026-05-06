.. highlight:: bash

.. _install:

Install minipole_interface
***************************

``minipole_interface`` is a python-only TRIQS application. It is installed
from source — there are no PyPI/conda binaries — into the same Python
environment as your TRIQS install. Two source-install paths are supported;
both are equally valid, pick whichever fits your workflow.

.. note:: To guarantee reproducibility in scientific calculations we strongly
   recommend the use of a stable
   `release <https://github.com/TRIQS/minipole_interface/releases>`_ of both
   TRIQS and its applications.

Prerequisites
=============

#. The :ref:`TRIQS <triqslibs:welcome>` library, see
   :ref:`TRIQS installation instructions <triqslibs:triqs_install>`.
   In the following, we assume that TRIQS is installed in the directory
   ``path_to_triqs`` and that you have sourced its environment::

     $ source path_to_triqs/share/triqs/triqsvars.sh

.. _install_pip:

Install from source via pip (recommended)
=========================================

::

    $ git clone https://github.com/TRIQS/minipole_interface
    $ pip install -e ./minipole_interface

Drop ``-e`` for a non-editable install. ``pip`` resolves the runtime Python
dependencies automatically — including the upstream ``mini_pole==0.7`` and
``kneed`` (the latter is imported at module-load time by ``mini_pole``'s
ESPRIT step but is missing from upstream's ``install_requires``, so we list it
defensively in our ``pyproject.toml``).

This path does **not** install the lmod modulefile, the ``vars.sh`` shell
script, or the CMake config files needed for ``find_package(minipole_interface)``;
use the CMake path below if you need any of those.

.. _install_cmake:

Install from source via CMake
=============================

::

    $ git clone https://github.com/TRIQS/minipole_interface minipole_interface.src
    $ cmake -S minipole_interface.src -B minipole_interface.build -GNinja
    $ ninja -C minipole_interface.build
    $ ninja -C minipole_interface.build test
    $ ninja -C minipole_interface.build install

The default install prefix is ``$TRIQS_ROOT``; override with
``-DCMAKE_INSTALL_PREFIX=...``. CMake does **not** install the runtime Python
dependencies — install them yourself into the same Python environment::

    $ pip install mini_pole==0.7 kneed

The exact pin of ``mini_pole==0.7`` matches what this version of the wrapper
was tested against; bumping it requires a coordinated wrapper release.

Version compatibility
=====================

The major and minor version of ``minipole_interface`` must match your
installed TRIQS library; see the :ref:`TRIQS website <triqslibs:versions>`.
The CMake configure step enforces this and hard-fails on mismatch; with
``pip`` it is your responsibility to install a compatible version.

Until a stable release is tagged, we recommend tracking the ``unstable``
branch::

    $ cd minipole_interface && git checkout unstable

Once a release is published, you can pin to a specific tag::

    $ cd minipole_interface && git tag         # list available tags
    $ git checkout <tag>                        # check out a specific version

and re-run the install step from your chosen path above.

Custom CMake options
====================

These options apply only to the :ref:`CMake install path <install_cmake>`.
Pass them when configuring::

    cmake -S minipole_interface.src -B build -DOPTION1=value1 -DOPTION2=value2 ...

+-----------------------------------------------------------------+----------------------------------------------------------+
| Option                                                          | Syntax                                                   |
+=================================================================+==========================================================+
| Specify an installation path other than ``$TRIQS_ROOT``         | ``-DCMAKE_INSTALL_PREFIX=path_to_minipole_interface``    |
+-----------------------------------------------------------------+----------------------------------------------------------+
| Disable testing (not recommended)                               | ``-DBuild_Tests=OFF``                                    |
+-----------------------------------------------------------------+----------------------------------------------------------+
| Build the documentation                                         | ``-DBuild_Documentation=ON``                             |
+-----------------------------------------------------------------+----------------------------------------------------------+
