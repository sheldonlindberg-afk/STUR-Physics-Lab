"""Measured inputs: the ONLY place a build may get a number with more than three significant digits.

A build imports this module (``from rebuild import inputs`` or ``import inputs``) and reads
named constants. It never types a measured value itself; the harness lint enforces that.
Each value names its source. They are the same values src/ladder_standalone.py uses, so a
correct build reproduces its results.

Layer: MEASURED INPUT (see rebuild/SPEC.md section 0). Nothing here is derived.
"""

# --- electroweak (PDG 2024) ---------------------------------------------------------------
G_F = 1.1663788e-5            # GeV^-2, Fermi constant
MZ_MEAS = 91.1880             # GeV
ALPHA_MZ_INV = 127.930        # 1/alpha_em(M_Z), MS-bar
S2_MZ = 0.23129               # sin^2 theta_W(M_Z), MS-bar
ALPHA_0 = 1 / 137.035999084   # alpha at q^2 = 0 (CODATA 2018)
MU_331 = 4.0e3                # GeV, the 3-3-1 breaking scale M_V of the reference spectrum (a choice, not a measurement)

# --- the charged pion's weak decay (PDG 2024) ------------------------------------------------
GAMMA_PI_MUNU = 3.8408e7      # s^-1, Gamma(pi+ -> mu+ nu), radiation inclusive (PDG 2024 leptonic-decays review)
DELTA_PI = 0.0176             # the radiative correction: Gamma = Gamma_tree (1 + DELTA_PI) (PDG 2024, eq. 72.4)
V_UD = 0.97367                # |V_ud| (PDG 2024 CKM review, eq. 12.7)
M_MU = 0.1056583755           # GeV, muon mass

# --- strong sector (PDG 2024, FLAG) -------------------------------------------------------
MU_PLUS_MD = 2.16e-3 + 4.70e-3        # GeV, m_u + m_d, MS-bar 2 GeV
MU_PLUS_MD_ERR = (0.07e-3**2 + 0.07e-3**2) ** 0.5
F_PI = 0.1302 / 2 ** 0.5              # GeV, f_pi = 92.07 MeV (the lattice value; the ladder derives its own, stage weak)
COND_13 = 0.272                       # GeV, |<qbar q>|^(1/3), FLAG 19 (N_f = 2+1)
COND_13_ERR = 0.005
M_PI0, M_PIC = 0.1349768, 0.13957039  # GeV
M_UD_FLAG, M_UD_FLAG_ERR = 3.364e-3, 0.041e-3   # GeV, (m_u + m_d)/2, FLAG 2024
FPI_OVER_F, FPI_OVER_F_ERR = 1.062, 0.007       # FLAG 19/21
LBAR3, LBAR3_ERR = 3.07, 0.64                   # FLAG 19/21
G_A, M_N = 1.2754, 0.9389187                    # nucleon axial coupling; nucleon mass (GeV)
G_PINN_EMP, G_PINN_ERR = 13.1, 0.1              # Baru et al. 2011
HBARC_GEV_FM = 0.1973269804
GAMMA_PI0, GAMMA_PI0_ERR = 7.802, (0.052**2 + 0.105**2) ** 0.5   # eV, PrimEx-I+II

# --- SI constants (CODATA 2018) -----------------------------------------------------------
G_NEWTON = 6.67430e-11        # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34        # J s
C_LIGHT = 2.99792458e8        # m/s
K_B = 1.380649e-23            # J/K
E_CH = 1.602176634e-19        # C
K_COUL = 8.9875517923e9       # 1/(4 pi eps0)
U_AMU = 1.66053906660e-27     # kg
L_PLANCK = 1.616255e-35       # m

# --- materials ------------------------------------------------------------------------------
EPS_DIAMOND = 5.7             # static permittivity of diamond
RHO_DIAMOND = 3510.0          # kg/m^3

# --- cosmology (Planck 2018 + BAO) ----------------------------------------------------------
LAMBDA_SI = 1.1056e-52        # m^-2

# --- the diamond experiment: design parameters (an engineering choice, not physics) ---------
# Design A is the output of the repository's design scan (src/stur_gravity_entanglement.py).
# They are inputs to the entangling phase, not something a build derives.
DESIGN_A_MASS = 1.4677992676220692e-14     # kg
DESIGN_A_DX = 7.208434242404264e-4         # m, full branch separation
DESIGN_A_HOLD = 0.08237744862210328        # s
DESIGN_A_RAMP = 1.5811388300841898         # s, each of two ramps
# The Casimir-safe criterion's baseline (stage casimir): mass, separation, time, fraction.
GAP_BASELINE_MASS, GAP_BASELINE_DX, GAP_BASELINE_TAU, GAP_FRACTION = 1e-14, 250e-6, 2.5, 0.1

# --- astrophysics ---------------------------------------------------------------------------
GM_SUN = 1.3271244e20         # m^3 s^-2 (IAU 2015)
PARSEC = 3.0856775814913673e16
M87_STARS = (6.6e9, 0.4e9, 17.9e6)            # M_sun, error, assumed distance (pc)
THETA_G_M87 = (3.8, 0.4, 0.4)                 # uas (value, lower error, upper error), EHT 2019
SGRA_VLTI, SGRA_KECK = (4.297e6, 8277.0), (3.975e6, 7959.0)   # (M_sun, pc)
THETA_G_SGRA = (4.8, 0.7, 1.4)                # uas, EHT 2022
GW_M1, GW_M2 = (33.6, 0.8, 1.2), (32.2, 1.3, 0.8)   # GW250114 component masses (M_sun, -, +)
GW_MF, GW_CHIF, GW_Z = 62.7, 0.68, (0.09, 0.01)
F220, G220 = (247.0, 6.0, 6.0), (221.0, 32.0, 39.0)   # ringdown-only 220 fit (Hz)
BCW_220 = (1.5251, -1.1568, 0.1292, 0.7000, 1.4187, -0.4990)   # Berti-Cardoso-Will 2006 fit

