# DERIVATION: stage `running` (build 2026-11-b)

Written before the code. Postulates: SPEC.md section 9 (one-loop running, Standard Model content, 3-3-1
content above the breaking scale, matching, definition of `landau_pole`) and section 2 (charge operator,
multiplet content, scalar X charges). Units: GeV, hbar = c = 1, alpha = g^2/(4 pi). Nothing is quoted. In
particular `inputs.POLES_331` (three-loop poles, layer QUOTED) is **not** used anywhere in this stage.

Nothing in this stage could not be derived. Two points of interpretation are listed in section 6.

---------------------------------------------------------------------------------------------------------

## 0. The master formula (SPEC section 9, first postulate)

    d(1/alpha)/d ln mu = -b/(2 pi)
    b = -(11/3) C2(G) + (2/3) sum_Weyl T(R) + (1/3) sum_complex-scalars T(R)                       (0.1)

C2(SU(N)) = N, C2(U(1)) = 0; T(fundamental or antifundamental of SU(N)) = 1/2, T(singlet) = 0; each multiplet
counted once per component of every *other* group factor (its multiplicity). For a U(1) with charge q a
multiplet of d components (under all other factors) contributes T -> d q^2.

Because b is constant at one loop, (0.1) integrates exactly:

    1/alpha(mu) = 1/alpha(mu0) - (b/(2 pi)) ln(mu/mu0)                                              (0.2)

Everything below is (0.1) applied to a list of multiplets and (0.2) applied to a boundary value.

A multiplet is recorded as (kind, mult, dim, charges): kind = Weyl or complex scalar; `mult` = number of
copies (generations x colours); `dim` = dimension under the non-abelian weak factor (1 = singlet, N =
fundamental); `charges` = the U(1) charge (one number; the U(1) commutes with the non-abelian factor so all
components of an irreducible multiplet share it). Then

    b_nonabelian = -(11/3) N + sum_multiplets w_kind * mult * (1/2 if dim == N else 0)             (0.3)
    b_U(1)       =             sum_multiplets w_kind * mult * dim * q^2                             (0.4)
    w_Weyl = 2/3, w_scalar = 1/3.

## 1. `sm_coefficients() -> (b_Y, b_2)`: exact Fractions

**Postulates** (SPEC section 9, second bullet): 3 colours, 3 generations; per generation, left-handed Weyl:
Q (doublet, Y = 1/6, 3 colours), u^c (singlet, Y = -2/3, 3 colours), d^c (singlet, Y = 1/3, 3 colours),
L (doublet, Y = -1/2), e^c (singlet, Y = 1); one complex Higgs doublet, Y = 1/2. Q = T3 + Y.

**Steps.** With N_g = 3 generations, N_c = 3 colours:

    sum_Weyl dim*mult*Y^2 per generation
        = 2*N_c*(1/6)^2 + N_c*(2/3)^2 + N_c*(1/3)^2 + 2*(1/2)^2 + 1
        = N_c/18 + 4N_c/9 + N_c/9 + 3/2 = 11 N_c/18 + 3/2
    b_Y = (2/3) N_g (11 N_c/18 + 3/2) + (1/3) * 2 * (1/2)^2                                         (1.1)
    b_2 = -(11/3)*2 + (2/3)(1/2) N_g (N_c + 1) + (1/3)(1/2)                                         (1.2)

At N_g = N_c = 3: b_Y = (2/3)*3*(10/3) + 1/6 = 41/6;  b_2 = -22/3 + 4 + 1/6 = -19/6. The code does **not**
type these: it evaluates (0.3), (0.4) on the multiplet list.

The hypercharges themselves are tied to rung 1 rather than only copied from the SPEC table: the code
builds the list from the table and the main block checks (second route B below) that Q = T3 + Y reproduces
`gauge331.quark_charges(3)` and the lepton charges (0, -1).

**Second routes.**
- A. Closed forms (1.1), (1.2) evaluated as Fractions in N_g, N_c, compared `==` with the multiplet sum.
- B. Consistency of the content: (i) Q = T3 + Y of the doublets gives (Q_u, Q_d) of rung 1 and (0, -1); the
  singlets' Y are minus those charges. (ii) Anomaly freedom of the same list: sum Y = 0 (gravitational),
  sum Y^3 = 0, sum over doublets Y = 0 ([SU(2)]^2 U(1)), sum over coloured Y = 0 ([SU(3)_c]^2 U(1)), all with
  multiplicities. A mistyped hypercharge or multiplicity breaks at least one of these exact sums.
