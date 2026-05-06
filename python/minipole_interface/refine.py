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

"""Pole-representation refinement entry point.

Wraps :class:`mini_pole.MiniPoleRfDPR`. The single public function
:func:`refine_poles` takes an existing pole representation (e.g. from
AAA, ``adapol``, or a previous ``minipole_*`` call), and returns a refined /
compressed one. Input may be a :class:`~minipole_interface.PoleResult`
directly or the underlying arrays ``(A_l, x_l)``.
"""

from typing import Optional, Union

import numpy as np

from mini_pole import MiniPoleRfDPR

from ._convert import PoleResult, _make_pole_result


def refine_poles(
    pole_or_Al: Union[PoleResult, np.ndarray],
    xl: Optional[np.ndarray] = None,
    *,
    interval_type: str = "infinite",
    w_min: float = -10.0,
    w_max: float = 10.0,
    wp_max: float = 1.0,
    err: Optional[float] = None,
    err_type: str = "abs",
    cutoff_err: Optional[float] = None,
    cutoff_err_type: str = "abs",
    M: Optional[int] = None,
    k_max: int = 999,
    Lfactor: float = 0.4,
    alpha: float = 1.0,
    minimal_k: bool = False,
) -> PoleResult:
    """Refine / compress an existing pole representation via MiniPoleRfDPR.

    Wraps :class:`mini_pole.MiniPoleRfDPR`. Accepts either a pre-existing pole
    representation as ``(Al_dpr, xl_dpr)`` arrays, or a previous
    :class:`PoleResult` directly (its const term, if any, is dropped — refinement
    operates on the pole sum only).

    Parameters
    ----------
    pole_or_Al : PoleResult or ndarray
        Either a :class:`PoleResult` (in which case ``xl`` must be ``None``) or the
        weights array ``Al_dpr`` of shape ``(r,)`` or ``(r, n_orb, n_orb)``.
    xl : ndarray or None
        Pole-location array of shape ``(r,)``. Required when ``pole_or_Al`` is
        an array; ignored when it is a :class:`PoleResult`.
    interval_type, w_min, w_max, wp_max, err, err_type, cutoff_err, cutoff_err_type, M, k_max, Lfactor, alpha, minimal_k
        Forwarded to :class:`mini_pole.MiniPoleRfDPR`.

    Returns
    -------
    PoleResult
    """
    if isinstance(pole_or_Al, PoleResult):
        if xl is not None:
            raise TypeError("Pass either a PoleResult or (Al, xl) — not both.")
        Al_dpr = pole_or_Al.pole_weight
        xl_dpr = pole_or_Al.pole_location
    else:
        if xl is None:
            raise TypeError(
                "When passing pole weights as an array, xl must also be supplied."
            )
        Al_dpr = np.asarray(pole_or_Al, dtype=complex)
        xl_dpr = np.asarray(xl, dtype=complex)

    p = MiniPoleRfDPR(
        Al_dpr,
        xl_dpr,
        interval_type=interval_type,
        w_min=w_min,
        w_max=w_max,
        wp_max=wp_max,
        err=err,
        err_type=err_type,
        cutoff_err=cutoff_err,
        cutoff_err_type=cutoff_err_type,
        M=M,
        k_max=k_max,
        Lfactor=Lfactor,
        alpha=alpha,
        minimal_k=minimal_k,
    )
    n_orb = Al_dpr.shape[1] if Al_dpr.ndim == 3 else 1
    return _make_pole_result(p, n_orb=n_orb)
