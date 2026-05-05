#!/usr/bin/env python

"""Real-frequency analytic continuation regression test for minipole_rf."""

import unittest

import numpy as np

from mini_pole_interface import minipole_rf


class TestRealFrequencyTwoPoles(unittest.TestCase):
    """G(z) = 1/(z - 0.3 + 0.05j) + 1/(z + 0.7 + 0.05j) recovered with M=2."""

    def setUp(self):
        # Two complex poles in the lower half-plane (retarded GF analytic in upper).
        self.poles = np.array([0.3 - 0.05j, -0.7 - 0.05j])
        self.G_rf = lambda z: 1.0 / (z - self.poles[0]) + 1.0 / (z - self.poles[1])
        self.res = minipole_rf(
            self.G_rf,
            func_type="complex",
            interval_type="infinite",
            wp_max=1.0,
            err=1e-9,
            M=2,
        )

    def test_pole_recovery(self):
        self.assertEqual(self.res.pole_weight.shape, (2, 1, 1))
        # Sort upstream's recovered poles by Re for stable comparison.
        got = np.array(sorted(self.res.pole_location, key=lambda p: p.real))
        want = np.array(sorted(self.poles, key=lambda p: p.real))
        np.testing.assert_allclose(got, want, atol=1e-4)

    def test_evaluate_matches_analytic(self):
        z = np.array([0.0 + 0.5j, 1.0 + 0.2j, 2.0 + 0.1j])
        got = self.res.evaluate(z)[..., 0, 0]
        want = self.G_rf(z)
        np.testing.assert_allclose(got, want, atol=1e-4)


if __name__ == "__main__":
    unittest.main()
