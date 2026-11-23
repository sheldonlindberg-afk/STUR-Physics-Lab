# M_W residual: what the literature says about the 0.04 GeV the ladder does not derive

Status: a literature compilation, not a derivation. Nothing here is a ladder link. Every number is labelled
**LIT** (taken from a source, with the source and how it was accessed), **CALC** (my arithmetic with the repo's
constants, reproducible with the script described in section 1), or **EST** (my rough inference, flagged).
Where a source could not be read, that is said and no number is invented.

Context (repo, Links 29, 31, 33): M_W = 80.410 GeV (alpha_s = 0.118; 80.415 at 0.108) against 80.3692 measured.
Gap = 0.041 GeV; the repo quotes Delta r_rest = +0.0022 (L33b, `ferm_dr_derived`).

## 1. Sensitivity (CALC)

Solving M_W^2 (1 - M_W^2/M_Z^2) = pi alpha(0) / (sqrt2 G_F) / (1 - Delta r) with the repo's constants
(alpha(0) = 1/137.035999084, G_F = 1.1663788e-5, M_Z = 91.1880, m_t = 172.57) and linearising at M_W = 80.410:

- dM_W/d(Delta r) = **-16.67 GeV per unit Delta r**, i.e. **-1.667 MeV per 1e-4** in Delta r (a positive Delta r lowers M_W).
- Closing 0.0412 GeV needs Delta delta r = +0.00245 on this linearisation (the repo's 0.0022 is the same quantity
  computed with its unrounded M_W; the difference is rounding of 80.410 and the nonlinearity, about 4 MeV).
- For a shift of Delta rho: Delta M_W = (M_W/2) c^2/(c^2 - s^2) Delta rho = **56.3 GeV x Delta rho** (CALC, s^2 = 0.2224).
  This is the formula quoted by Weiglein (hep-ph/0312314, eq. 5; LIT, read). Via Delta r = -(c^2/s^2) Delta rho
  and the sensitivity above one gets 58.3 GeV x Delta rho; the 3% difference is the M_W dependence of s^2, irrelevant here.
- Leading term: Delta rho_0 = 3 x_t, x_t = G_F m_t^2 / (8 sqrt2 pi^2) = 3.111e-3, Delta rho_0 = 9.332e-3 (CALC, matches the repo).
- Convention check: positive Delta r lowers M_W; negative Delta rho lowers M_W; the QCD terms below all have negative Delta rho coefficients.

## 2. The QCD series for Delta rho (pole mass)

LIT (Chetyrkin-Kuhn-Steinhauser, hep-ph/9502291, abstract read via WebFetch):
Delta rho = [3 G_F m_t^2 / (8 sqrt2 pi^2)] (1 - 2.8599 alpha_s/pi - 14.594 (alpha_s/pi)^2), m_t the pole mass.
The first coefficient equals the repo's c_pole = -(2/3)(1 + pi^2/3) = -2.8599 (Link 33a), a consistency check.
LIT (Chetyrkin, Faisst, Kuhn, Maierhofer, Sturm, hep-ph/0605201, read from the PDF text): the next term is
(alpha_s/pi)^3 with pole-mass coefficient **-93.1501**. Same normalisation, so Delta rho = 3 x_t (1 + c1 a + c2 a^2 + c3 a^3), a = alpha_s/pi.

| item | coefficient | Delta rho | Delta r | Delta M_W (alpha_s = 0.118) | (alpha_s = 0.108) |
|---|---|---|---|---|---|
| a^1 (in the repo, L33) | -2.8599 | -1.00e-3 | +35.0e-4 | -56.5 MeV | -51.7 MeV |
| (i) a^2 | -14.594 | -1.92e-4 | +6.7e-4 | **-10.8 MeV** | -9.1 MeV |
| (ii) a^3 | -93.1501 | -4.6e-5 | +1.6e-4 | **-2.6 MeV** | -2.0 MeV |

All CALC from the LIT coefficients (script: the numbers follow from Delta M_W = 56.3 GeV x Delta rho and c^2/s^2 = 3.496).
Series check (CALC): the terms are 1, -0.107, -0.0206, -0.0042 at alpha_s = 0.118, so the pole-mass series converges, with ratios of about 5.

### (i) O(alpha alpha_s^2), leading m_t^2

- LIT, hep-ph/0605201 (read): "For fixed pole mass of the top quark, the three-loop result leads to a shift of about 10 MeV
  in the mass of the W-boson"; the corresponding shift of the top pole mass is 1.5 GeV. Matches CALC (-10.8 MeV).
