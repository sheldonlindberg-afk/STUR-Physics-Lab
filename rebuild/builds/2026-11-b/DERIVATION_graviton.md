# DERIVATION: stage `graviton` (build 2026-11-b)

Written before the code. Postulates: SPEC.md section 5 (linearized GR, one-graviton exchange, branch profile,
phase), section 4 (parallel geometry), "Connections" (rung 2 -> 4, rung 3 -> 4). Signature eta = diag(-1,1,1,1).
Units: c = 1 inside the tensor algebra (restored at the end); SI for the phase.

Nothing here is quoted. Nothing could not be derived.

## 0. Common ground: the static solution of the field equation

Postulates (SPEC 5): g = eta + h, hbar_mn = h_mn - (1/2) eta_mn h, box hbar_mn = -16 pi G T_mn, matter coupling
L_int = (1/2) h_mn T^mn.

(0.1) Trace reversal is its own inverse in 4 dimensions. Taking the trace of hbar_mn = h_mn - (1/2) eta_mn h:
hbar = h - (1/2)(4) h = -h. Hence h_mn = hbar_mn - (1/2) eta_mn hbar.

(0.2) For a static source box -> laplacian, so lap hbar_mn = -16 pi G T_mn. Rung 2's exchange transform
Y(r) = `chiral.yukawa(r, 0)` is defined by (lap - m^2) Y = -delta^3 at m = 0, i.e. lap Y = -delta^3
(Y = 1/(4 pi r); this is the Fourier transform of 1/q^2). By linearity, for a point source
T_mn(x) = tau_mn delta^3(x) (tau_mn = the space integral of T_mn):

    hbar_mn(r) = 16 pi G Y(r) tau_mn.

(0.3) Using (0.1): h_mn = 16 pi G Y(r) [tau_mn - (1/2) eta_mn tau], tau = eta^ab tau_ab.
With P_mnrs = (1/2)(eta_mr eta_ns + eta_ms eta_nr - eta_mn eta_rs) and symmetric tau:
P_mnrs tau^rs = (1/2)(tau_mn + tau_nm - eta_mn tau) = tau_mn - (1/2) eta_mn tau. So

    h_mn(r) = 16 pi G Y(r) P_mnrs tau^rs.                                    (A)

This is why P is the numerator of the graviton propagator: it is the trace-reversal operator.

## 1. `point_mass_metric() -> (h00, hii)` in units of GM/(c^2 r)

Postulates: SPEC 5, first bullet. Source: mass M at rest, T^00 = M delta^3, all other components zero.
tau_00 = eta_00 eta_00 tau^00 = M. tau = eta^00 tau_00 = -M.

Route 1 (field equation, then undo the trace reversal).
- hbar_00 = 16 pi G M Y = 16 pi G M /(4 pi r) = 4 GM/r; hbar_0i = hbar_ij = 0. The rational coefficient is
  16 (field equation, in units of pi G) x 1/4 (Green function, in units of 1/pi) = 4.
- hbar = eta^00 hbar_00 = -4 GM/r.
- h_00 = hbar_00 - (1/2)(-1)(-4GM/r) = (4 - 2) GM/r = 2 GM/r.
- h_ii = 0 - (1/2)(+1)(-4GM/r) = 2 GM/r  (each i, no sum).

Result (restoring c: G -> G/c^2 for a mass source): **h00 = hii = 2**, PPN gamma = hii/h00 = 1.

Route 2 (independent check, done in `__main__`): (A) directly, h_mn = 16 pi G Y (P tau)_mn with the rank-4
tensor P built explicitly from eta: (P tau)_00 = M - (1/2)(-1)(-M) = M/2, (P tau)_ii = 0 - (1/2)(1)(-M) = M/2,
times 16/4 = 4 gives (2, 2). Route 3 (physical): a slow test mass has L = -m sqrt(-g_mn u^m u^n) ~ -m + (1/2) m h_00
so its potential energy is -(1/2) m h_00; h_00 = 2GM/r gives -GMm/r, Newton, and h_00 = -2 Phi.

In code, route 1 is carried out in Fractions (coefficients 16 and 1/4, the explicit eta); route 2 uses `tpt`'s
P tensor; `__main__` also checks numerically that 16 pi * chiral.yukawa(1, 0) = 4.

## 2. `tpt(T1, T2) -> T2.P.T1`

Postulate: SPEC 5, second bullet. T2^mn P_mnrs T1^rs with both stress tensors diagonal with upper indices,
T^mn = diag(T^00, T^11, T^22, T^33).

