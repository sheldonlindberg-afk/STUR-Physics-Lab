# DERIVATION: stage `chiral` (build 2026-11-b)

Postulates: SPEC.md section 3. Numerics: `toolkit` (SPEC.md section 1). Measured numbers: `inputs.py` only
(used in the `__main__` self-check, never inside an export, since every export takes its numbers as arguments).
Written before the code. Units: natural units, GeV, for the masses; `yukawa` is in (length)^-1 for r in length
and m in inverse length.

Notation: phi = (sigma, pi_1, pi_2, pi_3), phi^2 = phi.phi, lambda > 0, v > 0.

---------------------------------------------------------------------------------------------------------------

## 1. `goldstone_count(lam, v)`: zero modes of the O(4) model at its vacuum, H = 0

**Postulate.** V = (lambda/4)(phi^2 - v^2)^2 (SPEC section 3 with H = 0).

**Vacuum.** V >= 0 with equality iff phi^2 = v^2: the vacuum manifold is the sphere S^3 of radius v. Gradient
dV/dphi_i = lambda (phi^2 - v^2) phi_i. By O(4) invariance every point of S^3 is equivalent; take
phi_0 = (v, 0, 0, 0) (this *defines* the sigma direction).

**Hessian.**

    d^2V / dphi_i dphi_j = lambda (phi^2 - v^2) delta_ij + 2 lambda phi_i phi_j .

At phi_0: M^2 = diag(2 lambda v^2, 0, 0, 0). One massive mode (sigma, m_sigma^2 = 2 lambda v^2) and three
zero modes (the pions).

**Implementation (required by contract.CONNECTIONS T-chiral).** The Hessian is taken numerically with
`toolkit.hessian` at phi_0 and diagonalized with `toolkit.eigvalsh`; the count is the number of eigenvalues with
|e| < tol * max|e|.
- Step: the coordinates are O(v), so h = 1e-4 v (SPEC section 1: the caller scales h).
- Truncation error of the 3-point stencil on a quartic: (h^2/12) d^4V/dpi^4 = (h^2/12)(6 lambda) =
  lambda h^2 / 2 = 5e-9 lambda v^2, i.e. 2.5e-9 relative to m_sigma^2. (Off-diagonal entries vanish by the
  reflection symmetries pi_i -> -pi_i, which the 4-point stencil respects exactly.)
- Tolerance: tol = 1e-6, three orders above the truncation error and six below the massive mode.

**Second route (group theory).** Goldstone's theorem: the number of zero modes is dim G - dim H_unbroken. O(4)
has 4*3/2 = 6 generators; the stabilizer of phi_0 is O(3) acting on (pi_1, pi_2, pi_3), 3 generators. 6 - 3 = 3.
Explicitly the broken generators are the rotations in the (sigma, pi_a) planes, delta phi = eps_a e_a, which are
exactly the three flat directions of the Hessian. `__main__` prints the generator count, computed by counting
the antisymmetric 4x4 generators J_ij that annihilate phi_0, next to the Hessian count, and the analytic Hessian
eigenvalues next to the numerical ones.

---------------------------------------------------------------------------------------------------------------

## 2. `sigma_model_vacuum(lam, v, H)` -> (sigma0, mpi2)

**Postulate.** V = (lambda/4)(phi^2 - v^2)^2 - H sigma.

**Stationarity.** dV/dpi_a = lambda (phi^2 - v^2) pi_a = 0 and dV/dsigma = lambda (phi^2 - v^2) sigma - H = 0.
For H != 0 the second equation forbids phi^2 = v^2, so the first forces pi_a = 0. Then

    g(sigma) := lambda sigma (sigma^2 - v^2) = H.                                   (2.1)

**Which root is the vacuum (H > 0).** V(sigma, 0) - V(-sigma, 0) = -2 H sigma, so the global minimum has
sigma > 0. On 0 < sigma <= v, g <= 0 < H: no root. On sigma > v, g is strictly increasing (g' = lambda (3 sigma^2
- v^2) > 0) from 0 to infinity: exactly one root, sigma0 > v. It is the only stationary point with sigma > 0, and
the global minimum exists (V -> +infinity), so it is the vacuum. For H < 0 the map sigma -> -sigma gives
sigma0(H) = -sigma0(-H). For H = 0, sigma0 = v (the section 1 choice).

