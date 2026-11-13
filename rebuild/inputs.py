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

# --- link bounds ----------------------------------------------------------------------------
EPS_PE_BOUND = 1e-21          # |q_p + q_e|/e, Bressi et al. 2011

# --- quoted results from heavier repository code (layer: QUOTED) -----------------------------
# 3-3-1 Landau poles in GeV (N_c = 3, N_c = 5) at the reference spectrum, three loops,
# from src/m331_three_loop.py. A build may use them only as quoted inputs. The ladder derives
# its own at one loop (stage running); these stay as the precise values for g_window.
POLES_331 = {"+1/sqrt3": (3.49103e19, 5.15600e11), "-1/sqrt3": (2.28969e29, 1.12580e15)}
