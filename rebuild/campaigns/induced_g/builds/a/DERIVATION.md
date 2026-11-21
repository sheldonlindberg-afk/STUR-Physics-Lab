# Induced 1/G at one loop with a proper-time cutoff (build a)

All postulates from SPEC.md section 1; definitions from section 2.

## 1. Heat-kernel b1 for a Laplace-type operator

For D = -(g^{mn} nabla_m nabla_n + E) acting on sections of a bundle V (fibre dim tr 1), the small-t heat trace is

    Tr e^{-tD} = (4 pi t)^{-d/2} \int d^dx sqrt(g) tr[ 1 + t (R/6 + E) + O(t^2) ],

so b0 = tr 1 and b1 = tr(E) + (R/6) tr 1. (Sign convention: R > 0 on round spheres, SPEC 1; the R/6 is the
standard Seeley-DeWitt term in this sign convention, checked independently on spheres in section 6 below.)

## 2. Endomorphisms and k1 per kind (k1 = b1/R, bare trace, per field)

* **Real scalar**, D = -nabla^2 + xi R, so E = -xi R, tr 1 = 1:
  b1 = (1/6 - xi) R,  **k1_s = 1/6 - xi** (any d; linear in xi with slope -1).
* **Dirac**, Lichnerowicz: Dslash^2 = -nabla^2 + R/4 on spinors, so E = -(R/4) 1, tr 1 = 2^{floor(d/2)}:
  b1 = 2^{floor(d/2)} (1/6 - 1/4) R, **k1_D = -2^{floor(d/2)}/12**. d = 4: k1_D = -1/3.
* **Weyl** (even d): k1_W = k1_D / 2 = -2^{floor(d/2)}/24. d = 4: **k1_W = -1/6**.
* **Vector, no ghosts**: Feynman-gauge operator on A_m: (D A)_m = -nabla^2 A_m + R_m^n A_n
  (from -nabla^n F_{nm} + nabla_m nabla^n A_n, commuting covariant derivatives gives + Ric). So E_m^n = -R_m^n,
  tr E = -R, tr 1 = d: b1 = (d/6 - 1) R, **k1_{v,ng} = d/6 - 1**. d = 4: -1/3.
* **Ghosts**: a complex Grassmann pair c, cbar with operator -nabla^2 (E = 0): Z_gh = det(-nabla^2)^{+1}
  = [det(-nabla^2)^{-1/2}]^{-2}, i.e. minus two real scalars with xi = 0. Ghost part of k1 = -2 x 1/6 = -1/3
  (independent of d).
* **Vector with ghosts**: **k1_v = d/6 - 1 - 1/3 = d/6 - 4/3**. d = 4: **k1_v = -2/3**.

d = 4 summary: scalar 1/6 - xi; Dirac -1/3; Weyl -1/6; vector -2/3; vector_no_ghosts -1/3.

## 3. Statistics signs from Z (W = -ln Z)

Regularized ln det D = -\int_{1/kappa^2}^inf (dt/t) Tr e^{-tD}.

* Boson (real field): Z = det(D)^{-1/2}, so W = +(1/2) ln det D = -(1/2) \int (dt/t) Tr e^{-tD}.
* Ghosts: already inside k1_v with sign -, as they enter ln Z (Z_gh = det^{+1}).
* Dirac: Z = det(Dslash) = det(Dslash^2)^{1/2}, so W = -(1/2) ln det Dslash^2 = +(1/2) \int (dt/t) Tr e^{-t Dslash^2}.
  Weyl = half of that.

Define s = +1 for bosons (scalar, vector+ghosts), s = -1 for fermions. Then
W = -(s/2) \int_{1/kappa^2} (dt/t) Tr e^{-tD} per field.

## 4. The kappa^2 term in d = 4

The t^1 term of the heat trace gives, per field,
W ⊃ -(s/2) \int_{1/kappa^2}^inf dt t^{-1} (4 pi t)^{-2} t \int sqrt(g) k1 R
  = -(s/2) (1/(16 pi^2)) [\int_{1/kappa^2}^inf t^{-2} dt] k1 \int sqrt(g) R
  = -(s k1 kappa^2 / (32 pi^2)) \int sqrt(g) R.

Summing: W ⊃ -(kappa^2/(32 pi^2)) K \int sqrt(g) R, with
K = n_s k1_s + n_v k1_v - n_w k1_W = n_s (1/6 - xi) - (2/3) n_v + (1/6) n_w.

## 5. Matching to S_grav