**Bracket for the root.** Write sigma = v + d, d > 0: g = lambda (v + d) d (2v + d) >= lambda d^3. So
d* = (H/lambda)^(1/3) gives g(v + d*) >= H, and g(v) = 0 < H. The root lies in [v, v + (H/lambda)^(1/3)] and is
found with `toolkit.bisect` (to floating-point resolution, so the residual of (2.1) is ~1e-16 scale).

**Masses at the vacuum.** From the Hessian formula of section 1 (the -H sigma term is linear and drops out):

    m_pi^2    = lambda (sigma0^2 - v^2)                                            (2.2)
    m_sigma^2 = lambda (3 sigma0^2 - v^2)

and, using (2.1) in (2.2),

    m_pi^2 = H / sigma0.                                                            (2.3)

(2.3) is what the code returns: it is algebraically identical to (2.2) at the exact root, but free of the
cancellation sigma0^2 - v^2 when H is small. The pions are no longer massless: m_pi^2 is linear in H as
H -> 0, with sigma0 = v + H/(2 lambda v^2) + O(H^2), m_pi^2 = H/v - H^2/(2 lambda v^4) + ...

**Closed form.** (2.1) is a depressed cubic sigma^3 - v^2 sigma - H/lambda = 0. For
c := 3 sqrt3 H / (2 lambda v^3) <= 1 (three real roots) the largest is

    sigma0 = (2 v / sqrt3) cos( (1/3) arccos c ),

and for c > 1, sigma0 = (2 v / sqrt3) cosh( (1/3) arccosh c ). (Check: substitute sigma = (2v/sqrt3) cos t and
use 4 cos^3 t - 3 cos t = cos 3t.)

**Second routes** (printed by `__main__`): (a) the trigonometric closed form versus the bisection root;
(b) (2.2) versus (2.3); (c) the eigenvalues (`toolkit.eigvalsh`) of the numerical Hessian (`toolkit.hessian`) of
the full 4-field V at (sigma0, 0, 0, 0): three equal to m_pi^2, one to lambda (3 sigma0^2 - v^2), all positive
(it is a minimum).

---------------------------------------------------------------------------------------------------------------

## 3. `gmor_mpi(mq_sum, cond13, fpi)`: leading-order pion mass

**Postulates.** Section 2 above plus SPEC's identification f_pi = <sigma> = sigma0 and
H f_pi = (m_u + m_d) |<qbar q>|.

**Derivation.** (2.3) is exact in the model: m_pi^2 = H / sigma0 = H / f_pi. Multiply by f_pi^2:

    m_pi^2 f_pi^2 = H f_pi = (m_u + m_d) |<qbar q>|       (Gell-Mann--Oakes--Renner)

With |<qbar q>| = cond13^3:

    m_pi = sqrt( mq_sum * cond13^3 ) / f_pi.

Why H f_pi is the right identification (not needed for the code, but it is where the postulate comes from): the
QCD mass term is -m (ubar u + dbar d) per flavour-averaged mass; the model's explicit breaking is -H sigma;
taking d/dm of the vacuum energy on both sides, E_vac' = <qbar q> summed over u, d on the QCD side and
-sigma0 dH/dm on the model side, with H linear in m, gives H sigma0 = (m_u + m_d)|<qbar q>| at leading order
(<ubar u> = <dbar d> = -|<qbar q>|).

"Leading order": f_pi and the condensate are themselves taken at their physical values rather than in the chiral
limit; the difference is O(m_q^2) in m_pi^2 (section 4).

**Second route.** Run the model itself: choose any lambda, set H = mq_sum cond13^3 / f_pi and
v^2 = f_pi^2 - H/(lambda f_pi) (so that (2.1) is solved by sigma0 = f_pi); then
`sigma_model_vacuum(lambda, v, H)` must return sigma0 = f_pi and mpi2 = gmor_mpi^2, independent of lambda.
`__main__` prints this for two values of lambda. Scaling check: m_pi ~ sqrt(m_q), ~ 1/f_pi.