- LIT, Weiglein hep-ph/0312314 (read): the three-loop QCD correction Delta r^(alpha alpha_s^2) = 7.23e-4 (Table 1, M_W = 80.426, alpha_s = 0.119,
  m_t = 174.3) "leads to a shift in M_W of about -11 MeV". Matches (7.23e-4 x 1.667 = 12 MeV).
- LIT, arXiv 2604.18516 (only the search-result snippet seen; abstract page gave no MeV figures, body not read): quoted O(alpha alpha_s^2) tb shift
  of about -11.61 MeV (light quarks -0.23). Treat as UNVERIFIED; it agrees with the others.
- Avdeev-Fleischer-Mikhailov-Tarasov (hep-ph/9406363): the first result differed from CKS; the later CKS paper states "The result differs from the one
  recently calculated by Avdeev et al."; the Avdeev paper has an erratum (Phys. Lett. B349, 597). I could not read how the discrepancy was resolved or
  the Avdeev coefficient; the CKS number -14.594 is the one the later literature uses. Not independently confirmed.
- Direction: lowers M_W. Size: about -9 to -11 MeV (-9 at alpha_s = 0.108, -11 at 0.118).

### (ii) O(alpha_s^3) (four-loop Delta rho)

- LIT, hep-ph/0605201 (read): pole-mass coefficient -93.1501; "for fixed top mass, this corresponds to a shift of around 2 MeV in the W-boson mass". CALC gives -2.6 MeV at alpha_s = 0.118.
- In the MS-bar mass scheme (mu = m_t, six-flavour alpha_s): the four-loop coefficient is -1.6799 total = singlet -3.2866 + non-singlet +1.6067 (n_h = 1, n_l = 5; LIT, same paper, read). Inclusion of the non-singlet piece "halves the final value of the four-loop correction for the minimally renormalized top-quark mass".
  The MS-bar and pole numbers are not separately comparable in MeV; the MS-bar series carries the large terms at lower orders.
- Direction: lowers M_W. Size: about -2 to -3 MeV.

## 3. (iii) Two-loop electroweak, leading m_t^4 (van der Bij-Veltman, Barbieri et al.)

