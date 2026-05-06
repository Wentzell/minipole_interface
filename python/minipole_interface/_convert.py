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

from dataclasses import dataclass, field
from typing import Any, Optional, Union

import numpy as np


@dataclass
class PoleResult:
    """Result of a MiniPole analytic continuation.

    The continuation yields a sum-of-poles representation

        G(z) = sum_l pole_weight[l] / (z - pole_location[l]) + const

    Attributes
    ----------
    pole_location : ndarray, shape (M,), complex
        Pole locations (sorted by ``Re(xi)`` ascending).
    pole_weight : ndarray, shape (M, n_orb, n_orb), complex
        Pole weights. Always 3-D; for scalar input ``n_orb == 1``.
    const : ndarray, shape (n_orb, n_orb)
        Additive constant (zeros if ``compute_const`` was not requested).
    fit_error : float or None
        Maximum residual reported by the upstream ESPRIT fit (``upstream.err_max``
        when available). ``None`` if upstream did not expose it.
    upstream : object
        The underlying ``mini_pole.MiniPole*`` instance, kept for debugging /
        access to internal diagnostics (singular value spectrum, etc.).
    """

    pole_location: np.ndarray
    pole_weight: np.ndarray
    const: np.ndarray
    fit_error: Optional[float]
    upstream: Any = field(repr=False)

    @property
    def n_orb(self) -> int:
        return self.pole_weight.shape[1]

    def evaluate(self, z: Union[complex, np.ndarray]) -> np.ndarray:
        """Evaluate ``G(z) = sum_l A_l / (z - x_l) + const``.

        Parameters
        ----------
        z : complex or array_like of complex
            Point(s) at which to evaluate the pole representation. Any shape
            is accepted; the orbital indices are appended as the last two
            axes of the result.

        Returns
        -------
        out : ndarray, complex
            Shape ``(*z.shape, n_orb, n_orb)``, or ``(n_orb, n_orb)`` for
            scalar ``z``.
        """
        z = np.asarray(z, dtype=complex)
        z_flat = z.reshape(-1)
        denom = z_flat[:, None] - self.pole_location[None, :]
        out = np.einsum("kl,lij->kij", 1.0 / denom, self.pole_weight) + self.const
        return out.reshape(*z.shape, self.n_orb, self.n_orb)

    def to_gf_imfreq(self, mesh):
        """Construct a TRIQS Gf on a Matsubara mesh from this pole representation.

        Parameters
        ----------
        mesh : MeshImFreq
            Target Matsubara mesh.

        Returns
        -------
        g : triqs.gfs.Gf
            Gf with ``target_shape == (n_orb, n_orb)`` whose data is the
            evaluation of the pole sum at the mesh points.
        """
        from triqs.gfs import Gf

        iw = np.asarray(mesh.values(), dtype=complex)
        g = Gf(mesh=mesh, target_shape=(self.n_orb, self.n_orb))
        g.data[:] = self.evaluate(iw)
        return g

    def to_gf_refreq(self, mesh, eta: float = 1e-3):
        """Construct a retarded TRIQS Gf on a real-frequency mesh.

        Evaluates the pole sum at ``omega + i*eta`` to give a smooth
        retarded continuation; the spectral function follows from
        ``A(omega) = -Im G(omega) / pi``.

        Parameters
        ----------
        mesh : MeshReFreq
            Target real-frequency mesh.
        eta : float, optional
            Imaginary broadening (default ``1e-3``). Larger values produce
            smoother spectra; smaller values resolve sharper features but
            are noisier when poles lie close to the real axis.

        Returns
        -------
        g : triqs.gfs.Gf
            Gf with ``target_shape == (n_orb, n_orb)``.
        """
        from triqs.gfs import Gf

        omega = np.asarray(mesh.values())
        g = Gf(mesh=mesh, target_shape=(self.n_orb, self.n_orb))
        g.data[:] = self.evaluate(omega + 1j * eta)
        return g