---------------------------------------------------------------------------------------------------------------

## 4. `chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi)`: O(p^4) pion mass. QUOTED

**Not derived.** SPEC section 3 lists this as quoted (and contract `quoted_allowed`). Source: Gasser and
Leutwyler, Annals Phys. 158 (1984) 142, one-loop SU(2) chiral perturbation theory, in the conventions of the
FLAG review (F ~ 86 MeV normalization, lbar3 defined at the scale of the physical pion mass):

    M^2    = 2 mhat Sigma / F^2,   Sigma = cond13^3,   F = f_pi / (F_pi/F),   mhat = m_ud = (m_u + m_d)/2
    M_pi^2 = M^2 [ 1 - M^2 lbar3 / (32 pi^2 F^2) ]
    return sqrt(M_pi^2).

I did not derive the one-loop term (it needs the O(p^4) Lagrangian and the tadpole renormalization). What I
can and do check:

**Second route / consistency.** (a) lbar3 = 0 reduces to M, which is section 3's GMOR formula with
mq_sum = 2 mhat and the chiral-limit decay constant F in place of f_pi: `chpt_mpi(m, c, x, 0, f)` =
`gmor_mpi(2m, c, f/x)` identically. (b) The correction is perturbative: `__main__` prints the expansion
parameter M^2 lbar3/(32 pi^2 F^2) and compares with the first-order expansion
M_pi ~ M [1 - M^2 lbar3/(64 pi^2 F^2)].

If the bracket is negative (unphysically large lbar3 M^2) the square root does not exist; the code raises
ValueError rather than return a complex or clipped number.

---------------------------------------------------------------------------------------------------------------

## 4a. `chpt_mpi_from_rungs()`: the O(p^4) pion mass at the weak decay's f_pi. QUOTED

*Added with the contract change (SPEC section 3, last bullet; connection C-fpi). Chiral now depends on stage
`weak`.*

**What changed.** Until now the only f_pi available to this stage was the lattice input `inputs.F_PI`. Stage
`weak` derives f_pi from the measured pi -> mu nu width (SPEC section 10), so the ladder can feed its own
decay constant into the strong-force pion mass:

    chpt_mpi_from_rungs() = chpt_mpi(inputs.M_UD_FLAG, inputs.COND_13, inputs.FPI_OVER_F, inputs.LBAR3, f_92),
    f_92 = weak.fpi_from_pion_decay() / sqrt2.                                          (4a.1)

Both calls are made at call time as `weak.fpi_from_pion_decay()` and `chpt_mpi(...)` (the harness spies on
them). No other export changes; `chpt_mpi` itself still takes f_pi as an argument.

**The sqrt2.** Stage weak defines f by <0| ubar gamma^alpha gamma_5 d |pi-(p)> = i f p^alpha (the ~130 MeV
convention). The current ubar gamma gamma_5 d = A^1 - i A^2 in terms of the isospin currents
A^a = qbar gamma gamma_5 (tau^a/2) q, and pi- = (pi^1 + i pi^2)/sqrt2, so with <0|A^a|pi^b> = i F delta^ab p,
<0|A^1 - i A^2|pi-> = i F p (1 + 1)/sqrt2 = i sqrt2 F p. Hence f = sqrt2 F. The sigma model's f_pi = <sigma>
(section 3) is F: the Noether axial current of the O(4) model is A^a = sigma d pi^a - pi^a d sigma ->
<sigma> d pi^a. So the f_pi of `gmor_mpi`, `chpt_mpi` and `goldberger_treiman` is f/sqrt2 (~92 MeV), as the
SPEC states.

**Provenance.** `quoted`: it evaluates the quoted O(p^4) formula of section 4 (allowed for this export in
contract.py). What is derived upstream is only the decay constant that enters it.

