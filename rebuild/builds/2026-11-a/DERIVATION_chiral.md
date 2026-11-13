# DERIVATION: chiral (SPEC.md sections 0 and 3)

Postulates used (SPEC.md section 3 unless stated):
- (P1) linear sigma model V(phi) = (lam/4)(phi.phi - v^2)^2 - H sigma, phi = (sigma, pi1, pi2, pi3);
- (P2) GMOR identification f_pi = <sigma>, H f_pi = (m_u + m_d)|<qbar q>|, |<qbar q>| = cond13^3;
- (P3, QUOTED) O(p^4) ChPT: M_pi^2 = M^2 [1 - M^2 lbar3/(32 pi^2 F^2)], M^2 = 2 mhat Sigma / F^2,
  F = f_pi/(F_pi/F), Sigma = cond13^3 (Gasser & Leutwyler, Ann. Phys. 158 (1984) 142; FLAG conventions);
- (P4) boson exchange gives V(q) proportional to 1/(q^2 + m^2), normalized by (lap - m^2) V = -delta^3;
- (P5) Pauli matrices for spin; S12 = 3 (s1.qhat)(s2.qhat) - s1.s2;
- (P6) Goldberger-Treiman g_piNN = g_A M_N / f_pi, derived below from PCAC (pion-pole dominance).
SPEC.md section 0: only `chpt_mpi` may be quoted; everything else here is derived.
Numerics use toolkit (hessian, eigvalsh, bisect, trapezoid) only.

Units: sigma-model functions are in arbitrary consistent units; GMOR/ChPT in GeV (inputs.py).

---

## 1. `goldstone_count(lam, v)` (H = 0)

**Vacuum.** V depends on phi only through rho^2 = phi.phi (O(4) invariance). Along any ray
phi = rho n (|n| = 1):

    dV/drho = lam rho (rho^2 - v^2)  (H = 0),

zero at rho = 0 and rho = v. d^2V/drho^2 = lam (3 rho^2 - v^2): -lam v^2 < 0 at rho = 0 (a maximum,
for lam > 0) and 2 lam v^2 > 0 at rho = v. V(v n) = 0 < V(0) = lam v^4/4, so the true vacuum is
the sphere |phi| = v. The code finds rho0 by `toolkit.bisect` on dV/drho on [v/2, 2v]
(dV/drho(v/2) < 0 < dV/drho(2v)), along n = (1,0,0,0) (any n is equivalent by O(4)).

**Hessian.** d^2V/dphi_i dphi_j = lam[(phi^2 - v^2) delta_ij + 2 phi_i phi_j]. At phi0 = v n:
M_ij = 2 lam v^2 n_i n_j, a rank-1 projector: eigenvalue 2 lam v^2 (the sigma, radial) once and
0 three times (the directions tangent to the vacuum sphere S^3 = O(4)/O(3)). Goldstone count =
dim O(4) - dim O(3) = 6 - 3 = 3.

**Numerics.** `toolkit.hessian` with an absolute step h (QUESTIONS toolkit 1). Because V is a
quartic polynomial, the central differences terminate:

    D_ii(h) = f_ii + (h^2/12) f_iiii           (f^(6) = 0),
    D_ij(h) = f_ij + (h^2/6)(f_iiij + f_ijjj),

so the Richardson combination [4 D(h/2) - D(h)]/3 is EXACT up to rounding. The step is then
chosen large for low rounding error: h = s/2^6 with s = max(|phi0|, v) (a power of two times the
field scale, so the result scales with the field). Zero modes: eigenvalues (toolkit.eigvalsh)
with |e| <= 1e-9 max|e|. The code also checks that the vacuum is a minimum (no eigenvalue below
-1e-9 max|e|), and raises otherwise.

**Second route.** (a) Closed form: 2 lam v^2 once, 0 three times. (b) Repeat at a generic
direction n (all four components nonzero): count unchanged (symmetry argument). (c) Count at the
false vacuum phi = 0: four eigenvalues -lam v^2, no zero mode (so zero modes are a property of
the true vacuum, not of the model).

---

## 2. `sigma_model_vacuum(lam, v, H)` -> (sigma0, m_pi^2)

**Vacuum.** With H != 0 the term -H sigma picks the direction n = sign(H) e_sigma (for fixed
|phi|, -H sigma is minimized when phi is aligned with sign(H) e_sigma), so pi = 0 and sigma0 solves

    g(sigma) = dV/dsigma = lam sigma (sigma^2 - v^2) - H = 0.            (1)

