.. _welcome:

minipole_interface
*******************

.. sidebar:: minipole_interface |PROJECT_VERSION|

   This is the homepage of minipole_interface |PROJECT_VERSION|.
   For changes see the :ref:`changelog page <changelog>`.

      .. image:: _static/logo_github.png
         :width: 75%
         :align: center
         :target: https://github.com/triqs/minipole_interface

A TRIQS-side wrapper for the
`MiniPole <https://github.com/Green-Phys/MiniPole>`_ minimal-pole-method (MPM)
analytic continuation package. ``minipole_interface`` lets you call MiniPole
on TRIQS Green's-function containers — ``Gf`` / ``BlockGf`` on ``MeshImFreq``,
``MeshDLRImFreq``, ``MeshDLRImTime`` — as well as on analytic real-frequency
expressions, returning a :class:`PoleResult` carrying pole locations, weights,
and ready-made evaluators.

.. note::

   The MPM algorithm itself is implemented upstream in
   `Green-Phys/MiniPole <https://github.com/Green-Phys/MiniPole>`_; this
   package only provides the TRIQS adapter layer and pins ``mini_pole==0.7``.
   When using it, please cite L. Zhang and E. Gull,
   *Phys. Rev. B* **110**, 235131 (2024)
   (`doi:10.1103/PhysRevB.110.235131 <https://doi.org/10.1103/PhysRevB.110.235131>`_)
   and the related papers listed on the :ref:`about` page.

Start with :ref:`install`, then work through the :ref:`tutorials`, or jump
directly into the API :ref:`reference`.

.. toctree::
   :maxdepth: 2
   :hidden:

   install
   tutorials
   reference
   about
   issues
   ChangeLog.md
