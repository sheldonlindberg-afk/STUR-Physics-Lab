"""The build contract: the single source of truth for what an AI build must export.

A build is a directory rebuild/builds/<build_id>/ with one Python module per stage. Each
module must:
  * define every export listed for its stage, with the stated signature and meaning;
  * define PROVENANCE = {export_name: (kind, note)} for every export, where kind is
    "derived" (computed from postulates in this build), "input" (read from rebuild/inputs.py
    without further computation) or "quoted" (a published result used without derivation;
    allowed only for the exports listed in the stage's "quoted_allowed");
  * import only the Python standard library, rebuild/inputs.py, and the modules of EARLIER
    stages of the same build.

Conventions (units, bases, normalizations) are fixed here so that independent builds can be
compared number by number. The physics postulates are in rebuild/SPEC.md. Neither file
contains the answers: those live only in the oracle, which a builder must not read.
"""

VARIANTS = ("-1/sqrt3", "+1/sqrt3")

STAGES = [
    {
        "name": "toolkit",
        "module": "toolkit",
        "depends": [],
        "quoted_allowed": [],
        "exports": {
            "eigvalsh": "eigvalsh(A) -> list[float]: eigenvalues of a real symmetric matrix (list of lists), ascending.",
            "hessian": "hessian(f, x, h=1e-4) -> list[list[float]]: central-difference Hessian of f: R^n -> R at x.",
            "exact_derivative": "exact_derivative(f, x) -> Fraction: f'(x) EXACTLY, for f built from + - * / and"
                                " rational constants, x a Fraction (forward-mode dual numbers).",
            "bisect": "bisect(f, a, b, iters=200) -> float: a root of f in [a, b], f(a) f(b) < 0.",
            "golden_max": "golden_max(f, a, b, iters=200) -> float: the maximizer of a unimodal f on [a, b].",
            "trapezoid": "trapezoid(ys, dx) -> float: trapezoid rule over equally spaced samples.",
            "levi_civita": "levi_civita(p) -> int: sign of the permutation p of 0..n-1 (0 if repeated index).",
        },
    },
    {
        "name": "gauge331",
        "module": "gauge331",
        "depends": ["toolkit"],
        "quoted_allowed": [],
        "exports": {
            "triplet_charges": "triplet_charges(X, variant, anti=False) -> list[Fraction]: electric charge Q ="
                               " T3 + beta T8 + X of the 3 components of an SU(3)_L triplet (anti: antitriplet, -T*).",
            "quark_charges": "quark_charges(Nc) -> (Q_u, Q_d) Fractions, DERIVED from anomaly cancellation for N_c colours.",
            "doublet_charge_pairs": "doublet_charge_pairs(Nc, variant) -> set of frozenset: the charges of the first two"
                                    " components of every fermion triplet/antitriplet of SPEC.md's content.",
            "mass_matrix": "mass_matrix(variant, g, gX, w, v1, v2) -> 9x9 list: gauge-boson mass^2 matrix in the basis"
                           " (W^1..W^8, B_X), M2_AB = g_A g_B sum_phi <phi>^dag {t_A, t_B} <phi>, vevs <phi>_k = v/sqrt2.",
            "photon_direction": "photon_direction(variant, g, gX) -> list of 9 floats: the (unnormalized) massless direction n.",
            "inv_e2": "inv_e2(variant, g, gX) -> float: 1/e^2 of the unbroken U(1)_em.",
            "neutral_masses": "neutral_masses(variant, g, gX, w, v1, v2) -> (MZ2, MZp2): the two nonzero eigenvalues of the"
                              " neutral (W^3, W^8, B_X) block, ascending.",
            "vev_from_GF": "vev_from_GF(G_F) -> float GeV: v = (sqrt2 G_F)^(-1/2).",
            "mz_tree": "mz_tree(G_F, alpha_inv, s2) -> float GeV: tree-level M_Z from G_F, alpha, sin^2 theta_W.",
        },
    },
    {
        "name": "chiral",
        "module": "chiral",
        "depends": ["toolkit"],
        "quoted_allowed": ["chpt_mpi"],
        "exports": {
            "goldstone_count": "goldstone_count(lam, v) -> int: zero modes of the O(4) sigma model at its vacuum, H = 0.",
            "sigma_model_vacuum": "sigma_model_vacuum(lam, v, H) -> (sigma0, mpi2): vacuum and pion mass^2 with explicit breaking H.",
            "gmor_mpi": "gmor_mpi(mq_sum, cond13, fpi) -> GeV: leading-order pion mass from GMOR.",
            "chpt_mpi": "chpt_mpi(m_ud, cond13, fpi_over_F, lbar3, fpi) -> GeV: O(p^4) ChPT pion mass (FLAG conventions).",
            "yukawa": "yukawa(r, m) -> float: the potential whose Fourier transform is 1/(q^2 + m^2), unit normalized.",
            "tensor_identity_residual": "tensor_identity_residual(q) -> float: max |(s1.q)(s2.q) - (q^2/3)(s1.s2 + S12)| over"
                                        " the 4x4 spin matrix, q a 3-vector.",
            "goldberger_treiman": "goldberger_treiman(gA, MN, fpi) -> float: g_piNN.",
        },
    },
    {
        "name": "casimir",
        "module": "casimir",
        "depends": ["toolkit"],
        "quoted_allowed": ["cp_energy"],
        "exports": {
            "sphere_K": "sphere_K(eps) -> Fraction (or float for float eps): alpha/(4 pi eps0 R^3) of a dielectric sphere,"
                        " solved from Laplace's equation.",
            "green_tensor": "green_tensor(x, y, z, k) -> 3x3: dipole Green tensor at imaginary frequency, k = xi/c (SPEC.md).",
            "cp_integral": "cp_integral() -> Fraction: int_0^oo of Tr G.G r^6 / 2 du, exactly.",
            "cp_energy": "cp_energy(R1, R2, K1, K2, r) -> J: retarded Casimir-Polder energy of two spheres, constant alpha.",
            "diamond_radius": "diamond_radius(m) -> m: radius of a diamond sphere of mass m (inputs.RHO_DIAMOND).",
            "casimir_safe_gap": "casimir_safe_gap(m, dx, tau, fraction) -> m: smallest gap at which the Casimir entangling"
                                " phase is <= fraction x gravity's, parallel geometry (SPEC.md).",
        },
    },
    {
        "name": "graviton",
        "module": "graviton",
        "depends": ["toolkit", "chiral", "casimir"],
        "quoted_allowed": [],
        "exports": {
            "point_mass_metric": "point_mass_metric() -> (h00, hii) Fractions in units of GM/(c^2 r).",
            "tpt": "tpt(T1, T2) -> Fraction: T2.P.T1 for diagonal stress tensors given as 4-tuples (T^00, T^11, T^22, T^33).",
            "ramp_profile": "ramp_profile(t, hold, ramp) -> float in [0, 1]: the branch-opening profile of SPEC.md.",
            "entangling_phase": "entangling_phase(m, dx, hold, ramp, gap, n=4001) -> rad: Delta phi = phi_LL + phi_RR -"
                                " phi_LR - phi_RL, parallel geometry, trapezoid rule on n samples.",
            "design_phase": "design_phase() -> rad: design A's phase (inputs.DESIGN_A_*) at the Casimir-safe gap that"
                            " casimir.casimir_safe_gap gives for the baseline (inputs.GAP_BASELINE_*, GAP_FRACTION).",
        },
    },
    {
        "name": "desitter",
        "module": "desitter",
        "depends": ["toolkit"],
        "quoted_allowed": [],
        "exports": {
            "so41_generator": "so41_generator(A, B) -> 5x5: (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD, eta = diag(-1,1,1,1,1).",
            "spin_connection": "spin_connection(x, f, fp) -> (E, w): for -f dt^2 + dr^2/f + r^2 dOmega^2 at x = (t, r, th, ph),"
                               " the diagonal tetrad E[a][mu] and the Levi-Civita spin connection w[a][b][mu] ="
                               " omega^a_{b mu} (a up, b down), so that de^a + omega^a_b ^ e^b = 0.",
            "unbroken_generators": "unbroken_generators(V) -> list of (A, B), A < B: generators J_AB with J_AB V = 0.",
            "curvature_split_residual": "curvature_split_residual(M, l, x) -> float: on Schwarzschild-de Sitter at the point"
                                        " x = (t, r, theta, phi), max of |F^ab - R^ab + e^a^e^b/l^2| and |F^a4|.",
            "ds_curvature_max": "ds_curvature_max(l, x) -> float: max |F| for de Sitter space of radius l at x.",
            "action_coefficients": "action_coefficients(M, l, x) -> (cR, cV): eps R^e^e = cR e R and eps e^e^e^e = cV e.",
            "ell_from_lambda": "ell_from_lambda(Lam) -> m: de Sitter radius for cosmological constant Lam (m^-2).",
            "mm_coupling": "mm_coupling(Lam, lP) -> float: the dimensionless MacDowell-Mansouri coupling 3/(lP^2 Lam).",
        },
    },
    {
        "name": "blackholes",
        "module": "blackholes",
        "depends": ["toolkit", "desitter"],
        "quoted_allowed": ["qnm_220", "invert_220", "hawking_K"],
        "exports": {
            "sds_horizons": "sds_horizons(M, l) -> (r_b, r_c) or None: horizons of f = 1 - 2M/r - r^2/l^2 (G = c = 1).",
            "killing_kappa": "killing_kappa(f, r0, h) -> float: surface gravity from kappa^2 = -(nabla xi)^2/2, metric from f only.",
            "kappa_from_spin_connection": "kappa_from_spin_connection(M, l) -> (kappa_b, kappa_c): surface gravity on both"
                                          " SdS horizons as |omega^0_{1 t}| from desitter.spin_connection (rung 5).",
            "euclidean_cone_ratio": "euclidean_cone_ratio(f, rh, beta, eps) -> float: circumference/(2 pi proper radius)"
                                    " of the Euclidean (tau, r) circle at r_h + eps, tau-period beta.",
            "kerr_first_law": "kerr_first_law(p, q, dp, dq) -> (first, smarr) Fractions: dM - T dS - Omega dJ along"
                              " (dp, dq), and M - 2TS - 2 Omega J, for Kerr with horizons r+ = p, r- = q.",
            "nariai_mass_kg": "nariai_mass_kg(Lam) -> kg: the largest Schwarzschild-de Sitter black-hole mass.",
            "photon_sphere": "photon_sphere() -> (r, b): photon-sphere radius and critical impact parameter, M = 1, numerically.",
            "isco": "isco() -> (r, L2, E2): innermost stable circular orbit, M = 1, numerically.",
            "shadow_uas": "shadow_uas(m_sun, d_pc) -> uas: Schwarzschild shadow diameter.",
            "kerr_area_km2": "kerr_area_km2(m_sun, chi) -> km^2: horizon area.",
            "qnm_220": "qnm_220(m_det_sun, chi) -> (f Hz, damping rate Hz) from inputs.BCW_220.",
            "invert_220": "invert_220(f, damp, z) -> (source-frame M_sun, chi) from the 220 mode.",
            "hawking_K": "hawking_K(m_kg) -> K: Hawking temperature.",
        },
    },
    {
        "name": "links",
        "module": "links",
        "depends": ["toolkit", "gauge331", "chiral", "casimir", "graviton", "desitter", "blackholes"],
        "quoted_allowed": ["pi0_width_eV", "pi0_width_from_rungs"],
        "exports": {
            "qp_qe_minus_anomaly": "qp_qe_minus_anomaly(Nc, b, XL, Xt) -> Fraction: (q_p + q_e) - [SU(3)_L]^2 U(1)_X / N_g"
                                   " for b = beta/(2 sqrt3), lepton-triplet X = XL, quark-triplet X = Xt (SPEC.md).",
            "neutrality_per_nucleon": "neutrality_per_nucleon(m) -> e: the largest net charge per nucleon keeping Coulomb"
                                      " below inputs.GAP_FRACTION x gravity for two diamonds of mass m.",
            "pi0_width_eV": "pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd) -> eV: pi0 -> gamma gamma width.",
            "planck_mass_GeV": "planck_mass_GeV(G, hbar, c) -> GeV: sqrt(hbar c / G) c^2.",
            "g_window": "g_window(p3, p5, mpl) -> (lo, hi): range of G/G_meas for which pole_5 < M_Pl(G) < pole_3.",
            "schwarzschild_radius": "schwarzschild_radius(m) -> m.",
            "matter_charges": "matter_charges(Nc, variant) -> (q_p, q_n, q_e, Q_nu) Fractions, from rung 1's"
                              " gauge331.quark_charges and the lepton triplet's gauge331.triplet_charges.",
            "pi0_width_from_rungs": "pi0_width_from_rungs() -> eV: pi0 -> gamma gamma with rung 1's charges at N_c = 3"
                                    " and inputs.ALPHA_0, F_PI, M_PI0.",
            "planck_bh_kT_GeV": "planck_bh_kT_GeV() -> GeV: k_B T_H of a black hole of one Planck mass, from"
                                " blackholes.hawking_K and planck_mass_GeV.",
        },
    },
]

