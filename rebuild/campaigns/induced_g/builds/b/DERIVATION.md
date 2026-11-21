# Derivation (build b): induced 1/G, proper-time cutoff (SPEC sections 1-4)

## 1. Heat kernel
For D = -(nabla^2 + E) on a bundle: Tr e^{-tD} = (4 pi t)^{-d/2} Int sqrt(g) [ tr 1 + t tr(R/6 + E) + O(t^2) ].
So b0 = tr 1, b1 = tr(R/6 + E), k1 = b1/R.

## 2. Each k1 (E of each operator)
* Scalar, D = -nabla^2 + xi R  => E = -xi R, tr1 = 1:  k1 = 1/6 - xi.  (slope -1 in xi)
* Dirac, D^2 = -nabla^2 + R/4 (Lichnerowicz) => E = -R/4 * 1, tr 1 = N = 2^floor(d/2):
  k1 = N(1/6 - 1/4) = -N/12.   d=4 (N=4): -1/3.  Weyl = Dirac/2: -1/6 (d=4).
* Vector, Feynman gauge: (D A)_mu = -nabla^2 A_mu + R_mu^nu A_nu => (E)_mu^nu = -R_mu^nu, tr E = -R, tr 1 = d:
  b1 = (d/6 - 1) R. Ghosts: two Grassmann scalars with -nabla^2 (xi = 0), each enters ln Z with opposite
  sign to a boson of the same operator, so subtracted: -2 * (1/6) = -1/3 (d independent).
  k1(vector) = d/6 - 1 - 1/3 = d/6 - 4/3 ; d=4: -2/3. vector_no_ghosts: d/6 - 1 ; d=4: -1/3.

## 3. Statistics and the effective action
ln det D = -Int_{1/kappa^2}^inf dt/t Tr e^{-tD}.
* Real boson: Z = det^{-1/2}, W = -ln Z = +1/2 ln det D = -1/2 Int dt/t Tr e^{-tD}.
* Dirac: Z = det(Dslash), W = -ln det Dslash = -1/2 ln det D^2 = +1/2 Int dt/t Tr e^{-tD^2}. (opposite sign)
* Ghosts: Z_gh = det(D_gh) => same sign as a fermion; already inside k1(vector).
R-term: Int_{1/k^2}^inf dt/t * t^{1-d/2}, d=4: Int dt/t^2 = kappa^2. So
  Tr e^{-tD} |_R = (1/16 pi^2) * kappa^2 * k1 * Int sqrt(g) R.
  W_boson   (R term) = -(kappa^2/(32 pi^2)) k1 Int sqrt(g) R
  W_Dirac   (R term) = +(kappa^2/(32 pi^2)) k1_Dirac Int sqrt(g) R,  Weyl half of that.
Total W_R = -(kappa^2/(32 pi^2)) S Int sqrt(g) R,  S = n_s k1_s + n_v k1_v - n_w k1_w.

## 4. Matching
S_grav = -(1/(16 pi G)) Int sqrt(g) R, no tree term, so W_R = S_grav:
  1/(16 pi G) = kappa^2 S/(32 pi^2)  =>  1/G = kappa^2 S/(2 pi)
  1/G = (kappa^2/(2 pi)) [ n_s (1/6 - xi) + n_w/6 - (2/3) n_v ]   (d = 4; k1_w = -1/6 so -n_w k1_w = +n_w/6).
Signs: minimal scalar +, Weyl +, vector (with ghosts) -.

## 5. Independent second route (computed in builds/b/induced_g.py __main__)
Exact spectra on the round S^4 (radius a=1):
 scalar: l(l+3)+12 xi, deg (2l+3)(l+1)(l+2)/6 ; Dirac D^2: (n+2)^2, deg 8*C(n+3,3) (4 C(n+3,3) per sign of Dslash eigenvalue);
 vector (Hodge on 1-forms = -nabla^2+Ric): coexact (l+1)(l+2), l>=1, deg l(l+3)(2l+3)/2;
 exact: scalar eigenvalues l(l+3), l>=1 (same degeneracy as scalar).
Compute K(t), form (4 pi t)^2 K/V (V = 8pi^2/3), fit polynomial in t -> b1 = 12 k1 (R = 12). Compare k1.
Then the radius dependence: Int sqrt(g) R = 32 pi^2 a^2, so from W_R above W(a)|_{kappa^2 term} = -kappa^2 S a^2 ;
the exact-spectrum quantity -(1/2) s K(s) (= dW/dkappa^2) has constant term -(1/2) b1 V/(16 pi^2) = -S_part*... printed and compared.
Sign statement: induced 1/G > 0 iff W's kappa^2 a^2 term is negative, i.e. S > 0, i.e. the heat-kernel b1 of the
(statistics-weighted) field content is positive. Minimal scalar: W decreases with a  => positive 1/G.
Nothing underived. Mass terms ignored per SPEC.
