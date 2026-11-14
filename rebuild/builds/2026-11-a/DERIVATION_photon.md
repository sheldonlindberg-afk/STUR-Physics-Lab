# DERIVATION: photon (SPEC.md section 11)

Postulates used (all SPEC 11): QED of a Dirac fermion of mass m and charge Q (units of e > 0,
alpha = e^2/4pi), L = psibar(i dslash - m)psi - eQ psibar gamma^mu psi A_mu - (1/4)F^2; the one-loop
self-energy is transverse, Pi^{mu nu} = (q^2 g^{mu nu} - q^mu q^nu) Pi(q^2); on-shell renormalization
Pihat(s) = Pi(s) - Pi(0); alpha(s) = alpha/(1 - Dalpha(s)) with the overall sign fixed by screening
(Dalpha > 0 for spacelike s); leptons e, mu, tau with the charge of the lepton triplet's component 2
(SPEC 2, rung 1); the quoted relation 1/alphahat(M_Z) = (1 - Dalphahat)/alpha(0).
Inputs: M_E, M_MU, M_TAU, MZ_MEAS, ALPHA_MZ_INV, DALPHA_HAD, DALPHA_CONV, DALPHA_LEP_HIGHER.
inputs.ALPHA_0 is not read anywhere in the stage (not even in the self-check).
Nothing is tagged quoted (quoted_allowed is empty); alpha0_inv is derived but rests on the two quoted
*inputs* DALPHA_CONV and DALPHA_LEP_HIGHER and on the quoted relation of SPEC 11, and its note says so.

## Conventions

Timelike-positive metric g = diag(+,-,-,-) for this stage (SPEC 11: s = q^2 > 0 timelike).
{gamma^mu, gamma^nu} = 2 g^{mu nu}; Tr 1 = 4; Tr(gamma^mu gamma^nu) = 4 g^{mu nu};
Tr(gamma^mu gamma^a gamma^nu gamma^b) = 4(g^{mu a} g^{nu b} - g^{mu nu} g^{ab} + g^{mu b} g^{nu a}).
Fermion propagator i(pslash + m)/(p^2 - m^2 + i0), vertex -i e Q gamma^mu, closed loop factor -1.
x = s/m^2 throughout.

## 1. `vacuum_polarization(s, m)` = Dalpha(s)/alpha for one fermion, Q = 1

### 1a. The loop
    i Pi^{mu nu}(q) = -(-ieQ)^2 mu^eps Int d^dk/(2pi)^d
                      Tr[gamma^mu i(kslash + m) gamma^nu i(kslash + qslash + m)] / ((k^2 - m^2)((k+q)^2 - m^2))
                    = -(eQ)^2 mu^eps Int d^dk/(2pi)^d N^{mu nu} / (D_1 D_2),         d = 4 - eps,
    N^{mu nu} = 4[k^mu (k+q)^nu + k^nu (k+q)^mu - g^{mu nu}(k.(k+q) - m^2)].

Feynman parameter: 1/(D_1 D_2) = Int_0^1 du 1/(l^2 - Delta)^2, l = k + u q,
Delta = m^2 - u(1-u) q^2. Substituting k = l - u q and dropping terms odd in l:

    N^{mu nu} -> 4[2 l^mu l^nu - g^{mu nu} l^2 - 2u(1-u) q^mu q^nu + g^{mu nu}(m^2 + u(1-u) q^2)],
    l^mu l^nu -> g^{mu nu} l^2 / d.

Dimensional regularization (Wick rotated):

    Int d^dl/(2pi)^d 1/(l^2 - Delta)^2   =  i/(4pi)^{d/2} Gamma(2 - d/2) Delta^{d/2 - 2},
    Int d^dl/(2pi)^d l^2/(l^2 - Delta)^2 = -i/(4pi)^{d/2} (d/2) Gamma(1 - d/2) Delta^{d/2 - 1}.

The l^2 terms: (2/d - 1)(-d/2) Gamma(1 - d/2) Delta = (d/2 - 1) Gamma(1 - d/2) Delta = -Gamma(2 - d/2) Delta.
So the g^{mu nu} coefficient is 4 Gamma(2-d/2) Delta^{d/2-2} [-Delta + m^2 + u(1-u)q^2] = 8u(1-u) q^2 Gamma(..)..,
and the q^mu q^nu coefficient is -8u(1-u) Gamma(..)..: the result is transverse (the Ward identity,
which the quadratic divergence would violate with a naive cutoff), as SPEC 11 postulates:

    i Pi^{mu nu} = i (q^2 g^{mu nu} - q^mu q^nu) Pi(q^2),
    Pi(q^2) = -(8 e^2 Q^2/(4pi)^2) Int_0^1 du u(1-u) [2/eps - gamma_E + ln 4pi - ln(Delta/mu^2)] + O(eps)
            = -(2 alpha Q^2/pi) Int_0^1 du u(1-u) [2/eps - gamma_E + ln 4pi - ln((m^2 - u(1-u)q^2)/mu^2)].

