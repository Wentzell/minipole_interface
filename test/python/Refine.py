#!/usr/bin/env python

"""Refinement regression test for refine_poles."""

import unittest

import numpy as np

from minipole_interface import refine_poles, fit_poles_rf


class TestRefineCompressesRedundancy(unittest.TestCase):
    """Refining the output of fit_poles_rf reproduces the same pole set."""

    def setUp(self):
        self.poles = np.array([0.3 - 0.05j, -0.7 - 0.05j])
        self.G_rf = lambda z: 1.0 / (z - self.poles[0]) + 1.0 / (z - self.poles[1])
        self.want = np.array(sorted(self.poles, key=lambda p: p.real))

    def test_refine_from_pole_result(self):
        first = fit_poles_rf(
            self.G_rf,
            func_type="complex",
            interval_type="infinite",
            wp_max=1.0,
            err=1e-9,
            M=2,
        )
        refined = refine_poles(
            first,
            interval_type="infinite",
            wp_max=1.0,
            err=1e-9,
            M=2,
        )
        got = np.array(sorted(refined.pole_location, key=lambda p: p.real))
        np.testing.assert_allclose(got, self.want, atol=1e-3)

    def test_refine_from_arrays(self):
        Al = np.ones((2, 1, 1), dtype=complex)
        xl = self.poles.astype(complex)
        refined = refine_poles(
            Al,
            xl,
            interval_type="infinite",
            wp_max=1.0,
            err=1e-9,
            M=2,
        )
        got = np.array(sorted(refined.pole_location, key=lambda p: p.real))
        np.testing.assert_allclose(got, self.want, atol=1e-3)


if __name__ == "__main__":
    unittest.main()
