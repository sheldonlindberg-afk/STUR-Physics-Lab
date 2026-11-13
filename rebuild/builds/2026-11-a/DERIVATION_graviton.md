# DERIVATION: graviton (rung 4, SPEC.md section 5)

Conventions: signature eta = diag(-1, 1, 1, 1); indices 0..3; G and c kept symbolic where the
result is a pure number (units GM/(c^2 r)), SI from `inputs` at call time otherwise. Exact
quantities are `fractions.Fraction`.

Postulates used (SPEC.md section 5):
- P1 linearized GR: g = eta + h, hbar_{mu nu} = h_{mu nu} - (1/2) eta_{mu nu} h, box hbar_{mu nu} = -16 pi G T_{mu nu}.
- P2 one-graviton exchange: amplitude proportional to T2^{mu nu} P_{mu nu rho sigma} T1^{rho sigma},
  P = (1/2)(eta_{mu rho} eta_{nu sigma} + eta_{mu sigma} eta_{nu rho} - eta_{mu nu} eta_{rho sigma}).
- P3 branch profile y(t) = (dx/2) s(t) (SPEC 5).
- P4 phase, parallel geometry (SPEC 4 and 5), trapezoid rule on n samples.
- From rung 2 (SPEC 3, `chiral.yukawa`): the function whose Fourier transform is 1/(q^2 + m^2),
  unit normalized, (lap - m^2) V = -delta^3. At m = 0: lap V = -delta^3, V = 1/(4 pi r).

Standard matter coupling (part of linearized GR, P1): expanding S_matter[eta + h] to first order,
delta S = (1/2) Int h_{mu nu} T^{mu nu} d^4x. For a static configuration the interaction energy is
minus the interaction Lagrangian: U = -(1/2) Int h^{(1)}_{mu nu} T2^{mu nu} d^3x, with h^{(1)} the
field sourced by body 1 only (no double counting: the field of 2 acting on 1 is the same term,
already contained in the 1/2 of the quadratic action once the field equation is used).

---------------------------------------------------------------------------------------------------
## 1. point_mass_metric() -> (h00, hii) in units GM/(c^2 r)

**Source.** Point mass at rest: T^{00} = M c^2 delta^3(x) (energy density), all other components 0.
With lowered indices T_{00} = eta_00 eta_00 T^{00} = T^{00}.

**Static Poisson.** box -> lap for static fields: lap hbar_{00} = -16 pi G T_{00}/c^4 = -16 pi (G M/c^2) delta^3.
Since lap(1/(4 pi r)) = -delta^3 (rung 2 at m = 0), hbar_{00} = 16 pi (GM/c^2) /(4 pi r) = 4 GM/(c^2 r).
All other hbar_{mu nu} = 0 (sourceless, decaying).

**Trace reversal.** hbar = eta^{mu nu} hbar_{mu nu} = eta^{00} hbar_00 = -hbar_00. Since the trace of
hbar is -h (in 4D), h = -hbar and h_{mu nu} = hbar_{mu nu} - (1/2) eta_{mu nu} hbar:
- h_00 = hbar_00 - (1/2)(-1)(-hbar_00) = hbar_00 / 2 = 2 GM/(c^2 r)
- h_ii = 0 - (1/2)(+1)(-hbar_00) = hbar_00 / 2 = 2 GM/(c^2 r)  (each i, no sum)

**Closed form.** (h00, hii) = (2, 2) in units GM/(c^2 r). g_00 = -(1 - 2 Phi/c^2) with Phi = GM/r
(Newtonian limit recovered: geodesic d^2x/dt^2 = (c^2/2) grad h_00 = -grad(-GM/r)), and
g_ij = (1 + 2 gamma Phi/c^2) delta_ij with **PPN gamma = hii/h00 = 1**.

