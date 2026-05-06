#!/usr/bin/env python

"""BlockGf dispatch regression test."""

import unittest

import numpy as np
from triqs.gfs import BlockGf, Gf, MeshImFreq

from minipole_interface import PoleResult, minipole_matsubara


class TestBlockGfDispatch(unittest.TestCase):
    """Two-block BlockGf with different single poles per block."""

    def setUp(self):
        self.beta = 10.0
        self.x_up, self.x_dn = 0.3, -0.4
        mesh = MeshImFreq(self.beta, "Fermion", 200)
        g_up = Gf(mesh=mesh, target_shape=(1, 1))
        g_dn = Gf(mesh=mesh, target_shape=(1, 1))
        iw = np.asarray(mesh.values(), dtype=complex)
        g_up.data[:, 0, 0] = 1.0 / (iw - self.x_up)
        g_dn.data[:, 0, 0] = 1.0 / (iw - self.x_dn)
        self.bg = BlockGf(name_list=["up", "dn"], block_list=[g_up, g_dn])
        self.out = minipole_matsubara(self.bg, M=1)

    def test_returns_dict_keyed_by_block(self):
        self.assertIsInstance(self.out, dict)
        self.assertEqual(set(self.out.keys()), {"up", "dn"})
        for v in self.out.values():
            self.assertIsInstance(v, PoleResult)

    def test_per_block_poles(self):
        self.assertAlmostEqual(self.out["up"].pole_location[0], self.x_up + 0j, places=8)
        self.assertAlmostEqual(self.out["dn"].pole_location[0], self.x_dn + 0j, places=8)
        np.testing.assert_allclose(self.out["up"].pole_weight[0], 1.0, atol=1e-8)
        np.testing.assert_allclose(self.out["dn"].pole_weight[0], 1.0, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
