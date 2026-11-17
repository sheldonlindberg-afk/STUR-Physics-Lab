# Derivation: grey-body factors and Hawking power (build greybody-b)

## Postulates used (SPEC s1-s3)
Units G=c=hbar=k_B=M=1, f=1-2/r, r*=r+2ln(r/2-1), T=1/(8 pi). psi'' + (w^2 - V) psi = 0 (' = d/dr*).
Bosons V = f[j(j+1)/r^2 + 2(1-s^2)/r^3]. Fermions V = W^2 + sigma dW/dr*, W=k sqrt(f)/r, k=j+1/2.
Compute dW/dr* = f d/dr(k sqrt f / r) = k sqrt(f) (3/r^3 - 1/r^2) (using f'=2/r^2).
So V = k^2 f/r^2 + sigma k sqrt(f)(3/r^3 - 1/r^2). Both signs give same Gamma (SPEC); I use sigma=-1 (and check +1 in __main__).
Boundary: psi -> e^{-i w r*} at horizon; psi -> A_in e^{-iwr*} + A_out e^{+iwr*}. Gamma = 1/|A_in|^2 (flux w at horizon / flux w|A_in|^2 incident).
Emission: P_s = sum_j (2j+1) Int_0^inf dw/(2 pi) w Gamma/(e^{w/T} -+ 1).

## Numerical scheme (all steps derived here)
1. Near horizon variable: r = 2 + e^t. With d = e^t, f = d/(2+d), dr* = dr/f, define Phi = f dpsi/dr = dpsi/dr*.
   d psi/dt = r Phi,   d Phi/dt = -(w^2 - V) r psi.  (regular in t; from dpsi/dr = Phi/f, dr = d dt, f = d/r.)
   Start at d0 = 1e-8 min(1,w)^2 with psi = e^{-i w r*}, Phi = -i w psi (error O(V/w) ~ d0/w).
2. Far field: formal solutions psi_pm = e^{ +- i w r*} u_pm(x), x=1/r, u = sum c_n x^n. Substituting into the wave eq:
   2 i w u_r + (f u_r)_r - g u = 0, g = V/f. With u_r = -x^2 du/dx, f=1-2x, g = sum_{p>=2} g_p x^p:
   c_m = [ (m-1)m c_{m-1} - 2(m-2) m c_{m-2} - sum_{p=2}^{m+1} g_p c_{m+1-p} ] / (2 i w m), c_0=1  (w -> -w for psi_-).
   Bosons: g = L x^2 + 2(1-s^2) x^3. Fermions: g = k^2 x^2 + sigma k (3x^3 - x^2)(1-2x)^{-1/2}, (1-2x)^{-1/2} = sum C(2n,n) 2^{-n} x^n.
   Series is asymptotic; truncate at smallest term (<1e-17 or when terms start to grow). Match at R large (w R >= ~60 and R >= ~ 60+ big for large j).
   psi_*, = e^{+-iwr*}(+- i w u + f u_r).
3. Solve psi = A_in psi_- + A_out psi_+ at R via 2x2 linear solve (Wronskian). Gamma = 1/|A_in|^2.
4. Power: Gauss-Legendre in w on [0, w_max] panels (w_max where e^{-w/T} < 1e-25), j summed until Gamma_j < 1e-14.

## Independent second routes
(a) Flux conservation: Gamma' = 1 - |A_out/A_in|^2 must equal 1/|A_in|^2 (tests the numerics + asymptotics independently of the formula).
(b) Vary R, d0, rtol, GL nodes (x2), j cutoff, w_max; P_s must move < 1e-6 relative.
(c) fermion sigma=+1 vs -1 same Gamma.
(d) Low-w analytic: Gamma_00 -> 16 w^2 (horizon area / pi... 4 pi r_h^2 /pi) as a check, not an input.
Nothing not derived; no tabulated numbers used.