STAGE_NAMES = [s["name"] for s in STAGES]

# Connections: where one rung's output must actually be USED by another, not recomputed.
# The harness wraps each upstream function in a spy, calls the downstream one, and fails
# if the upstream was never called. So a stage must reach upstream code as
# `import <stage>` and `<stage>.<function>(...)` at call time (never `from <stage> import`).
# Arguments are fixed probes; the check is about the call, not the value.
CONNECTIONS = [
    {"id": "T-gauge", "down": ("gauge331", "neutral_masses", ("-1/sqrt3", 0.652, 0.79, 4000.0, 150.0, 190.0)),
     "up": [("toolkit", "eigvalsh")], "why": "masses are eigenvalues: use the shared, validated solver"},
    {"id": "T-chiral", "down": ("chiral", "goldstone_count", (2.0, 1.0)),
     "up": [("toolkit", "hessian"), ("toolkit", "eigvalsh")], "why": "Goldstones are the Hessian's zero modes"},
    {"id": "T-casimir", "down": ("casimir", "casimir_safe_gap", (1e-14, 250e-6, 2.5, 0.1)),
     "up": [("toolkit", "bisect")], "why": "the safe gap is a root"},
    {"id": "L-2to4", "down": ("graviton", "entangling_phase", (1e-14, 5e-4, 0.1, 1.0, 2e-4)),
     "up": [("chiral", "yukawa"), ("toolkit", "trapezoid")],
     "why": "rung 2 -> 4: Newton's 1/r is rung 2's exchange transform at m = 0"},
    {"id": "L-3to4", "down": ("graviton", "design_phase", ()),
     "up": [("casimir", "casimir_safe_gap"), ("graviton", "entangling_phase")],
     "why": "rung 3 -> 4: electromagnetism's background sets the gap gravity's phase is computed at"},
    {"id": "L-5to6a", "down": ("blackholes", "nariai_mass_kg", (1e-52,)),
     "up": [("desitter", "ell_from_lambda")], "why": "rung 5 -> 6: the de Sitter radius caps black-hole size"},
    {"id": "L-5to6b", "down": ("blackholes", "kappa_from_spin_connection", (1.0, 9.0)),
     "up": [("desitter", "spin_connection"), ("blackholes", "sds_horizons")],
     "why": "rung 5 -> 6: the temperature is read off rung 5's spin connection"},
    {"id": "T-bh", "down": ("blackholes", "photon_sphere", ()),
     "up": [("toolkit", "golden_max")], "why": "the photon sphere is the potential's maximum"},
    {"id": "L1", "down": ("links", "matter_charges", (3, "-1/sqrt3")),
     "up": [("gauge331", "quark_charges"), ("gauge331", "triplet_charges")],
     "why": "link 1: neutral matter uses rung 1's charges"},
    {"id": "L2", "down": ("links", "pi0_width_from_rungs", ()),
     "up": [("gauge331", "quark_charges"), ("links", "pi0_width_eV")],
     "why": "link 2: pi0 -> gamma gamma uses rung 1's charges"},
    {"id": "L5", "down": ("links", "planck_bh_kT_GeV", ()),
     "up": [("blackholes", "hawking_K"), ("links", "planck_mass_GeV")],
     "why": "link 5: rung 6's temperature at link 3's cutoff"},
]


def stage(name):
    for s in STAGES:
        if s["name"] == name:
            return s
    raise KeyError(name)


def upto(name):
    """Stages in build order up to and including name."""
    return STAGES[: STAGE_NAMES.index(name) + 1]
