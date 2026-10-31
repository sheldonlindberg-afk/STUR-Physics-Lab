# Refinement round 5: deriving the Lagrangian for the twist

Date: 2026-10-31. Script: [`src/checks/r5_lagrangian.py`](../src/checks/r5_lagrangian.py) (about 2 s).

**Outcome.** Deriving the 5D Lagrangian **rules out round 4's torsion
twist**: the field &chi; does not exist on S&sup1;/Z&#8322;. The derivation also **upgrades
the dilemma to an exact theorem**. It identifies the **one kind of local term
that escapes the theorem**: a brane coupling that breaks the orbifold parity.
That is a precise form of "the orbifold twists". The torsion route to dark
matter and dark energy is **withdrawn**.

## 1. The Lagrangian

Coordinates x^&mu; and y &isin; S&sup1;/Z&#8322; (y ~ &minus;y ~ y + 2&pi;R). The circumference of the
covering circle is L = 2&pi;R, and the branes sit at y = 0 and y = &pi;R. Signature is
mostly-minus.

**Bulk.**

S_bulk = &int;d&#8308;x &int;dy e [ L_PGT + L_B + L_Y + L_CS + L_&psi; + L_&phi; ]

- **Gravity (quadratic Poincar&eacute; gauge theory).** The vielbein e^A_M and the
  Lorentz connection &omega;^AB_M are independent. Torsion is T^A = De^A.

  L_PGT = &minus;(M&#8325;&sup3;/2) R(&omega;) + &sum;_{i=1..3} a_i T^(i)&middot;T^(i) + &sum;_{j=1..6} b_j R^(j)&middot;R^(j)

  The T^(i) are the three irreducible torsion pieces (vector, axial,
  tensor) and the R^(j) the six curvature pieces. TEGR is recovered for
  a particular choice of the a_i with b_j = 0.
- **The birefringence gauge field B** (the source of &theta;):
  L_B = &minus;G_MN G^MN/(4g&#8325;&sup2;), with G = dB.
- **Hypercharge in the bulk (R2.3):** L_Y = &minus;Y_MN Y^MN/(4g&#8325;_Y&sup2;).
- **Chern&ndash;Simons term:** L_CS = (&kappa;/8&pi;&sup2;) &epsilon;^{MNPQR} B_M Y_NP Y_QR, with &kappa; &isin; &Zopf; + &frac12;
  (R1.1, R2.2, R3.2).
- **The fermion pair (R2.2):**

  L_&psi; = &sum;_{i=1,2} &psi;&#772;_i (i&Gamma;^M D_M &minus; M_i) &psi;_i + (1/8) T_[ABC] &psi;&#772;&Gamma;^{ABC}&psi; + c_T T_A &psi;&#772;&Gamma;^A&psi;

  - M&#8321; = M and M&#8322; = &minus;M;
  - the covariant derivative is D_M = &part;_M + &frac14;&omega;_M^{AB}&Gamma;_AB &minus; i q_B B_M + i g_Y Y_M;
  - the &Gamma;^{ABC} term is the minimal Cartan coupling to torsion; the c_T term is
    the most general non-minimal vector coupling.
- **The charged scalar** (same B charge and twist as &psi;, R2.2):
  L_&phi; = |D&phi;|&sup2; &minus; M_&phi;&sup2;|&phi;|&sup2;.

**Branes.**

S_brane = &int;d&#8308;x [ L_0 &delta;(y) + L_&pi; &delta;(y &minus; &pi;R) ]

- The SM fields live on the branes, and brane mixing of &psi; with a lepton is
  allowed only at y = 0 (R2.2).
- Each brane may carry a scalar &Sigma; that is **odd under the orbifold parity**:

  L_0 &sup; &frac12;(&part;&Sigma;)&sup2; &minus; V(&Sigma;) &minus; y_S &Sigma; &psi;&#772;&Gamma;^y&psi;

  (likewise &Sigma;&prime; on the y = &pi;R brane). This term is the outcome of section 4.

**Orbifold parities** (y &rarr; &minus;y). The rule is "even iff the number of y indices
is even", times the intrinsic parity of each field:

| Field | Even (has a zero mode) | Odd |
|---|---|---|
| geometry: e, &omega;, T | components with an even number of y indices: g_&mu;&nu;, T_[&mu;&nu;&rho;], T_&mu; | odd number of y indices: g_&mu;y, T_[&mu;&nu;y], **T_y** |
| B (Z&#8322;-odd U(1), R2.2) | B_y, so &theta; = &oint;B_y survives | B_&mu; |
| Y (hypercharge) | Y_&mu; | Y_y |
| &psi;&#8321;, &psi;&#8322; | exchanged: &psi;&#8321;(&minus;y) = &Gamma;^y &psi;&#8322;(y) | |
| &Sigma; (brane) | | odd (intrinsic) |

The parities of the geometric fields are fixed by the reflection itself.
Unlike B, they cannot be chosen.

## 2. Result: 5D torsion cannot twist fermions

A twist along y needs a coupling to the y-component of a vector current,
X&middot;&psi;&#772;&Gamma;^y&psi;, with a background X whose integral over the circle is nonzero.

- **Minimal Cartan coupling.** Only the totally antisymmetric torsion T_[ABC]
  couples, through &Gamma;^{ABC}. T_[&mu;&nu;&rho;] gives a 4D axial-vector coupling, and
  T_[&mu;&nu;y] gives a dipole coupling &psi;&#772;&sigma;_&mu;&nu;&psi;. **Neither shifts the y-momentum.**
- **Non-minimal coupling c_T T_A&psi;&#772;&Gamma;^A&psi;.** This does contain c_T T_y J^y, which is
  a twist. But **T_y has one y index, so it is Z&#8322;-odd**: the phase is +a on
  (0, &pi;R) and &minus;a on (&pi;R, 2&pi;R), and the holonomy over the covering circle
  **vanishes identically**. The numerical check gives 2&times;10&#8315;&#8309;, which is grid error.
- **A frame rotation along y** that commutes with 4D Lorentz symmetry does not
  exist in 5D. The only frame twist is the discrete (&minus;1)^F, which is the spin
  structure itself.

**Therefore round 4's &chi; is not realised in 5D Poincar&eacute; gauge theory on S&sup1;/Z&#8322;.**
The R4 conclusions that relied on &chi; are withdrawn: "&beta; = &alpha;/2 without
tuning via torsion" and "torsion twist = dark matter". The R4 dynamics are
correct for a field like &chi;; such a field simply does not arise here. It
could arise in six or more dimensions, where internal rotation planes exist.

## 3. Result: the dilemma is an exact theorem

**Theorem (positivity).** Take a unitary 5D theory on R&#8308;&times;S&sup1; with the boundary
conditions of a smooth birth (bosons periodic, fermions antiperiodic) and
holonomies &theta;_i coupling to integer charges Q_i. Then the vacuum energy
satisfies E(&theta;) &ge; E(0) **to all orders and non-perturbatively**.

*Proof.* Use y as Euclidean time, which is allowed by reflection positivity.
With these boundary conditions the partition function is a trace with positive
weights:

Z(&theta;) = Tr[e^{&minus;LH} e^{i&theta;&middot;Q}] = &sum;_n e^{&minus;LE_n} e^{i&theta;&middot;q_n}.

Hence |Z(&theta;)| &le; Z(0), and since E(&theta;) = &minus;ln Z(&theta;)/V&#8324;, E(&theta;) &ge; E(0).

On the orbifold, Z(&theta;) = &lang;B&#8320;|e^{&minus;&pi;RH}U(&theta;)|B_&pi;&rang;. When the two boundary states are
identical, which is the half-disc birth condition, Cauchy&ndash;Schwarz gives the
same bound. &#8718;

This generalises R4.A from one loop to all orders. It also shows why the
original `stur_final.py` hilltop works: with **periodic** fermions the trace
contains (&minus;1)^F, the weights are not positive, and no bound applies. But a
smooth birth forbids periodic fermions.

**Brane terms that preserve the orbifold parity do not help** (R5.L2).
On the orbifold the two bulk segments are equal, so the transfer-matrix trace is
Tr(Q e^{J&#8320;}) with Q &gt; 0, which is positive. In 20,000 random brane terms (masses,
kinetic terms, mixings at either brane), **no case** turns the birth point
into a hilltop. With unequal segments (not an orbifold), 783 cases do. So the
protection comes from the orbifold geometry itself.

## 4. Result: the one local term that escapes

To escape the theorem the boundary weights must stop being positive. For a
**local** brane term, that requires one that is **odd under the orbifold
parity**. The minimal such term is

&delta;L_0 = &minus;y_S &Sigma;(x) &psi;&#772;&Gamma;^y&psi; &delta;(y),

with &Sigma; an orbifold-odd brane scalar. The current &psi;&#772;&Gamma;^y&psi; is odd, &Sigma; is odd, so the
product is even and the term is allowed.

- **Before** &Sigma; condenses (&lang;&Sigma;&rang; = 0, e.g. at birth): the term vanishes, the branes
  are untwisted, the theorem holds, and &theta; = 0 is the minimum. **Consistent with
  a smooth birth.**
- **After** &Sigma; condenses through its ordinary, local, tree-level potential V(&Sigma;):
  the orbifold parity is broken on the brane. In the transfer matrix this is a
  pure phase e^{&minus;i&delta;} with &delta; = y_S&lang;&Sigma;&rang;, i.e. a **localized twist that acts on &psi;
  only**. The scalar &phi; is not affected unless it is given its own coupling.
- **The &theta; hilltop moves to &theta; = &pi; &minus; &delta;** (R5.L3). It sits exactly at the birth
  point for &delta; = &pi;. Starting from the birth point, &beta; is within 3% of &alpha;/2 if
  |&delta; &minus; &pi;| &lt; 0.094.

**What this means for "the orbifold twists" and "resistance".** The twist is
the spontaneous breaking of the orbifold parity on a brane. The "resistance"
is the brane potential V(&Sigma;): a classical, local energy that makes the
untwisted brane unstable once the universe has cooled. This also restores the
original STUR-ROLL statement that "the trigger is cooling", now as a
brane phase transition.

## 5. What remains open

1. **&delta; = &pi; is not yet derived.** With an ordinary (non-compact) &Sigma;, &delta; = y_S&lang;&Sigma;&rang;
   is a continuous parameter, so the 3% accuracy requirement moves from a
   random initial condition to a parameter relation. One possible fix is a
   compact brane field (an angle &vartheta;, coupling &vartheta;J^y) whose potential has its
   minimum at the CP-symmetric point &vartheta; = &pi;. Then &delta; = &pi; exactly by symmetry. Building
   this, including how the two branes' contributions combine, is the next step.
2. **Brane domain walls.** A Z&#8322;-odd &Sigma; has two vacua &plusmn;v. If &delta; = &plusmn;&pi;, both give the
   same twist modulo 2&pi;, but the walls between them on the brane still need a
   cosmological check (bias, or inflating them away).
3. **Dark matter and dark energy.** The derivation leads away from torsion.
   Within STUR-ROLL neither is explained. Dark matter remains a standard
   component and dark energy a cosmological constant, unless a separate sector
   is added. Teleparallel f(T) acceleration [T3 in R4] has not been tested.
4. **Six dimensions.** If a continuous fermion-only frame twist is wanted, it
   needs at least six dimensions. The positivity theorem still constrains it:
   any holonomy born untwisted sits at a minimum unless something breaks
   positivity, as the brane term does here.

## References

- Positivity of the trace with imaginary chemical potential: standard. The
  proof above is self-contained. For the related use of positivity to restrict
  symmetry breaking, see C. Vafa, E. Witten, *Nucl. Phys. B* **234**, 173 (1984).†
- Poincar&eacute; gauge theory and torsion couplings: [T1], [T2] in
  [`REFINEMENT_R4.md`](REFINEMENT_R4.md).
- Orbifold parities and the fermion pair: [`R2_ORBIFOLD_LEVEL.md`](R2_ORBIFOLD_LEVEL.md).
