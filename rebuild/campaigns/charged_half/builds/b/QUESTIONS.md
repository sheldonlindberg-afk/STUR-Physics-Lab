# Ambiguities in SPEC.md and resolutions
1. Phase phi: SPEC says "phase int w~ dr*"; I use phi = w r* - g ln(r-2) (exact integral). Gamma = 1/|A_in|^2 by flux conservation (J_horizon=-1).
2. "Tails below 1e-14 dropped": normalise, drop pi<1e-14, renormalise (sum=1).
3. P(0,0), N(0,0): per helicity state, sum over j of (2j+1) as stated.
4. Energy range w in [0, 1.7] (n_F<1e-17 above); below 1e-3 an analytic w^(2j+1) tail (relative 1e-5 of N).
5. g sampling: ln Gamma Chebyshev-interpolated in g on [-0.25,0.25] (15 nodes), range doubled if |g| larger.
6. For rules where r_gb != r_mu the pair (g_gb, g_mu) is used jointly in N and P as in S3.
Not derived: no closed form for Gamma_j (numerical).

## Accuracy finding (round 2)
Verifier saw Gamma errors ~7e-6. Cause: asymptotic-series truncation in _series stopped at the first term larger than its predecessor; for g ~ 0 (and the exactly terminating kappa=1, g=0 case) low-order terms dip, so the sum was cut after 1-2 orders (error ~ (kappa^2/(2 w R))^2). Fix: envelope max(t_m,t_{m-1}), full generation to past the minimum. Also rtol 1e-10 -> 1e-12 (J drift 1e-9 at large R), and the Schrodinger route now applies the first-order near-horizon correction (its old 4e-6 gap was its own sloppy start at r*=-60 plus the main-route truncation bug). Study: R in {0.5,1,3}x, y0 -32/-45, rtol 1e-12/1e-13 agree to <=1.4e-11 over j=1/2..15/2, w=0.003..1.7, g=-0.12..0.12.
