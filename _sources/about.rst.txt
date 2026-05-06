.. _about:

About minipole_interface
*************************

``minipole_interface`` is a TRIQS-side wrapper around the
`Green-Phys/MiniPole <https://github.com/Green-Phys/MiniPole>`_ analytic
continuation package. The Minimal Pole Method (MPM) algorithm — the
matrix-valued ESPRIT step, the conformal maps, and the DLR / real-frequency
variants — is implemented upstream by the
`Egull group <https://github.com/Green-Phys>`_. This package pins the
``mini_pole==0.7`` PyPI release and exposes its functionality through TRIQS
Green's-function containers (``Gf`` / ``BlockGf`` on ``MeshImFreq``,
``MeshDLRImFreq``, ``MeshDLRImTime``).

A sister TRIQS-orbit package, `adapol <https://github.com/flatironinstitute/adapol>`_,
provides a different analytic continuation algorithm (AAA + semi-definite
programming). The two coexist; pick whichever matches your data.

Authors
=======

Wrapper layer: N. Wentzell.

Upstream MiniPole authors: L. Zhang, Y. Yu, and E. Gull (University of
Michigan).

Citing
======

When using this package, please cite the upstream MPM publications:

.. code-block:: bibtex

    @article{Zhang2024MatrixMPM,
      author = {Zhang, Lei and Gull, Emanuel},
      title = {Minimal pole representation and controlled analytic
               continuation of matrix-valued correlation functions},
      journal = {Phys. Rev. B},
      volume = {110},
      pages = {235131},
      year = {2024},
      doi = {10.1103/PhysRevB.110.235131}
    }

    @article{Zhang2024ScalarMPM,
      author = {Zhang, Lei and Yu, Yang and Gull, Emanuel},
      title = {Minimal pole representation and analytic continuation of
               matrix-valued correlation functions},
      journal = {Phys. Rev. B},
      volume = {110},
      pages = {035154},
      year = {2024},
      doi = {10.1103/PhysRevB.110.035154}
    }

    @article{Zhang2025RFMPM,
      author = {Zhang, Lei and Gull, Emanuel},
      title = {Minimal pole representation for spectral functions},
      journal = {J. Chem. Phys.},
      volume = {162},
      pages = {214111},
      year = {2025},
      doi = {10.1063/5.0273073}
    }

A reference to ``triqs/minipole_interface`` is appreciated when you also wish
to acknowledge the TRIQS-side wrapper.

License
=======

``minipole_interface`` is published under the GNU General Public License v3
(see ``LICENSE.txt``), in line with TRIQS conventions.
