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

"""DLR entry point.

Wraps :class:`mini_pole.MiniPoleDLR` for TRIQS Green's-function containers
carrying a DLR mesh (``MeshDLR``, ``MeshDLRImFreq``, or ``MeshDLRImTime``).
The single public function :func:`minipole_dlr` extracts cppdlr's pole
representation directly and hands ``(A_l, x_l, beta)`` to upstream — see
:func:`minipole_interface._convert._dlr_to_pole_repr` for the
dimensionless-rf-nodes-divided-by-beta basis bridge.
"""

from typing import Union

from mini_pole import MiniPoleDLR

from ._convert import (
    PoleResult,
    _dlr_to_pole_repr,
    _is_block_gf,
    _make_pole_result,
)


def minipole_dlr(
    g,
    *,
    n0: int,
    nmax=None,
    err=None,
    err_type: str = "abs",
    M=None,
    symmetry: bool = False,
    k_max: int = 200,
    Lfactor: float = 0.4,
) -> Union[PoleResult, dict]:
    """Run MiniPoleDLR on a TRIQS Gf carrying a DLR mesh.

    Wraps :class:`mini_pole.MiniPoleDLR` by extracting cppdlr's pole
    representation directly. Both representations describe

        G(z) = sum_l A_l / (z - x_l),

    so the bridge is just a unit conversion: cppdlr stores the real-frequency
    DLR nodes in dimensionless form (multiplied by ``beta``), which we divide
    out before handing them to upstream.

    Parameters
    ----------
    g : Gf or BlockGf on MeshDLR / MeshDLRImFreq / MeshDLRImTime
    n0 : int
        Initial Matsubara index used by upstream's contour-integral construction.
        Typical range (0, 10).
    nmax, err, err_type, M, symmetry, k_max, Lfactor
        Forwarded to :class:`mini_pole.MiniPoleDLR`.

    Returns
    -------
    PoleResult, or dict[str, PoleResult] for BlockGf.
    """
    kw = {k: v for k, v in locals().items() if k != "g"}
    if _is_block_gf(g):
        return {name: minipole_dlr(blk, **kw) for name, blk in g}

    Al_dlr, xl_dlr, beta = _dlr_to_pole_repr(g)
    p = MiniPoleDLR(Al_dlr, xl_dlr, beta, **kw)
    return _make_pole_result(p, n_orb=Al_dlr.shape[1])
