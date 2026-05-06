.. _issues:

Reporting issues
****************

This package sits between two upstream codebases. To get a fast resolution,
file your issue in the right tracker:

* **Bugs in the wrapper layer** (Gf ↔ ndarray conversion, ``PoleResult``
  helpers, ``BlockGf`` dispatch, build/install on top of TRIQS, missing
  CMake glue, documentation): file at
  `<https://github.com/TRIQS/minipole_interface/issues>`_.

* **Bugs in the MPM algorithm itself** (incorrect pole locations, ESPRIT /
  conformal-map behavior, knee detection, upstream API changes, regressions
  between ``mini_pole`` releases): file at
  `<https://github.com/Green-Phys/MiniPole/issues>`_. We pin
  ``mini_pole==0.7``, so please verify the behavior reproduces with that
  exact version.

* **TRIQS Green's-function or DLR issues** (mesh construction,
  ``make_gf_dlr`` semantics, ``BlockGf`` API): file at
  `<https://github.com/TRIQS/triqs/issues>`_.

When in doubt, open it here and we will redirect.

In all cases please include:

#. The version of ``minipole_interface``, ``mini_pole``, and TRIQS you are
   using (``triqs --version``, ``pip show mini_pole``, the git SHA of this
   repository).
#. For build problems: your operating system and compiler, the output of
   ``cmake`` and ``ninja``, and the ``CMakeCache.txt`` from the build
   directory. Attach as a `gist <https://gist.github.com/>`_.
#. For runtime problems: a self-contained script that reproduces the issue
   on a small example.

Thanks!
