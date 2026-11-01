# STUR-ROLL predictions and falsification

> **In plain terms.** A good theory sticks its neck out. STUR-ROLL makes one
> headline number, a rotation of 0.209&deg;, plus a pattern that says *when*
> the rotation happened. The LiteBIRD satellite (launch planned for the
> 2030s) can check both. Below are the numbers and the exact results that
> would kill the idea.

## Headline

    |beta| = alpha / 2 = 0.2091 deg      (k = 1, no fitted parameter)
    computed: 0.2080 deg                  (m = 1e-30 eV, seed 1e-4)

| Dataset | Measured &beta; | Pull |
|---|---|---|
| joint 2026 (ACT DR6 + Planck) | 0.277 &plusmn; 0.057&deg; | &minus;1.21&sigma; |
| ACT DR6 | 0.215 &plusmn; 0.074&deg; | &minus;0.09&sigma; |
| WMAP + Planck PR4 | 0.342 &plusmn; 0.0925&deg; | &minus;1.45&sigma; |

A pull is (prediction &minus; measurement)/error: all three measurements lie
within 1.5 standard deviations of the prediction.

## &beta;(&ell;): the multipole pattern

> **In plain terms.** The CMB polarization we see was produced twice: once
> when the CMB was released (fine-grained patterns, high &ell;) and again when
> the first stars re-ionized the universe (sky-wide patterns, low &ell;). Light
> from the first event was rotated by the full &alpha;/2. Light from the second
> event was rotated less, because by then the field had already rolled
> part or all of the way. So the angle depends on the angular scale &ell;.

Full &beta;(&ell;) from the CLASS E-mode source (seed 10&#8315;&#8308;). Same cosmology
and tanh reionization, with z_re = 7.690. The projection reproduces the shape
of CLASS C_&ell;^EE to 0.2% for &ell; = 2&ndash;100 and returns a constant angle
exactly.

| m [eV] | &ell;=2 | 3 | 4 | 6 | 8 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| 1e-31 | 0.1244 | 0.1632 | 0.1850 | 0.2020 | 0.2067 | 0.2057 | 0.2025 | 0.2017 | 0.2019 |
| 3e-31 | 0.0212 | 0.0349 | 0.0494 | 0.0804 | 0.0958 | 0.1178 | 0.1780 | 0.2035 | 0.2055 |
| 1e-30 | 0.0000 | 0.0009 | 0.0023 | 0.0109 | 0.0345 | 0.0524 | 0.1507 | 0.2029 | 0.2075 |

(degrees). From &ell; ~ 6 the recombination E modes contribute, and &beta;(&ell;)
climbs to the &alpha;/2 plateau by &ell; ~ 20. The in-script
reionization-only projection (`Reion`) agrees with CLASS to &le; 0.005&deg; for
&ell; &le; 4 (R7 A6) but misses that rise, so use this table. The CLASS run
script (`class_check.py`) is not yet in the repository; the &ell; &ge; 30 values
match the plateau computed independently by `stur_final.py`.

## Shape alone does not discriminate

A generic axion-like particle (ALP) with a quadratic potential, a free mass
and a free amplitude fits these curves ([`src/alp_vs_stur.py`](../src/alp_vs_stur.py)):

| m_STUR [eV] | best ALP mass [eV] | rms residual | &beta;(2) &minus; &beta;(30) |
|---|---|---|---|
| 1e-31 | 1.1e-32 | 0.0051&deg; | &minus;0.0775&deg; |
| 3e-31 | 4.4e-32 | 0.0072&deg; | &minus;0.1843&deg; |
| 1e-30 | 3.6e-31 | 0.0003&deg; | &minus;0.2074&deg; |

## What does discriminate

These separate STUR-ROLL from a *generic* ALP. They do not separate it from
the hilltop scenario of Lee, Murai, Takahashi & Yin [3] with c_&gamma; = 1 and
a mass in the same window; STUR-ROLL is a derivation of that scenario, not a
rival to it (R1.3, R2.1).

1. **The amplitude.** The plateau is exactly &alpha;/2. Testing this needs an
   absolute calibration of the polarization angle.
2. **The calibration-free difference.** A miscalibration rotates every &ell;
   equally, so &beta;(&ell;) &minus; &beta;(30) is immune to it. Its size is
   never more than &alpha;/2 = 0.209&deg;. An ALP has no such bound, because
   its amplitude is free.
3. **No anisotropic birefringence at high &ell;.** &theta; &asymp; 0 at every
   recombination emission point, so that rotation is uniform across the sky.

## The tomographic test (sharpest)

> **In plain terms.** Compare the rotation of the "late" light (from
> reionization) with that of the "early" light (from the CMB release). In
> STUR-ROLL the late light is rotated much less, so the difference is large
> and negative. If instead the rotation were an instrument error, or a field
> that rolled only recently, the difference would be zero.

In the derived-amplitude window 2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim;
10&#8315;&sup2;&#8312; eV (R2.1, corrected in R7 A2):

| Case | &Delta;&beta; = &beta;_reio &minus; &beta;_rec | at LiteBIRD (&sigma; &asymp; 0.05&deg;) |
|---|---|---|
| our reionization shell in one domain | [&minus;0.209&deg;, &minus;0.146&deg;] | 2.9&ndash;4.2&sigma; from zero |
| expected opposite-domain fraction, N_extra &ge; 60 (&le; 0.085) | [&minus;0.209&deg;, &minus;0.122&deg;] | 2.4&ndash;4.2&sigma; from zero |
| half the shell in an opposite domain (rare) | &asymp; 0 | indistinguishable from zero, **but** with a large-scale anisotropic rotation, sky rms &asymp; 0.2&deg; |

An opposite-sign domain rotates reionization light by &alpha; &minus; &beta;_own
instead of &beta;_own, which is why the window widens (R7 A2).

## Falsification criteria (LiteBIRD)

STUR-ROLL is falsified if any of these holds:

1. **|&beta;| &asymp; 0.2&deg; is confirmed with &Delta;&beta; &asymp; 0 and no
   large-scale anisotropic reionization rotation.** (The only way STUR-ROLL
   can give &Delta;&beta; &asymp; 0 is a half-and-half sky, which would show up
   as that anisotropy.)
2. **|&beta;| moves away from 0.209&deg;.** The amplitude is fixed.
3. **|&beta;(low &ell;) &minus; &beta;(high &ell;)| exceeds 0.209&deg;.**
   Calibration-free.
4. **No single &theta; mass fits the measured &beta;(&ell;).**
5. **Anisotropic birefringence is found at high &ell;** (recombination era).

If the current &beta; signal turns out to be a calibration systematic, the
test disappears. STUR-ROLL is then not confirmed, and only weakly disfavoured.

## Further predictions (rounds 3&ndash;6)

- **Tensor modes:** r &lesssim; 10&#8315;&sup3; unless f &gtrsim; 10&sup1;&#8308; GeV. If
  the nucleation phase is R&sup2; inflation: r &asymp; 0.003,
  2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 3&times;10&#8315;&sup3;&#8304; eV and
  f &asymp; 2&ndash;8&times;10&sup1;&#8308; GeV (R3.3).
- **Colliders:** a KK hypercharge boson near 6 TeV, with 4&ndash;5&times; the SSM
  dilepton rate, appears only at the 1/L &asymp; 1 TeV edge (R2.3).
- **No fractionally charged colour-singlet particles** (Z&#8326; structure, R3.2).
- **One sign of &beta; on our sky.** The recombination-era rotation has the same
  sign in every direction, set by &theta; in our own region. The sign is random
  from region to region of the wider universe; the brane twist does not fix it
  (corrected in R7 A1).
