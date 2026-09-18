# Domain Wall Energy: Why a Symmetry-Breaking Scalar Must Be Complex, Not Real

**Document Type:** Standard field-theory calculation (cosmology)
**Status:** Verified, self-contained

---

## 1. The Problem Statement

A common construction in field theory posits a scalar field that spontaneously breaks a
symmetry as it varies across space (e.g. along a compactified or cosmological direction).
A natural question: can that field be a single real scalar, or must it be complex
(a doublet)?

This note shows that a real scalar with a simple symmetry-breaking potential produces
domain walls with catastrophic energy density, ruled out by standard cosmological bounds,
while a complex (winding) field configuration avoids the problem entirely. This is a
textbook argument (Zel'dovich, Kobzarev & Okun 1974; Vilenkin & Shellard 2000) worked
through explicitly with numbers.

---

## 2. Real Scalar Field Domain Wall Derivation

### 2.1 Setup

Consider a real scalar field R with the standard double-well potential:

```
V(R) = (lambda/4)(R^2 - v^2)^2
```

**Vacuum structure:**
- Minimum at R = +v (true vacuum)
- Minimum at R = -v (true vacuum)
- Maximum at R = 0 (unstable)

The potential barrier height is:
```
V(0) - V(+/-v) = (lambda/4) v^4
```

### 2.2 Energy Functional

The total energy for a static configuration R(x) varying in one spatial direction:

```
E = integral dx [ (1/2)(dR/dx)^2 + V(R) ]
```

where the first term is gradient (kinetic) energy and the second is potential energy.

### 2.3 Equation of Motion

Minimizing E via Euler-Lagrange:

```
d^2R/dx^2 = dV/dR = lambda R (R^2 - v^2)
```

### 2.4 First Integral (Bogomolny Trick)

Multiply by dR/dx and integrate:

```
(1/2)(dR/dx)^2 = V(R) + C
```

For a domain wall interpolating from R(-infinity) = -v to R(+infinity) = +v, the boundary
conditions require C = 0:

```
(1/2)(dR/dx)^2 = V(R)
```

Therefore:
```
dR/dx = +/- sqrt(2V(R)) = +/- sqrt(lambda/2) |R^2 - v^2|
```

Taking the + sign for the kink (wall going from -v to +v):
```
dR/dx = sqrt(lambda/2) (v^2 - R^2)   [for |R| < v]
```

### 2.5 Wall Profile Solution

Separating variables:
```
integral dR / (v^2 - R^2) = sqrt(lambda/2) integral dx
```

Using the identity: integral dR/(v^2 - R^2) = (1/v) artanh(R/v)

```
(1/v) artanh(R/v) = sqrt(lambda/2) (x - x_0)
```

Therefore:
```
R(x) = v tanh[(x - x_0) / delta]
```

where the **wall thickness** is:
```
delta = sqrt(2/lambda) / v = sqrt(2) / (sqrt(lambda) v)
```

### 2.6 Surface Tension Calculation

The surface tension (energy per unit area) is:

```
sigma = integral_{-infinity}^{+infinity} dx [ (1/2)(dR/dx)^2 + V(R) ]
```

Using the Bogomolny relation (1/2)(dR/dx)^2 = V(R):

```
sigma = integral dx [ 2 * (1/2)(dR/dx)^2 ]
      = integral dx (dR/dx)^2
      = integral dR (dR/dx)
      = integral_{-v}^{+v} sqrt(2V(R)) dR
```

Substituting V(R):
```
sigma = integral_{-v}^{+v} sqrt(lambda/2) |R^2 - v^2| dR
      = sqrt(lambda/2) integral_{-v}^{+v} (v^2 - R^2) dR
      = sqrt(lambda/2) [v^2 R - R^3/3]_{-v}^{+v}
      = sqrt(lambda/2) [(v^3 - v^3/3) - (-v^3 + v^3/3)]
      = sqrt(lambda/2) [2v^3 - 2v^3/3]
      = sqrt(lambda/2) * (4v^3/3)
```

**Final result for surface tension:**
```
sigma = (2 sqrt(2) / 3) sqrt(lambda) v^3
```

Or equivalently:
```
sigma = (4/3) v^3 / delta
```

---

## 3. Explicit Numerical Calculation

### 3.1 Input Parameters

For a GUT/Planck-scale scalar field (illustrative choice — the argument is scale-independent
qualitatively, see Section 8):

| Parameter | Symbol | Value |
|-----------|--------|-------|
| VEV | v | 10^18 GeV (GUT/Planck scale) |
| Coupling | lambda | 1 (O(1) natural value) |

### 3.2 Wall Thickness

```
delta = sqrt(2/lambda) / v
      = sqrt(2) / (sqrt(1) * 10^18 GeV)
      = 1.414 / 10^18 GeV
      = 1.414 * 10^{-18} GeV^{-1}
```

Converting to meters (using hbar*c = 1.97 * 10^{-16} GeV*m):
```
delta = 1.414 * 10^{-18} GeV^{-1} * (1.97 * 10^{-16} GeV*m)
      = 2.8 * 10^{-34} m
      ~ 17.3 * l_Planck
```

The wall is about 17 times larger than the Planck length (using l_Planck = 1.616e-35 m).

### 3.3 Surface Tension

```
sigma = (2 sqrt(2) / 3) * sqrt(lambda) * v^3
      = (2 * 1.414 / 3) * 1 * (10^18 GeV)^3
      = 0.943 * 10^54 GeV^3
      ~ 10^54 GeV^3
```

### 3.4 Unit Conversion

Surface tension has dimensions of [Energy]/[Area] = [Energy]^3 in natural units.

```
sigma^{1/3} ~ 10^18 GeV ~ 10^21 times above 1 MeV
```

---

## 4. Cosmological Constraints on Domain Walls

### 4.1 Domain Wall Domination

Domain walls, once formed, scale as:
```
rho_wall ~ sigma / t
```

where t is cosmic time. In contrast:
- Radiation: rho_rad ~ 1/t^2
- Matter: rho_mat ~ 1/t^{3/2}

**Domain walls dilute slower than matter or radiation**, eventually dominating the universe.

### 4.2 The Zel'dovich-Kobzarev-Okun Bound

The classic constraint (Zel'dovich, Kobzarev, Okun 1974): domain walls must not dominate
before matter-radiation equality. This requires:
```
sigma < (1 MeV)^3 = (10^{-3} GeV)^3 = 10^{-9} GeV^3
```

### 4.3 More Stringent Modern Bounds

CMB observations constrain domain walls more strongly (Planck 2018):
```
sigma < (few MeV)^3
```

For stable domain walls (not annihilating):
```
sigma < (100 keV)^3 ~ 10^{-12} GeV^3
```

### 4.4 Comparison: Calculated vs. Allowed

| Quantity | Calculated | Allowed | Ratio |
|----------|------------|---------|-------|
| sigma | 9.43x10^53 GeV^3 | 10^{-9} GeV^3 | ~10^63 |
| sigma^{1/3} | 10^18 GeV | 10^{-3} GeV | 10^21 |

**The real scalar domain wall exceeds cosmological bounds by approximately 63 orders
of magnitude.** The qualitative conclusion — real-scalar domain walls at a high symmetry-
breaking scale are catastrophically ruled out — is robust; only the precise exponent
depends on the illustrative v chosen above.

---

## 5. The Catastrophe in Detail

### 5.1 Energy Density at Formation

If domain walls form at the GUT scale T ~ 10^16 GeV:

```
rho_wall(formation) ~ sigma * H
                    ~ 10^54 GeV^3 * 10^{-6} GeV (Hubble at GUT scale)
                    ~ 10^48 GeV^4
```

Compare to radiation energy density at GUT scale:
```
rho_rad ~ T^4 ~ 10^64 GeV^4
```

Initially, walls are subdominant, but they dilute more slowly than radiation and would
come to dominate at very early times.

### 5.2 Universe Overclosure

```
Omega_wall = rho_wall / rho_critical ~ (sigma/t) / (3 H^2 M_Pl^2)
```

For sigma ~ 10^54 GeV^3 and t ~ 10^17 s (today): Omega_wall >> 1.

**Domain walls at this scale would have overclosed the universe long ago.**

### 5.3 Observable Consequences (If They Existed)

Had such walls existed: the universe would collapse before nucleosynthesis, there would
be no observable CMB, and no galaxies, stars, or planets could form.

---

## 6. Why a Complex (Doublet) Field Solves the Problem

### 6.1 Complex Field Definition

Instead of a single real scalar R, use a complex field (equivalently, a two-component
real doublet):
```
R = (R_1, R_2) with |R|^2 = R_1^2 + R_2^2
```

In polar form: R_1 = rho cos(phi), R_2 = rho sin(phi).

### 6.2 Vacuum Manifold

**Single real scalar:**
- Vacuum: R = +/-v (two disconnected points)
- pi_0(vacuum) = Z_2 (non-trivial)
- **Domain walls exist** (walls separate +v and -v regions)

**Complex field:**
- Vacuum: |R| = v (a circle S^1)
- pi_0(vacuum) = 0 (trivial, circle is connected)
- **No domain walls** (any two points on the circle connect continuously)

### 6.3 Energy Comparison

**Single real scalar on a circle with a Z_2 identification:**
```
R(X=0) = -v  -->  R(X=L/2) = +v  -->  R(X=L) = -v
```
Contains two domain walls with total energy:
```
E_wall = 2 * sigma * A ~ 2 * 10^54 GeV^3 * A
```

**Complex field (helix/winding configuration):**
```
R_1(X) = v cos(2 pi X / L)
R_2(X) = v sin(2 pi X / L)
|R| = v (constant everywhere!)
```

Energy is purely from gradient in the phase angle phi:
```
E_winding = integral dX (1/2) |dR/dX|^2
          = integral dX (1/2) v^2 (d phi/dX)^2
          = (1/2) v^2 (2 pi / L)^2 * L
          = 2 pi^2 v^2 / L
```

### 6.4 Energy Ratio

```
E_wall / E_winding ~ (sigma * A) / (v^2/L)
                   ~ (sqrt(lambda) v^3 * A) / (v^2/L)
                   ~ sqrt(lambda) v * A * L
```

For A ~ L^2 (typical cosmological scales): E_wall / E_winding ~ sqrt(lambda) v L^3 >> 1.

**The winding (complex-field) configuration has vastly lower energy than the domain-wall
configuration.** This is the standard argument for why symmetry-breaking scalars that vary
along a compact or cosmological direction should be complex-valued rather than real-valued.

---

## 7. Mathematical Summary

**Wall thickness:** delta = sqrt(2) / (sqrt(lambda) v)

**Surface tension:** sigma = (2 sqrt(2) / 3) sqrt(lambda) v^3

**Cosmological bound:** sigma < (1 MeV)^3 = 10^{-9} GeV^3

**Required VEV for marginal viability of a real-scalar wall:**
```
v_max = (sigma_max / sqrt(lambda))^{1/3} ~ (10^{-9})^{1/3} ~ 10^{-3} GeV
```

This is far below any GUT/Planck-scale symmetry breaking, confirming that a real scalar
breaking a symmetry at high scales is cosmologically excluded, while the complex-field
(winding) alternative is not.

---

## 8. Appendix: Detailed Numerical Checks

### 8.1 Wall Profile Verification

For R(x) = v tanh(x/delta):

- At x = 0: R(0) = v tanh(0) = 0 (wall center)
- At x = +/- delta: R(+/-delta) = v tanh(+/-1) = +/-0.762 v
- At x = +/- 3*delta: R(+/-3*delta) = v tanh(+/-3) = +/-0.995 v (essentially vacuum)

The wall is concentrated within ~3*delta of the center.

### 8.2 Energy Integration Check

Direct integration of E = integral dx [(1/2)(dR/dx)^2 + V(R)] with
R(x) = v tanh(x/delta), delta = sqrt(2/lambda)/v:

```
dR/dx = (v/delta) sech^2(x/delta)
(dR/dx)^2 = (v^2/delta^2) sech^4(x/delta)
V(R) = (lambda/4) v^4 sech^4(x/delta)
```

Check: (1/2)(dR/dx)^2 = (v^2)/(2*delta^2) sech^4 = (lambda v^4/4) sech^4 = V(R). Consistent.

```
E = integral_{-inf}^{+inf} dx [2 V(R)]
  = (lambda v^4/2) integral dx sech^4(x/delta)
  = (lambda v^4/2) * delta * (4/3)
  = (2/3) lambda v^4 delta
  = (2 sqrt(2)/3) sqrt(lambda) v^3   [matches Section 2.6]
```

### 8.3 Numerical Value Summary

| Quantity | Formula | Numerical Value |
|----------|---------|-----------------|
| v | Input | 10^18 GeV |
| lambda | Input | 1 |
| delta | sqrt(2/lambda)/v | 1.4e-18 GeV^-1 (2.8e-34 m) |
| sigma | (2sqrt(2)/3) sqrt(lambda) v^3 | 0.94e54 GeV^3 |
| Bound on sigma | ZKO constraint | < 1e-9 GeV^3 |
| Violation factor | sigma / sigma_bound | ~1e63 |

---

## References

1. Zel'dovich, Ya. B., Kobzarev, I. Yu., Okun, L. B. (1974). "Cosmological consequences of a
   spontaneous breakdown of a discrete symmetry." Zh. Eksp. Teor. Fiz. 67, 3-11
   [Sov. Phys. JETP 40, 1-5 (1975)].
2. Vilenkin, A., Shellard, E. P. S. (2000). "Cosmic Strings and Other Topological Defects."
   Cambridge University Press.
3. Kibble, T. W. B. (1976). "Topology of cosmic domains and strings." J. Phys. A 9, 1387.
4. Planck Collaboration (2018). "Planck 2018 results. VI. Cosmological parameters."
   arXiv:1807.06209.
</content>
