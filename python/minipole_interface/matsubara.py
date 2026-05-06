################################################################################
#
# minipole_interface: TRIQS interface to the MiniPole analytic continuation package
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

"""Matsubara-frequency entry point.

Wraps :class:`mini_pole.MiniPole` for TRIQS Green's-function containers. The
single public function :func:`fit_poles_matsubara` accepts a ``Gf`` on
``MeshImFreq`` (matrix- or scalar-valued) or a ``BlockGf`` whose blocks live
on ``MeshImFreq``, slices the fermionic mesh to its non-negative half (which
upstream's contour-integral construction requires), and returns a
:class:`~minipole_interface.PoleResult` (or a ``dict[str, PoleResult]``
keyed by block name).
"""

from typing import Union

from mini_pole import MiniPole

from ._convert import (
    PoleResult,
    _gf_imfreq_to_arrays,
    _is_block_gf,
    _make_pole_result,
)


def fit_poles_matsubara(
    g,
    *,
    n0="auto",
    n0_shift: int = 0,
    err=None,
    err_type: str = "abs",
    M=None,
    symmetry: bool = False,
    G_symmetric: bool = False,
    compute_const: bool = False,
    plane=None,
    include_n0: bool = False,
    k_max: int = 999,
    ratio_max=10,
) -> Union[PoleResult, dict]:
    """Run MiniPole's matrix-valued MPM on a TRIQS Gf or BlockGf.

    Wraps :class:`mini_pole.MiniPole`. The fermionic Matsubara grid is sliced to
    its non-negative half (mini_pole assumes ``w[0] >= 0``).

    Parameters
    ----------
    g : Gf on MeshImFreq, or BlockGf
    n0, n0_shift, err, err_type, M, symmetry, G_symmetric, compute_const, plane, include_n0, k_max, ratio_max
        Forwarded verbatim to :class:`mini_pole.MiniPole`. See that class's
        docstring for a full description.

    Returns
    -------
    PoleResult, or dict[str, PoleResult] for BlockGf.
    """
    kw = {k: v for k, v in locals().items() if k != "g"}
    if _is_block_gf(g):
        return {name: fit_poles_matsubara(blk, **kw) for name, blk in g}

    G_w, w = _gf_imfreq_to_arrays(g)
    p = MiniPole(G_w, w, **kw)
    return _make_pole_result(p, n_orb=G_w.shape[1])