### 1b. On-shell subtraction: finite and regulator independent
    Pihat(s) = Pi(s) - Pi(0) = (2 alpha Q^2/pi) Int_0^1 du u(1-u) ln(1 - u(1-u) s/m^2 - i0).

The pole 2/eps, gamma_E, ln 4pi and mu all cancel; only ln(Delta(s)/Delta(0)) survives, a function of
s/m^2 alone. Any other gauge-invariant regulator (e.g. Pauli-Villars) differs from this Pi(s) by an
s-independent constant, which the subtraction removes. Above threshold (s > 4m^2) the log's argument
is negative for part of the u range and Pihat acquires an imaginary part; the real part is ln| |.

### 1c. Sign: screening
With i Pi^{mu nu} inserted as above, the geometric series of the propagator gives
-i g_{mu nu}/(q^2 (1 - Pi(q^2))), so e^2 -> e^2/(1 - Pihat(s)) after fixing the residue at q^2 = 0:
alpha(s) = alpha/(1 - Pihat(s)), i.e. Dalpha(s) = +Re Pihat(s) in *this* sign convention for Pi.
SPEC 11 writes "minus the real part" (the opposite convention for the sign of Pi, e.g. the self-energy
added to the inverse propagator) and says the overall sign is fixed by screening. Check: for s < 0 the
log's argument is 1 + u(1-u)|s|/m^2 > 1, so the expression below is > 0: alpha(s) > alpha at short
distance (vacuum polarization screens the bare charge at long distance). Hence, for Q = 1,

    Dalpha(s)/alpha = (2/pi) Int_0^1 du u(1-u) ln|1 - u(1-u) x|,        x = s/m^2.        (*)

(Recorded in QUESTIONS.md.)

### 1d. Closed form
w = 2u - 1, u(1-u) = (1 - w^2)/4, integrand even in w:

    I(x) = Int_0^1 du u(1-u) ln|1 - u(1-u)x| = (1/4) Int_0^1 dw (1 - w^2) ln|1 - x(1 - w^2)/4|.

By parts with G = w - w^3/3 (boundary term vanishes: G(0) = 0, log = 0 at w = 1), and
d/dw ln|1 - x(1-w^2)/4| = 2w/(w^2 - B), B = 1 - 4/x = 1 - 4m^2/s:

    I = -(1/2) Int_0^1 dw (w^2 - w^4/3)/(w^2 - B)
      = -(1/2) Int_0^1 dw [ -w^2/3 + (1 - B/3) + B(1 - B/3)/(w^2 - B) ]
      = -(1/2) [ 8/9 - B/3 + B(1 - B/3) J ],      J = P Int_0^1 dw/(w^2 - B).

- B > 0 (s < 0, where beta = sqrt(B) > 1, or s > 4m^2, where 0 < beta < 1; principal value in the latter):
  J = -(1/(2 beta)) ln|(1 + beta)/(1 - beta)|, so

      Dalpha/alpha = (1/pi) [ -8/9 + beta^2/3 + (beta(3 - beta^2)/6) ln|(1 + beta)/(1 - beta)| ].

- B < 0 (0 < s < 4m^2), b = sqrt(-B): J = (1/b) arctan(1/b), so

      Dalpha/alpha = (1/pi) [ -8/9 - b^2/3 + (b(3 + b^2)/3) arctan(1/b) ].

Equivalently, with y = 4m^2/s: (1/3pi)[-5/3 - y + (1 + y/2) beta ln|(1+beta)/(1-beta)|].

### 1d'. Large |x|: evaluating the logarithm without cancellation (fix after the strengthened slope check)
The closed form is exact, but its naive evaluation is not: for |x| >> 1, B = 1 - 4/x is within 4/|x| of 1,
so beta -> 1 and the floating-point difference 1 - beta carries a relative rounding error ~ 1e-16 |x|/2.
At x = 1e12..1e14 that is 1e-5..1e-3 in the argument of the log, i.e. an absolute error of that size in
Dalpha/alpha (the first implementation's slope over 1e12..1e14 was off by 1.8e-4; the electron at M_Z has
x ~ 3e10, where the error was ~1e-7 relative in its term). The cure is algebraic, not numerical:

    1 - beta^2 = 1 - B = 4/x   =>   |1 - beta| = (4/|x|)/(1 + beta)     (both for x < 0, beta > 1, and x > 4, beta < 1)
    =>  ln|(1 + beta)/(1 - beta)| = ln( (1 + beta)^2 |x| / 4 ),

