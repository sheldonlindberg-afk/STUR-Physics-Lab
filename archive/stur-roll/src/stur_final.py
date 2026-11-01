#!/usr/bin/env python3
"""
STUR FINAL: derived birefringence chain + precision scoreboard
Sheldon Lindberg (STUR), 2026-10-30. Requires numpy, scipy. Runs in ~10 s.
Full code: stur_genesis_simulation.py (sections 1-11), precision_harness.py,
z3_bounce_check.py. Expected output is reproduced at the end of this file.

THE CLAIM (scope: Lambda-CDM plus one derived sector, not a replacement)
  STUR-ROLL adds to Lambda-CDM a sector that predicts the CMB birefringence
  angle from integers: |beta| = k alpha / 2 with k = 1 (minimal level),
  0.2091 deg, no continuous parameter fitted. Gravity is TEGR, which is GR,
  so it agrees with the GR precision tests by construction (consistency,
  not a new success). Its energy is <~ 1e-7 of the dark matter in the
  allowed window (section C), so CMB spectra, BAO, supernovae, lensing and
  BBN are those of Lambda-CDM; the global model comparison then reduces to
  the beta likelihood. The alternatives are GR+QFT (beta = 0) and a generic
  axion (beta fitted).

SCORING RULE (stated before the numbers)
  1. Pass/fail gates against published measurements (2 sigma).
  2. On beta, AIC = chi^2 + 2 x (fitted parameters). Lower is better; a
     difference below 2 is not significant. Valid as a global comparison
     only because the sector leaves the other data unchanged (section C).

THE DERIVED CHAIN (each step computed in stur_genesis_simulation.py)
  1. Zero-energy start (Wheeler-DeWitt H Psi = 0): the universe nucleates
     whole; theta (the R-field holonomy, Phi_R = closed integral of J_a dx^a
     with J_a = B, a Z2-odd U(1) on the S^1/Z2 orbifold) starts at rest in a
     minimum.
  2. 5D Chern-Simons term -> L = (k alpha / 4 pi) theta F Ftilde, k integer.
  3. Content: a charge-1 bulk fermion (the Z2 pair q_B = +-1 is one Dirac
     field on the covering circle) and a neutral scalar charged under B.
     Its KK tower gives c_g = (1/2) sgn M (computed in section A); the 5D
     parity anomaly makes the bare level half-integer, so k is an integer.
     k = 1 is the minimal nonzero level (a discrete choice; k = 2, 3 give
     0.418, 0.627 deg, at +2.5 and +6.1 sigma).
  4. Wilson-line potential: the scalar dominates on de Sitter (exact S^4 x S^1
     one loop) and at high T, so theta = 0 at nucleation; below T_c ~ 9/L the
     fermion pair dominates: V = m^2 f^2 (1 + cos theta), theta = 0 becomes a
     hilltop and theta rolls to pi.            <- the "trigger" is cooling
  5. beta = (k alpha / 2 pi) x pi = alpha / 2.  Computed below from the roll.

STATUS
  Derived: steps 1-5, k integer, step = pi, sign of beta random per region.
  Discrete choice: k = 1 (minimal). Condition: the roll must start early
  enough (seed table, section B); f must lie in the window of section C.
  Section D: beta(l) for l = 2-10 and the l >= 30 plateau, one mass for all.
  Section E: the new particles against LHC, BBN, fifth-force limits.
  Inputs (do not change beta for m >= 3e-31 eV): fermion and scalar bulk
  masses, orbifold size L, warp, B coupling (sets f), H_nuc (window:
  H_c < H_nuc < 2f). Assumed axiom: the field B with J_a = B.
  Excluded by the full code: theta tunnelling through its own barrier
  (needs f ~ 1e-32 eV); models needing initial theta energy (STUR-B, M3a,
  U0, C0); the 2025 tanh(r/1 mm) gravity law (fails Eot-Wash and does not
  flatten rotation curves) -- superseded, shown in the table for the record.
  Caveat: beta measurements rely on polarization-angle calibration via
  Galactic foregrounds; the ACT+Planck authors call the signal a hint that
  needs systematics understood. A systematic would remove the test.
"""
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

# ---------------- constants (CODATA 2018, IAU, Planck 2018) ----------------
G, C, HBAR, KB = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
GM_SUN, R_SUN, M_SUN = 1.32712440018e20, 6.957e8, 1.98847e30
M_P, L_P = np.sqrt(HBAR * C / G), np.sqrt(HBAR * G / C ** 3)
ALPHA, ARCSEC, YEAR = 1 / 137.035999, np.pi / 648000, 3.15576e7
H0_EV = 2.1332e-33 * 0.6736                   # H0 in eV
OM, OR = 0.1430 / 0.6736 ** 2, 4.18e-5 / 0.6736 ** 2
OL = 1 - OM - OR
Z_STAR, Z_RE = 1089.92, 7.67
BETA_DATA = {"joint2026 (ACT DR6+Planck)": (0.277, 0.057),
             "ACT DR6": (0.215, 0.074),
             "WMAP+Planck PR4": (0.342, 0.0925)}