In code: hbar_00 coefficient = 16 pi * (1/(4 pi)) = 4 is computed as Fraction(16) * Fraction(1, 4)
(the 4 pi of Poisson's Green function cancels the 4 pi of 16 pi G exactly), and the trace reversal
is done component by component with the Fraction metric eta.

**Second route.** Momentum space via P2: h_{mu nu}(q) = (16 pi G/q^2)(T_{mu nu} - (1/2) eta_{mu nu} T)
= (16 pi G / q^2) P_{mu nu rho sigma} T^{rho sigma} (P2's numerator acting on T1 gives exactly the
trace-reversed source). For T1 = (1,0,0,0): P.T1 has components (1/2, 1/2, 1/2, 1/2) on the diagonal,
so h00 : hii = 1 : 1 and h00 = 16 pi * (1/2) / (4 pi) = 2. The self-check builds P as a 4^4 tensor
and contracts it with T1 independently of the closed-form trace reversal.

---------------------------------------------------------------------------------------------------
## 2. tpt(T1, T2) -> Fraction: T2^{mu nu} P_{mu nu rho sigma} T1^{rho sigma}, diagonal T

Indices are raised/lowered with eta (P has all indices down, T both up). For diagonal
T^{mu nu} = diag(a0, a1, a2, a3) = T1 and diag(b0, ..., b3) = T2:
- term 1: eta_{mu rho} eta_{nu sigma} T2^{mu nu} T1^{rho sigma} = sum_mu eta_mumu^2 b_mu a_mu = sum_mu a_mu b_mu
- term 2: identical by symmetry of diagonal T: sum_mu a_mu b_mu
- term 3: (eta_{mu nu} T2^{mu nu})(eta_{rho sigma} T1^{rho sigma}) = tr(T2) tr(T1), tr(T) = -T^00 + T^11 + T^22 + T^33.

**Closed form.** tpt = sum_mu a_mu b_mu - (1/2) tr(T1) tr(T2). Manifestly symmetric in T1 <-> T2
(P_{mu nu rho sigma} = P_{rho sigma mu nu}).

**Couplings.**
- static mass: T = M c^2 (1, 0, 0, 0): tr = -1, tpt(T, T) = 1 - 1/2 = **1/2** (per unit M1 M2 c^4).
- photon (energy E along z; T^{00} = T^{33} = E, traceless): with a static mass,
  tpt(T_m, T_ph) = 1*1 - (1/2)(-1)(0) = **1**.
- ratio photon/mass = **2**: light couples twice as strongly as a slow mass of the same energy.
  The tracelessness of the photon kills the -1/2 tr tr term that halves the mass-mass coupling.

**Second route.** (a) Build P as an explicit 4x4x4x4 Fraction tensor from the eta's and do the full
quadruple sum (self-check) - must equal the closed form for random diagonal T's. (b) The photon
ratio from the metric of section 1: a photon couples to h_{mu nu} T^{mu nu} = E (h00 + h33), a slow
mass to M c^2 h00; ratio (h00 + hii)/h00 = 1 + gamma = 2, i.e. light deflection 4GM/(c^2 b),
twice the Newtonian 2GM/(c^2 b). Two independent routes (P2 contraction vs P1 metric) agree.

---------------------------------------------------------------------------------------------------
## 3. Static potential between two masses: why U = -4 pi G m1 m2 * chiral.yukawa(r, 0)

From section 1's second route, the field of body 1 in momentum space is
h^{(1)}_{mu nu}(q) = (16 pi G / q^2) (P T1)_{mu nu}, with T1 the Fourier transform of the
source (for a point mass at rest, T1^{00}(q) = m1 c^2 e^{-i q.x1}). The interaction energy
U = -(1/2) Int h^{(1)}_{mu nu} T2^{mu nu} becomes, per unit of the Fourier factor,

  U(q) = -(1/2)(16 pi G / q^2) T2.P.T1 / c^4 = -8 pi G tpt(T1, T2) / q^2   (T in units m c^2)

For two static masses tpt = (1/2) m1 m2, so U(q) = -4 pi G m1 m2 / q^2. Going back to position
space needs the inverse transform of 1/q^2, which is by definition rung 2's exchange transform at
zero mass: Int d^3q/(2 pi)^3 e^{i q.r}/q^2 = chiral.yukawa(r, 0) = 1/(4 pi r)
(check: (lap - 0) yukawa = -delta^3, matching the -q^2 * (1/q^2) = -1 in Fourier space). Therefore

  **U(r) = -8 pi G tpt(T_m1, T_m2) * chiral.yukawa(r, 0) = -4 pi G m1 m2 * chiral.yukawa(r, 0) = -G m1 m2 / r.**

Newton's law (and its sign: attraction, because tpt > 0 and the exchanged spin-2 field couples
with the same sign to like sources) is an output, not an assumption. In code the coefficient
-8 pi G tpt((1,0,0,0),(1,0,0,0)) m^2 is computed by calling `tpt` and multiplied by
`chiral.yukawa(r, 0)` at every sample.

