# Domain Wall Energy Calculation: Why STUR Requires a Doublet

**Document Type:** Technical Derivation (Peer Review Ready)
**Version:** 1.0
**Date:** 2026-01-25
**Purpose:** Explicit numerical demonstration that real scalar domain walls are cosmologically forbidden

---

## 1. The Problem Statement

In STUR, the R-field must interpolate between different configurations along the extra dimension X. The question is:

**Can R be a single real scalar, or must it be a doublet?**

This document shows that a single real scalar creates domain walls with catastrophically large energy density, while a doublet (winding) configuration avoids this entirely.

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

where:
- First term: gradient (kinetic) energy
- Second term: potential energy

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

For a domain wall interpolating from R(-infinity) = -v to R(+infinity) = +v, the boundary conditions require C = 0:

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

For a GUT/Planck-scale scalar field relevant to STUR:

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
      ~ 17.3 * l_Planck   [corrected — using l_Planck = 1.616e-35 m, the ratio
                            delta/l_Planck = 17.3, not 0.02. The wall is about 17x
                            LARGER than the Planck length, not smaller.]
```

**The wall is about 17 times larger than the Planck length**, not thinner as
previously (incorrectly) stated — the "sub-Planckian" claim was backwards. This
correction does not affect the paper's main conclusion, which rests on the
surface-tension bound below, not on this length comparison.

### 3.3 Surface Tension

```
sigma = (2 sqrt(2) / 3) * sqrt(lambda) * v^3
      = (2 * 1.414 / 3) * 1 * (10^18 GeV)^3
      = 0.943 * 10^54 GeV^3
      ~ 10^54 GeV^3
```

### 3.4 Unit Conversion

Surface tension has dimensions of [Energy]/[Area] = [Energy]^3 in natural units.

Converting to SI-like units:
```
sigma ~ 10^54 GeV^3
      = 10^54 * (1.6 * 10^{-10} J)^3 / (1.97 * 10^{-16} m)^2
      = 10^54 * 4.1 * 10^{-30} J^3 / (3.9 * 10^{-32} m^2)
      ~ 10^{56} J/m^2
```

Or in terms of mass:
```
sigma^{1/3} ~ 10^18 GeV ~ 10^21 times above 1 MeV   [corrected — dimensionally,
      sigma^{1/3} (GeV) should be compared to 1 MeV (GeV), not (1 MeV)^3;
      10^18 GeV / 10^{-3} GeV = 10^21, consistent with §4.4 below]
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

