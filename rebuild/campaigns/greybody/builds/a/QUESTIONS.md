# Spec ambiguities and how they were resolved (greybody-a)

1. "degree of freedom" for P_s: taken literally as SPEC section 3 states, one helicity state, sum over j and m
   (factor 2j+1), no factor for particle/antiparticle or number of helicities.
2. Fermion sign V = W^2 +- dW/dr*: both give the same Γ (verified numerically to 10 digits); V = W^2 + dW/dr* is used.
3. transmission(s, j, w) for j < s or w <= 0 returns 0 (not a physical partial wave / no flux); not exercised by the spec.
4. absorption_sum "all j that matter": j summed from s until j + 1/2 > 3 sqrt(3) w + 3 and the term is < 1e-12 of the sum.
5. Numerics conventions (SPEC 5): r* from -80 (horizon BC) to r*(3); then r from 3 to R = max(60, (30 + L_eff)/w),
   matched to the asymptotic series; w in [0, 2.5] with Gauss-Legendre panels; convergence shown in DERIVATION section 9.

## Revision 2 (verifier finding: low-frequency fermion Gamma to 1e-8)
6. Cause: horizon boundary condition for s = 1/2 neglected the O(sqrt f) correction (V ~ sqrt f near the horizon for the
   Dirac reduction), at r*_min = -80 (sqrt f ~ 1e-9). The neglected term admixes a horizon-outgoing wave of relative
   size ~ k sqrt(f)/(8 w), giving Gamma errors 6e-8 ... 2.7e-7 at w = 0.002 - 0.01. Fixed by the series term
   u = 1 + c sqrt f, c = +-2k/(1 - 8iw), and r*_min = -160; rtol tightened to 1e-12. Claimed accuracy now 1e-9 relative
   for all spins at w in [0.002, 3]; observed <= 3e-11 versus rtol 1e-13 / r*_min x2 / R x2.
7. The min(1, .) clip on Gamma was removed; unclipped Gamma exceeds 1 by <= 6e-12 at high w (DERIVATION section 1).