- C. GUT cross-check of normalisation: for a complete generation, (3/5) sum Y^2 dim mult equals the SU(2)
  index sum, i.e. (3/5) * (10/3) = 2 = (1/2)(3+1): fermions alone contribute equally to all (GUT-normalised)
  b's. Exact Fraction identity.

## 2. `b_331(Nc, variant) -> (b_X, b_L)`: exact Fractions

**Postulates** (SPEC sections 2 and 9, third bullet). Gauge group SU(3)_C x SU(3)_L x U(1)_X; N_c colours;
N_g = N_c generations.

Charges are obtained from rung 1 at call time (connection R-content):

    s  = gauge331.triplet_charges(0, variant)            = diag(T3 + beta T8)   (triplet, X = 0)
    sa = gauge331.triplet_charges(0, variant, anti=True) = -s
    (Q_u, Q_d) = gauge331.quark_charges(Nc)

- Lepton triplet: the electron is the T3 = -1/2 component (index 1) with charge -1:
      X_L = -1 - s[1].                                                                              (2.1)
  (SPEC states X_L = -1/3, -2/3; (2.1) reproduces both, checked `==` in the main block.)
- Quark triplet: first two components (Q_u, Q_d):  X_t = Q_u - s[0]; consistency s[1] + X_t == Q_d holds
  since s[0] - s[1] = 1 = Q_u - Q_d.                                                                (2.2)
- Quark antitriplet: first two components are (Q_u, Q_d) "in some order". sa[0] - sa[1] = -1, so the order
  must be (Q_d, Q_u):  X_a = Q_u - sa[1], and sa[0] + X_a == Q_d.  The code tries both orders and keeps the
  one that is consistent (exactly one is).                                                          (2.3)
- Numbers of families: n_A = (1 + N_c)/2 antitriplets, n_T = N_g - n_A triplets, each in N_c colours.
- SU(3)_L singlets (left-handed Weyl): for every component of charge q != 0 of every fermion triplet or
  antitriplet, one singlet with X = -q, with the same colour multiplicity (the conjugate colour
  representation has the same dimension, which is all that enters). Neutral components have no partner.
- Scalars: three complex triplets, colour singlets, X charges of SPEC section 2 for the variant:
  (-1/3, 2/3, -1/3) or (1/3, 1/3, -2/3).

**Steps.** Multiplet list (kind, mult, dim, X):

    Weyl   N_g          3   X_L
    Weyl   n_T N_c      3   X_t
    Weyl   n_A N_c      3   X_a
    Weyl   N_g          1   -q         for each q != 0 in triplet_charges(X_L, variant)
    Weyl   n_T N_c      1   -q         for each q != 0 in triplet_charges(X_t, variant)
    Weyl   n_A N_c      1   -q         for each q != 0 in triplet_charges(X_a, variant, anti=True)
    scalar 1            3   X_k        k = 1, 2, 3

and (0.3), (0.4) with N = 3:

    b_L = -11 + (2/3)(1/2)(N_g + n_T N_c + n_A N_c) + (1/3)(1/2)*3
        = -11 + (1/3) N_g (1 + N_c) + 1/2                                                            (2.4)
    b_X = (2/3)[ N_g (3 X_L^2 + S_L) + N_c n_T (3 X_t^2 + S_t) + N_c n_A (3 X_a^2 + S_a) ]
          + (1/3) * 3 * sum_k X_k^2                                                                  (2.5)

with S_m = sum of q^2 over the charged components of multiplet m.

Hand evaluation at N_c = 3, beta = -1/sqrt3 (to be compared with the code, not typed into it): s = (1/3, -2/3,
1/3); X_L = -1/3, lepton charges (0, -1, 0), S_L = 1; Q_u = 2/3, X_t = 1/3, charges (2/3, -1/3, 2/3), S_t = 1;
X_a = 0, charges (-1/3, 2/3, -1/3), S_a = 2/3; n_T = 1, n_A = 2.
Fermions: 3(1/3 + 1) + 3*1*(1/3 + 1) + 3*2*(0 + 2/3) = 4 + 4 + 4 = 12; scalars: 3*(1/9 + 4/9 + 1/9) = 2.
b_X = (2/3)*12 + (1/3)*2 = 26/3;  b_L = -11 + 4 + 1/2 = -13/2.

