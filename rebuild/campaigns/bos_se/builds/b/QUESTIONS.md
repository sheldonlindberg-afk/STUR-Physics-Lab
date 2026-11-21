# Ambiguities in SPEC.md and resolutions (bos_se-b)
1. Sign of Sigma: resolved by the dressed propagator -i g/(k^2-M^2+Sigma): Sigma = i x (g^{mn} coefficient of the sum of 1PI diagrams), so Sigma = -Pi.
2. Sign of Sigma^AZ: fixed by the stated Z = c W3 - s B, A = s W3 + c B (this makes Sigma^AZ(0) = -(alpha/2pi) M_W^2/(sc) B0(0;W,W); the opposite convention for the A/Z rotation flips it).
3. "mu is a mass argument": mu^2 = mu*mu enters ln(m^2/mu^2); Delta dropped entirely (no gamma_E, ln 4pi left).
4. k^2 = 0: evaluated as the limit k^2 = 1e-30 M_W^2 with raised precision (functions are analytic there).
5. Above threshold: real part (ln|.|), at threshold the finite limit.
6. Gauge-fixing/ghost sign conventions are not given: they are fixed by requiring cancellation of the gauge-scalar mixing (derived in gen/vtx.py).
7. Tadpoles excluded as stated; no other renormalization of parameters inside the loops (g, g', v, lam are tree-level, M_W = g v/2).
