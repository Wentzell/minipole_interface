.. highlight:: bash

.. _install:

Install mini_pole_interface
***************************

``mini_pole_interface`` is a python-only TRIQS application. Two installs are
required: the upstream MiniPole Python package (and its missing dependency
``kneed``), and this wrapper, which builds against your TRIQS installation.

.. note:: To guarantee reproducibility in scientific calculations we strongly
   recommend the use of a stable
   `release <https://github.com/TRIQS/mini_pole_interface/releases>`_ of both
   TRIQS and its applications.

Prerequisites
=============

#. The :ref:`TRIQS <triqslibs:welcome>` library, see
   :ref:`TRIQS installation instructions <triqslibs:triqs_install>`.
   In the following, we assume that TRIQS is installed in the directory
   ``path_to_triqs``.

Runtime Python dependencies
===========================

The wrapper imports from `mini_pole`_, which itself imports
``kneed.KneeLocator`` at module load. ``kneed`` is **not** declared in
``mini_pole``'s ``install_requires`` (an upstream packaging omission), so we
list it explicitly. Install both into the same Python environment as your
TRIQS install:

.. _mini_pole: https://github.com/Green-Phys/MiniPole

::

    $ pip install mini_pole==0.7 kneed

The exact pin of ``mini_pole==0.7`` matches what this version of the wrapper
was tested against; bumping it requires a coordinated wrapper release.

Compiling mini_pole_interface from source
=========================================

#. Download the source code from GitHub::

     $ git clone https://github.com/TRIQS/mini_pole_interface mini_pole_interface.src

#. Source the TRIQS environment so ``find_package(TRIQS)`` resolves::

     $ source path_to_triqs/share/triqs/triqsvars.sh

#. Configure, build, and install::

     $ cmake -S mini_pole_interface.src -B mini_pole_interface.build -GNinja
     $ ninja -C mini_pole_interface.build
     $ ninja -C mini_pole_interface.build test
     $ ninja -C mini_pole_interface.build install

   The default install prefix is ``$TRIQS_ROOT``; override with
   ``-DCMAKE_INSTALL_PREFIX=...``.

Version compatibility
=====================

The major and minor version of ``mini_pole_interface`` must match your
installed TRIQS library; see the :ref:`TRIQS website <triqslibs:versions>`.
Until a stable release is tagged, we recommend tracking the ``unstable``
branch::

    $ cd mini_pole_interface.src && git checkout unstable

Once a release is published, you can pin to a specific tag::

    $ cd mini_pole_interface.src && git tag         # list available tags
    $ git checkout <tag>                            # check out a specific version

and follow the build steps above.

Custom CMake options
====================

The compilation of ``mini_pole_interface`` can be configured using
CMake-options::

    cmake -S mini_pole_interface.src -B build -DOPTION1=value1 -DOPTION2=value2 ...

+-----------------------------------------------------------------+----------------------------------------------------------+
| Option                                                          | Syntax                                                   |
+=================================================================+==========================================================+
| Specify an installation path other than ``$TRIQS_ROOT``         | ``-DCMAKE_INSTALL_PREFIX=path_to_mini_pole_interface``   |
+-----------------------------------------------------------------+----------------------------------------------------------+
| Disable testing (not recommended)                               | ``-DBuild_Tests=OFF``                                    |
+-----------------------------------------------------------------+----------------------------------------------------------+
| Build the documentation                                         | ``-DBuild_Documentation=ON``                             |
+-----------------------------------------------------------------+----------------------------------------------------------+