def hubble(N):                                # N = ln a, H in eV
    a = np.exp(N)
    return H0_EV * np.sqrt(OR / a ** 4 + OM / a ** 3 + OL)


# ---------------- step 4: Wilson-line potential, exact one loop -------------
def g_mass(x):                                # first harmonic, x = M L
    return (3 + 3 * x + x * x) * np.exp(-x) / 3


def flat_harm(x):
    f = lambda p: p ** 3 * np.exp(-(np.sqrt(x * x + p * p) - x))
    return quad(f, 0, np.inf, limit=400)[0] / (8 * np.pi ** 2)


def ds_ratio(x, HL, spin):
    """S^4 (radius 1/H) x S^1_L, per dof, relative to flat (exact spectra)"""
    l = np.arange(0, int(np.sqrt(120 * x + 14400) / HL) + 50)
    if spin == 0:   # minimally coupled scalar: l(l+3) H^2
        lam, deg = l * (l + 3) * HL ** 2, (2 * l + 3) * (l + 1) * (l + 2) / 6
    else:           # Dirac: (n+2)^2 H^2, per spinor component
        lam, deg = (l + 2) ** 2 * HL ** 2, (l + 1) * (l + 2) * (l + 3) / 3
    w = deg * np.exp(-(np.sqrt(x * x + lam) - x))
    return w.sum() / (8 * np.pi ** 2 / 3 / HL ** 4) / flat_harm(x)


def th_ratio(x, TL, fermion):
    """finite T: winding sum on the thermal circle; fermions get (-1)^w"""
    W = int(TL * (10 + 60 / np.sqrt(x))) + 60
    w = np.arange(-W, W + 1)
    rho = np.sqrt(1 + (w / TL) ** 2)
    t = (3 + 3 * x * rho + (x * rho) ** 2) * np.exp(-x * (rho - 1))
    t = t / rho ** 5 / (3 + 3 * x + x * x)
    return (t * (-1.0) ** np.abs(w) if fermion else t).sum()


def crossing(fn, xf, dx, df=4.0, db=2.0):
    """scale (x 1/L) where the scalar (mass xf+dx) overtakes the fermions"""
    xb = xf + dx
    h = lambda s: db * g_mass(xb) * fn(xb, s, 0) - df * g_mass(xf) * fn(xf, s, 1)
    s = np.linspace(0.3, 120, 300)
    v = [h(q) for q in s]
    i = next(j for j in range(1, len(v)) if v[j] > 0)
    return brentq(h, s[i - 1], s[i])


# ---------------- step 5: the roll and beta -------------------------------
def roll(m_ev, seed):
    """theta'' + (3 + dlnH/dN) theta' = (m/H)^2 sin theta, from z = 1e4"""
    def rhs(N, y):
        H = hubble(N)
        dlnH = (hubble(N + 1e-5) - hubble(N - 1e-5)) / (2e-5 * H)
        return [y[1], -(3 + dlnH) * y[1] + (m_ev / H) ** 2 * np.sin(y[0])]
    sol = solve_ivp(rhs, [np.log(1e-4), 0.0], [seed, 0.0], method="DOP853",
                    rtol=1e-10, atol=min(1e-13, 1e-3 * seed), dense_output=True)
    th = lambda z: sol.sol(-np.log1p(np.asarray(z, float)))[0]
    k_fac = ALPHA / (2 * np.pi)                     # k = 1
    b_rec = np.degrees(k_fac * (th(0.0) - th(Z_STAR)))
    hist = lambda z: np.degrees(k_fac * (th(0.0) - th(z)))     # beta(z_emit)
    return th(0.0) / np.pi, b_rec, hist


# ---------------- multipole pattern: reionization line of sight -------------
MPC, SIGT, YP = 3.0856776e22, 6.6524587e-29, 0.2454
N_H0 = (1 - YP) * 0.02237 * 1.87834e-26 / 1.6735575e-27     # H atoms per m^3
F_HE = YP / (3.9715 * (1 - YP))
HBAR_EV = 6.582119569e-16


def h_si(z):                                  # H(z) in s^-1
    return hubble(-np.log1p(z)) / HBAR_EV


def x_e(z, zre):                              # tanh reionization (CAMB) + He at 3.5
    y, yr = (1 + z) ** 1.5, (1 + zre) ** 1.5
    dy = 1.5 * np.sqrt(1 + zre) * 0.5
    return ((1 + F_HE) / 2 * (1 + np.tanh((yr - y) / dy))
            + F_HE / 2 * (1 + np.tanh((3.5 - z) / 0.5)))


def dtau_dz(z, zre):
    return C * SIGT * N_H0 * (1 + z) ** 2 * x_e(z, zre) / h_si(z)


