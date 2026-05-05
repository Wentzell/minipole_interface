################################################################################
#
# mini_pole_interface: TRIQS interface to the MiniPole analytic continuation package
#
# Copyright (C) 2026, The Simons Foundation
#   author: N. Wentzell
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
################################################################################

r"""TRIQS interface to the MiniPole analytic continuation package.

Public entry points:

* :func:`minipole_matsubara` — wraps :class:`mini_pole.MiniPole` and accepts a
  TRIQS ``Gf``/``BlockGf`` on ``MeshImFreq``.
* :func:`minipole_dlr` — wraps :class:`mini_pole.MiniPoleDLR` and accepts a
  ``Gf``/``BlockGf`` on ``MeshDLR`` / ``MeshDLRImFreq`` / ``MeshDLRImTime``.
* :func:`minipole_rf` — wraps :class:`mini_pole.MiniPoleRf`; accepts analytic
  real-frequency expressions as callables.
* :func:`minipole_refine` — wraps :class:`mini_pole.MiniPoleRfDPR`; refines /
  compresses an existing pole representation.

All four return a :class:`PoleResult` (or a ``dict[block_name, PoleResult]`` for
``BlockGf`` input) carrying ``pole_location``, ``pole_weight``, ``const``, and
``evaluate`` / ``to_gf_imfreq`` / ``to_gf_refreq`` helpers.
"""

from ._convert import PoleResult
from .dlr import minipole_dlr
from .matsubara import minipole_matsubara
from .real_frequency import minipole_rf
from .refine import minipole_refine

__all__ = [
    "PoleResult",
    "minipole_matsubara",
    "minipole_dlr",
    "minipole_rf",
    "minipole_refine",
]