**Second route** (printed by `__main__`, section "4a"). Neither `weak` nor `chpt_mpi` is called:
(a) f_pi from the width formula of DERIVATION_weak solved by hand,

    Gamma_tree = GF^2 V_ud^2 f^2 m_mu^2 (m_pi^2 - m_mu^2)^2 / (8 pi m_pi^3)
    =>  f^2 = 8 pi m_pi^3 Gamma_tree / (GF V_ud m_mu (m_pi^2 - m_mu^2))^2,
    Gamma_tree = hbar GAMMA_PI_MUNU / (1 + DELTA_PI);

(b) the quoted formula rewritten directly in f (F = f/(sqrt2 r), r = F_pi/F):

    M^2 = 4 m_ud Sigma r^2 / f^2,     M_pi^2 = M^2 [1 - M^2 lbar3 r^2 / (16 pi^2 f^2)].

The two agree with (4a.1) to rounding. Also printed: the result with the input F_PI, and the check that the
ratio of the two follows the leading-order scaling M_pi ~ 1/f (ratio of the decay constants) up to the small
O(p^4) term.

---------------------------------------------------------------------------------------------------------------

## 5. `yukawa(r, m)`: the exchange potential

**Postulate.** Exchange of a boson of mass m gives Vtilde(q) = 1/(q^2 + m^2) with unit strength, i.e.
(nabla^2 - m^2) V = -delta^3 (SPEC section 3).

**Derivation.** V(r) = Int d^3q/(2 pi)^3 e^{i q.r} / (q^2 + m^2). Angular integral
(Int dOmega e^{i q r cos th} = 4 pi sin(qr)/(qr)):

    V(r) = (1 / (2 pi^2 r)) Int_0^oo dq  q sin(qr) / (q^2 + m^2)
         = (1 / (4 pi^2 r)) Im Int_-oo^oo dq  q e^{iqr} / (q^2 + m^2).

Close the contour in the upper half plane (r > 0); the pole q = i m has residue
(i m) e^{-mr} / (2 i m) = e^{-mr}/2; the integral is 2 pi i * e^{-mr}/2 = i pi e^{-mr}. Hence

    V(r) = e^{-m r} / (4 pi r).

Checks of the postulated equation: for r > 0, with u = r V = e^{-mr}/(4 pi), nabla^2 V = u''/r = m^2 V.
Normalization: the flux of -grad V through a small sphere, -4 pi r^2 V'(r) = (1 + m r) e^{-mr} -> 1 as r -> 0,
which is Gauss's law for -delta^3. At m = 0: V = 1/(4 pi r) (Coulomb/Newton; rung 4 uses this).

**Second route (different representation, different numerics).** Schwinger proper time:
1/(q^2 + m^2) = Int_0^oo ds e^{-s (q^2 + m^2)}. The q integral is Gaussian:
Int d^3q/(2 pi)^3 e^{i q.r - s q^2} = (4 pi s)^{-3/2} e^{-r^2/(4s)}. So

    V(r) = Int_0^oo ds (4 pi s)^{-3/2} exp( -r^2/(4s) - m^2 s ),

an absolutely convergent integral with no oscillation, also valid at m = 0. `__main__` evaluates it with
`toolkit.trapezoid` in t = ln s and prints it next to e^{-mr}/(4 pi r).

---------------------------------------------------------------------------------------------------------------

## 6. `tensor_identity_residual(q)`

**Postulates.** Pauli matrices; S12 = 3 (s1.qhat)(s2.qhat) - s1.s2 (SPEC section 3).

**Identity.** With q = |q| qhat:

    (q^2/3)(s1.s2 + S12) = (q^2/3) * 3 (s1.qhat)(s2.qhat) = (s1.q)(s2.q).

Equivalently (s1.q)(s2.q) = (q^2/3) s1.s2 [central, rank 0] + (q^2/3) S12 [tensor, rank 2]: the one-pion-exchange
vertex product splits into a spin-spin and a tensor force. The decomposition is that of q_i q_j into its trace
(q^2/3) delta_ij and its traceless part.

**Implementation.** Explicit 4x4 complex matrices on the two-spin space: s1_i = sigma_i (x) 1, s2_i = 1 (x) sigma_i
(Kronecker product), so (s1.a)(s2.b) = (sigma.a) (x) (sigma.b) and s1.s2 = Sum_i sigma_i (x) sigma_i. The left
side uses q directly; the right side builds qhat = q/|q|, S12 from its definition, and the sum. Return the
largest |entry| of the difference. For q = 0 both sides vanish (the right side is q^2 times a bounded matrix),
and qhat is undefined: return 0.

