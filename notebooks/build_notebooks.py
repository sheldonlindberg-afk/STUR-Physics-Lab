#!/usr/bin/env python3
"""Generate and execute the study notebooks. Run from the repository root:
    python3 notebooks/build_notebooks.py               # all
    python3 notebooks/build_notebooks.py 05_...ipynb   # only the named ones
"""
import os
import nbformat as nbf
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
SETUP = ("import os, sys\n"
         "sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))\n"
         "import numpy as np")


def nb(cells):
    book = nbf.v4.new_notebook()
    book.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    book.cells = [nbf.v4.new_markdown_cell(c[1]) if c[0] == "md" else nbf.v4.new_code_cell(c[1])
                  for c in cells]
    return book


BOOKS = {}

BOOKS["01_tegr_classic_tests.ipynb"] = nb([
("md", r"""# 1. Teleparallel gravity and the classic tests of GR

**Prerequisites:** tetrads and the metric $g_{\mu\nu}=\eta_{ab}e^a{}_\mu e^b{}_\nu$; the
Schwarzschild solution and geodesics at the level of Carroll, *Spacetime and Geometry*,
ch. 5. **Reference:** Aldrovandi & Pereira, *Teleparallel Gravity* (Springer, 2013).

In TEGR the connection is the Weitzenböck connection $\Gamma^\rho{}_{\mu\nu}=e_a{}^\rho\partial_\mu e^a{}_\nu$:
curvature-free, with gravity carried by torsion
$T^\rho{}_{\mu\nu}=\Gamma^\rho{}_{\nu\mu}-\Gamma^\rho{}_{\mu\nu}$. The action
$S=(c^4/16\pi G)\int e\,\mathbb{T}\,d^4x$ differs from Einstein–Hilbert by a boundary
term, $\mathbb{T}=-R+\text{divergence}$, so the field equations are GR's.

This notebook derives the static spherical solution **from the TEGR field equations**
and then computes the four classic tests from its geodesics. No curvature is used."""),
("code", SETUP + "\nimport stur_tegr_gr as F"),
("md", r"""## Field equations for a static spherical tetrad
Take $e^0=e^{A(r)}dt$, $e^1=e^{B(r)}dr$ and the standard angular legs. The TEGR field
equations reduce to ODEs in $A$ and $B$:"""),
("code", "eqs = F.tegr_spherical_equations()\nfor e in eqs[:3]:\n    display(e)"),
("md", r"""Two combinations give $2rA'=e^{2B}-1$ and $2rB'=1-e^{2B}$. With $y=e^{-B}$ these
integrate to $e^{-2B}=1-r_s/r$ and $A=-B$: Schwarzschild, uniquely (Birkhoff)."""),
("code", "sol = F.solve_spherical()\nsol[-1]"),
("md", r"""## The classic tests
Each number below is a numerical geodesic integral of that metric (arbitrary-precision
quadrature with `mpmath`), not the textbook closed form."""),
("code", """GM_SUN = 1.32712440018e20          # m^3/s^2
R_SUN = 6.957e8                     # m
a_merc, e_merc = 5.7909e10, 0.2056
T_merc_days = 87.969
dphi = F.perihelion_shift(GM_SUN, a_merc, e_merc)           # rad per orbit
arcsec_per_century = dphi * (36525 / T_merc_days) * 180 / np.pi * 3600
print(f"Mercury perihelion: {arcsec_per_century:.2f} arcsec/century (GR part of the observed value: 42.98)")
defl = F.light_deflection(GM_SUN, R_SUN) * 180 / np.pi * 3600
print(f"Light deflection at the solar limb: {defl:.4f} arcsec (VLBI: 1.7512)")
print("PPN gamma:", F.ppn_gamma())
net, grav = F.gps_offset_us_per_day()
print(f"GPS clocks: net {net:.2f} us/day, gravitational part {grav:.2f} us/day")"""),
("md", r"""## Exercises
1. Compare `perihelion_shift` with the leading-order formula
   $\Delta\phi=6\pi GM/[c^2a(1-e^2)]$. At what eccentricity or semi-major axis does the
   difference first exceed $10^{-6}$ of the effect?
2. Newtonian gravity gives half the light deflection. In the tetrad language, which leg,
   $e^0$ or $e^1$, supplies each half? (Hint: set $B=0$ by hand and recompute.)
3. Split `gps_offset_us_per_day` into its special- and general-relativistic parts. Find the
   orbital radius at which they cancel.
4. Show that $\mathbb{T}=-R+\nabla_\mu(\ldots)$ for the spherical tetrad, using
   `stur_tegr.identity_check` as a numerical check of your algebra."""),
])

