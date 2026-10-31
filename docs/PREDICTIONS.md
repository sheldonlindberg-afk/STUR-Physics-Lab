# STUR-ROLL predictions and falsification

## Headline

    |beta| = alpha / 2 = 0.2091 deg      (k = 1, no fitted parameter)
    computed: 0.2080 deg                  (m = 1e-30 eV, seed 1e-4)

| Dataset | Measured &beta; | Pull |
|---|---|---|
| joint 2026 (ACT DR6 + Planck) | 0.277 &plusmn; 0.057&deg; | &minus;1.21&sigma; |
| ACT DR6 | 0.215 &plusmn; 0.074&deg; | &minus;0.09&sigma; |
| WMAP + Planck PR4 | 0.342 &plusmn; 0.0925&deg; | &minus;1.45&sigma; |

## &beta;(&ell;): the multipole pattern

Full &beta;(&ell;) from the CLASS E-mode source (seed 1e-4). The same cosmology and
tanh reionization are used, with z_re = 7.690. The projection reproduces the
shape of CLASS C_&ell;^EE to 0.2% for &ell; = 2&ndash;100 and returns a constant angle
exactly.

| m [eV] | &ell;=2 | 3 | 4 | 6 | 8 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| 1e-31 | 0.1244 | 0.1632 | 0.1850 | 0.2020 | 0.2067 | 0.2057 | 0.2025 | 0.2017 | 0.2019 |
| 3e-31 | 0.0212 | 0.0349 | 0.0494 | 0.0804 | 0.0958 | 0.1178 | 0.1780 | 0.2035 | 0.2055 |
| 1e-30 | 0.0000 | 0.0009 | 0.0023 | 0.0109 | 0.0345 | 0.0524 | 0.1507 | 0.2029 | 0.2075 |

(degrees). From &ell; ~ 6 the recombination E modes contribute, and &beta;(&ell;) climbs
to the &alpha;/2 plateau by &ell; ~ 20. The in-script reionization-only projection
(`Reion`) agrees with CLASS to &le; 0.004&deg; for &ell; &le; 5 but misses that rise, so
use this table.

Reionization-era angle relative to recombination (full line-of-sight
projection): &beta;_reio / &beta;_rec = 0.6&ndash;0.8 at m = 1e-31 eV, ~0.2 at 3e-31 eV,
and ~0 for m &ge; 1e-30 eV.

## Shape alone does not discriminate

A generic ALP with a quadratic potential, a free mass and a free amplitude
fits these curves ([`src/alp_vs_stur.py`](../src/alp_vs_stur.py)):

| m_STUR [eV] | best ALP mass [eV] | rms residual | &beta;(2) &minus; &beta;(30) |
|---|---|---|---|
| 1e-31 | 1.1e-32 | 0.0051&deg; | &minus;0.0775&deg; |
| 3e-31 | 4.4e-32 | 0.0072&deg; | &minus;0.1843&deg; |
| 1e-30 | 3.6e-31 | 0.0003&deg; | &minus;0.2074&deg; |

## What does discriminate

> **Scope of these discriminators (refinement round 1).** They separate
> STUR-ROLL from a *generic* ALP. They do **not** separate it from the hilltop
> domain-wall scenario of Lee, Murai, Takahashi & Yin (PRD 112, 043538,
> 2025) with c_&gamma; = 1, which has the same amplitude and the same
> isotropy. A distinguishing prediction would have to come from the 5D sector;
> see [`REFINEMENT_R1.md`](REFINEMENT_R1.md), open item 3.


1. **The amplitude.** The plateau is exactly &alpha;/2. Testing this needs an
   absolute calibration of the polarization angle.
2. **The calibration-free difference.** A miscalibration rotates every &ell;
   equally, so &beta;(&ell;) &minus; &beta;(30) is immune to it. STUR-ROLL fixes the size:
   |&beta;(2) &minus; &beta;(30)| = 0.078, 0.184 and 0.207&deg; for m = 1e-31, 3e-31 and
   1e-30 eV, and it is **never more than &alpha;/2 = 0.209&deg;**. An ALP has no such
   bound, because its amplitude is free.
3. **No anisotropic birefringence at high &ell;.** &theta; = 0 at every emission point,
   so the recombination rotation is exactly uniform. An ALP with initial-angle
   fluctuations rotates patchily there.

## Falsification criteria (LiteBIRD)

**Sharpest test (round 2, R2.1).** In the derived-amplitude window
2e-31 &lesssim; m &lesssim; 1e-28 eV, STUR-ROLL predicts
**&Delta;&beta; = &beta;_reio &minus; &beta;_rec &isin; [&minus;0.209&deg;, &minus;0.146&deg;]**. With LiteBIRD&rsquo;s
&sigma;(&Delta;&beta;) &asymp; 0.05&deg; this is 2.9&ndash;4.2&sigma; from zero. An instrumental miscalibration
and late-rolling (dark-energy-like) fields give &Delta;&beta; &asymp; 0 instead.

STUR-ROLL is falsified if:

- |&beta;| &asymp; 0.2&deg; is confirmed together with &Delta;&beta; &asymp; 0;

- |&beta;| moves away from 0.209&deg;;
- |&beta;(low &ell;) &minus; &beta;(high &ell;)| exceeds 0.209&deg; (calibration-free);
- no single &theta; mass fits the measured &beta;(&ell;);
- anisotropic birefringence is found at high &ell;.

If the current &beta; signal turns out to be a calibration systematic, the
test disappears. STUR-ROLL is then not confirmed, and it is only weakly
disfavoured.