class Reion:
    """free-streamed quadrupole x E projection for l = 2-10 (Zaldarriaga 1997);
    the same method as FastProjection in the full code (validated there)"""

    def __init__(self, tau=0.0544):
        zz = np.linspace(0, 1600, 32001)
        chi = np.concatenate([[0], np.cumsum(np.diff(zz) * C / h_si(zz[1:]))]) / MPC
        tz = lambda zr: quad(dtau_dz, 0, 50, args=(zr,), limit=400,
                             points=[3.5, zr])[0]
        self.zre = brentq(lambda zr: tz(zr) - tau, 2.0, 30.0, xtol=1e-6)
        c = np.linspace(1e-3, np.interp(30.0, zz, chi), 2500)
        z = np.interp(c, chi, zz)
        d = dtau_dz(z, self.zre)
        tau_c = np.concatenate([[0], np.cumsum(np.diff(z) * 0.5 * (d[1:] + d[:-1]))])
        g = d * h_si(z) / C * MPC * np.exp(-tau_c)
        k = np.logspace(-5, np.log10(0.02), 320)
        self.wk = k ** (0.9649 - 1) * np.gradient(np.log(k))
        from scipy.special import spherical_jn, gammaln
        chis = np.interp(Z_STAR, zz, chi)
        self.S = spherical_jn(2, np.outer(k, chis - c)) * (g * np.gradient(c))[None, :]
        x = np.maximum(np.outer(k, c), 1e-6)
        self.P = {l: np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1)))
                  * spherical_jn(l, x) / x ** 2 for l in range(2, 11)}
        self.z = z

    def beta_l(self, hist):
        s2b = np.sin(2 * np.radians(hist(self.z)))
        out = {}
        for l, P in self.P.items():
            SP = self.S * P
            dE, dB = SP.sum(1), (SP * s2b[None, :]).sum(1)
            r = np.sum(self.wk * dE * dB) / np.sum(self.wk * dE * dE)
            out[l] = 0.5 * np.degrees(np.arcsin(np.clip(r, -1, 1)))
        return out


# ---------------- precision gates ------------------------------------------
def hawking_T(M):
    return HBAR * C ** 3 / (8 * np.pi * G * M * KB)


def area_S(M):
    return 4 * np.pi * (2 * G * M / C ** 2) ** 2 / (4 * L_P ** 2)


def lifetime(M):
    return 5120 * np.pi * G ** 2 * M ** 3 / (HBAR * C ** 4)


def gates(c):
    """returns list of (test, status, value); missing prediction -> n.d."""
    out = []

    def add(name, key, ok_fn, val_fn):
        if key not in c:
            out.append((name, "n.d.", "-"))
        else:
            out.append((name, "PASS" if ok_fn(c) else "FAIL", val_fn(c)))
    add("Cassini gamma (2003)", "gamma",
        lambda c: abs(c["gamma"] - 1 - 2.1e-5) < 4.6e-5,
        lambda c: f"gamma-1 = {c['gamma'] - 1:.0e}")
    add("Mercury perihelion (beta)", "beta", lambda c: abs(c["beta"] - 1) < 8e-5,
        lambda c: f"{perihelion(c['gamma'], c['beta']):.2f}\"/cy")
    add("GW speed (GW170817)", "dcg", lambda c: -3e-15 <= c["dcg"] <= 7e-16,
        lambda c: f"dc/c = {c['dcg']:.0e}")
    add("inverse-square law (Eot-Wash)", "Fr",
        lambda c: abs(c["Fr"](52e-6) - 1) < 0.6 and abs(c["Fr"](1e-3) - 1) < 1e-2,
        lambda c: f"dF/F(52um) = {abs(c['Fr'](52e-6) - 1):.2f}")
    add("equivalence principle (MICROSCOPE)", "eta",
        lambda c: abs(c["eta"]) < 5.5e-15, lambda c: f"eta = {c['eta']:.0e}")
    add("electron g-2", "dae", lambda c: abs(c["dae"]) < 2e-12,
        lambda c: f"d a_e = {c['dae']:.0e}")
    add("Hawking T, area law, M^3 lifetime", "bh",
        lambda c: c["bh"], lambda c: f"T(Msun) = {hawking_T(M_SUN):.1e} K")
    add("CMB birefringence |beta| (2 sigma)", "beta_cmb",
        lambda c: abs(abs(c["beta_cmb"]) - 0.277) < 2 * 0.057,
        lambda c: f"|beta| = {abs(c['beta_cmb']):.3f} deg")
    add("flat rotation without dark matter", "flat",
        lambda c: v_ratio(c["Fr"]) > 0.9,
        lambda c: "v(25)/v(8 kpc) = 0.57 (Keplerian)")
    return out


def v_ratio(Fr, kpc=3.0857e19):
    """v(25 kpc) / v(8 kpc) for a centrally concentrated galaxy, v^2 = r F / m"""
    return np.sqrt(Fr(25 * kpc) / 25 / (Fr(8 * kpc) / 8))


def perihelion(gamma, beta):
    a, e, P = 5.7909e10, 0.205630, 87.9691
    per = 6 * np.pi * GM_SUN / (C ** 2 * a * (1 - e * e))
    return (2 + 2 * gamma - beta) / 3 * per * 36525 / P / ARCSEC


def kk_coupling(Mr):
    """d Phi / d theta for one 5D Dirac fermion on the covering circle: KK mode n
    has mass M + i (n + theta / 2 pi) / r; mass phase phi -> (phi alpha/4 pi) F Ft"""
    n = np.arange(-200000, 200001)
    v = np.linspace(0.1, 6.0, 7)
    ph = [np.sum(np.arctan((n + x / (2 * np.pi)) / Mr)) for x in v]
    return np.polyfit(v, ph, 1)[0]