BOOKS["02_complementarity_and_decoherence.ipynb"] = nb([
("md", r"""# 2. Which-path records, complementarity and decoherence

**Prerequisites:** density matrices, partial trace, coherent and thermal states of a
harmonic oscillator. **References:** Englert, PRL 77, 2154 (1996); Zurek, Rev. Mod. Phys.
75, 715 (2003).

A particle in two paths couples to an environment that ends in $|E_1\rangle$ or
$|E_2\rangle$. The reduced density matrix's off-diagonal element is multiplied by
$\langle E_2|E_1\rangle$, so the fringe visibility is $V=|\langle E_1|E_2\rangle|$ and the
which-path distinguishability is $D=\sqrt{1-V^2}$ for pure environment states."""),
("code", SETUP + "\nimport stur_measurement as M, stur_lab_test as L"),
("md", "## Englert's relation $V^2+D^2=1$ for a pure detector"),
("code", """for theta in np.linspace(0, np.pi / 2, 7):
    y, P, V, D = M.double_slit(theta)
    print(f"theta = {theta:5.3f}   V = {V:.4f}   D = {D:.4f}   V^2 + D^2 = {V**2 + D**2:.6f}")"""),
("md", r"""## A thermal environment: visibility counts exchanged quanta
A trapped ion's motional mode, thermal with occupation $\bar n$, is displaced by
$\pm\alpha$ depending on the path. Then $V=\langle(-1)^{\Delta N}\rangle$ and, for this
displaced-oscillator model, $-\ln V=2\,\mathrm{Var}(\Delta N)$: heat destroys more contrast."""),
("code", """alpha = 0.5
for nbar in (0.1, 0.5, 1, 2, 5):
    V, mean, var = L.fock_space(alpha, nbar)
    print(f"nbar = {nbar:4}   V = {V:.3f}   -ln V = {-np.log(V):.4f}   2 Var(dN) = {2*var:.4f}")"""),
("md", r"""## Exercises
1. Derive $V=\exp[-2|\alpha|^2(2\bar n+1)]$ for the displaced thermal state, and check it
   against `L.fock_space`.
2. Prove $-\ln V=2\,\mathrm{Var}(\Delta N)$ for this model. Does it hold for a general
   environment? Find a counterexample with a two-level detector.
3. For a mixed detector state, $V^2+D^2\le 1$. Construct a mixed environment with
   $V^2+D^2<1$, compute both sides, and identify where the missing information went.
4. Decoherence explains the loss of interference, not the selection of one outcome.
   State precisely what the reduced density matrix does and does not tell you."""),
])

BOOKS["03_gravity_mediated_entanglement.ipynb"] = nb([
("md", r"""# 3. Gravity-mediated entanglement of two masses

**Prerequisites:** two-qubit states, concurrence and negativity; Newtonian gravity as a
static potential. **References:** Bose et al., PRL 119, 240401 (2017); Marletto & Vedral,
PRL 119, 240402 (2017).

Two masses $m$, each split by $\Delta x$ and held for time $\tau$, at closest separation
`gap`. If each branch pair $(i,j)$ feels its own Newtonian potential, it picks up
$\phi_{ij}=Gm^2\tau/(\hbar d_{ij})$, and the state becomes entangled when
$\Delta\phi=\phi_{00}+\phi_{11}-\phi_{01}-\phi_{10}\neq0$. A classical gravitational field
cannot generate this entanglement (LOCC)."""),
("code", SETUP + "\nimport stur_gravity_entanglement as g"),
("code", """p = dict(g.BASE)
print("parameters:", p)
ph = g.phases(**p)
print("branch phases (rad):\\n", ph)
print(f"entangling phase = {g.entangling_phase(ph):.4f} rad")
print(f"concurrence      = {g.concurrence_pure(ph):.4f}")"""),
("md", "## Scaling with mass and separation"),
("code", """for m in (1e-15, 3e-15, 1e-14, 3e-14):
    q = dict(p, m=m)
    print(f"m = {m:.0e} kg   radius = {g.radius(m)*1e6:6.2f} um   dphi = {g.entangling_phase(g.phases(**q)):+.4f} rad")"""),
("md", r"""## Decoherence from residual gas
Each gas collision that resolves the split destroys the coherence. The rate below is a
kinetic-theory derivation, not an interpolation."""),
("code", """for P in (1e-13, 1e-14, 1e-15):
    G = g.gas_decoherence_rate(p['m'], P, 0.15)
    print(f"P = {P:.0e} Pa   Gamma = {G:.3e} /s   Gamma*tau = {G*p['tau']:.3f}")"""),
("md", r"""## Exercises
1. Derive the entangling phase for the linear geometry to leading order in
   $\Delta x/\text{gap}$. How does it scale with $\Delta x$?
2. The Casimir–Polder interaction must stay below gravity. Using
   `g.casimir_vs_gravity_gap`, find the smallest safe gap at $m=10^{-14}$ kg.
3. Include the dephasing $\Gamma\tau$ through `g.state(ph, gamma_tau)` and find the
   pressure at which the negativity vanishes.
4. Why does observing entanglement rule out classical gravity, and why does it *not*
   by itself establish the existence of gravitons? (See the LOCC argument and its
   loopholes.)"""),
])

