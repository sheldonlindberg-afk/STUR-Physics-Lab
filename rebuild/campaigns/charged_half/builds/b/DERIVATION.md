# DERIVATION  (build charged_half-b)

Units G=c=hbar=k_B=1, M=1, r_h=2, f=1-2/r, T=1/(8 pi). SPEC sections cited as S1..S5.

## 1. Radial system and flux (S1, S2)
With w~(r)=w-g/r and kappa=j+1/2, W=kappa sqrt(f)/r:
  (d/dr* - i w~) R_- = W R_+ ,   (d/dr* + i w~) R_+ = W R_- .
Flux: d|R_-|^2/dr* = 2W Re(R_-^* R_+) = d|R_+|^2/dr*, hence J=|R_-|^2-|R_+|^2 is constant (verified numerically).
Phase: phi(r*) = int w~ dr* = w r* - g ln(r-2)  (dr*/dr = r/(r-2), so int (g/r) dr* = g ln(r-2)): the logarithmic
Coulomb phase is carried exactly, never approximated by w r*.

Horizon (r*->-inf, W->0, w~->w-g/2): R_+ = e^{-i(w-g/2)r*}, R_-=0, so J=-1 (valid for either sign of w-g/2).
I start at r*~-64 (y=ln(r-2)=-32) with the first-order near-horizon correction R_- = c W R_+, c=1/(1/4-2i w~_h)
(near the horizon dW/dr* = W/4); the neglected terms are O(W^2)~1e-13.
Integration variable: y=ln(r-2), d/dy = r d/dr*, r=2+e^y, f=e^y/r (no cancellation near horizon, no
stiffness). Integrated to r=R with w R = 30+4 kappa^2 (>=60), adaptive DOP853, rtol 1e-12.

## 2. Asymptotic boundary condition (large r, log phase)
Two exact asymptotic solutions as 1/r series (x=1/r):
  psi_in : (R_+,R_-) = e^{-i phi}(P, s q),   psi_out : (R_-,R_+) = e^{+i phi}(P~, s q~),
with s=sqrt(1-2x), P'=kappa x q (' = d/dr), (1-2x) q' + x^2 q - 2i(w-gx) q = kappa x P (substituting Q=s q removes the sqrt).
With P=sum p_m x^m, q=sum c_m x^m, p_0=1, c_0=0:
   c_m = [kappa p_{m-1} + (m-1)c_{m-1} - (2m-3)c_{m-2} - 2 i g c_{m-1}] / (-2 i w),   p_m = -kappa c_m / m.
psi_out is psi_in with (w,g)->(-w,-g) and R_+<->R_- (the system is symmetric under that map).
Series is asymptotic; all orders up to past the smallest term are generated and each element is summed up to the minimum of the envelope max(t_m,t_{m-1}) (or the first order where it is <1e-19). NOTE: an earlier version stopped at the first term that was larger than its predecessor, which truncates prematurely when low orders nearly vanish (g ~ 0, kappa=1 exactly terminates at g=0): error ~1e-6. At r=R solve the 2x2
system (R_+,R_-)=A_in psi_in + A_out psi_out. The unit amplitude of psi_in has flux -1, so by flux conservation
|A_out|^2-|A_in|^2=-1 and  Gamma = 1/|A_in|^2  (used; no cancellation for tiny Gamma). Check: 1-|A_out|^2/|A_in|^2 and J.

## 3. Thermal integrals (S3)
N(gb,gmu)=sum_j (2j+1) int dw/(2 pi) Gamma_j(w;gb) n_F(w;gmu), n_F=1/(exp((w-gmu/2)/T)+1); P has an extra w.
Gauss-Legendre on geometric panels of [w_lo, w_hi]=[1e-3,1.7]; below w_lo, Gamma~Gamma(w_lo)(w/w_lo)^{2j+1}
(analytic, contribution ~1e-5 relative) integrated exactly times n_F(w_lo/2). Above 1.7, n_F<1e-17. j=1/2..9.5
(Gamma_j beyond is < 1e-17 relative at w<=1.7).
g dependence: ln Gamma_j(w_i; g) sampled on Chebyshev nodes of [-gm,gm] (gm=0.25; doubled if needed) and interpolated
barycentrically (Gamma is analytic in g); accuracy checked against direct ODE solves.

## 4. Charge process (S3)
Rule (r_gb, r_mu); n_before=n, n_mid=n-q/2, n_after=n-q. up(n)=N at q=-1: g=-alpha n_r; down(n)=N at q=+1: g=+alpha n_r.
Birth-death chain: pi(n+1) down(n+1) = pi(n) up(n) (detailed balance, exact for 1D chain; stationary = zero-flux).
Mirror symmetry (q,n)->(-q,-n) gives down(n)=up(-n), hence pi(n)=pi(-n). pi(n+1)/pi(n)=up(n)/down(n+1);
built in log space for n>=0 until terms <1e-17, mirrored, tails <1e-14 dropped, renormalised.
<P> = sum pi(n)[P(e-) + P(e+)]/2 with the rule's (gb,gmu) pair, <N> likewise; ratios per S4.

## 5. Independent second routes (printed under __main__)
(a) Gamma at g=0: Chandrasekhar real form Z_+=R_+ + R_-, Z_+''+(w^2 - W^2 - W')Z_+=0 integrated in r* from the
    horizon with a different integrator/variables (LSODA, r from Lambert W) and matched to plane waves at large r with
    Richardson extrapolation in 1/R. Also Gamma vs 1-|Aout|^2/|Ain|^2 and J=-1, and variation of R, y0, rtol.
(b) Gamma at g != 0 vs. different matching radius R (2x) which changes the series order used; and vs direct solve
    in rotating variables.
(c) Stationary distribution: null vector of the (truncated) generator matrix by linear solve (scipy.linalg) vs the
    detailed-balance product; thermal integral by scipy.integrate.quad for a few (j) against the Gauss-Legendre sum;
    node-count doubling for the w-grid, g-nodes, j max, w_hi, w_lo.
(d) Low-frequency check Gamma_j ~ w^{2j+1} (slopes), Gamma->1 at high w, g->0 continuity.
Not derived: no closed form for Gamma_j; everything else is derived above.

## Erratum / accuracy study (second round)
Cause of the 1e-6 Gamma errors: premature series truncation (see section 2). Fixed; Gamma now R-, y0-, rtol-independent to <=1e-11 relative on a 4x7x5 grid (j, w, g) incl. Gamma~1 and Gamma~1e-57, and agrees with the Schrodinger/WKB route (with near-horizon correction added) to 1e-9..5e-8 (that route is limited by LSODA accumulation over long ranges).