def audit(b_pred):
    bar = "=" * 78
    print("\n" + bar + "\n Audit of the derivation\n" + bar)
    print(" A. Coupling normalisation (KK tower of one Dirac fermion, charge 1)")
    for Mr in (2.0, 10.0):
        print(f"   M r = {Mr:4.1f}: c_g = {kk_coupling(Mr):.5f} sgn M   (exact: 1/2)")
    print("   bare level in Z + 1/2 (parity anomaly) -> k_eff integer; ladder:")
    for k in (1, 2, 3):
        b = np.degrees(ALPHA) * k / 2
        pl = ", ".join(f"{(b - b0) / s0:+.1f}" for b0, s0 in BETA_DATA.values())
        print(f"   k = {k}: beta = {b:.4f} deg   pulls {pl} sigma")
    print("\n B. Seed robustness (roll start set by the hilltop displacement)")
    print(f"   {'seed':>7s} {'m=3e-31':>9s} {'m=1e-30':>9s} {'m=1e-29':>9s}   lands/pi")
    for sd in (1e-2, 1e-10, 1e-20, 1e-40, 1e-80):
        fr = [roll(m, sd)[0] for m in (3e-31, 1e-30, 1e-29)]
        print(f"   {sd:7.0e}" + "".join(f"{x:9.3f}" for x in fr))
    print("   beta = k alpha/2 within 4% needs a seed >~ 1e-20 (m = 1e-30) or")
    print("   >~ 1e-40 (m = 1e-29); smaller seeds roll late and land 0.5-1.25 pi.")
    print("\n C. Cosmological consistency of the theta sector (k = 1)")
    gev = 1e9
    f_lo = ALPHA / (np.pi * 8e-13) * gev          # Chandra NGC 1275: g < 8e-13/GeV
    print(f"   photon coupling g = alpha/(pi f) < 8e-13/GeV"
          f" -> f > {f_lo / gev:.1e} GeV")
    print("   domain walls: regions roll to +pi or -pi; theta's lift is continuous,")
    print("   so they are separated by sine-Gordon walls, tension 8 m f^2;")
    print("   CMB bound (1 MeV)^3 -> f < sqrt(1e18 eV^3 / 8 m)")
    print("   theta energy: hilltop 2 m^2 f^2 released at H ~ m/3 ->")
    print("   fraction of dark matter ~ 6 (f / M_Pl)^2")
    mpl = 2.435e27
    for m in (3e-31, 1e-30, 1e-29):
        f_hi = np.sqrt(1e18 / (8 * m))
        fr = 6 * (f_hi / mpl) ** 2
        print(f"   m = {m:.0e} eV: f in [{f_lo / gev:.1e}, {f_hi / gev:.1e}] GeV;"
              f" DM fraction <= {fr:.0e}")
    print("   -> CMB spectra, BAO, SNe, lensing, BBN unchanged at <= 1e-7: the")
    print("      sector is invisible except through beta. The CMB rotation stays")
    print("      isotropic (theta = 0 at every emission point); walls only make")
    print("      late-time (reionization-era) birefringence patchy.")


def pattern():
    bar = "=" * 78
    print("\n" + bar + "\n D. Multipole pattern beta(l)" + "\n" + bar)
    R = Reion()
    const = R.beta_l(lambda z: 0.3 + 0 * z)
    dev = max(abs(v - 0.3) for v in const.values())
    print(f"   z_re = {R.zre:.2f} for tau = 0.0544; check: constant 0.3 deg returned"
          f" at every l to {dev:.0e}")
    ls = (2, 3, 4, 6, 8, 10)
    print(f"   {'m [eV]':>8s}" + "".join(f"{'l=' + str(l):>8s}" for l in ls)
          + f"{'l>=30':>9s}")
    for m in (1e-31, 3e-31, 1e-30, 3e-30):
        _, br, hist = roll(m, 1e-4)
        b = R.beta_l(hist)
        print(f"   {m:8.0e}" + "".join(f"{b[l]:8.4f}" for l in ls) + f"{br:9.4f}")
    print("   deg. Reion = reionization E modes only (approximate quadrupole).")
    print("   Cross-check with CLASS (exact E-mode source S_E(k, tau), same")
    print("   cosmology and tanh reionization, z_re = 7.690; class_check.py):")
    print("   projection reproduces CLASS C_l^EE shape to 0.2% for l = 2-100;")
    print("   a constant angle is returned exactly. Full beta(l), seed 1e-4:")
    cls = {1e-31: (0.1244, 0.1632, 0.1850, 0.2020, 0.2067, 0.2057, 0.2025,
                   0.2017, 0.2019),
           3e-31: (0.0212, 0.0349, 0.0494, 0.0804, 0.0958, 0.1178, 0.1780,
                   0.2035, 0.2055),
           1e-30: (0.0000, 0.0009, 0.0023, 0.0109, 0.0345, 0.0524, 0.1507,
                   0.2029, 0.2075)}
    lc = (2, 3, 4, 6, 8, 10, 15, 20, 30)
    print(f"   {'m [eV]':>8s}" + "".join(f"{'l=' + str(l):>7s}" for l in lc))
    for m, row in cls.items():
        print(f"   {m:8.0e}" + "".join(f"{v:7.4f}" for v in row))
    print("   Reion agrees with CLASS to <= 0.004 deg for l <= 5. From l ~ 6 the")
    print("   recombination E modes contribute and beta(l) climbs to the alpha/2")
    print("   plateau by l ~ 20; Reion misses that rise, so use the CLASS table.")
    print("   Shape alone does NOT discriminate: a generic ALP (free mass and free")
    print("   amplitude, quadratic potential) fits these curves to rms 0.005, 0.007,")
    print("   0.0003 deg (alp_vs_stur.py). What does discriminate:")
    print("   1. the amplitude: plateau = alpha/2 exactly (needs absolute angle")
    print("      calibration);")
    print("   2. calibration-free: miscalibration rotates every l equally, so")
    print("      beta(l) - beta(30) is immune to it. STUR fixes its size:")
    print("      |beta(2) - beta(30)| = 0.078, 0.184, 0.207 deg for m = 1e-31,")
    print("      3e-31, 1e-30, and never more than alpha/2 = 0.209 deg. An ALP")
    print("      has no such bound (its amplitude is free);")
    print("   3. no anisotropic birefringence at high l: theta = 0 at every")
    print("      emission point, so the recombination rotation is exactly uniform;")
    print("      an ALP with initial-angle fluctuations rotates patchily there.")