S_grav = -(1/(16 pi G)) \int sqrt(g) R (SPEC 1). Sakharov: W's R-term is all of S_grav, so
1/(16 pi G) = kappa^2 K / (32 pi^2), i.e. 1/G = kappa^2 K / (2 pi):

    **1/G = (kappa^2 / (12 pi)) [ n_s (1 - 6 xi) + n_w - 4 n_v ]**.

Signs: minimally coupled scalars (xi < 1/6) and Weyl fermions induce G > 0 (attractive); conformal scalars
(xi = 1/6) induce nothing; gauge vectors in Feynman gauge with ghosts induce a negative 1/G (-kappa^2/(3 pi) each).
mpl = sqrt(1/G) only when 1/G > 0.

## 6. Independent second route: exact spectra on the round S^4 (and S^2)

Computed numerically in induced_g.py `__main__`, without using any b1 formula:

(a) Heat trace from exact spectra, radius a = 1, fitted as t^2 K(t) = c0 + c1 t + c2 t^2 + ... (S^4),
compared with (4 pi t)^{-2} Vol(S^4) [tr1 + t k1 R], Vol = 8 pi^2/3, R = 12, giving c1 = 2 k1:
  * scalar with -nabla^2 + xi R: eigenvalues l(l+3) + 12 xi, deg (2l+3)(l+1)(l+2)/6;
  * Dslash^2: eigenvalues (n+2)^2, total deg 2 * 4 * C(n+3,3) (both signs of Dslash);
  * Hodge operator on 1-forms (= Feynman-gauge vector operator -nabla^2 + Ric): exact forms l(l+3), l >= 1,
    deg as scalars; coexact forms (l+1)(l+2), l >= 1, deg l(l+3)(2l+3)/2 (l = 1: 10 Killing vectors);
  * ghosts: two scalars at xi = 0 subtracted.
  S^2 cross-check of the scalar: eigenvalues l(l+1), deg 2l+1; t K = c0 + c1 t, c1 = 2 k1 (Vol 4 pi, R = 2).

(b) Sign of 1/G from W(kappa) itself: W(kappa) = -(s/2) sum_modes deg E1(lambda/kappa^2) (exact proper-time
integral per mode; zero modes dropped, they only give ln kappa), fitted in kappa as
W = A kappa^4 + B kappa^2 + C ln kappa + D. On S^4 of radius 1, S_grav = -(1/(16 pi G)) * (8 pi^2/3) * 12 = -2 pi/G,
so 1/G = -B/(2 pi) (per kappa^2). This directly gives the sign of induced 1/G from the effective action.

Results are listed in section 7.

## 7. Second-route results (python3 induced_g.py)

```
k1 (d=4): main formula vs exact S^4 spectrum fit (c1/2)
  scalar            xi=0.0: k1=+0.1666666667  spectrum=+0.1666666667  (tr1/6 check c0=0.16666667)
  scalar            xi=0.3: k1=-0.1333333333  spectrum=-0.1333333333  (tr1/6 check c0=0.16666667)
  dirac             xi=0.0: k1=-0.3333333333  spectrum=-0.3333333333  (tr1/6 check c0=0.66666667)
  vector            xi=0.0: k1=-0.6666666667  spectrum=-0.6666666667  (tr1/6 check c0=0.33333333)
  vector_no_ghosts  xi=0.0: k1=-0.3333333333  spectrum=-0.3333333333  (tr1/6 check c0=0.66666667)
  S^2 scalar xi=0: k1 spectrum = +0.1666666667
1/G per kappa^2 per field: formula vs W(kappa) from exact S^4 spectrum
  scalar xi=0   : formula +0.0265258238   W-route +0.0265258238
  scalar xi=0.5 : formula -0.0530516477   W-route -0.0530516467
  Weyl          : formula +0.0265258238   W-route +0.0265258238
  vector+ghosts : formula -0.1061032954   W-route -0.1061032954
```

The heat-trace fits reproduce every k1 to 1e-10, including the R/6 term and the sign of E (scalar at xi = 0.3 goes negative,
the Dirac and vector values match). The W(kappa) route, which never uses b1, gives the kappa^2 coefficient of W with
the same sign and size as the formula: W gets a NEGATIVE kappa^2 a^2 term for a minimal scalar and for a Weyl fermion, so
1/G > 0 (attractive); for xi = 1/2 scalars and for gauge vectors with ghosts the term is positive, so 1/G < 0.

Nothing was left underived.