Main route (code): build P_mnrs = (1/2)(eta_mr eta_ns + eta_ms eta_nr - eta_mn eta_rs) explicitly and sum over
all four indices; only m = n, r = s contribute for diagonal tensors. All arithmetic in Fractions (ints and
Fractions in -> Fraction out).

Closed form: eta_mr eta_ns T2^mn T1^rs = sum_m (eta_mm)^2 T2^mm T1^mm = sum_m T2^mm T1^mm (signs square away), and
eta_mn T^mn = -T^00 + T^11 + T^22 + T^33 =: tr T, so

    T2.P.T1 = sum_m T2^mm T1^mm - (1/2) tr T2 tr T1.

Second route (in `__main__`): this closed form vs. the explicit 4-index contraction on random Fraction tuples;
symmetry under T1 <-> T2 (P_mnrs = P_rsmn); and the identity "traceless source": for a photon-like
T = (1,0,0,1), tr T = 0 so T.P.T' = sum only.
Consequences: static masses T = (1,0,0,0): T.P.T = 1 - 1/2 = 1/2. Mass and light (1,0,0,1): 1 - 0 = 1. Ratio 2
(light bending is twice the Newtonian value).

## 3. The exchange potential (not exported, but everything below rests on it)

Postulates: SPEC 5 bullets 1-2 and "Rung 2 -> 4".

Source 1 creates the field (A). Source 2, a point source with integrated stress tau2^mn, couples through
L_int = (1/2) h_mn T2^mn, so its interaction Lagrangian is L = (1/2) h_mn(r) tau2^mn and, for static sources,
the interaction energy is U = -L:

    U(r) = -(1/2) (16 pi G) Y(r) tau2^mn P_mnrs tau1^rs = -8 pi G (T2.P.T1) Y(r).           (B)

The factor 1/2 (coupling) x 16 pi G (field equation) = 8 pi G is the normalization SPEC says the two postulates
fix. No double counting: (1/2) h T with h the field of the *other* body is exactly the cross term of the
quadratic action evaluated on the solution (same result as the test-particle route 3 of section 1).

For two masses at rest (speeds here are ~ dx/ramp ~ 1e-3 m/s, corrections O(v^2/c^2) ~ 1e-23 are dropped):
tau_i^mn = m_i c^2 diag(1,0,0,0), and G -> G/c^4, so the c's cancel and T2.P.T1 = m1 m2 * tpt(e, e) with
e = (1,0,0,0), tpt(e, e) = 1/2:

    U(r) = -8 pi G m1 m2 (1/2) Y(r) = -4 pi G m1 m2 chiral.yukawa(r, 0) = -G m1 m2 / r.

This reproduces SPEC's connection formula and Newton's law; the code evaluates (B) with `tpt` and
`chiral.yukawa(r, 0)` and never writes 1/r.

Second route: (i) the flux of -grad Y through a sphere is 1 (Gauss), checked by finite differences in
`__main__`: -4 pi r^2 dY/dr = 1; (ii) U(r) r / (G m^2) = -1 printed.

## 4. `ramp_profile(t, hold, ramp) -> s(t)`

Postulate: SPEC 5 "Branch profile", verbatim. T = hold + 2 ramp, clamp(x) = min(1, max(0, x)),
up(x) = 2x^2 (x < 1/2), 1 - 2(1-x)^2 (x >= 1/2).

    s(t) = up(clamp(t/ramp))          t < ramp
         = 1                          ramp <= t <= ramp + hold
         = up(clamp((T - t)/ramp))    t > ramp + hold

Properties (the second route, checked in `__main__`): up(0) = 0, up(1/2) = 1/2 from both pieces (continuous),
up(1) = 1, up'(x) = 4x and 4(1-x) (continuous at 1/2, zero at both ends: smooth start/stop, constant
acceleration magnitude); up(x) + up(1-x) = 1; time-reversal symmetry s(t) = s(T - t); s = 0 for t <= 0 and
t >= T by the clamp.
Edge case not in SPEC: ramp = 0 (no ramp). Then the profile is the limit, s = 1 on [0, T] and 0 outside.

## 5. `entangling_phase(m, dx, hold, ramp, gap, n)`

Postulates: SPEC 4 (parallel geometry, phase of a potential), SPEC 5 "Phase", and (B).