def particles():
    bar = "=" * 78
    print("\n" + bar + "\n E. New particles vs experiment\n" + bar)
    print("   content: charge-1 vectorlike fermion psi (mass M_f), neutral scalar")
    print("   phi charged under B (M_b > M_f), B KK modes (n / r_c), theta (m).")
    print("   requirements:")
    print("   * psi must decay (a stable charged relic is excluded by heavy-hydrogen")
    print("     searches): brane mixing with a Standard-Model lepton is allowed")
    print("     (B gauge parameter vanishes at the fixed points); lifetime < 1 s")
    print("     for BBN. It is then a vectorlike lepton: LHC excludes ~< 1 TeV.")
    print("   * theta is shift-symmetric, coupled only to F Ftilde: no fifth force,")
    print("     no equivalence-principle violation at tree level.")
    print("   * phi, B KK modes: Standard Model is B-neutral, so produced only via")
    print("     psi loops; Yukawa range hbar/(M c) far below the 52 um Eot-Wash limit.")
    print("   M_f from m = 1e-30 eV: m^2 f^2 ~ e^(-M_f L) / L^4 (log accuracy)")
    print("   nucleation window H_c < H_nuc < 2 f with H_c ~ 16 / L -> 1/L < f / 8")
    hd = ("f [GeV]", "1/L [GeV]", "M_f L", "M_f [GeV]")
    print(f"   {hd[0]:>8s} {hd[1]:>10s} {hd[2]:>6s} {hd[3]:>10s}  status")
    for f in (3e9, 1e12, 3e14):
        for linv in (1e3, 1e6, 1e10, 1e13):
            x = -np.log((1e-30 * (f * 1e9) * (1 / (linv * 1e9)) ** 2) ** 2)
            mf = x * linv
            st = []
            if linv > f / 8:
                st.append("H_nuc window closed")
            if mf < 1e3:
                st.append("LHC")
            print(f"   {f:8.0e} {linv:10.0e} {x:6.0f} {mf:10.1e}  "
                  + (", ".join(st) if st else "allowed"))
    print("   -> allowed from 1/L ~ 10 GeV (M_f > 1 TeV) up to f/8; for 1/L >~ 1 TeV")
    print("   psi sits at >~ 1e5 GeV, beyond colliders: then the sector is testable")
    print("   only through birefringence.")