**Second route.** Position space directly from section 1: U = -(1/2) m2 c^2 h00^{(1)}(r) =
-(1/2) m2 c^2 * 2 G m1/(c^2 r) = -G m1 m2/r. Same answer; the blind check compares with explicit 1/r.

---------------------------------------------------------------------------------------------------
## 4. ramp_profile(t, hold, ramp) -> s in [0, 1]

SPEC 5 verbatim: T = hold + 2 ramp; s = up(t/ramp) for t < ramp; 1 for ramp <= t <= ramp + hold;
up((T - t)/ramp) for t > ramp + hold; up(x) = 2x^2 (x < 1/2), 1 - 2(1-x)^2 (x >= 1/2).

**Clamp.** I clamp the argument x to [0, 1] before applying up (then up maps [0,1] onto [0,1]
monotonically, so the result is in [0, 1]). This is what makes s = 0 for t <= 0 and t >= T
(without clamping x, up(x<0) = 2x^2 > 0 would re-open the branches after T). See QUESTIONS.

Properties (derivation of the shape): up(0) = 0, up(1/2) = 1/2 from both pieces, up(1) = 1;
up'(x) = 4x and 4(1-x): continuous (= 2 at x = 1/2), zero at both ends - a C^1 minimum-jerk-like
"bang-bang" acceleration profile (constant acceleration +4/ramp^2 then -4/ramp^2 in units dx/2).
Ramp-down is the time mirror of ramp-up: s(T - t) = s(t).

**Second route.** Symmetry s(T - t) = s(t) and the exact integral Int_0^1 up dx = 1/2 (Fraction:
Int_0^{1/2} 2x^2 = 1/12, Int_{1/2}^1 [1 - 2(1-x)^2] = 1/2 - 1/12 = 5/12, sum 1/2) checked against
toolkit.trapezoid over sampled ramp_profile.

---------------------------------------------------------------------------------------------------
## 5. entangling_phase(m, dx, hold, ramp, gap, n=4001)

**Geometry (SPEC 4, 5).** Each diamond in superposition of +-y(t) along a line perpendicular to the
line joining them (parallel geometry). Same-side branch pairs (LL, RR) stay at distance gap;
opposite pairs (LR, RL) are at sqrt(gap^2 + (2y)^2), 2y = dx s(t) (full separation dx in the hold).

**Branch phases.** In the joint state (1/2) sum_{ij} |i>|j>, each branch pair evolves under its
own (classical, static-exchange) potential: |i j> -> exp(i phi_ij)|i j>,
phi_ij = -(1/hbar) Int_0^T U(d_ij(t)) dt (Schroedinger phase e^{-i E t/hbar}).