The classic constraint (Zel'dovich, Kobzarev, Okun 1974):

Domain walls must not dominate before matter-radiation equality. This requires:
```
sigma < (1 MeV)^3 = (10^{-3} GeV)^3 = 10^{-9} GeV^3   [corrected — the previous
      "~10^{-3} GeV^3" treated the linear 1 MeV = 10^{-3} GeV as if it were already
      cubed; independently verified: (10^{-3})^3 = 10^{-9}, a six-order-of-magnitude
      cubing error]
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
| sigma | 9.43×10^53 GeV^3 | 10^{-9} GeV^3 [corrected, was 10^{-3}] | ~10^63 [corrected, was 10^57] |
| sigma^{1/3} | 10^18 GeV | 10^{-3} GeV | 10^21 |

**The real scalar domain wall exceeds cosmological bounds by approximately 63 orders
of magnitude** [corrected from the previously stated 57 — using the correct bound
sigma < (1 MeV)^3 = 10^{-9} GeV^3 with sigma ≈ 9.43×10^53 GeV^3, the violation factor
is 9.43×10^53 / 10^{-9} ≈ 10^63, verified independently by python3]. The qualitative
conclusion (real-scalar domain walls are catastrophically ruled out, motivating the
doublet structure) is unaffected; only the specific quoted magnitude changes.

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

Initially, walls are subdominant. But they become dominant at:
```
t_dom ~ (sigma / rho_rad)^{-1} H^{-1} ~ very early
```

### 5.2 Universe Overclosure

The domain wall contribution to Omega:

```
Omega_wall = rho_wall / rho_critical
           ~ (sigma/t) / (3 H^2 M_Pl^2)
```

For sigma ~ 10^54 GeV^3 and t ~ 10^17 s (today):

```
Omega_wall >> 1
```

**Domain walls would have overclosed the universe long ago.**

### 5.3 Observable Consequences (If They Existed)

Had such walls existed:
1. Universe collapses before nucleosynthesis
2. No CMB (universe too dense)
3. No galaxies, stars, planets
4. We would not exist to discuss this

---

## 6. Why a Doublet Solves the Problem

### 6.1 Real Doublet Definition

Instead of a single real scalar R, use a doublet:
```
R = (R_1, R_2) with |R|^2 = R_1^2 + R_2^2
```

In polar form:
```
R_1 = rho cos(phi)
R_2 = rho sin(phi)
```

### 6.2 Vacuum Manifold

**Single real scalar:**
- Vacuum: R = +/-v (two disconnected points)
- pi_0(vacuum) = Z_2 (non-trivial)
- **Domain walls exist** (walls separate +v and -v regions)

**Real doublet:**
- Vacuum: |R| = v (a circle S^1)
- pi_0(vacuum) = 0 (trivial, circle is connected)
- **No domain walls** (can continuously connect any two points on the circle)

### 6.3 Energy Comparison

**Single real scalar on orbifold S^1/Z_2:**
```
R(X=0) = -v  -->  R(X=L/2) = +v  -->  R(X=L) = -v
```
Contains two domain walls with total energy:
```
E_orbifold = 2 * sigma * A ~ 2 * 10^54 GeV^3 * A
```

**Real doublet (helix configuration):**
```
R_1(X) = v cos(2 pi X / L)
R_2(X) = v sin(2 pi X / L)
|R| = v (constant everywhere!)
```

Energy is purely from gradient in angle phi:
```
E_helix = integral dX (1/2) |dR/dX|^2
        = integral dX (1/2) v^2 (d phi/dX)^2
        = (1/2) v^2 (2 pi / L)^2 * L
        = 2 pi^2 v^2 / L
```

### 6.4 Energy Ratio

```
E_orbifold / E_helix ~ (sigma * A) / (v^2/L)
                     ~ (sqrt(lambda) v^3 * A) / (v^2/L)
                     ~ sqrt(lambda) v * A * L
```

For A ~ L^2 (typical cosmological scales):
```
E_orbifold / E_helix ~ sqrt(lambda) v L^3 >> 1
```

**The doublet (helix) configuration has exponentially lower energy.**

---

## 7. XCRM Implications

### 7.1 XCRM Term with Single Real Scalar

```
L_XCRM = chi R dR/dX
```

On the orbifold with kink profile:
```
integral dX chi R dR/dX = chi [R^2/2]_{-v}^{+v} = chi * 0 = 0
```

The XCRM term integrates to zero (or contributes only at boundaries)!

### 7.2 XCRM Term with Doublet

```
L_XCRM = chi (R_1 dR_2/dX - R_2 dR_1/dX) = chi rho^2 dphi/dX
```

For the helix phi(X) = 2 pi n X / L:
```
integral dX chi rho^2 dphi/dX = chi v^2 * 2 pi n
```

**Non-zero topological contribution!** This is essential for the STUR mechanism.

### 7.3 Physical Interpretation

| Aspect | Single Real Scalar | Real Doublet |
|--------|-------------------|--------------|
| Topology | Z_2 kink | U(1) winding |
| Domain walls | Present (catastrophic) | Absent |
| Energy density | ~10^54 GeV^3 | ~v^2/L^2 |
| XCRM contribution | Zero (boundary only) | Topological (winding) |
| Cosmological viability | **RULED OUT** | Viable |

---

## 8. Mathematical Summary

### 8.1 Key Formulas

**Wall thickness:**
```
delta = sqrt(2) / (sqrt(lambda) v)
```

**Surface tension:**
```
sigma = (2 sqrt(2) / 3) sqrt(lambda) v^3
```

**Cosmological bound:**
```
sigma < (1 MeV)^3 = 10^{-9} GeV^3   [corrected, was 10^{-3} GeV^3]
```

**Required VEV for marginal viability:**
```
v_max = (sigma_max / sqrt(lambda))^{1/3} ~ (10^{-9})^{1/3} ~ 10^{-3} GeV   [corrected,
      was 10^{-1} GeV — off by two orders of magnitude due to the propagated (1 MeV)^3
      error; 10^{-3} GeV = 1 MeV is also dimensionally as expected: v_max should be
      of order the bound scale itself]
```

This is FAR below the GUT/Planck scale needed for STUR!

### 8.2 The Conclusion

For v ~ 10^18 GeV (STUR scale):
- Single real scalar: sigma ~ 9.43×10^53 GeV^3 **RULED OUT by ~10^63** [corrected, was "10^54 GeV^3 RULED OUT by 10^57"]
- Real doublet: No domain walls, E ~ v^2/L^2 **VIABLE**

**STUR must use a doublet, not a single real scalar.**

---

## 9. Connection to Three Generations

### 9.1 Why N = 3?

The doublet winds around the extra dimension:
```
R(X + L) = e^{2 pi i / N} R(X)
```

For N = 3 (three-fold winding):
- Three distinct phases: 0, 2pi/3, 4pi/3
- Corresponds to three generations of fermions
- ∞₃ center of SU(3) color

### 9.2 The Deep Connection

The requirement for a doublet (to avoid domain walls) naturally leads to:
1. Winding topology (essential for XCRM)
2. Discrete symmetry (Z_N)
3. N = 3 selection (from path integral quantization)
4. Three generations (from three phases)

**The cosmological constraint (no domain walls) is secretly connected to the existence of three generations!**

---

## 10. Appendix: Detailed Numerical Checks

### 10.1 Wall Profile Verification

For R(x) = v tanh(x/delta):

At x = 0:
```
R(0) = v tanh(0) = 0  (at the wall center)
```

At x = +/- delta:
```
R(+/-delta) = v tanh(+/-1) = +/-0.762 v
```

At x = +/- 3*delta:
```
R(+/-3*delta) = v tanh(+/-3) = +/-0.995 v  (essentially at vacuum)
```

The wall is concentrated within ~3*delta of the center.

### 10.2 Energy Integration Check

Direct numerical integration of E = integral dx [(1/2)(dR/dx)^2 + V(R)]:

Using R(x) = v tanh(x/delta) with delta = sqrt(2/lambda)/v:
```
dR/dx = (v/delta) sech^2(x/delta)
(dR/dx)^2 = (v^2/delta^2) sech^4(x/delta)

V(R) = (lambda/4)(v^2 tanh^2(x/delta) - v^2)^2
     = (lambda/4) v^4 (tanh^2(x/delta) - 1)^2
     = (lambda/4) v^4 sech^4(x/delta)
```

Note: (1/2)(dR/dx)^2 = (v^2)/(2*delta^2) sech^4 = (lambda v^4/4) sech^4 = V(R) CHECK!

```
E = integral_{-inf}^{+inf} dx [2 V(R)]
  = (lambda v^4/2) integral dx sech^4(x/delta)
  = (lambda v^4/2) * delta * integral du sech^4(u)
  = (lambda v^4/2) * delta * (4/3)
  = (2/3) lambda v^4 delta
  = (2/3) lambda v^4 * sqrt(2/lambda)/v
  = (2/3) sqrt(2 lambda) v^3
  = (2 sqrt(2)/3) sqrt(lambda) v^3  CHECK!
```

### 10.3 Numerical Value Summary

| Quantity | Formula | Numerical Value |
|----------|---------|-----------------|
| v | Input | 10^18 GeV |
| lambda | Input | 1 |
| delta | sqrt(2/lambda)/v | 1.4 * 10^{-18} GeV^{-1} |
| delta (meters) | delta * hbar*c | 2.8 * 10^{-34} m |
| sigma | (2sqrt(2)/3) sqrt(lambda) v^3 | 0.94 * 10^54 GeV^3 |
| sigma^{1/3} | - | 10^18 GeV |
| Bound on sigma | ZKO constraint | < 10^{-9} GeV^3 [corrected, was 10^{-3}] |
| Violation factor | sigma / sigma_bound | ~10^63 [corrected, was 10^57] |

---

## 11. References

1. Zel'dovich, Ya. B., Kobzarev, I. Yu., Okun, L. B. (1974). "Cosmological consequences of a spontaneous breakdown of a discrete symmetry." Zh. Eksp. Teor. Fiz. 67, 3-11 [Sov. Phys. JETP 40, 1-5 (1975)].

2. Vilenkin, A., Shellard, E. P. S. (2000). "Cosmic Strings and Other Topological Defects." Cambridge University Press.

3. Kibble, T. W. B. (1976). "Topology of cosmic domains and strings." J. Phys. A 9, 1387.

4. Planck Collaboration (2018). "Planck 2018 results. VI. Cosmological parameters." arXiv:1807.06209.

---

**Document Status:** Complete, peer-review ready
**Key Result:** Domain walls from a real scalar at GUT scale violate cosmological bounds by approximately 10^63 [corrected from a previously stated 10^57, which used an incorrectly-cubed (1 MeV)^3 bound; independently verified by python3], necessitating a doublet structure for STUR.