BOOKS["04_area_law.ipynb"] = nb([
("md", r"""# 4. The entanglement area law (Srednicki's method)

**Prerequisites:** Gaussian states, symplectic eigenvalues, partial-wave decomposition of
a free scalar field. **Reference:** M. Srednicki, PRL 71, 666 (1993).

Discretize a free massless scalar on radial shells of spacing $a$ and trace out the
region outside radius $R=(n+\tfrac12)a$. Each partial wave $\ell$ is a chain of coupled
oscillators; its entropy follows from the symplectic eigenvalues of $XP$ restricted to the
inside. Summing over $\ell$ gives $S\approx c_s(R/a)^2$, with $c_s\approx0.30$."""),
("code", SETUP + "\nimport stur_unification as U"),
("code", """N = 40
rows = []
for n in (6, 8, 10, 12, 14):
    S = U.srednicki(N=N, n=n, lmax=600)
    R = n + 0.5
    rows.append((R, S))
    print(f"R/a = {R:5.1f}   S = {S:8.3f}   S/(R/a)^2 = {S/R**2:.4f}")
R, S = np.array(rows).T
c = np.polyfit(R**2, S, 1)[0]
print(f"fitted slope c_s = {c:.3f}  (Srednicki: 0.30; the repository's converged value: 0.3046)")"""),
("md", r"""## Exercises
1. Show that the entropy of a single partial wave is finite but the sum over $\ell$ needs a
   cutoff. Where does the $\ell$ cutoff enter `U.srednicki`?
2. Vary the outer size $N$ and confirm the coefficient is insensitive to it once
   $N\gg n$.
3. Add a mass term. How does the area coefficient change, and when do you see the
   $\ln(R)$ correction?
4. Jacobson's argument identifies $1/(4G\hbar)$ with the entanglement per area. Explain
   why $c_s$ being regulator-dependent makes this an identification, not a prediction
   of $G$."""),
])


