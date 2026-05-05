#!/usr/bin/env python

"""Single-pole Matsubara analytic continuation regression test."""

import unittest

import numpy as np
from triqs.gfs import Gf, MeshImFreq, MeshReFreq

from mini_pole_interface import minipole_matsubara


class TestMatsubaraSinglePole(unittest.TestCase):
    """G(iw) = 1/(iw - 0.3) recovered with M=1."""

    def setUp(self):
        self.beta = 10.0
        self.x0 = 0.3
        mesh = MeshImFreq(self.beta, "Fermion", 200)
        self.g = Gf(mesh=mesh, target_shape=(1, 1))
        iw = np.asarray(mesh.values(), dtype=complex)
        self.g.data[:, 0, 0] = 1.0 / (iw - self.x0)
        self.res = minipole_matsubara(self.g, M=1)

    def test_pole_recovery(self):
        self.assertEqual(self.res.pole_location.shape, (1,))
        self.assertEqual(self.res.pole_weight.shape, (1, 1, 1))
        self.assertAlmostEqual(self.res.pole_location[0], self.x0 + 0j, places=8)
        self.assertAlmostEqual(self.res.pole_weight[0, 0, 0], 1.0 + 0j, places=8)

    def test_evaluate_matches_analytic(self):
        z = np.array([0.5 + 0.01j, 1.0 + 0.01j, 2.0 + 0.01j])
        got = self.res.evaluate(z)[..., 0, 0]
        want = 1.0 / (z - self.x0)
        np.testing.assert_allclose(got, want, atol=1e-8)

    def test_to_gf_refreq_shape_and_values(self):
        rmesh = MeshReFreq(-2.0, 2.0, 41)
        g_re = self.res.to_gf_refreq(rmesh, eta=1e-3)
        self.assertEqual(g_re.data.shape, (41, 1, 1))
        omega = np.asarray(rmesh.values())
        want = 1.0 / (omega + 1j * 1e-3 - self.x0)
        np.testing.assert_allclose(g_re.data[:, 0, 0], want, atol=1e-6)


if __name__ == "__main__":
    unittest.main()
