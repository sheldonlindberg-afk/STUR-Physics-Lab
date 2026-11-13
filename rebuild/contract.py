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
        },
    },
    {
        "name": "desitter",
        "module": "desitter",
        "depends": ["toolkit"],
        "quoted_allowed": [],
        "exports": {
            "so41_generator": "so41_generator(A, B) -> 5x5: (J_AB)^C_D = delta^C_A eta_BD - delta^C_B eta_AD, eta = diag(-1,1,1,1,1).",
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
        "depends": ["toolkit", "gauge331", "chiral", "graviton", "blackholes"],
        "quoted_allowed": ["pi0_width_eV"],
        "exports": {
            "qp_qe_minus_anomaly": "qp_qe_minus_anomaly(Nc, b, XL, Xt) -> Fraction: (q_p + q_e) - [SU(3)_L]^2 U(1)_X / N_g"
                                   " for b = beta/(2 sqrt3), lepton-triplet X = XL, quark-triplet X = Xt (SPEC.md).",
            "neutrality_per_nucleon": "neutrality_per_nucleon(m) -> e: the largest net charge per nucleon keeping Coulomb"
                                      " below inputs.GAP_FRACTION x gravity for two diamonds of mass m.",
            "pi0_width_eV": "pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd) -> eV: pi0 -> gamma gamma width.",
            "planck_mass_GeV": "planck_mass_GeV(G, hbar, c) -> GeV: sqrt(hbar c / G) c^2.",
            "g_window": "g_window(p3, p5, mpl) -> (lo, hi): range of G/G_meas for which pole_5 < M_Pl(G) < pole_3.",
            "schwarzschild_radius": "schwarzschild_radius(m) -> m.",
        },
    },
]

STAGE_NAMES = [s["name"] for s in STAGES]


def stage(name):
    for s in STAGES:
        if s["name"] == name:
            return s
    raise KeyError(name)


def upto(name):
    """Stages in build order up to and including name."""
    return STAGES[: STAGE_NAMES.index(name) + 1]