For H > 0, the global minimum has sigma0 > v: g(v) = -H < 0 and, with b = v + (H/lam)^(1/3),
g(b) = lam b (b - v)(b + v) - H >= lam (b - v)^3 - H = 0, since b (b + v) >= (b - v)^2
(strict for v > 0, so g(b) > 0). The root in [v, b] is unique (g' = lam(3 sigma^2 - v^2) > 0 there)
and is found with `toolkit.bisect`. The other roots of (1) lie at sigma < 0 (or not at all), where
-H sigma > 0 raises V: they are a saddle/maximum. H < 0 is the mirror image (sigma -> -sigma);
H = 0 gives sigma0 = v.

**Pion mass.** At (sigma0, 0, 0, 0), from the Hessian formula of section 1:

    M_sigma sigma = lam (3 sigma0^2 - v^2),   M_pi_a pi_a = lam (sigma0^2 - v^2),   off-diagonal 0.

Using (1), lam(sigma0^2 - v^2) = H/sigma0, so

    m_pi^2 = H / sigma0,    m_sigma^2 = 2 lam sigma0^2 + H/sigma0 > m_pi^2.     (2)

The code obtains m_pi^2 NOT from (2) but from the Richardson-extrapolated `toolkit.hessian` at the
bisected vacuum, diagonalized with `toolkit.eigvalsh`: the three lowest eigenvalues are the pions
(by (2) they are always below m_sigma^2); their mean is returned (their spread is printed in the
self-check). Rounding error ~ eps |V| / h^2, i.e. ~1e-12 relative for the tested parameters.

**Second route.** (2) itself (the Ward identity of the explicitly broken symmetry: the pion
curvature equals the tilt H divided by the vev); and the limit H -> 0 reproduces three zero modes.

---

## 3. `gmor_mpi(mq_sum, cond13, fpi)`

From (2) with sigma0 = f_pi and H = (m_u + m_d) Sigma / f_pi, Sigma = cond13^3 (P2):

    m_pi^2 = H/f_pi = (m_u + m_d) cond13^3 / f_pi^2,   m_pi = sqrt(mq_sum cond13^3) / fpi.   (3)

Scaling: m_pi ~ sqrt(m_q), ~ 1/f_pi (exact).

**Second route.** Build an explicit sigma model whose vacuum IS f_pi: for any lam > 0 choose
v^2 = f_pi^2 - H/(lam f_pi) (from (1) with sigma0 = f_pi), solve with `sigma_model_vacuum`,
and compare sqrt(m_pi^2) with (3) for several lam (lam-independence is the content of GMOR).

---

## 4. `chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi)`  (QUOTED, P3)

    F = fpi/fpi_over_F,  Sigma = cond13^3,  M^2 = 2 m_ud Sigma / F^2,
    x = M^2 lbar3 / (32 pi^2 F^2),  M_pi = M sqrt(1 - x).

m_ud is mhat = (m_u + m_d)/2 (FLAG). Raises if x >= 1 (outside the expansion).
Not derived: the one-loop chiral log and the definition of lbar3 are taken from Gasser-Leutwyler.

**Second route / limits.** lbar3 = 0 gives M = sqrt(2 mhat Sigma)/F, which is (3) with
m_u + m_d = 2 mhat and f_pi -> F (the chiral-limit decay constant): the LO term is the sigma-model
GMOR result. lbar3 > 0 lowers M_pi.

**Uncertainty** (self-check). Linear propagation in logarithmic derivatives, uncorrelated inputs
(m_ud, cond13, F_pi/F, lbar3; F_PI has no quoted error). With L = ln M_pi^2 = ln M^2 + ln(1 - x),
d ln F = -d ln r (r = F_pi/F), d ln M^2 = d ln m + 3 d ln c + 2 d ln r,
d ln x = d ln M^2 + 2 d ln r + d ln lbar3:

    dL = (1 - k)(dm/m + 3 dc/c) + (2 - 4k) dr/r - k dl/l,     k = x/(1 - x),
    d M_pi / M_pi = dL / 2.

Cross-checked by central finite differences in the self-check. For GMOR (3) similarly
d m_pi/m_pi = (1/2) sqrt((d mq/mq)^2 + (3 dc/c)^2).

---

## 5. `yukawa(r, m)`

Solve (lap - m^2) V = -delta^3 by Fourier transform: V(q) = 1/(q^2 + m^2) (unit strength), and

    V(r) = int d^3q/(2pi)^3 e^{iq.r}/(q^2 + m^2)
         = (1/(2 pi^2 r)) int_0^oo q sin(q r)/(q^2 + m^2) dq
         = (1/(2 pi^2 r)) (pi/2) e^{-m r} = e^{-m r} / (4 pi r).                       (4)

(The q-integral by closing in the upper half plane on the pole q = i m:
int_-oo^oo q e^{iqr}/(q^2+m^2) dq = 2 pi i (i m e^{-mr})/(2 i m) = i pi e^{-mr}; take Im/2.)

Direct check in position space: for r > 0, with u = r V = e^{-mr}/(4 pi), lap V = u''/r = m^2 V,
so (lap - m^2)V = 0; the flux through a small sphere, -4 pi r^2 V'(r) = e^{-mr}(1 + m r) -> 1,
gives the -delta^3 with unit weight. m = 0: V = 1/(4 pi r) (Coulomb/Newton).

**Second route.** The inverse direction of (4) numerically: for q > 0,
int d^3r V(r) e^{-iq.r} = (4 pi/q) int_0^oo r V(r) sin(q r) dr = (1/q) int_0^oo e^{-mr} sin(qr) dr,
evaluated with `toolkit.trapezoid` on [0, 40/m] and compared with 1/(q^2 + m^2); plus a
finite-difference Laplacian and the flux.

---

## 6. `tensor_identity_residual(q)`

Spin space C^2 (x) C^2 (4x4). s1_i = sigma_i (x) 1, s2_i = 1 (x) sigma_i, Kronecker products
formed explicitly from the Pauli matrices (complex 2x2). With |q| > 0, qhat = q/|q|:

    A = (s1.q)(s2.q),    B = (q^2/3)(s1.s2 + S12),   S12 = 3 (s1.qhat)(s2.qhat) - s1.s2.

Algebraically B = (q^2/3) 3 (s1.qhat)(s2.qhat) = A (this is why one-pion exchange, whose vertex
gives (s1.q)(s2.q)/(q^2+m^2), splits into a central (s1.s2) piece and a tensor S12 piece with
equal weight q^2/3). The code does NOT use this: it forms all three 4x4 matrix products numerically
and returns max_ij |A_ij - B_ij|. q = 0: both sides are the zero matrix (A = 0 exactly; B has the
prefactor q^2 = 0), residual 0.

**Second route.** Spectral checks with the same explicit matrices: the complex Hermitian S12 is
embedded as the real symmetric 8x8 [[Re, -Im], [Im, Re]] (each eigenvalue doubled) and
diagonalized with `toolkit.eigvalsh`. Expected (closed form, qhat = z): on the triplet,
s1.s2 = 1 and s1z s2z = +1 (M = +-1) or -1 (M = 0), so S12 = 2, 2, -4; on the singlet
s1.s2 = -3, s1z s2z = -1, S12 = 0. Spectrum {-4, 0, 2, 2} for every qhat (rotation invariance),
trace 0 (the tensor force averages to zero), s1.s2 spectrum {-3, 1, 1, 1}, and the operator
identity S12^2 = 6 + 2 s1.s2 - 2 S12.

---

## 7. `goldberger_treiman(gA, MN, fpi)`

**Derivation (PCAC, pion-pole dominance).** Nucleon matrix element of the isovector axial current,
q = p' - p:

    <N(p')| A_mu^a |N(p)> = ubar(p') [ G_A(q^2) gamma_mu gamma5 + G_P(q^2) q_mu gamma5 ] (tau^a/2) u(p).

Contract with q^mu and use the Dirac equation (pslash u = M u, ubar' pslash' = M ubar'):
ubar' qslash gamma5 u = ubar'(pslash' gamma5 + gamma5 pslash) u = 2 M_N ubar' gamma5 u. So

    <N'| d.A^a |N> ∝ [2 M_N G_A(q^2) + q^2 G_P(q^2)] ubar' gamma5 (tau^a/2) u.

Chiral limit (m_pi -> 0): d.A = 0, so G_P = -2 M_N G_A/q^2 has a massless pole: the Goldstone
pion. Its residue is fixed by the pion's two couplings: <0|A_mu^a|pi^b(q)> = i f_pi q_mu delta^ab
(this defines f_pi; in the sigma model A_mu^a contains f_pi d_mu pi^a with f_pi = <sigma>), and
the pi N N vertex g_piNN ubar' i gamma5 tau^a u; the pole term is then
G_P q_mu gamma5 (tau/2) = (f_pi q_mu)(1/q^2)(2 g_piNN) gamma5 (tau/2) up to the common phase
convention, i.e. q^2 G_P -> -2 f_pi g_piNN at q^2 -> 0 (sign fixed by the conservation condition).
Matching residues: 2 M_N G_A(0) = 2 f_pi g_piNN:

    g_piNN = g_A M_N / f_pi,   g_A = G_A(0).                                           (5)

Off the chiral limit the same holds up to O(m_pi^2) (the Goldberger-Treiman discrepancy), which
this export does not include. The overall phase of the pion-pole term is convention; the magnitude
is fixed by residue matching. Tagged derived (PCAC sketch above).

**Second route.** Gell-Mann-Levy sigma model with nucleons (consistent with P1):
L = psibar i dslash psi - g psibar (sigma + i gamma5 tau.pi) psi. Then M_N = g <sigma> = g f_pi
and, at tree level, g_A = 1 and g_piNN = g, so g_piNN = M_N/f_pi = g_A M_N/f_pi with g_A = 1:
(5) at g_A = 1. The self-check also prints (5) from inputs against inputs.G_PINN_EMP.