def _ensure_3d(data) -> np.ndarray:
    """Reshape scalar-valued (1-D) Gf data to (n_w, 1, 1); pass through otherwise."""
    data = np.asarray(data)
    return data.reshape(-1, 1, 1) if data.ndim == 1 else data


def _make_pole_result(p, n_orb: int) -> PoleResult:
    """Build a PoleResult from an upstream mini_pole.MiniPole* instance.

    Normalizes the pole_weight to shape ``(M, n_orb, n_orb)``. Captures the
    additive constant and the ESPRIT residual when available.
    """
    pw = np.asarray(p.pole_weight)
    if pw.ndim == 1:
        pw = pw.reshape(-1, 1, 1)
    assert pw.ndim == 3 and pw.shape[1] == pw.shape[2] == n_orb, (
        f"unexpected pole_weight shape {pw.shape} for n_orb={n_orb}"
    )

    const = getattr(p, "const", 0.0)
    if np.isscalar(const):
        const = np.full((n_orb, n_orb), const, dtype=complex)
    else:
        const = np.asarray(const, dtype=complex).reshape(n_orb, n_orb)

    fit_error = getattr(p, "err_max", None)
    if fit_error is not None:
        fit_error = float(fit_error)

    return PoleResult(
        pole_location=np.asarray(p.pole_location, dtype=complex),
        pole_weight=pw.astype(complex, copy=False),
        const=const,
        fit_error=fit_error,
        upstream=p,
    )


def _gf_imfreq_to_arrays(g):
    """Extract ``(G_data, w)`` from a Gf on MeshImFreq, restricted to non-negative
    Matsubara frequencies (a requirement of mini_pole.MiniPole).

    For matrix-valued Gf returns ``G_data`` of shape ``(n_w, n_orb, n_orb)``.
    For scalar-valued Gf reshapes to ``(n_w, 1, 1)``.
    """
    w_full = np.asarray(g.mesh.values(), dtype=complex).imag
    pos = w_full >= 0.0
    if not pos.any():
        raise ValueError("Gf has no non-negative Matsubara frequencies.")
    data = _ensure_3d(g.data)
    return data[pos], w_full[pos]


def _is_block_gf(g) -> bool:
    """True iff ``g`` is a TRIQS BlockGf (not a single Gf)."""
    from triqs.gfs import BlockGf

    return isinstance(g, BlockGf)


def _dlr_to_pole_repr(g):
    """Extract MiniPoleDLR-compatible (Al_dlr, xl_dlr, beta) from a TRIQS Gf
    on MeshDLRImFreq, MeshDLRImTime, or MeshDLR.

    cppdlr stores
        G(iw_n) = sum_l c_l / (iw_n - omega_l)
    where the coefficient mesh ``MeshDLR`` exposes ``omega_l`` in dimensionless
    units (multiplied by beta). Dividing by beta yields the physical real-frequency
    pole locations expected by ``mini_pole.MiniPoleDLR`` as ``xl_dlr``.

    Returns
    -------
    Al_dlr : ndarray, shape (r, n_orb, n_orb)
    xl_dlr : ndarray, shape (r,)
    beta   : float
    """
    from triqs.gfs import MeshDLR, MeshDLRImFreq, MeshDLRImTime, make_gf_dlr

    if isinstance(g.mesh, MeshDLR):
        g_coef = g
    elif isinstance(g.mesh, (MeshDLRImFreq, MeshDLRImTime)):
        g_coef = make_gf_dlr(g)
    else:
        raise TypeError(
            f"Gf mesh must be MeshDLR, MeshDLRImFreq, or MeshDLRImTime; got "
            f"{type(g.mesh).__name__}"
        )

    beta = float(g_coef.mesh.beta)
    xl_dlr = np.asarray(g_coef.mesh.values(), dtype=float) / beta
    Al_dlr = _ensure_3d(g_coef.data).astype(complex, copy=False)
    return Al_dlr, xl_dlr, beta
