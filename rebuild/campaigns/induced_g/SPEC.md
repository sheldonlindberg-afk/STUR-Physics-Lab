# SPEC: Newton's constant induced by quantum fields at one loop (Sakharov), with a proper-time cutoff

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. Euclidean signature throughout.

## 1. The theory (postulates)

* Free quantum fields on a smooth, compact, curved Euclidean d-dimensional manifold with metric g, coupled
  only to the metric. The metric is classical, not quantized: no graviton loop.
* Curvature sign: the scalar curvature R is **positive on a round sphere** (R = d(d−1)/a² on S^d of radius a).
* Gravity's Euclidean action is S_grav = −(1/(16πG)) ∫ d^dx √g R. **G > 0 means attractive gravity.**
  Sakharov's postulate: there is no tree-level term. All of 1/G comes from the one-loop effective action of the
  fields below.
* Effective action: W = −ln Z, with Z the Euclidean path integral of the fields. For a boson with a
  Laplace-type kinetic operator D, Z = (det D)^(−1/2) per real field. Fermions are Grassmann: a Dirac fermion
  contributes Z = det(D̸), with D̸ the (Hermitian) Dirac operator. A Weyl fermion is half a Dirac fermion
  in even d. Gauge vectors are quantized in Feynman gauge with Faddeev–Popov ghosts, which are Grassmann scalars.
* Regularization: Schwinger proper time with a lower cutoff 1/κ², i.e. ln det D → −∫_{1/κ²}^∞ (dt/t) Tr e^{−tD}.
  κ is the cutoff energy.
* Fields, all massless (masses ≪ κ, so they only change finite terms):
  - real scalar with kinetic operator −∇² + ξR (ξ a real number);
  - Dirac fermion with D̸² as its Laplace-type operator (spinor dimension 2^⌊d/2⌋); Weyl = half a Dirac (even d only);
  - abelian gauge vector (one generator of a gauge group counts as one vector at one loop), in Feynman gauge, with its ghosts;
  - also, for comparison, the same vector operator without its ghosts.

## 2. The quantities (definition)

* For each field kind, k₁ is defined without normalisation choices as follows. Write the heat trace of the field's Laplace-type operator(s) as
  Tr e^{−tD} = (4πt)^{−d/2} ∫ d^dx √g [b₀ + t b₁ + O(t²)], and set **k₁ = b₁ / R**, the coefficient of R in b₁, summed over
  the operators that make up the field (with **no** sign for statistics: the bare trace) and per field. For the Dirac
  fermion use the operator D̸² on spinors; for the vector, the vector operator plus the ghost operators (ghosts count
  with their own statistics' sign **inside** k₁, i.e. as subtracted operators, exactly as they enter ln Z), and the
  'vector_no_ghosts' kind without them. Weyl is half of Dirac. Fermion statistics are **not** in k₁.
* **1/G**: the coefficient fixed by matching the κ² ∫√g R term of W to S_grav, in d = 4, for a collection of
  n_s real scalars (all with the same ξ), n_w Weyl fermions and n_v gauge vectors with ghosts. Its sign is part
  of the answer and follows from the conventions above.

## 3. Exports (exact signatures in campaign.py)

`k1(kind, d=4, xi=0.0)` for kind in 'scalar', 'weyl', 'dirac', 'vector', 'vector_no_ghosts' (Weyl only for even d);
`inv_G(kappa, n_s, n_w, n_v, xi=0.0)` → 1/G in units of κ² (ħ = c = 1, d = 4), so with κ in GeV, 1/G in GeV²;
`mpl(kappa, n_s, n_w, n_v, xi=0.0)` → √(1/G) when 1/G > 0, and None otherwise.

## 4. What to show in DERIVATION.md

The endomorphism E of each operator (D = −(∇² + E)), the general b₁, each k₁ as a function of d, the
statistics signs from Z, the matching to S_grav including every sign, and an **independent second route**:
for example the heat trace of the scalar Laplacian on a round S² or S^d computed numerically from its exact spectrum
(eigenvalues l(l + d − 1)/a² with their degeneracies) and fitted for b₁, or the dependence of W on the radius of a
sphere, checked against your sign for 1/G.
