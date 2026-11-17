# Spec ambiguities and how they were resolved (greybody-a)

1. "degree of freedom" for P_s: taken literally as SPEC section 3 states, one helicity state, sum over j and m
   (factor 2j+1), no factor for particle/antiparticle or number of helicities.
2. Fermion sign V = W^2 +- dW/dr*: both give the same Γ (verified numerically to 10 digits); V = W^2 + dW/dr* is used.
3. transmission(s, j, w) for j < s or w <= 0 returns 0 (not a physical partial wave / no flux); not exercised by the spec.
4. absorption_sum "all j that matter": j summed from s until j + 1/2 > 3 sqrt(3) w + 3 and the term is < 1e-12 of the sum.
5. Numerics conventions (SPEC 5): r* from -80 (horizon BC) to r*(3); then r from 3 to R = max(60, (30 + L_eff)/w),
   matched to the asymptotic series; w in [0, 2.5] with Gauss-Legendre panels; convergence shown in DERIVATION section 9.