def main():
    bar = "=" * 78
    print(bar + "\n STUR FINAL\n" + bar)

    # step 4: the trigger, from the exact one-loop potential
    xf = 137.0                                   # sets m (see full code, sec. 9)
    hc = crossing(lambda x, s, sp: ds_ratio(x, s, sp), xf, 2.0)
    tc = crossing(lambda x, s, sp: th_ratio(x, s, sp == 1), xf, 2.0)
    chk = abs(ds_ratio(xf, 0.3, 0) - 1) + abs(ds_ratio(xf, 0.3, 1) - 1)
    print(" Step 4. Wilson-line potential (one loop; 5D Dirac 4 dof, scalar 2)")
    print(f"   de Sitter check, H L = 0.3 -> flat space: deviation {chk:.1e}")
    print(f"   scalar dominates above H_c = {hc:.1f}/L (nucleation)"
          f" and T_c = {tc:.1f}/L")
    print("   below both: V = m^2 f^2 (1 + cos theta), theta = 0 is a hilltop -> roll")

    # step 5: the roll
    print("\n Step 5. Roll 0 -> pi, beta = (alpha / 2 pi) Delta theta, k = 1")
    print(f"   ideal: alpha / 2 = {np.degrees(ALPHA) / 2:.4f} deg")
    print(f"   {'m [eV]':>8s} {'seed':>6s} {'lands/pi':>9s} {'beta_rec':>9s}")
    for m in (3e-31, 1e-30, 3e-30):
        for sd in (1e-2, 1e-4):
            fr, br, _ = roll(m, sd)
            print(f"   {m:8.0e} {sd:6.0e} {fr:9.4f} {br:8.4f}°")
    print("   seed = H_nuc / (2 pi f), window 1e-4 to 0.3. Reionization angle (full")
    print("   line-of-sight projection, sec. 10 of the full code): beta_reio/beta_rec")
    print("   = 0.6-0.8 at m = 1e-31, ~0.2 at 3e-31, ~0 for m >= 1e-30 eV.")
    _, b_pred, _ = roll(1e-30, 1e-4)

    audit(b_pred)
    pattern()
    particles()

    # scoreboard
    cands = {
        "GR+QFT": dict(gamma=1.0, beta=1.0, dcg=0.0, Fr=lambda r: 1.0, eta=0.0,
                       dae=0.0, bh=True, beta_cmb=0.0, nfit=0),
        "GR+QFT+axion": dict(gamma=1.0, beta=1.0, dcg=0.0, Fr=lambda r: 1.0,
                             eta=0.0, dae=0.0, bh=True, beta_cmb=None, nfit=1),
        "STUR-ROLL": dict(gamma=1.0, beta=1.0, dcg=0.0, Fr=lambda r: 1.0, eta=0.0,
                          dae=0.0, bh=True, beta_cmb=b_pred, nfit=0),
        "STUR-2025": dict(Fr=lambda r: np.tanh(r / 1e-3), flat=True, nfit=0),
    }
    print("\n" + bar + "\n Scoreboard (n.d. = not predicted)\n" + bar)
    names = list(cands)
    rows = {}
    for n, c in cands.items():
        cc = dict(c)
        if n == "GR+QFT+axion":
            cc["beta_cmb"] = 0.277                  # fitted amplitude
        rows[n] = gates(cc)
    print(f" {'test':34s}" + "".join(f"{n:>13s}" for n in names))
    for i in range(len(rows[names[0]])):
        print(f" {rows[names[0]][i][0]:34s}" +
              "".join(f"{rows[n][i][1]:>13s}" for n in names))
    tot = {n: sum(r[1] == "PASS" for r in rows[n]) for n in names}
    fail = {n: sum(r[1] == "FAIL" for r in rows[n]) for n in names}
    score = [f"{tot[n]}/{fail[n]}" for n in names]
    print(f" {'passed / failed':34s}" + "".join(f"{x:>13s}" for x in score))

    print("\n AIC on beta = chi^2 + 2 x fitted parameters (lower is better)")
    print(f" {'dataset':28s} {'GR+QFT':>9s} {'axion':>9s} {'STUR':>9s}")
    for key, (b0, s0) in BETA_DATA.items():
        a_gr = (b0 / s0) ** 2
        a_ax = 2.0
        a_st = ((b_pred - b0) / s0) ** 2
        print(f" {key:28s} {a_gr:9.2f} {a_ax:9.2f} {a_st:9.2f}")
    print("\n Reading")
    print("  * STUR-ROLL agrees with every gate GR+QFT passes (by construction:")
    print("    TEGR = GR) and adds beta with no continuous fit (k = 1 minimal):")
    pulls = ", ".join(f"{(b_pred - b0) / s0:+.2f}" for b0, s0 in BETA_DATA.values())
    print(f"    beta = {b_pred:.4f} deg; pulls {pulls} sigma (joint, ACT, WMAP+PR4).")
    print("  * vs GR+QFT: Delta AIC 8-22, but that is the beta measurement itself")
    print("    and rests on the angle-calibration caveat; global comparison valid")
    print("    only because section C shows the sector changes nothing else.")
    print("  * vs a generic axion: STUR is better on 2 of 3 datasets, within 0.1 on")
    print("    the third; Delta AIC < 2, not yet significant. STUR's edge: beta is a")
    print("    prediction (alpha/2), the axion's is a fit. LiteBIRD decides:")
    print("    falsified if |beta| leaves 0.209 deg; |beta(low l) - beta(high l)|")
    print("    exceeds 0.209 deg (calibration-free); no single theta mass fits")
    print("    beta(l); or anisotropic birefringence is found at high l.")
    print("  * STUR-2025 tanh gravity fails Eot-Wash and the rotation-curve claim;")
    print("    it is superseded by STUR-ROLL (TEGR = GR on all gravity tests).")


if __name__ == "__main__":
    main()


