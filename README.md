[![build](https://github.com/TRIQS/minipole_interface/workflows/build/badge.svg)](https://github.com/TRIQS/minipole_interface/actions?query=workflow%3Abuild)

# minipole_interface

*TRIQS interface to the [MiniPole](https://github.com/Green-Phys/MiniPole)
minimal-pole-method analytic continuation package.*

`minipole_interface` lets you call MiniPole on TRIQS Green's-function
containers — `Gf` / `BlockGf` on `MeshImFreq`, `MeshDLRImFreq`, `MeshDLRImTime`,
or DLR coefficient meshes — and on user-supplied analytic real-frequency
expressions, without writing the array-shuffling glue yourself. All four entry
points return a `PoleResult` carrying the pole locations, weights, and
ready-made evaluators (`evaluate(z)`, `to_gf_imfreq`, `to_gf_refreq`).

## Upstream and citation

The Minimal Pole Method (MPM) algorithm itself is **not** implemented here. It
lives in the [Green-Phys/MiniPole](https://github.com/Green-Phys/MiniPole)
package, which we pin to `mini_pole==0.7`. This repository is purely the TRIQS
adapter layer.

If you use this interface, please cite the upstream papers:

* L. Zhang and E. Gull, *Minimal pole representation and controlled analytic
  continuation of matrix-valued correlation functions*,
  [Phys. Rev. B **110**, 235131 (2024)](https://doi.org/10.1103/PhysRevB.110.235131)
* L. Zhang, Y. Yu, and E. Gull, *Minimal pole representation and analytic
  continuation of matrix-valued correlation functions*,
  [Phys. Rev. B **110**, 035154 (2024)](https://doi.org/10.1103/PhysRevB.110.035154)
* L. Zhang and E. Gull, *Minimal pole representation for spectral functions*,
  [J. Chem. Phys. **162**, 214111 (2025)](https://doi.org/10.1063/5.0273073)

A reference back to `triqs/minipole_interface` is appreciated when you also
want to acknowledge the TRIQS-side wrapper.

## Install

This is a python-only TRIQS app. Install into the same environment as your
TRIQS install. Two paths are supported; pick whichever fits your workflow:

**Recommended — pip:**

```bash
git clone https://github.com/TRIQS/minipole_interface
pip install -e ./minipole_interface
```

Drop `-e` for a non-editable install. `pip` pulls in `mini_pole==0.7` and
`kneed` automatically.

**CMake (equal path; needed if you want the lmod modulefile, the `vars.sh`
shell script, or the `find_package(minipole_interface)` config files):**

```bash
git clone https://github.com/TRIQS/minipole_interface minipole_interface.src
cmake -S minipole_interface.src -B build -GNinja
ninja -C build && ninja -C build install
```

The CMake path enforces that the major and minor version of
`minipole_interface` match your installed TRIQS library.

## Quickstart

```python
from triqs.gfs import Gf, MeshImFreq, MeshReFreq
from minipole_interface import fit_poles_matsubara

g = Gf(mesh=MeshImFreq(beta=10.0, statistic='Fermion', n_iw=200), target_shape=(1, 1))
for iw in g.mesh:
    g[iw] = 1.0 / (complex(iw) - 0.3)        # single pole at omega = 0.3

res = fit_poles_matsubara(g, M=1)
print(res.pole_location, res.pole_weight[0, 0, 0])

g_re = res.to_gf_refreq(MeshReFreq(-2.0, 2.0, 401), eta=1e-3)
```

For a full Matsubara → spectral-function example and a DLR-input variant, see
the tutorial notebooks in the documentation.

## Entry points

| Function | Input | Wraps | Use when … |
| --- | --- | --- | --- |
| `fit_poles_matsubara` | `Gf` / `BlockGf` on `MeshImFreq` | `mini_pole.MiniPole` | you have dense Matsubara samples |
| `fit_poles_dlr` | `Gf` / `BlockGf` on `MeshDLR*` | `mini_pole.MiniPoleDLR` | you have a compact DLR representation |
| `fit_poles_rf` | callable(s) `G_ij(z)` analytic in upper half-plane | `mini_pole.MiniPoleRf` | you have an analytic real-frequency expression |
| `refine_poles` | existing `(A_l, x_l)` or a `PoleResult` | `mini_pole.MiniPoleRfDPR` | you want to refine / compress an existing pole set |

## Documentation

Full API reference and tutorials:
[https://triqs.github.io/minipole_interface](https://triqs.github.io/minipole_interface)

## License

`minipole_interface` is published under the GNU General Public License v3 —
see [`LICENSE.txt`](LICENSE.txt).