**Second route.** Spectrum of S12. On the singlet s1.s2 = -3 and (s1.qhat)(s2.qhat) = -1, so S12 = 0. On the
triplet s1.s2 = +1 and (s1.qhat)(s2.qhat) = 2 (S.qhat)^2 - 1 = +1 (m = +-1), -1 (m = 0): S12 = 2, 2, -4. So
eigenvalues (-4, 0, 2, 2), trace 0 (rank-2 tensor has no scalar part), independent of qhat. `__main__` takes q in
the x-z plane (where every matrix is real: sigma_y (x) sigma_y is real), and prints `toolkit.eigvalsh(S12)`,
together with the eigenvalues of (s1.q)(s2.q), which must be q^2 times (+1, +1, -1) on the triplet and -1 on
the singlet, i.e. q^2 (-1, -1, 1, 1) in ascending order.

---------------------------------------------------------------------------------------------------------------

## 7. `goldberger_treiman(gA, MN, fpi)`: g_piNN. Derived from PCAC

**Postulates.** PCAC in the form used above (the axial current is conserved in the chiral limit, the pion is its
Goldstone boson with <0|A^a_mu|pi^b(q)> = i f_pi q_mu delta^ab, f_pi = <sigma> ~ 92 MeV normalization as in
`inputs.F_PI`), and the pion-nucleon coupling L = -i g_piNN Nbar gamma_5 tau^a N pi^a.

**Derivation.** Lorentz covariance and isospin give the nucleon matrix element of the axial current

    <N(p')| A^a_mu |N(p)> = ubar(p') [ g_A(q^2) gamma_mu gamma_5 + h_A(q^2) q_mu gamma_5 ] (tau^a/2) u(p),  q = p' - p.

Contract with q^mu and use the Dirac equation, ubar(p') qslash gamma_5 u(p) = 2 M_N ubar gamma_5 u:

    q^mu <A_mu> = [ 2 M_N g_A(q^2) + q^2 h_A(q^2) ] ubar gamma_5 (tau^a/2) u.

Chiral limit: d.A = 0, so h_A(q^2) = -2 M_N g_A(q^2)/q^2: a pole at q^2 = 0 = m_pi^2. The only massless state
that can produce it is the pion: the current creates a pion (amplitude f_pi q_mu), which propagates (1/q^2) and
is absorbed by the nucleon (g_piNN ubar gamma_5 tau^a u). The pole term is therefore

    h_A(q^2)|pole = -2 f_pi g_piNN / q^2

(the overall sign/phase follows the same convention on both sides; only the modulus matters). Equating residues
at q^2 -> 0 with g_A = g_A(0):

    f_pi g_piNN = M_N g_A      =>      g_piNN = g_A M_N / f_pi.

The same result follows in the linear sigma model with nucleons, L = -g Nbar (sigma + i gamma_5 tau.pi) N:
M_N = g <sigma> = g f_pi, g_piNN = g, g_A = 1, i.e. g_piNN = M_N/f_pi = g_A M_N/f_pi at tree level. This is the
second route (a model in which the relation can be read off the Lagrangian); `__main__` prints g_A = 1 case and
the comparison with the measured `inputs.G_PINN_EMP` (the Goldberger-Treiman discrepancy, a few per cent, is the
O(m_pi^2) correction from evaluating at q^2 = 0 rather than m_pi^2).

Tagged `derived` (SPEC section 3 allows either). The steps "the pole is saturated by one pion" and the
smoothness of g_A(q^2) between 0 and m_pi^2 are PCAC assumptions, not theorems.

---------------------------------------------------------------------------------------------------------------

## Not derived

- `chpt_mpi`: the O(p^4) coefficient (section 4), quoted as the SPEC permits.
- `chpt_mpi_from_rungs`: the same quoted formula at the f_pi of stage `weak` (section 4a), quoted as the SPEC
  permits.
- Nothing else. No number is taken from outside `inputs.py`.