- LIT: Delta rho = 3 x_t [1 + x_t rho^(2)(M_H/m_t)], with rho^(2)(M_H = 0) = 19 - 2 pi^2 = -0.739 (van der Bij-Hoogeveen at M_H -> 0; Barbieri et al., Phys. Lett. B288, 95 (1992) and Nucl. Phys. B409, 105 (1993), for arbitrary M_H). Sources: web search summaries and a PDF-extracted statement (the form of the bracket came from a fetch tool's recollection, not text I could read); I could NOT read the explicit M_H function, so I have no LIT value of rho^(2) at M_H = 125 GeV (m_H/m_t = 0.73). The reviews say the M_H dependence is strong.
- CALC at M_H = 0: Delta rho = 3 x_t^2 (-0.739) = -2.1e-5, Delta M_W = **-1.2 MeV**.
- EST: if rho^(2) at M_H = 125 were between -0.74 and -2 (the -2 is illustrative, NOT LIT), the shift would be -1 to -3 MeV. The leading-m_t^4 term is a small part of the whole two-loop electroweak correction (next bullet).
- LIT (Weiglein, hep-ph/0312314, Table 1, read), Delta r in units of 1e-4 at M_W = 80.426 in the expanded convention M_W^2 (1 - M_W^2/M_Z^2) = pi alpha / (sqrt2 G_F) (1 + Delta r):

  | M_H | Delta r^(alpha) | alpha alpha_s | alpha alpha_s^2 | alpha^2 ferm | alpha^2 bos | G^2 alpha_s m_t^4 | G^3 m_t^6 |
  |---|---|---|---|---|---|---|---|
  | 100 | 283.41 | 35.89 | 7.23 | 28.56 | 0.64 | -1.27 | -0.16 |
  | 200 | 307.35 | 35.89 | 7.23 | 30.02 | 0.35 | -2.11 | -0.09 |
  | 300 | 323.27 | 35.89 | 7.23 | 31.10 | 0.23 | -2.77 | -0.03 |

  The pure-fermion-loop 3- and 4-loop terms have "a net effect of only about 1 MeV in M_W". The O(G^2 alpha_s m_t^4) term gives up to 5 MeV (for M_H <~ 350 GeV), O(G^3 m_t^6) at most 1 MeV, both from the sign above raising M_W (negative Delta r).
  Interpolating in ln M_H to 125 GeV: G^2 alpha_s m_t^4 is about -1.5e-4, i.e. about +2.5 MeV (EST/CALC; wrong sign relative to the gap, small). G^3 m_t^6 about -0.15e-4, +0.3 MeV.
- Full two-loop fermionic Delta r^(alpha^2)_ferm = 28.6 to 31.1e-4 in that table. Taken naively it would lower M_W by 48 to 52 MeV, but the expanded convention includes the reducible term (Delta r^(alpha))^2 = (283e-4)^2 = 8.0e-4 that the repo already contains through 1/(1 - Delta r).
  EST: the irreducible two-loop electroweak piece (ferm + bos) is about 29 - 8 = **+(20 +- 5)e-4**, i.e. **-34 MeV (about -25 to -42)** at M_H = 125. This is my own subtraction, not a literature number; the sign of the cross terms with Delta alpha and the QCD pieces, and the different M_W/m_t inputs (80.426, 174.3), are uncontrolled.
  It is also the one item that is the right size: the repo's remaining Delta r_rest = +22e-4 (or 24.5e-4 on my linearisation).
- LIT (Awramik et al., hep-ph/0311148, search snippet): the revised two-loop fermionic result shifted M_W by about -1.3 MeV relative to an earlier calculation (detail not read).
- Direction: the two-loop EW terms as a whole lower M_W by tens of MeV; the leading-m_t^4 piece alone only by a few MeV.

## 4. (iv) Non-leading O(alpha alpha_s)

- LIT (Weiglein Table 1, read): the complete two-loop QCD Delta r^(alpha alpha_s) = 35.89e-4 (alpha_s = 0.119, m_t = 174.3).
- CALC: the repo's leading-m_t^2 pole-mass term at alpha_s = 0.118, m_t = 172.57 gives 35.0e-4 (table above); rescaled to Weiglein's inputs (m_t^2 ratio 1.020, alpha_s ratio 1.008) it is about 36.0e-4.
  EST: the non-leading and m_b-dependent parts are therefore small, at most about 1e-4 in Delta r, **|Delta M_W| <~ 2 MeV**, sign not determined by this comparison (input differences are of the same order). I could not read a source giving the non-leading O(alpha alpha_s) formulas separately (Djouadi-Verzegnassi, Kniehl-Kuhn-Stuart, Kniehl-Sirlin are the references; none fetched), so this is a bound from the comparison, not a derivation. Also the Weiglein number includes the Delta alpha-type light-quark/charm pieces, which the comparison cannot separate.
- LIT (arXiv 2604.18516, snippet only, UNVERIFIED): the on-shell O(alpha alpha_s) tb shift about -59.62 MeV and light quarks -1.98 MeV; compare CALC leading term -56.5 MeV, consistent with a non-leading remainder of order a few MeV.

## 5. (v) alpha_s scale and top-mass scheme

- alpha_s: moving 0.118 -> 0.108 changes the O(alpha alpha_s) term by +4.8 MeV (CALC; the repo's 80.410 -> 80.415), the higher a^2, a^3 terms by +1.7 and +0.6 MeV. A genuine scale choice (mu between m_t/2 and 2 m_t, alpha_s(m_t) = 0.108 vs alpha_s(M_Z) = 0.118) is the same size, so about +-5 MeV on the a^1 term; the unknown a^3 and higher terms are the compensating part. Direction of the effect on the gap: a larger alpha_s lowers M_W (towards the data); the freedom runs the wrong way to supply 41 MeV (it adds at most a few MeV of lowering).
- LIT (Weiglein Table 2, read): dM_W/d alpha_s(M_Z) = 1.7 MeV per 0.0027, i.e. 0.63 MeV per 0.001 in the full prediction (it includes the effect on other terms).
- Pole vs MS-bar top: the repo's L33a gives c_MS-bar(mu = m_bar) = C_F(3/2 - pi^2/6) = -0.1932 against c_pole = -2.8599. For the same Delta rho the two are the same physics only if m_t is converted: m_pole = m_bar [1 + C_F (alpha_s/pi)(1 + 3/4 ln(mu^2/m_bar^2))]. At alpha_s = 0.118 (CALC) this relation gives m_pole - m_bar = (4/3)(0.0376) m_bar = 0.050 m_bar, about 8 GeV at one loop, and the whole of the difference is in the QCD coefficient, so the conversion is the largest scheme effect and what the higher orders must absorb.
- LIT (Weiglein Table 2, read): dM_W/dm_t = 31 MeV per 5.1 GeV, i.e. **6.1 MeV per GeV** of m_t. Consistent with the 10 MeV for 1.5 GeV in hep-ph/0605201 (CALC: 9 MeV). So the unavoidable ambiguity in what m_t = 172.57 GeV (PDG direct-measurement average, not a pure pole mass) means is itself worth several MeV; I found no sourced number for the scheme uncertainty of the measured mass, so none is quoted. A shift of m_t by 0.5 GeV would be 3 MeV.
- LIT (Degrassi-Gambino-Giardino, arXiv 1411.7040, abstract read): the full MS-bar prediction is m_W = 80.357 +- 0.009 (parametric) +- 0.003 (theory) GeV, and the on-shell-scheme result differs by about 6 MeV. LIT (Weiglein): the remaining uncertainty of the on-shell prediction is about 4 MeV for M_H <~ 300 GeV.

## 6. Which items account for the 0.04 GeV

Required: lower M_W from 80.410 by 41 MeV (Delta r + 24.5e-4 linearised; repo 22e-4). Literature total SM prediction: 80.357 GeV (LIT, 1411.7040), i.e. a total of about 53 MeV below the repo's 80.410 and 12 MeV below the measurement (within the quoted +-9 MeV parametric and the +-13 MeV PDG error).

| contribution | shift of M_W (MeV) | direction | status |
|---|---|---|---|
| (i) O(alpha alpha_s^2) leading m_t^2 | -9 to -11 | lowers | derived-size LIT, plausible, 1/4 of the gap |
| (ii) O(alpha_s^3) | -2 to -3 | lowers | small |
| (iii) leading m_t^4 two-loop EW, M_H = 125 | about -1 to -3 (CALC at M_H = 0: -1.2) | lowers | small; no M_H = 125 value found |
| (iii') full two-loop EW (ferm + bos), irreducible part | about -34 (EST -25 to -42) | lowers | **the plausible main account**, right size |
| three-loop mixed/EW (G^2 alpha_s m_t^4, G^3 m_t^6, pure fermion) | +2.5, +0.3, about +1 | raises | small, partly cancels |
| (iv) non-leading O(alpha alpha_s) | within +-2 | either | small |
| (v) alpha_s scale, a few MeV; m_t scheme about 6 MeV per GeV | +-5; +-3 | either | the error band |

Sum of the shifts that are known in sign: (i) + (ii) = about -13 MeV, plus (iii') about -34 gives **-47 MeV**, against the -41 MeV needed (and -53 MeV expected from the full literature prediction); the three-loop mixed terms add back about +4 MeV. The difference (a few MeV to about 12 MeV) is inside the stated 4-9 MeV theory/parametric uncertainties and my EST error on the two-loop subtraction.

Plausibly account for the 0.04 GeV: the two-loop electroweak correction (iii'), with (i) and (ii) supplying about 13 MeV of it by themselves.
Would not account for it on their own: (i) (about 10 MeV), (ii) (about 2 MeV), the leading-m_t^4 term (1 to 3 MeV), the non-leading O(alpha alpha_s) (<= 2 MeV), the alpha_s scale (about 5 MeV).
Would overshoot: nothing that is individually sized, but (iii') quoted naively (28.6 to 31.1e-4, giving 48 to 52 MeV) overshoots by double counting the reducible (Delta r^(alpha))^2 term and should not be used as is; all of (i), (ii), (iii') together overshoot the 41 MeV gap slightly (47 vs 41, the literature's full answer being 53 vs 41), i.e. the repo's prediction after adding the known terms would land about 6 to 12 MeV below the measurement, as the literature prediction does.

## Sources and access status

- hep-ph/9502291 (CKS): abstract read, coefficients -2.8599 and -14.594; MS-bar coefficients not on that page.
- hep-ph/0605201: PDF text read (3-loop 10 MeV, 4-loop pole -93.1501, MS-bar -1.6799, 2 MeV).
- hep-ph/0312314 (Weiglein review): PDF text read (Tables 1 and 2, equations 5-11).
- hep-ph/9406363 (Avdeev et al.): search summary only; erratum noted; not read.
- Barbieri et al., Nucl. Phys. B409 (1993) 105 and Phys. Lett. B288 (1992) 95; van der Bij-Hoogeveen: referenced only (reference list of 0605201 and search summaries); explicit rho^(2)(M_H) not read. hep-ph/9603374 PDF could not be text-extracted for formulae of interest (no extracted numbers used).
- arXiv 1411.7040: abstract read. arXiv 2604.18516: abstract page and search snippet only; its MeV numbers are unverified. arXiv 2610.08282: not used.
- hep-ph/0311148 (Awramik et al.): search summary only.
