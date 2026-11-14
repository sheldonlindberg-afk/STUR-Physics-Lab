# DERIVATION: stage `photon` (build 2026-11-b)

Written before the code. Postulates: SPEC.md section 11 (QED Lagrangian, on-shell renormalization, the quoted
M_Z -> 0 relation) and section 2 (the lepton triplet's charge). Inputs: `inputs.MZ_MEAS, ALPHA_MZ_INV, M_E,
M_MU, M_TAU, DALPHA_HAD, DALPHA_CONV, DALPHA_LEP_HIGHER`. `inputs.ALPHA_0` is never read by the module's
exports. Nothing was left underived except what SPEC 11 itself quotes (the M_Z -> 0 relation, DALPHA_HAD,
DALPHA_CONV, DALPHA_LEP_HIGHER), which enter as inputs.

Natural units; metric g = diag(+1, -1, -1, -1) (SPEC 11: "timelike-positive"), so s = q^2 > 0 is timelike.
{gamma^mu, gamma^nu} = 2 g^{mu nu}; Tr 1 = 4.

## 0. Feynman rules from the Lagrangian (SPEC 11, postulate 1)

L = psibar (i d-slash - m) psi - e Q psibar gamma^mu psi A_mu - (1/4) F^2 gives

    fermion propagator   i (p-slash + m)/(p^2 - m^2 + i eps)
    vertex               -i e Q gamma^mu
    photon propagator    -i g_{mu nu}/(q^2 + i eps)      (Feynman gauge; the gauge term is irrelevant below)
    closed fermion loop  factor (-1) and a trace.

## 1. `vacuum_polarization(s, m)`

### 1.1 The loop

Define i Pi^{mu nu}(q) as the one-particle-irreducible two-photon amplitude (sum of 1PI insertions). At one loop

    i Pi^{mu nu}(q) = -(-i e Q)^2 Int d^dk/(2 pi)^d  Tr[ gamma^mu i(k-slash + m) gamma^nu i(k-slash + q-slash + m) ]
                                                     / [(k^2 - m^2)((k+q)^2 - m^2)]
                    = -e^2 Q^2 Int d^dk/(2 pi)^d  N^{mu nu} / [(k^2 - m^2)((k+q)^2 - m^2)] ,

    N^{mu nu} = Tr[gamma^mu (k-slash + m) gamma^nu (k-slash + q-slash + m)]
              = 4 [ k^mu (k+q)^nu + k^nu (k+q)^mu - g^{mu nu} (k.(k+q) - m^2) ]

(Tr[gamma^mu gamma^a gamma^nu gamma^b] = 4(g^{mu a} g^{nu b} - g^{mu nu} g^{ab} + g^{mu b} g^{a nu}),
Tr[gamma^mu gamma^nu] = 4 g^{mu nu}, odd traces vanish; (-ieQ)^2 i^2 = +e^2Q^2 and the loop sign gives the
overall minus.)

**Regulator: dimensional regularization**, d = 4 - epsilon, coupling e -> e mu^{epsilon/2}. It is chosen
because it preserves the Ward identity, so transversality (SPEC postulate 2) comes out rather than being imposed.

Feynman parameter: 1/(AB) = Int_0^1 dx 1/[xB + (1-x)A]^2, and

    x((k+q)^2 - m^2) + (1-x)(k^2 - m^2) = l^2 - Delta ,   l = k + x q ,   Delta = m^2 - x(1-x) q^2 .

Shift k = l - x q; drop terms odd in l; replace l^mu l^nu -> g^{mu nu} l^2/d:

    N^{mu nu}/4 -> (2/d - 1) g^{mu nu} l^2 - 2x(1-x) q^mu q^nu + g^{mu nu} (m^2 + x(1-x) q^2) .

Wick rotation (l^0 = i l_E^0):

    Int d^dl/(2 pi)^d 1/(l^2 - Delta)^2     =  i/(4 pi)^{d/2}  Gamma(2 - d/2) Delta^{d/2 - 2}
    Int d^dl/(2 pi)^d l^2/(l^2 - Delta)^2   = -i/(4 pi)^{d/2} (d/2) Gamma(1 - d/2) Delta^{d/2 - 1} .

In the l^2 term, (2/d - 1)(-d/2) Gamma(1 - d/2) = -(1 - d/2) Gamma(1 - d/2) = -Gamma(2 - d/2), so it equals
-g^{mu nu} Delta times the first integral. The bracket becomes

    g^{mu nu} (-Delta + m^2 + x(1-x) q^2) - 2x(1-x) q^mu q^nu = 2 x(1-x) (q^2 g^{mu nu} - q^mu q^nu) .

So the self-energy is transverse (SPEC postulate 2), i Pi^{mu nu} = i (q^2 g^{mu nu} - q^mu q^nu) Pi(q^2), with

    Pi(q^2) = -(8 e^2 Q^2 mu^epsilon/(4 pi)^{d/2}) Int_0^1 dx x(1-x) Gamma(epsilon/2) Delta^{-epsilon/2}
            = -(2 alpha Q^2/pi) Int_0^1 dx x(1-x) [ 2/epsilon - gamma_E + ln(4 pi mu^2) - ln Delta ] + O(epsilon) .

The pole, gamma_E and mu are q-independent. On-shell subtraction (SPEC postulate 2):

    Pihat(q^2) = Pi(q^2) - Pi(0) = (2 alpha Q^2/pi) Int_0^1 dx x(1-x) ln[ (m^2 - x(1-x) q^2 - i eps)/m^2 ] .     (1.1)

Finite, regulator independent (every regulator-dependent piece cancelled in the difference), and a function of
t = q^2/m^2 = s/m^2 only.

### 1.2 Sign and the effective coupling (SPEC postulate 3)

Summing the geometric series of insertions, with i Pi^{mu nu} as defined above, the propagator between
conserved currents becomes -i g_{mu nu}/(q^2 (1 - Pi(q^2))). The residue at q^2 = 0 is 1/(1 - Pi(0)), absorbed
in e (that is the renormalization "alpha is measured at q^2 = 0"), leaving

    alpha(s) = alpha/(1 - Re Pihat(s))     =>     Delta alpha(s) = + Re Pihat(s)   in this sign convention.

SPEC writes "minus the real part" for a self-energy defined with the opposite overall sign (Pi^{mu nu} as the
term added to the inverse propagator); the SPEC says the sign is to be fixed by screening, and (1.1) does that:
for s < 0 the logarithm's argument is 1 + x(1-x)|s|/m^2 > 1, so Delta alpha > 0. Hence, for Q = 1,

    vacuum_polarization(s, m) = Delta alpha/alpha = (2/pi) Int_0^1 dx x(1-x) ln| 1 - x(1-x) t | ,  t = s/m^2 .   (1.2)

(Real part: for t > 4 the argument is negative on part of the x range and ln(-|a| - i eps) = ln|a| - i pi.)

### 1.3 Closed form

Put x = (1+z)/2: x(1-x) = (1-z^2)/4, the integrand is even in z, and 1 - (1-z^2) t/4 = (t/4)(z^2 - b),

    b = 1 - 4/t = 1 - 4 m^2/s        (b > 1: spacelike;  0 < b < 1: above threshold;  b < 0: 0 < s < 4m^2).

    I = Int_0^1 dx x(1-x) ln|...| = Int_0^1 dz (1-z^2)/4 ln|(t/4)(z^2 - b)| .

Integrate by parts with P(z) = (z - z^3/3)/4 (P(0) = 0; the logarithm vanishes at z = 1 since (t/4)(1-b) = 1):

    I = -Int_0^1 P(z) 2z/(z^2 - b) dz = -(1/2) PV Int_0^1 (z^2 - z^4/3)/(z^2 - b) dz .

Polynomial division: (z^2 - z^4/3)/(z^2 - b) = -z^2/3 + (1 - b/3) + b(1 - b/3)/(z^2 - b), so

    I = -(1/2) [ 8/9 - b/3 + (b(3-b)/3) J ] ,     J = PV Int_0^1 dz/(z^2 - b) ,

    vacuum_polarization = (2/pi) I = -(1/(3 pi)) [ 8/3 - b + b(3-b) J ] .                                         (1.3)

    b > 0:  J = (1/(2 sqrt b)) ln|(1 - sqrt b)/(1 + sqrt b)| = -(1/(2 sqrt b)) ln[(1 + sqrt b)^2 |t|/4]
            (using |1 - sqrt b| = |1-b|/(1+sqrt b) = (4/|t|)/(1+sqrt b); this form has no cancellation at large |t|)
    b < 0:  J = (1/sqrt c) arctan(1/sqrt c),  c = -b .

Explicitly

    b > 0:  vp = (1/(3 pi)) [ -8/3 + b + ((3-b) sqrt b / 2) ln((1+sqrt b)^2 |t|/4) ]                              (1.4a)
    b < 0:  vp = (1/(3 pi)) [ -8/3 - c + (3+c) sqrt c arctan(1/sqrt c) ] ,  c = 4/t - 1                           (1.4b)

In the familiar variables (y = 4m^2/s, beta = sqrt(1-y)) (1.4a) is (1/3pi)[-5/3 - y + (1 + y/2) beta
ln|(1+beta)/(1-beta)|]. s = 4m^2 (b = 0) is excluded by the contract (the value there is finite, -8/(9 pi),
but the slope is singular).

### 1.4 Small |t|: series (used by the code for |t| <= 1, where (1.4) cancels badly)

Expand the logarithm in (1.2), ln(1 - u) = -Sum_{n>=1} u^n/n, and use the Beta function
Int_0^1 [x(1-x)]^{n+1} dx = ((n+1)!)^2/(2n+3)! =: a_n:

    vp = -(2/pi) Sum_{n>=1} a_n t^n / n ,   a_0 = 1/6 ,  a_{n+1}/a_n = (n+2)/(2(2n+5)) ,  converges for |t| < 4.   (1.5)

Leading term: a_1 = 1/30, vp = -t/(15 pi) + O(t^2): linear in s, zero at s = 0, positive for spacelike s and
negative for small timelike s. The coefficients are exact rationals (`fractions.Fraction` in the code).

### 1.5 Limits (checks on the closed form)

- |t| -> infinity (both signs): b -> 1, vp -> (1/(3 pi)) (ln|t| - 5/3). Slope in ln|s| is 1/(3 pi)
  = b_1/(4 pi) with SPEC 9's U(1) coefficient b_1 = (2/3) x (2 Weyl fields) x 1^2 = 4/3. Timelike and spacelike
  agree up to O(1/t) (the real part does not see the sign of s at high energy).
- t -> 0 from (1.4b): (3+c) sqrt c arctan(1/sqrt c) = c + 8/3 - 4/(5c) + ..., so vp -> -(4/(5c))/(3 pi)
  = -t/(15 pi), the same as (1.5).
- Monotonic for s < 0: d/d|t| of (1.2) has a positive integrand.

### 1.6 Second route (independent of the loop integral's regulator): unitarity + dispersion relation

The imaginary part of Pihat needs no regulator. From (1.1), for t > 4, ln has imaginary part -pi where
x(1-x) t > 1, i.e. |z| < beta = sqrt(1 - 4m^2/s):

    Im Pihat(s + i eps) = -(2 alpha/pi) pi Int_{-beta}^{beta} (dz/2) (1 - z^2)/4 = -(alpha/3) R(s) ,
    R(s) = beta (3 - beta^2)/2 .

R(s) is exactly the tree-level ratio sigma(l+ l- -> f fbar)/(4 pi alpha^2/(3s)) for a Dirac fermion (the
spin-averaged |M|^2 = e^4 [1 + cos^2 th + (4m^2/s) sin^2 th] integrated over the angle with the flux and the
factor beta from phase space gives (4 pi alpha^2/3s) beta (1 + 2m^2/s) = (4 pi alpha^2/3s) beta(3 - beta^2)/2),
as the optical theorem requires: the cut of the vacuum polarization is the production cross section.

Pihat(s) is analytic in the s plane cut along [4m^2, infinity), vanishes at s = 0, and grows only like ln s, so
the once-subtracted dispersion relation holds:

    Pihat(s) = (s/pi) Int_{4m^2}^infinity ds' Im Pihat(s')/(s' (s' - s - i eps))

    =>  vacuum_polarization(s, m) = -(s/(3 pi)) PV Int_{4m^2}^infinity ds' R(s')/(s' (s' - s)) .                  (1.6)

This is the form in which the hadronic contribution is measured (SPEC 11: "a dispersion integral over
e+e- -> hadrons data"), here applied to a lepton whose R is known in closed form.

For the numerical evaluation put s' = 4 m^2 cosh^2 v (v from 0 to infinity): beta = tanh v, ds'/s' = 2 tanh v dv,
s' - s = m^2 (4 cosh^2 v - t), so

    vp = -(t/(3 pi)) PV Int_0^infinity dv tanh^2 v (3 - tanh^2 v)/(4 cosh^2 v - t) .                              (1.7)

The integrand is smooth and even in v (trapezoid rule is then very accurate), decays like e^{-2v}. For t > 4
there is a simple pole at cosh v0 = sqrt(t)/2, where 4cosh^2 v - t = 4 sinh(v+v0) sinh(v-v0); the principal
value is taken by folding the interval [0, 2 v0] about v0 (the sum F(v0+u) + F(v0-u) is regular at u = 0, with
limit 2 G'(v0), G = numerator/(4 sinh(v + v0))).

The `__main__` block evaluates (1.7) with `toolkit.trapezoid` and prints it next to the closed form, at the
harness's probe points, at each lepton at M_Z^2, below threshold and for spacelike s. It also evaluates

- a third route, the Feynman-parameter integral (1.2) itself by `toolkit.trapezoid` (spacelike and below
  threshold, where the integrand is smooth), and
- the series (1.5) against the closed form (1.4) at their junction.

(Analytically, (1.7) with z = tanh v reproduces (1.3): the same polynomial division. The numerical evaluation
is what makes the check independent of that algebra.)

## 2. `dalpha_lep()`

Postulates: SPEC 11 "Leptons"; SPEC 2 (Q = T3 + beta T8 + X, lepton triplet X_L = -1/3 for beta = -1/sqrt3,
-2/3 for beta = +1/sqrt3); connection P-lep.

A fermion of charge Q has every vertex multiplied by Q, so (1.1) is multiplied by Q^2. The charged lepton's Q is
component 2 of `gauge331.triplet_charges(X_L, variant)`: T3 = -1/2, T8 = 1/(2 sqrt3), so
Q = -1/2 + beta/(2 sqrt 3) + X_L = -1/2 - 1/6 - 1/3 = -1 (beta = -1/sqrt3) and -1/2 + 1/6 - 2/3 = -1
(beta = +1/sqrt3). The code takes it from rung 1 (variant "-1/sqrt3"; the `__main__` block shows the other variant
gives the same Fraction).

    dalpha_lep = Sum_{l = e, mu, tau} Q_l^2 vacuum_polarization(M_Z^2, m_l) ,  M_Z = inputs.MZ_MEAS .             (2.1)

All three are far above threshold (t >= 2.6e3), so (1.4a) applies. Second route: the leading logarithm,
(1/(3 pi)) Sum (ln(M_Z^2/m_l^2) - 5/3), which must agree to O(m_tau^2/M_Z^2) (next term: -6 m^2/s per lepton
inside the bracket, from expanding (1.4a) in y = 4m^2/s: -y from b, and -y/2 from ln((1+sqrt b)^2/4), the
y ln t terms cancelling between (3-b)/2 = 1 + y/2 and sqrt b = 1 - y/2), and the dispersion integral (1.7) for
each lepton.

## 3. `alpha0_inv(higher=True)`

Postulates: SPEC 11 "From M_Z to q = 0" (quoted relation) and the last bullet. Write A = inputs.ALPHA_MZ_INV,
L = dalpha_lep(), H = DALPHA_HAD + DALPHA_CONV (+ DALPHA_LEP_HIGHER if `higher`), a = alpha(0):

    A = (1 - Dhat)/a ,    Dhat = a L + H
    =>  A = (1 - H)/a - L
    =>  1/alpha(0) = (A + L)/(1 - H) .                                                                            (3.1)

The relation is linear in 1/a, so the solution is unique and closed. Signs: 1/alpha(0) rises with A, with H
(H < 1) and with L (lighter leptons); with `higher` it is larger than without (H larger); and it exceeds A.

Second route: solve f(x) = (1 - x^{-1} L - H) x - A = 0 for x = 1/alpha(0) with `toolkit.bisect` (no algebra),
and a fixed-point iteration x <- (A + L)/(1 - H) reached from x_{k+1} = A/(1 - L/x_k - H). The `__main__` block
prints both next to (3.1), and only there compares with the measured 1/inputs.ALPHA_0.

## 4. What could not be derived

Nothing beyond what SPEC 11 quotes: the hadronic term (measured), the on-shell -> MS-bar conversion, the
two- and three-loop leptonic terms, and the relation 1/alpha-hat = (1 - Delta alpha-hat)/alpha(0) itself. They
are read from `inputs`; no export is labelled `quoted` (quoted_allowed is empty for this stage): the three
exports are computed here, with those quoted numbers entering `alpha0_inv` as inputs, which its PROVENANCE note
states.