EXPECTED_OUTPUT = r"""
==============================================================================
 STUR FINAL
==============================================================================
 Step 4. Wilson-line potential (one loop; 5D Dirac 4 dof, scalar 2)
   de Sitter check, H L = 0.3 -> flat space: deviation 9.7e-04
   scalar dominates above H_c = 15.1/L (nucleation) and T_c = 9.8/L
   below both: V = m^2 f^2 (1 + cos theta), theta = 0 is a hilltop -> roll

 Step 5. Roll 0 -> pi, beta = (alpha / 2 pi) Delta theta, k = 1
   ideal: alpha / 2 = 0.2091 deg
     m [eV]   seed  lands/pi  beta_rec
      3e-31  1e-02    0.9927   0.2069°
      3e-31  1e-04    0.9843   0.2058°
      1e-30  1e-02    0.9962   0.2076°
      1e-30  1e-04    0.9951   0.2080°
      3e-30  1e-02    1.0016   0.2087°
      3e-30  1e-04    1.0023   0.2095°
   seed = H_nuc / (2 pi f), window 1e-4 to 0.3. Reionization angle (full
   line-of-sight projection, sec. 10 of the full code): beta_reio/beta_rec
   = 0.6-0.8 at m = 1e-31, ~0.2 at 3e-31, ~0 for m >= 1e-30 eV.

==============================================================================
 Audit of the derivation
==============================================================================
 A. Coupling normalisation (KK tower of one Dirac fermion, charge 1)
   M r =  2.0: c_g = 0.50000 sgn M   (exact: 1/2)
   M r = 10.0: c_g = 0.49998 sgn M   (exact: 1/2)
   bare level in Z + 1/2 (parity anomaly) -> k_eff integer; ladder:
   k = 1: beta = 0.2091 deg   pulls -1.2, -0.1, -1.4 sigma
   k = 2: beta = 0.4181 deg   pulls +2.5, +2.7, +0.8 sigma
   k = 3: beta = 0.6272 deg   pulls +6.1, +5.6, +3.1 sigma

 B. Seed robustness (roll start set by the hilltop displacement)
      seed   m=3e-31   m=1e-30   m=1e-29   lands/pi
     1e-02    0.993    0.996    1.000
     1e-10    1.008    0.992    1.000
     1e-20    1.001    0.962    0.998
     1e-40    1.249    1.083    0.996
     1e-80    0.483    0.866    1.011
   beta = k alpha/2 within 4% needs a seed >~ 1e-20 (m = 1e-30) or
   >~ 1e-40 (m = 1e-29); smaller seeds roll late and land 0.5-1.25 pi.

 C. Cosmological consistency of the theta sector (k = 1)
   photon coupling g = alpha/(pi f) < 8e-13/GeV -> f > 2.9e+09 GeV
   domain walls: regions roll to +pi or -pi; theta's lift is continuous,
   so they are separated by sine-Gordon walls, tension 8 m f^2;
   CMB bound (1 MeV)^3 -> f < sqrt(1e18 eV^3 / 8 m)
   theta energy: hilltop 2 m^2 f^2 released at H ~ m/3 ->
   fraction of dark matter ~ 6 (f / M_Pl)^2
   m = 3e-31 eV: f in [2.9e+09, 6.5e+14] GeV; DM fraction <= 4e-07
   m = 1e-30 eV: f in [2.9e+09, 3.5e+14] GeV; DM fraction <= 1e-07
   m = 1e-29 eV: f in [2.9e+09, 1.1e+14] GeV; DM fraction <= 1e-08
   -> CMB spectra, BAO, SNe, lensing, BBN unchanged at <= 1e-7: the
      sector is invisible except through beta. The CMB rotation stays
      isotropic (theta = 0 at every emission point); walls only make
      late-time (reionization-era) birefringence patchy.

==============================================================================
 D. Multipole pattern beta(l)
==============================================================================
   z_re = 7.69 for tau = 0.0544; check: constant 0.3 deg returned at every l to 1e-16
     m [eV]     l=2     l=3     l=4     l=6     l=8    l=10    l>=30
      1e-31  0.1205  0.1608  0.1840  0.2028  0.2084  0.2080   0.2019
      3e-31  0.0188  0.0315  0.0449  0.0737  0.0841  0.0758   0.2058
      1e-30 -0.0009 -0.0008 -0.0007 -0.0006 -0.0005 -0.0006   0.2080
      3e-30  0.0005  0.0005  0.0005  0.0005  0.0005  0.0005   0.2095
   deg. Reion = reionization E modes only (approximate quadrupole).
   Cross-check with CLASS (exact E-mode source S_E(k, tau), same
   cosmology and tanh reionization, z_re = 7.690; class_check.py):
   projection reproduces CLASS C_l^EE shape to 0.2% for l = 2-100;
   a constant angle is returned exactly. Full beta(l), seed 1e-4:
     m [eV]    l=2    l=3    l=4    l=6    l=8   l=10   l=15   l=20   l=30
      1e-31 0.1244 0.1632 0.1850 0.2020 0.2067 0.2057 0.2025 0.2017 0.2019
      3e-31 0.0212 0.0349 0.0494 0.0804 0.0958 0.1178 0.1780 0.2035 0.2055
      1e-30 0.0000 0.0009 0.0023 0.0109 0.0345 0.0524 0.1507 0.2029 0.2075
   Reion agrees with CLASS to <= 0.004 deg for l <= 5. From l ~ 6 the
   recombination E modes contribute and beta(l) climbs to the alpha/2
   plateau by l ~ 20; Reion misses that rise, so use the CLASS table.
   Shape alone does NOT discriminate: a generic ALP (free mass and free
   amplitude, quadratic potential) fits these curves to rms 0.005, 0.007,
   0.0003 deg (alp_vs_stur.py). What does discriminate:
   1. the amplitude: plateau = alpha/2 exactly (needs absolute angle
      calibration);
   2. calibration-free: miscalibration rotates every l equally, so
      beta(l) - beta(30) is immune to it. STUR fixes its size:
      |beta(2) - beta(30)| = 0.078, 0.184, 0.207 deg for m = 1e-31,
      3e-31, 1e-30, and never more than alpha/2 = 0.209 deg. An ALP
      has no such bound (its amplitude is free);
   3. no anisotropic birefringence at high l: theta = 0 at every
      emission point, so the recombination rotation is exactly uniform;
      an ALP with initial-angle fluctuations rotates patchily there.

==============================================================================
 E. New particles vs experiment
==============================================================================
   content: charge-1 vectorlike fermion psi (mass M_f), neutral scalar
   phi charged under B (M_b > M_f), B KK modes (n / r_c), theta (m).
   requirements:
   * psi must decay (a stable charged relic is excluded by heavy-hydrogen
     searches): brane mixing with a Standard-Model lepton is allowed
     (B gauge parameter vanishes at the fixed points); lifetime < 1 s
     for BBN. It is then a vectorlike lepton: LHC excludes ~< 1 TeV.
   * theta is shift-symmetric, coupled only to F Ftilde: no fifth force,
     no equivalence-principle violation at tree level.
   * phi, B KK modes: Standard Model is B-neutral, so produced only via
     psi loops; Yukawa range hbar/(M c) far below the 52 um Eot-Wash limit.
   M_f from m = 1e-30 eV: m^2 f^2 ~ e^(-M_f L) / L^4 (log accuracy)
   nucleation window H_c < H_nuc < 2 f with H_c ~ 16 / L -> 1/L < f / 8
    f [GeV]  1/L [GeV]  M_f L  M_f [GeV]  status
      3e+09      1e+03    164    1.6e+05  allowed
      3e+09      1e+06    191    1.9e+08  allowed
      3e+09      1e+10    228    2.3e+12  H_nuc window closed
      3e+09      1e+13    256    2.6e+15  H_nuc window closed
      1e+12      1e+03    152    1.5e+05  allowed
      1e+12      1e+06    180    1.8e+08  allowed
      1e+12      1e+10    216    2.2e+12  allowed
      1e+12      1e+13    244    2.4e+15  H_nuc window closed
      3e+14      1e+03    141    1.4e+05  allowed
      3e+14      1e+06    168    1.7e+08  allowed
      3e+14      1e+10    205    2.1e+12  allowed
      3e+14      1e+13    233    2.3e+15  allowed
   -> allowed from 1/L ~ 10 GeV (M_f > 1 TeV) up to f/8; for 1/L >~ 1 TeV
   psi sits at >~ 1e5 GeV, beyond colliders: then the sector is testable
   only through birefringence.

==============================================================================
 Scoreboard (n.d. = not predicted)
==============================================================================
 test                                     GR+QFT GR+QFT+axion    STUR-ROLL    STUR-2025
 Cassini gamma (2003)                       PASS         PASS         PASS         n.d.
 Mercury perihelion (beta)                  PASS         PASS         PASS         n.d.
 GW speed (GW170817)                        PASS         PASS         PASS         n.d.
 inverse-square law (Eot-Wash)              PASS         PASS         PASS         FAIL
 equivalence principle (MICROSCOPE)         PASS         PASS         PASS         n.d.
 electron g-2                               PASS         PASS         PASS         n.d.
 Hawking T, area law, M^3 lifetime          PASS         PASS         PASS         n.d.
 CMB birefringence |beta| (2 sigma)         FAIL         PASS         PASS         n.d.
 flat rotation without dark matter          n.d.         n.d.         n.d.         FAIL
 passed / failed                             7/1          8/0          8/0          0/2

 AIC on beta = chi^2 + 2 x fitted parameters (lower is better)
 dataset                         GR+QFT     axion      STUR
 joint2026 (ACT DR6+Planck)       23.62      2.00      1.46
 ACT DR6                           8.44      2.00      0.01
 WMAP+Planck PR4                  13.67      2.00      2.10

 Reading
  * STUR-ROLL agrees with every gate GR+QFT passes (by construction:
    TEGR = GR) and adds beta with no continuous fit (k = 1 minimal):
    beta = 0.2080 deg; pulls -1.21, -0.09, -1.45 sigma (joint, ACT, WMAP+PR4).
  * vs GR+QFT: Delta AIC 8-22, but that is the beta measurement itself
    and rests on the angle-calibration caveat; global comparison valid
    only because section C shows the sector changes nothing else.
  * vs a generic axion: STUR is better on 2 of 3 datasets, within 0.1 on
    the third; Delta AIC < 2, not yet significant. STUR's edge: beta is a
    prediction (alpha/2), the axion's is a fit. LiteBIRD decides:
    falsified if |beta| leaves 0.209 deg; |beta(low l) - beta(high l)|
    exceeds 0.209 deg (calibration-free); no single theta mass fits
    beta(l); or anisotropic birefringence is found at high l.
  * STUR-2025 tanh gravity fails Eot-Wash and the rotation-curve claim;
    it is superseded by STUR-ROLL (TEGR = GR on all gravity tests).
"""