Geometry. The two masses sit a distance `gap` apart along x. Each is split along y into branches at
+-y(t), y(t) = (dx/2) s(t). Branch pair (a, b), a, b in {L, R}: same side -> distance d_LL = d_RR = gap;
opposite sides -> transverse offset 2y, d_LR = d_RL = sqrt(gap^2 + (2y)^2) = sqrt(gap^2 + dx^2 s^2).

Phase. Branch pair (a, b) evolves with e^{-i/hbar int U(d_ab) dt}: phi_ab = -(1/hbar) int_0^T U(d_ab(t)) dt.
The state sum_ab e^{i phi_ab}|a>|b>/2 is a product state iff phi_LL + phi_RR - phi_LR - phi_RL = 0, so

    Delta phi = phi_LL + phi_RR - phi_LR - phi_RL
              = (1/hbar) int_0^T [ -2 U(gap) + 2 U(d_LR(t)) ] dt .

With (B) for equal masses, U(r) = -8 pi G m^2 tpt(e,e) Y(r):

    Delta phi = (8 pi G m^2 tpt(e,e) / hbar) int_0^T 2 [ Y(gap) - Y(sqrt(gap^2 + (2y)^2)) ] dt
              = (G m^2 / hbar) int_0^T 2 [ 1/gap - 1/sqrt(gap^2 + (2y(t))^2) ] dt  >= 0,

which is SPEC's formula, now derived. Numerics: t_i = T i/(n-1), i = 0..n-1, integrand sampled at t_i,
`toolkit.trapezoid(samples, T/(n-1))`. Y is `chiral.yukawa(., 0)` at call time; G, hbar read from `inputs` at
call time. Scalings: ~ m^2, ~ G, ~ 1/hbar exactly; during the hold the integrand is constant, so the phase is
linear in `hold` up to trapezoid error at the hold/ramp joints.

No closed form for the ramp part (the integral of 1/sqrt(g^2 + dx^2 up(x)^2) is an elliptic-type integral).
Second routes (all in `__main__`):
 (a) different numerical method: composite Simpson on each smooth piece (the two half-ramps of each ramp and the
     hold) with an explicit 1/r integrand, not through yukawa or toolkit.trapezoid; the pieces are joined at the
     kinks of s'' so Simpson converges at 4th order, while the n = 4001 trapezoid has O(h^2) error.
 (b) limit ramp -> 0: Delta phi = (G m^2/hbar) 2 hold [1/gap - 1/sqrt(gap^2 + dx^2)] (closed form).
 (c) limit dx << gap: 1/gap - 1/sqrt(gap^2 + dx^2 s^2) -> dx^2 s^2/(2 gap^3), so
     Delta phi -> (G m^2/hbar)(dx^2/gap^3)(hold + 2 ramp I2), I2 = int_0^1 up(x)^2 dx
     = int_0^{1/2} 4x^4 dx + int_0^{1/2} (1 - 2u^2)^2 du = 1/40 + (1/2 - 1/6 + 1/40) = 23/60
     (computed exactly in Fractions in `__main__`, not typed in).

## 6. `design_phase()`

Postulate: SPEC 5 last bullet and "Rung 3 -> 4". Pure composition:

    gap = casimir.casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                   inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
    design_phase = entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD,
                                    inputs.DESIGN_A_RAMP, gap)        (default n)

The design parameters are inputs (an engineering choice); the gap is rung 3's derived root; the phase is section 5.
Second route: Simpson route (a) at the same gap; and monotonicity: a weaker Casimir background (smaller eps)
gives a smaller gap and a larger phase, since d(Delta phi)/d(gap) < 0 (each of 1/g - 1/sqrt(g^2 + a^2) decreases
in g for a != 0).

## 7. Outcome of the second routes (after implementation; `python3 graviton.py`)

- point_mass_metric: trace-reversal route and propagator route both give (2, 2) exactly.
- tpt: explicit contraction = closed form, and symmetric, on 200 random Fraction pairs (difference exactly 0).
- potential: Gauss flux 1 to 1e-11; U r/(G m1 m2) = -1.
- entangling_phase at design A and the Casimir-safe gap: trapezoid (n = 4001, via yukawa) and piecewise Simpson
  (explicit 1/r) agree to 1e-11 relative; trapezoid n = 2001/4001/8001 converge at second order.
  ramp -> 0 limit agrees with its closed form to 1e-16; dx = dx_A/1000 agrees with the leading small-dx form to
  9e-6 relative, the expected O(dx^2/gap^2) correction.
- No derivation error was found by the gate; nothing in sections 0-6 was changed after coding.
