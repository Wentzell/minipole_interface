#!/usr/bin/env python

"""DLR-mesh single-pole regression test for minipole_dlr."""

import unittest

import numpy as np
from triqs.gfs import Gf, MeshDLRImFreq

from minipole_interface import minipole_dlr


class TestDlrSinglePole(unittest.TestCase):
    """G(iw) = 1/(iw - 0.3) on a DLR Matsubara mesh -> recover pole exactly."""

    def setUp(self):
        self.beta = 10.0
        self.x0 = 0.3
        mesh = MeshDLRImFreq(self.beta, "Fermion", w_max=4.0, eps=1e-12)
        self.g = Gf(mesh=mesh, target_shape=(1, 1))
        iw = np.asarray(mesh.values(), dtype=complex)
        self.g.data[:, 0, 0] = 1.0 / (iw - self.x0)
        self.res = minipole_dlr(self.g, n0=2, M=1)

    def test_pole_recovery(self):
        self.assertEqual(self.res.pole_location.shape, (1,))
        self.assertEqual(self.res.pole_weight.shape, (1, 1, 1))
        self.assertAlmostEqual(self.res.pole_location[0], self.x0 + 0j, places=6)
        self.assertAlmostEqual(self.res.pole_weight[0, 0, 0], 1.0 + 0j, places=6)

    def test_evaluate_matches_analytic(self):
        z = np.array([0.5 + 0.01j, 1.0 + 0.01j, 2.0 + 0.01j])
        got = self.res.evaluate(z)[..., 0, 0]
        want = 1.0 / (z - self.x0)
        np.testing.assert_allclose(got, want, atol=1e-5)


if __name__ == "__main__":
    unittest.main()