which has no subtraction of nearly equal numbers. It is the same function; the code now uses this form for
all B >= 0. Limit check: beta -> 1 gives ln|x|, the asymptote of 1f. (B itself still rounds to 1 for huge
|x|, which is harmless: the result's sensitivity to B is O(1), so the error is O(1e-16).)

### 1e. Small |x|: series (used for |x| < 1/2, where 1d cancels O(1) terms to O(x))
ln(1 - t x) = -Sum_{n>=1} t^n x^n/n and Int_0^1 [u(1-u)]^{n+1} du = B(n+2, n+2) = ((n+1)!)^2/(2n+3)!:

    Dalpha/alpha = -(2/pi) Sum_{n>=1} (x^n/n) B_n,  B_1 = 1/30,  B_{n+1}/B_n = (n+2)/(2(2n+5)).

Converges for |x| < 4. Leading term -x/(15 pi): vanishes linearly at s = 0, positive for s < 0,
negative for small s > 0.

### 1f. Limits
|x| -> infinity: beta -> 1, |1 - beta| -> 2/|x|, so Dalpha/alpha -> (1/3pi)(ln|x| - 5/3), the same on both
sides; slope in ln|s| is 1/(3 pi) = (4/3)/(4 pi), SPEC 9's b = (2/3)(2 Weyl fields)(q^2 = 1) = 4/3.

### 1g. Independent second routes (printed by `python3 photon.py`)
1. **Direct quadrature of (*)**: toolkit.trapezoid on the Feynman-parameter integral, never using 1d/1e
   (spacelike, below threshold; above threshold the integrable log singularities limit it to ~1e-5).
2. **Dispersion relation / optical theorem** (a different physical route: no loop integral over
   Feynman parameters, only the tree-level pair-production rate). Im Pihat(s') = -(alpha/3)(1 + 2m^2/s')
   sqrt(1 - 4m^2/s') for s' > 4m^2 in the convention of 1c (it is (s'/4 pi alpha) sigma(e+e- -> f fbar) up to
   sign), and the once-subtracted dispersion integral gives

       Dalpha(s)/alpha = -(s/3pi) Int_{4m^2}^inf ds' (1 + 2m^2/s') sqrt(1 - 4m^2/s') / (s'(s' - s)).

   With s' = 4m^2/v^2, v = sin(theta):

       Dalpha/alpha = -(x/6pi) Int_0^{pi/2} dtheta sin(theta) cos^2(theta) (1 + sin^2(theta)/2) / (1 - x sin^2(theta)/4),

   a smooth integrand for x < 4 (spacelike and below threshold), evaluated with toolkit.trapezoid.
   Check at small x: Int = 2/5, giving -x/(15 pi), the same as 1e.
3. **Series vs closed form** in the overlap 1/2 <= |x| < 4 (two different evaluations of (*)).
5. **Slope at very large |x|** (1e8..1e10, 1e12..1e14, 1e18..1e20, both signs) against 1/(3 pi): the
   deviation must fall like the true O(1/x) correction, not grow with x.
4. **Asymptote** (1/3pi)(ln(s/m^2) - 5/3) at s = M_Z^2 for each lepton (corrections O(m^2/s)).

## 2. `dalpha_lep()` = one-loop Dalpha_lep(M_Z^2)/alpha

Each lepton is an independent Dirac fermion loop; the vertex factor (eQ)^2 gives Q^2:

    dalpha_lep = Sum_{l = e, mu, tau} Q_l^2 vacuum_polarization(M_Z^2, m_l),   M_Z = inputs.MZ_MEAS.

Q_l is component 2 (index 1) of gauge331.triplet_charges(X_L, variant) for the lepton triplet, with
X_L = -1/3 for beta = -1/sqrt3 (SPEC 2). The same Q results for beta = +1/sqrt3 with X_L = -2/3 (checked
in the self-check); it is -1, exactly, as a Fraction, and Q^2 = 1. All three leptons sit in triplets
with the same X_L (one per generation), so one call serves all three.

Second route: the asymptote of 1f summed over leptons, and direct quadrature of (*) (above threshold).

## 3. `alpha0_inv(higher=True)` = 1/alpha(0)

SPEC 11's quoted relation, with a = alpha(0), L = dalpha_lep(), and
C = DALPHA_HAD + DALPHA_CONV (+ DALPHA_LEP_HIGHER if higher):

    1/alphahat = (1 - Dalphahat)/a,     Dalphahat = a L + C
    => 1/alphahat = (1 - C)/a - L
    => 1/a = (1/alphahat + L)/(1 - C).

The relation is linear in 1/a, so the solution is unique and in closed form. L > 0 and 0 < C < 1 give
1/a > 1/alphahat; a larger C (higher = True, more hadrons) raises 1/a; heavier leptons lower L and 1/a.

Second route: toolkit.bisect on g(a) = (1 - a L - C)/a - 1/alphahat for a between 1/(2 x ALPHA_MZ_INV)
and 1/ALPHA_MZ_INV (g > 0 at the lower end, g < 0 at the upper end, since Dalphahat > 0); and the
first-order iteration 1/a ~ (1/alphahat)(1 + Dalphahat + ...) is not used.

Not derived here (inputs, per SPEC 11): the hadronic Dalpha (data), the on-shell -> MS-bar conversion
DALPHA_CONV (quoted input) and the two- and three-loop leptonic terms DALPHA_LEP_HIGHER (quoted input).
