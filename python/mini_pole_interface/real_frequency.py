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

"""Analytic real-frequency entry point.

Wraps :class:`mini_pole.MiniPoleRf`. The single public function
:func:`minipole_rf` accepts the analytic continuation of a Green's-function
matrix as a callable (scalar), a flat list of ``n_orb**2`` callables in
row-major order, or a nested ``n_orb x n_orb`` list. Each callable
``G_ij(z)`` must be analytic in the upper half-plane. There is no Gf input
here: TRIQS containers do not carry the analytic continuation of the
function, so the user must supply the analytic form themselves.
"""

from typing import Callable, Sequence, Union

import numpy as np

from mini_pole import MiniPoleRf

from ._convert import PoleResult, _make_pole_result


def minipole_rf(
    G_rf: Union[Callable, Sequence[Callable], Sequence[Sequence[Callable]]],
    *,
    func_type: str = "real",
    interval_type: str = "infinite",
    w_min: float = -10.0,
    w_max: float = 10.0,
    wp_max: float = 1.0,
    sing_vals=None,
    err: float,
    M=None,
    compute_const: bool = False,
    k_max: int = 999,
    Lfactor: float = 0.4,
) -> PoleResult:
    """Run MiniPoleRf on analytic real-frequency Green's-function expression(s).

    Wraps :class:`mini_pole.MiniPoleRf`. Unlike :func:`minipole_matsubara` /
    :func:`minipole_dlr`, this entry point does not accept a TRIQS Gf: TRIQS
    containers do not carry the analytic continuation of the Green's function,
    so the user must supply the analytic form ``G_ij(z)`` themselves.

    Parameters
    ----------
    G_rf : callable, list of callables, or n_orb x n_orb nested list
        Analytic expressions of the real-frequency Green's functions evaluated
        in the upper half-plane. Either a single callable (scalar), a flat list
        of length ``n_orb**2`` in row-major order (passed straight to upstream),
        or a nested ``n_orb x n_orb`` list which is flattened in row-major order.
    func_type, interval_type, w_min, w_max, wp_max, sing_vals, err, M, compute_const, k_max, Lfactor
        Forwarded to :class:`mini_pole.MiniPoleRf`. ``err`` is required by
        upstream.

    Returns
    -------
    PoleResult
    """
    G_rf_list = _flatten_rf_input(G_rf)
    n_orb = int(round(np.sqrt(len(G_rf_list))))
    if n_orb * n_orb != len(G_rf_list):
        raise ValueError(
            f"G_rf has {len(G_rf_list)} entries; expected n_orb**2 for some integer n_orb."
        )

    p = MiniPoleRf(
        G_rf_list,
        func_type=func_type,
        interval_type=interval_type,
        w_min=w_min,
        w_max=w_max,
        wp_max=wp_max,
        sing_vals=sing_vals,
        err=err,
        M=M,
        compute_const=compute_const,
        k_max=k_max,
        Lfactor=Lfactor,
    )
    return _make_pole_result(p, n_orb=n_orb)


def _flatten_rf_input(G_rf) -> list:
    """Normalize G_rf to a flat list of n_orb**2 callables, row-major."""
    if callable(G_rf):
        return [G_rf]
    seq = list(G_rf)
    if not seq:
        raise ValueError("G_rf must contain at least one callable.")
    if callable(seq[0]):
        return seq
    rows = [list(row) for row in seq]
    n_orb = len(rows)
    if any(len(row) != n_orb for row in rows):
        raise ValueError("Nested G_rf must be square (n_orb x n_orb).")
    return [rows[i][j] for i in range(n_orb) for j in range(n_orb)]