# --- the Standard Model's other parameters (the chain's step 9; PDG 2024) ---------------------
M_T = 172.57                  # GeV, top pole mass
M_T_ERR_MEV = 290             # MeV, its error (in MeV: 0.29 would collide with an ordinary number in a build)
M_H = 125.20                  # GeV, Higgs mass (+- 0.11)
M_W = 80.3692                 # GeV
ALPHA_S_MZ = 0.1180           # strong coupling at M_Z
M_E, M_TAU, M_TAU_ERR = 0.51099895e-3, 1.77693, 0.00009   # GeV, charged-lepton pole masses
M_D_2GEV, M_S_2GEV = (4.70e-3, 0.04e-3), (93.5e-3, 0.5e-3)   # GeV, MS-bar at 2 GeV (value, error)
S12_CKM = (0.22501, 0.00068)  # sin(theta_12), PDG 2024 CKM review, eq. (12.28)
# MS-bar quark Yukawa couplings at M_Z from the PDG 2024 inputs: Antusch, Hinze, Saad, arXiv:2510.01312, eq. (2.4)
YUKAWA_MZ = {"u": 7.04e-6, "c": 3.56e-3, "t": 0.967, "d": 1.54e-5, "s": 3.06e-4, "b": 1.630e-2}
RHO_0 = (1.00039, 0.00019)    # the global fit's rho parameter beyond the Standard Model, Erler, arXiv:1908.07346

# --- quoted formulas for step 9 (layer: QUOTED) -----------------------------------------------
# Lower-case names: these are coefficients of published formulas, not measured values. The build
# lint (rebuild/harness.py) guards the upper-case measured inputs against being typed into a build;
# small formula coefficients such as 1.5 would collide with ordinary numbers there.
# Buttazzo et al., JHEP 12 (2013) 089, arXiv:1307.3536. Reference point: M_t, M_h, alpha_s and its
# unit, M_W and its unit.
b13_ref = (173.34, 125.15, 0.1184, 0.0007, 80.384, 0.014)
# eqs. (55)-(60): MS-bar couplings at mu = M_t. lambda: (value, per GeV of M_h, per GeV of M_t);
# y_t and g_3: (value, per GeV of M_t or per unit of alpha_s as marked); g_2, g_Y: (value, per GeV of M_t, per unit of M_W).
b13_at_mt = {"lam": (0.12604, 0.00206, -0.00004), "yt": (0.93690, 0.00556, -0.00042),
             "g3": (1.1666, 0.00314, -0.00046), "g2": (0.64779, 0.00004, 0.00011), "gY": (0.35830, 0.00011, -0.00020)}
# eq. (61): couplings at M_Pl. g1 (GUT-normalised): (value, per GeV of M_t, per unit of M_W); g3: (value, per unit of
# alpha_s); yt: (value, per GeV of M_t, per unit of alpha_s); lam: (value, per GeV of M_t, per unit of alpha_s, per GeV of M_h).
b13_at_mpl = {"g1": (0.6154, 0.0003, -0.0006), "g2": 0.5055, "g3": (0.4873, 0.0002),
              "yt": (0.3825, 0.0051, -0.0021), "lam": (-0.0143, -0.0066, 0.0018, 0.0029)}
b13_stability = (129.6, 2.0, 0.5)     # eq. (64): M_h > 129.6 + 2.0 (M_t - 173.34) - 0.5 (alpha_s - 0.1184)/0.0007 GeV
b13_mt_max = (171.53, 0.42)           # eq. (66): M_t < 171.53 +- 0.42 GeV
# Shaposhnikov and Wetterich, Phys. Lett. B 683, 196 (2010), arXiv:0912.0208, eq. (12):
# m_min = 126.3 + (m_t - 171.2)/2.1 * 4.1 - (alpha_s - 0.1176)/0.002 * 1.5 GeV, theory error 2.2 GeV
sw10_mmin = (126.3, 171.2, 2.1, 4.1, 0.1176, 0.002, 1.5, 2.2)
eh17_mt = 171.0               # GeV, top pole mass from asymptotic safety, Eichhorn and Held, arXiv:1707.01107 (abstract)

# --- link bounds ----------------------------------------------------------------------------
EPS_PE_BOUND = 1e-21          # |q_p + q_e|/e, Bressi et al. 2011

# --- quoted results from heavier repository code (layer: QUOTED) -----------------------------
# 3-3-1 Landau poles in GeV (N_c = 3, N_c = 5) at the reference spectrum, three loops,
# from src/m331_three_loop.py. A build may use them only as quoted inputs. The ladder derives
# its own at one loop (stage running); these stay as the precise values for g_window.
POLES_331 = {"+1/sqrt3": (3.49103e19, 5.15600e11), "-1/sqrt3": (2.28969e29, 1.12580e15)}