**Why Delta phi = phi_LL + phi_RR - phi_LR - phi_RL is the observable.** The state
(1/2) sum e^{i phi_ij}|i>|j> is unchanged (up to global phase) by local phase redefinitions
|i>_1 -> e^{i a_i}|i>_1, |j>_2 -> e^{i b_j}|j>_2, i.e. phi_ij -> phi_ij + a_i + b_j (these also absorb
each diamond's own self-energy and any potential depending on one body only). The combination
phi_LL + phi_RR - phi_LR - phi_RL is the unique (up to scale) linear invariant of that shift. The
2x2 coefficient matrix C_ij = e^{i phi_ij}/2 has det C = (1/4) e^{i(phi_LL+phi_RR)}(1 - e^{-i Delta phi}),
so the state is a product state iff Delta phi = 0 mod 2 pi, and the concurrence is
2|det C| = |sin(Delta phi / 2)|. Delta phi is what a witness measures.

**Summing over the four pairs.**
Delta phi = (1/hbar) Int_0^T [-U(d_LL) - U(d_RR) + U(d_LR) + U(d_RL)] dt,
and with U from section 3:
Delta phi = (G m^2/hbar) Int_0^T 2 [1/gap - 1/sqrt(gap^2 + (2y)^2)] dt   (positive: LL/RR are closer).

**Numerics.** n samples t_k = T k/(n-1), dt = T/(n-1); integrand w_k = -U(gap) - U(gap) +
U(d_LR(t_k)) + U(d_RL(t_k)) with U = -8 pi G tpt m^2 chiral.yukawa(d, 0) evaluated at call time
(inputs.G_NEWTON, inputs.HBAR); Delta phi = toolkit.trapezoid(w, dt)/inputs.HBAR.

Scalings (exact in the formula): proportional to m^2, G, 1/hbar; linear in hold (the hold adds
2 (1/gap - 1/sqrt(gap^2+dx^2)) G m^2/hbar per second; the trapezoid error is in the ramps only and
changes by O(dt^2) as hold changes the grid).

**Closed form / second route.** Splitting [0, T] at the profile's smooth pieces,
Delta phi = (2 G m^2/hbar) [ hold f(dx) + 2 ramp Int_0^1 f(dx up(x)) dx ],  f(a) = 1/gap - 1/sqrt(gap^2 + a^2)
(the two ramps contribute equally by s(T - t) = s(t)). The ramp integral is elliptic (not elementary);
the second route evaluates it on the two smooth pieces [0, 1/2], [1/2, 1] of up, where the integrand
is analytic, by Richardson-extrapolated toolkit.trapezoid (= composite Simpson, O(h^4)), with the
hold term exact. The main route (single trapezoid across the kinks of s'' at t = ramp/2, ramp, ...)
converges as O(1/n^2) to it; the self-check prints the table in n.

**Small-separation limit (exact).** For dx << gap, f(a) = a^2/(2 gap^3) + O(a^4), so
Delta phi -> (G m^2 dx^2/(hbar gap^3)) [hold + 2 ramp Int_0^1 up^2 dx], with
Int_0^1 up^2 = Int_0^{1/2} 4x^4 + Int_0^{1/2} (1 - 4u^2 + 4u^4) du = 1/40 + 43/120 = 23/60 (Fraction,
computed by exact polynomial integration in the self-check). The ratio numerics/limit -> 1 with
deviation O((dx/gap)^2).

---------------------------------------------------------------------------------------------------
## 6. design_phase()

gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION) (rung 3), then
entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD, inputs.DESIGN_A_RAMP, gap)
with the default n = 4001. Everything read at call time, so changing EPS_DIAMOND moves the gap
(lower eps -> weaker Casimir -> smaller gap -> larger phase).

**Second route.** The Simpson/hold-analytic evaluation of section 5 at the same gap, and the n -> oo
extrapolation of the trapezoid table.

Nothing in this stage was quoted; nothing was left underived.

---------------------------------------------------------------------------------------------------
## 7. Self-check results (python3 graviton.py)

- h00 = hii = 2, gamma = 1; P.T1 route gives (2, 2, 2, 2) on the diagonal.
- tpt: mass-mass 1/2, mass-photon 1 (ratio 2), equal to the explicit 4^4 tensor contraction and
  symmetric for 50 random rational pairs; metric route (h00 + hii)/h00 = 2.
- Probe (1e-14, 5e-4, 0.1, 1.0, 2e-4): trapezoid 0.4569018415750, piecewise Simpson 0.4569018415821.
- Small-dx limit (dx = 1e-7, gap = 2e-4): Int up^2 = 23/60; numerics/limit - 1 = -1.5e-7, of order
  (dx/gap)^2 = 2.5e-7 as expected for the next term of f.
- Design A at the safe gap 1.811072782572763e-4 m: design_phase = 2.18778676033019 rad, second route
  2.1877867603092453 rad (rel 9.6e-12 at n = 4001). The trapezoid error is not a clean c/n^2 sequence:
  the integrand is C^1 with f' = 0 at t = 0, T (s' = 0 there, so the Euler-Maclaurin end term vanishes);
  the error comes from the jumps of s'' at t = ramp/2, ramp, ramp + hold, ramp + hold + ramp/2, and
  depends on where those fall relative to the grid. Bounded by O(n^-2), observed smaller.