BOOKS["05_teleparallel_3d_quantum.ipynb"] = nb([
("md", r"""# 5. Teleparallel gravity in 3D and the Ponzano–Regge amplitude

**Prerequisites:** notebook 1; SU(2) recoupling (Clebsch–Gordan and 6j symbols) at the
level of a quantum-mechanics course. **References:** G. Ponzano and T. Regge (1968);
J. Roberts, Geom. Topol. 3, 21 (1999); C. Delcamp, L. Freidel and F. Girelli,
[arXiv:1803.03246](https://arxiv.org/abs/1803.03246); and, for context,
[QUANTUM_TEGR.md](../QUANTUM_TEGR.md).

Quantum gravity is solved in one case: three spacetime dimensions. 3D Euclidean gravity
is a BF theory, $S=\frac{1}{16\pi G}\int \mathrm{tr}(e\wedge F(\omega))$, with two
equations of motion:

- **flatness**, $F(\omega)=0$;
- **zero torsion**, $d_\omega e=0$.

It has no local degrees of freedom. The standard loop quantization imposes the torsion
(Gauss) constraint first and flatness last. The *dual* quantization imposes flatness
first, $\omega$ pure gauge, so gravity is carried by the triad and its torsion: the
teleparallel choice. Every result in this notebook is known. The aim is to compute them,
not to add to them."""),
("code", SETUP + "\nfrom fractions import Fraction as F\nimport stur_tegr3d as U"),
("md", r"""## The TEGR identity holds in 3D
As in 4D, $\mathbb{T}=-R+B$ with $B$ a total divergence, so 3D TEGR and 3D GR differ by a
boundary term. With a rational tetrad the check is exact:"""),
("code", """for d, T, R in U.identity_3d():
    print(f"T = {T:+.6e}   R = {R:+.6e}   T + R - B = {d}  (exact)")"""),
("md", r"""## The amplitude: 6j symbols
The Ponzano–Regge model cuts space into tetrahedra, labels each edge with a spin $j$ (its
length is $j+\tfrac12$ in Planck units) and assigns each tetrahedron a Wigner 6j symbol.
`U.sixj` computes it exactly from Racah's formula."""),
("code", """print("{1 1 1; 1 1 1} =", U.sixj(1, 1, 1, 1, 1, 1), "(exact 1/6)")
print("worst difference from sympy over 30 cases:", U.check_against_sympy())"""),
("md", r"""## The classical limit is the Regge action
For large spins,
$$\begin{Bmatrix} j_1 & j_2 & j_3\\ j_4 & j_5 & j_6\end{Bmatrix}\approx
\frac{1}{\sqrt{12\pi V}}\cos\Big(\sum_e (j_e+\tfrac12)\,\theta_e+\frac{\pi}{4}\Big),$$
with $V$ the volume and $\theta_e$ the exterior dihedral angles of the tetrahedron.
$\sum_e l_e\theta_e$ is the Regge action, discrete 3D gravity. So the quantum amplitude
oscillates with the classical action, as a WKB wavefunction does."""),
("code", """for k, ex, a, err in U.pr_scan():
    js = [k * b for b in (5, 6, 7, 6, 5, 6)]
    print(f"j = {js}: exact {ex:+.6e}  asymptotic {a:+.6e}  |diff|/envelope {err:.1e}")"""),
("md", r"""## No local degrees of freedom: the 2–3 move
Two tetrahedra glued on a face can be re-cut into three sharing an edge. The amplitude is
unchanged because of the Biedenharn–Elliott identity, so it does not depend on the
triangulation. This is the quantum form of "3D gravity has no local degrees of
freedom". Orthogonality of the 6j symbols does the same for the 1–4 move, up to a
divergent factor that has to be regularized."""),
("code", """worst, hits = U.be_check()
print(f"Biedenharn-Elliott: {hits} random spin sets, worst |LHS - RHS| = {worst:.1e}")
ps, M = U.orthogonality(1, F(3, 2), 1, F(3, 2))
print("orthogonality matrix:\\n", np.round(M, 12))"""),
("md", r"""## Exercises
1. **Schläfli's identity.** Show numerically, with `U.tetrahedron`, that
   $\sum_e l_e\, d\theta_e=0$ under a small change of edge lengths. Use it to prove that
   $\partial S_{\rm Regge}/\partial l_e=\theta_e$: the Regge equations say the deficit
   angles vanish, i.e. space is flat.
2. **Non-Euclidean tetrahedra.** Find admissible spins for which `U.tetrahedron` returns
   `None` (no Euclidean tetrahedron exists). Show that the 6j symbol there decays
   exponentially with $k$ instead of oscillating. This is tunnelling.
3. **Two orderings.** Delcamp, Freidel and Girelli (1803.03246) impose flatness first.
   Read their section on the dual vacuum. What plays the role of the spin-network basis,
   and what replaces the SU(2) holonomy as the basic variable?
4. **What doesn't carry over.** In 3D both quantizations describe a theory without local
   degrees of freedom. Explain why that makes 3D a poor guide to whether TEGR and GR
   differ as quantum theories in 4D, where gravitons propagate."""),
])


def main(names=None):
    for name, book in BOOKS.items():
        if names and name not in names:
            continue
        path = os.path.join(HERE, name)
        NotebookClient(book, timeout=900, kernel_name="python3",
                       resources={"metadata": {"path": HERE}}).execute()
        nbf.write(book, path)
        print("wrote", path)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:] or None)          # e.g. python3 notebooks/build_notebooks.py 05_teleparallel_3d_quantum.ipynb