**Second routes.**
- A. Closed forms (2.4), (2.5) coded separately in the main block from the per-multiplet charge sums and
  compared `==` with the generic multiplet-list sum; and the hand value above for (3, "-1/sqrt3").
- B. Anomaly freedom of the list that is being counted (exact Fractions, all N_c in (1, 3, 5, 7), both
  variants): [SU(3)_L]^2 U(1)_X: sum over (anti)triplets mult X = 0 (the condition rung 1 solved);
  [SU(3)_L]^3: (#triplets) - (#antitriplets) = N_g + N_c n_T - N_c n_A = 0; gravitational sum mult dim X = 0;
  [U(1)_X]^3: sum mult dim X^3 = 0; [SU(3)_C]^2 U(1)_X: sum over coloured fields of X (per colour) = 0. If a
  singlet were missed or given the wrong sign of X these fail.
- C. Embedding check: U(1)_Y = beta T8 + X, so Tr Y^2 over the 3-3-1 content of fields = beta^2 Tr T8^2 + Tr X^2
  (cross term vanishes multiplet by multiplet since Tr T8 = 0). So

      b_Y(3-3-1 matter, no gauge bosons) = beta^2 * (matter part of b_L) + b_X = (1/3) (b_L + 11) + b_X.   (2.6)

  Independently, b_Y of the 3-3-1 matter can be computed directly from the electric charges and T3 of every
  component: Y = Q - T3 with T3 = (1/2, -1/2, 0) for triplet components (minus that for antitriplets), 0 for
  singlets. The main block evaluates sum w * mult * (Q - T3)^2 component by component and compares `==` with
  the right-hand side of (2.6). This tests b_X and b_L together through a route that never uses X of the
  triplets directly (only the electric charges returned by rung 1).
- D. Monotonicity: b_X > 0 and strictly increasing in N_c (also in the harness).

## 3. `couplings_at(mu) -> (1/alpha_Y, 1/alpha_2)`

**Postulates** (SPEC section 9): at M_Z = inputs.MZ_MEAS, 1/alpha_Y = (1 - s^2)/alpha-hat, 1/alpha_2 =
s^2/alpha-hat, 1/alpha-hat = inputs.ALPHA_MZ_INV, s^2 = inputs.S2_MZ. (These follow from e = g_2 s = g_Y c:
1/e^2 = 1/g_2^2 + 1/g_Y^2, s^2 = e^2/g_2^2.)

**Result** from (0.2):

    1/alpha_i(mu) = 1/alpha_i(M_Z) - (b_i/(2 pi)) ln(mu/M_Z),   (b_Y, b_2) = sm_coefficients().     (3.1)

**Second route.** Integrate d(1/alpha)/d ln mu = -b/(2 pi) numerically with `toolkit.trapezoid` on a grid in
ln mu (the integrand is constant, so this checks the bookkeeping of sign, 2 pi and the log, not the
quadrature) and, more substantively, integrate the *non-linear* form d alpha/d ln mu = (b/(2 pi)) alpha^2 with
a fourth-order Runge-Kutta in the main block and compare 1/alpha at mu with (3.1). Also the group property:
running M_Z -> mu1 -> mu2 equals M_Z -> mu2, and the sum rule 1/alpha_Y(M_Z) + 1/alpha_2(M_Z) = 1/alpha-hat.

## 4. `matching_331(mu, variant) -> (1/alpha_X, 1/alpha_L)`

**Postulates** (SPEC section 9, matching, no thresholds): g_L(mu) = g_2(mu); rung 1's 1/e^2 at (g_L, g_X)
equals the Standard Model's 1/e^2 = (1/alpha_Y + 1/alpha_2)/(4 pi).

**Steps.** 1/alpha_L = 1/alpha_2, g_L = sqrt(4 pi alpha_2). Let u = 1/g_X^2 and

    E(u) = gauge331.inv_e2(variant, g_L, u^(-1/2)).

E is the squared norm of the photon direction n with sum_A n_A g_A T_A = Q (rung 1, DERIVATION_gauge331
section 6); the U(1)_X component is n_9 = 1/g_X, so E is affine in u. The code does not assume the slope or
the intercept: it evaluates E at two probe values u1, u2 (two calls of `gauge331.inv_e2`, connection
R-match), forms slope = (E(u2) - E(u1))/(u2 - u1), intercept = E(u1) - slope*u1, and solves

    slope * u + intercept = (1/alpha_Y + 1/alpha_2)/(4 pi)   =>   u = (target - intercept)/slope,   (4.1)
    1/alpha_X = 4 pi / g_X^2 = 4 pi u.

If u <= 0 there is no real g_X (the matching has no solution at that mu); the code raises ValueError.

**Closed form** (from rung 1's E = (1 + beta^2)/g_L^2 + 1/g_X^2, beta^2 = 1/3):

    1/alpha_X = 1/alpha_Y - beta^2/alpha_2 = 1/alpha_Y - (1/3)(1/alpha_2).                          (4.2)

This is also the statement Y = beta T8 + X: 1/g_Y^2 = beta^2/g_L^2 + 1/g_X^2. It is independent of the sign
of beta, so both variants match to the same alpha_X(mu); they differ only through b_X.

**Second routes.** (i) closed form (4.2), printed next to (4.1); (ii) solve
inv_e2(variant, g_L, g_X) - target = 0 for g_X with `toolkit.bisect` (no linearity assumed);
(iii) substitute back: 4 pi * inv_e2(g_L, g_X) vs 1/alpha_Y + 1/alpha_2.

## 5. `landau_pole(Nc, variant) -> GeV`

**Postulates** (SPEC section 9, last bullet): mu0 = inputs.MU_331; 1/alpha_X(mu0) = matching_331(mu0, variant)[0];
one-loop running with b_X = b_331(Nc, variant)[0]; return mu with alpha_X(mu) = 1. Only U(1)_X enters.

**Result** from (0.2): 1/alpha_X(mu) = 1/alpha_X(mu0) - (b_X/(2 pi)) ln(mu/mu0) = 1 gives

    mu_pole = mu0 * exp( 2 pi (1/alpha_X(mu0) - 1) / b_X ).                                          (5.1)

b_X > 0 (section 2), and 1/alpha_X(mu0) > 1 for the measured inputs, so mu_pole > mu0. Note this is the scale
of alpha_X = 1 (SPEC's definition, "the perturbative limit"), not the true divergence 1/alpha_X = 0, which lies
a factor exp(2 pi / b_X) higher. If 1/alpha_X(mu0) <= 1 no such scale exists above mu0; the code raises.

Dependence on N_c: 1/alpha_X(mu0) does not depend on N_c (the Standard Model below mu0 is fixed at 3 colours by
SPEC), b_X grows with N_c, so the pole falls with N_c.

**Second routes.** (i) root of F(t) = 1/alpha_X(mu0) - (b_X/(2 pi)) t - 1 in t = ln(mu/mu0) with
`toolkit.bisect`, compared with (5.1); (ii) Runge-Kutta integration of d alpha_X/dt = (b_X/(2 pi)) alpha_X^2
from t = 0 to t_pole, which must end at alpha_X = 1; (iii) scaling: doubling mu0 at fixed inputs changes the pole
by the factor 2 * exp(2 pi (Delta 1/alpha_X)/b_X) with Delta from the SM slopes (4.2):
Delta = -(b_Y - b_2/3) ln2/(2 pi), i.e. pole(2 mu0)/pole(mu0) = 2^(1 - (b_Y - b_2/3)/b_X).

## 6. Interpretation points (also in QUESTIONS.md)

1. **Colour multiplicity of the singlet partners.** SPEC says each charged component "has one singlet
   partner". Resolved: one partner per component *per copy of the multiplet*, i.e. the partner of a quark
   component is a colour antitriplet-like field with N_c colours, and there is one per family (as u^c, d^c in
   the SM). Supported by the anomaly sums of section 2 route B, which vanish only with this counting.
2. **Scalars have no singlet partners and are colour singlets**; the three scalar triplets are the only
   scalars above the 3-3-1 scale (SPEC lists no others). The X charges of the scalars are postulates of SPEC
   section 2 and are entered as exact thirds.
3. **N_c even**: n_A = (1 + N_c)/2 is not an integer; the code does not reject it (b's stay exact Fractions),
   but the content is only meaningful for odd N_c.
4. **Standard Model below mu0 is always the 3-colour, 3-generation one**, also when `landau_pole` is called
   with N_c = 5: `couplings_at` takes no N_c, and SPEC says "3 colours, 3 generations" below the scale.
