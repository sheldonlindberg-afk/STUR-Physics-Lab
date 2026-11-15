#!/usr/bin/env python3
"""
The forces in one chain: from the 3-3-1 gauge theory down through the electroweak, strong and
electromagnetic forces to the diamond experiment's gravity, gravity written as a broken gauge
theory, and black holes, which evaporate back up through every force.

Each stage is a function. It takes, as arguments, values that earlier stages returned, and
returns new ones. A ledger records every hand-off: which stage produced a value and which
stages used it. Measured inputs are named where they enter, at the stage that needs them.
Nothing is retyped between stages; tests/test_force_chain.py checks that every stage after
the first uses earlier stages' outputs and that the ledger is complete.

The derivations themselves live in the modules this file calls (src/m331_*.py,
src/chiral_breaking.py, src/casimir_diamonds.py, src/graviton_exchange.py,
src/macdowell_mansouri.py, src/black_holes.py, src/ladder_links.py); this file is the order
in which they hand results to each other.

  1  Unification. SU(3)_C x SU(3)_L x U(1)_X breaks to the Standard Model and then to
     electromagnetism. Out: the quark charges for N_c = 3 (anomaly-fixed), q_p + q_e = 0
     exactly, the Planck mass from the measured G, and the 3-3-1 Landau poles that select
     N_c = 3 against it. In: G (CODATA 2018), 1/alpha-hat(M_Z), G_F, M_Z (PDG 2024).
  2  Electroweak to the photon. The same coupling run from M_Z to zero momentum: alpha(0).
     In: the hadronic vacuum polarization (PDG 2024), the scheme conversion.
  3  Weak to strong. G_F and the measured pi -> mu nu rate give f_pi. In: the rate, delta_pi,
     |V_ud| (PDG 2024).
  4  The strong force. With stage 3's f_pi, stage 2's alpha and stage 1's charges: the pi0
     width, the O(p^4) pion mass, the electromagnetic pion splitting, the nuclear force's
     range; and where the nucleon's mass comes from. In: FLAG lattice constants and sigma
     terms; m_rho, m_a1.
  5  Electromagnetism in the lab. With stage 1's exact neutrality and stage 2's alpha: the
     charge neutrality the experiment needs; the Casimir-Polder gap. In: diamond's
     permittivity.
  6  Gravity in the lab. With stage 1's G: design A's 2.19 rad entangling phase; with
     stage 4's mass budget, what it would be without the light quarks' masses.
  7  Gravity as a broken de Sitter gauge theory. With stage 1's G and the measured Lambda:
     the gauge theory's length l, its coupling, and why Lambda can't change stage 6's phase.
     In: Lambda (Planck 2018).
  8  Black holes. Stage 7's spin connection gives the surface gravity; the EHT and GW250114
     test the strong field; an evaporating hole's temperature then passes back through every
     scale above, from stage 6's cryostat to stage 1's Planck mass, and its emission counts
     stage 1's particles.

Seven branches leave the chain where its values meet a measurement it did not use
(src/chain_branches.py). They are numbered by the stage they follow:
  2a The W mass, from stage 1's G_F and stage 2's alpha: the running of alpha and the top
     quark's loop bring the tree-level value to 0.13% of the measurement. In: M_Z, m_t, M_W.
  2b The electron's magnetic moment: the measurement stage 2's alpha ultimately rests on,
     inverted through the QED series.
  2c The weak mixing angle at zero momentum, from the same loops that run alpha in stage 2.
  3a The neutron lifetime, from stage 1's G_F and stage 3's |V_ud|. In: g_A, the neutron-proton
     mass difference, the quoted radiative corrections.
  4a Primordial helium, from stage 1's G (through M_Pl), stage 2's alpha and 3a's lifetime:
     all four forces in one number. In: the baryon density, the deuteron's binding energy,
     two nuclear cross sections.
  4b The neutron-proton mass difference: quoted from lattice QCD + QED, and what it controls
     in 3a and 4a.
  7a The masses at which cold matter collapses, from stage 1's Planck mass and the nucleon
     mass: two pure numbers times M_Pl^3/m_N^2. Stage 8's black holes lie above them.

Labels as in the modules called. Independent work, not peer reviewed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LEDGER = []          # (name, value, produced_in, [used_in, ...])
INPUTS = []          # (stage, name, value, source)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def produce(stage, name, value):
    LEDGER.append([name, value, stage, []])
    return value


def use(stage, name):
    for row in LEDGER:
        if row[0] == name:
            if stage not in row[3]:
                row[3].append(stage)
            return row[1]
    raise KeyError(name)


def order(stage):
    """Position in the chain: stages are 1..8, branches '2a', '3a', ... follow their stage."""
    return (stage, "") if isinstance(stage, int) else (int(stage[:-1]), stage[-1])


def measured(stage, name, value, source):
    INPUTS.append((stage, name, value, source))
    return value


# ------------------------------------------------------------------------------- stage 1
def unification():
    st = 1
    import m331_breaking as B
    import m331_three_loop as T3
    import m331_margin as M
    import ladder_links as LL
    G = measured(st, "G", 6.67430e-11, "CODATA 2018")
    ainv = measured(st, "1/alpha-hat(M_Z)", 127.930, "PDG 2024 (MS-bar)")
    GF = measured(st, "G_F", 1.1663788e-5, "PDG 2024")
    MV = measured(st, "M_V floor", 3755.1, "LHC Z' recast (src/m331_zprime_recast.py)")
    rows, ok, (Qu, Qd) = B.charges("+1/sqrt3", 3)
    qp, qn, qe, qnu, _ = LL.rung1_matter_charges()[("+1/sqrt3", 3)]
    hbar, c, e = 1.054571817e-34, 2.99792458e8, 1.602176634e-19
    mpl = math.sqrt(hbar * c / G) * c**2 / e / 1e9
    p3 = T3.pole(3, "+1/sqrt3", MV=4e3, gmax=M.ALPHA1)
    p5 = T3.pole(5, "+1/sqrt3", MV=4e3, gmax=M.ALPHA1)
    banner("1  Unification: SU(3)_C x SU(3)_L x U(1)_X -> Standard Model -> electromagnetism")
    print(f"   anomaly-fixed quark charges at N_c = 3: Q_u = {Qu}, Q_d = {Qd};  q_p + q_e = {qp + qe} exactly")
    print(f"   Planck mass from the measured G: {mpl:.5e} GeV")
    print(f"   Landau poles (beta = +1/sqrt3, alpha = 1, three loops): N_c = 3 at {p3 / mpl:.2f} M_Pl,"
          f" N_c = 5 at {p5 / mpl:.1e} M_Pl -> N_c = 3 selected: {p5 < mpl < p3}")
    for k, v in (("G", G), ("Q_u", Qu), ("Q_d", Qd), ("q_p + q_e", qp + qe), ("M_Pl", mpl),
                 ("1/alpha-hat(M_Z)", ainv), ("G_F", GF), ("N_c", 3), ("M_V floor", MV)):
        produce(st, k, v)


# ------------------------------------------------------------------------------- stage 2
def electroweak_to_photon():
    st = 2
    import ladder_links as LL
    ainv = use(st, "1/alpha-hat(M_Z)")
    measured(st, "Delta alpha_had", LL.DALPHA_HAD[0], "PDG 2024 electroweak review")
    d = LL.DALPHA_LEP_3LOOP + LL.DALPHA_HAD[0] + LL.DALPHA_CONV
    a0inv = ainv / (1 - d)
    num, _ = LL.dalpha_lep_one_loop()
    banner("2  Electroweak to the photon: one coupling from M_Z to zero momentum")
    print(f"   leptons' running at one loop {num * 1e4:.3f}e-4 (computed); hadrons {LL.DALPHA_HAD[0]} (measured)")
    print(f"   1/alpha(0) = {ainv} / (1 - {d:.6f}) = {a0inv:.6f}  (CODATA 137.035999)")
    produce(st, "alpha(0)", 1 / a0inv)
    produce(st, "Delta alpha (leptons, hadrons)", (LL.DALPHA_LEP_3LOOP, LL.DALPHA_HAD[0]))


# ------------------------------------------------------------------------------- stage 3
def weak_to_strong():
    st = 3
    import ladder_links as LL
    GF = use(st, "G_F")
    measured(st, "Gamma(pi -> mu nu)", LL.GAMMA_PI_MUNU, "PDG 2024 (with delta_pi, |V_ud|)")
    g0 = LL.GAMMA_PI_MUNU * LL.HBAR_GEV_S / (1 + LL.DELTA_PI[0])
    mpi, mmu = LL.M_PIC_GEV, LL.M_MU
    f = math.sqrt(8 * math.pi * g0 / (GF**2 * mmu**2 * mpi * (1 - mmu**2 / mpi**2) ** 2)) / LL.V_UD[0]
    banner("3  Weak to strong: G_F and the pion's weak decay give the pion decay constant")
    print(f"   f_pi = {f * 1e3:.2f} MeV (lattice, not used: 130.2 +- 1.2)")
    produce(st, "f_pi", f)
    produce(st, "|V_ud|", LL.V_UD[0])


# ------------------------------------------------------------------------------- stage 4
def strong_force():
    st = 4
    import chiral_breaking as CB
    import ladder_links as LL
    f = use(st, "f_pi")
    a0 = use(st, "alpha(0)")
    Qu, Qd, Nc = use(st, "Q_u"), use(st, "Q_d"), use(st, "N_c")
    measured(st, "FLAG constants (m_ud, Sigma, F_pi/F, lbar_3) and sigma terms", None, "FLAG 2024, FLAG 19/21")
    measured(st, "m_rho, m_a1", (LL.M_RHO[0], LL.M_A1[0]), "PDG 2024")
    F = f / math.sqrt(2)
    A = a0 * Nc * float(Qu**2 - Qd**2) / (math.pi * F)
    width = A**2 * LL.M_PI0_GEV**3 / (64 * math.pi) * 1e9
    Fc = F / CB.FPI_OVER_F[0]
    M2 = 2 * CB.M_UD_FLAG[0] * CB.SIGMA_CUBE_ROOT**3 / Fc**2
    mpi4 = math.sqrt(M2 * (1 - M2 / (32 * math.pi**2 * Fc**2) * CB.LBAR3[0]))
    ma, mr = LL.M_A1[0], LL.M_RHO[0]
    dm2 = 3 * a0 / (4 * math.pi) * mr**2 * ma**2 / (ma**2 - mr**2) * math.log(ma**2 / mr**2) * 1e6
    budget, _ = LL.mass_budget("2+1")
    banner("4  The strong force: chiral symmetry breaking, pions, nucleons")
    print(f"   pi0 -> gamma gamma with stage 1's charges, stage 2's alpha, stage 3's f_pi: {width:.3f} eV"
          f" (PrimEx 7.802 +- 0.117)")
    print(f"   pion mass at O(p^4) with F = f_pi/sqrt2/{CB.FPI_OVER_F[0]}: {mpi4 * 1e3:.1f} MeV (measured 135.0)")
    print(f"   electromagnetic splitting from stage 2's alpha (rho + a1 saturation): {dm2:.0f} MeV^2 (measured 1261)")
    print(f"   one-pion exchange range: {CB.HBARC / CB.M_PIC:.3f} fm")
    print("   the nucleon's mass: " + ";  ".join(f"{k} {100 * v:+.2f}%" for k, v in budget.items()))
    produce(st, "pi0 width", width)
    produce(st, "m_pi O(p^4)", mpi4)
    produce(st, "mass budget", budget)


# ------------------------------------------------------------------------------- stage 5
def electromagnetism_in_the_lab():
    st = 5
    import ladder_links as LL
    import stur_gravity_full as GF
    a0 = use(st, "alpha(0)")
    G = use(st, "G")
    neutral = use(st, "q_p + q_e")
    measured(st, "diamond permittivity", 5.7, "tabulated (AUDIT.md)")
    hbar, c, u = 1.054571817e-34, 2.99792458e8, 1.66053906660e-27
    delta = math.sqrt(0.1 * G * u**2 / (a0 * hbar * c))
    gap = GF.casimir_safe_gap()
    banner("5  Electromagnetism in the lab: the background the diamonds must suppress")
    print(f"   matter is neutral (stage 1): q_p + q_e = {neutral}; with stage 2's alpha the experiment needs"
          f" < {delta:.2e} e per nucleon")
    print(f"   Casimir-Polder is 10% of gravity at a gap of {gap * 1e6:.1f} um")
    produce(st, "neutrality needed", delta)
    produce(st, "gap", gap)


# ------------------------------------------------------------------------------- stage 6
def gravity_in_the_lab():
    st = 6
    import graviton_exchange as GX
    import stur_gravity_entanglement as GE
    G = use(st, "G")
    gap = use(st, "gap")
    budget = use(st, "mass budget")
    assert G == GE.G
    phi, _, _, (m, dx, g_used, hold, ramp) = GX.branch_phases()
    assert abs(g_used / gap - 1) < 1e-12
    light = phi * (1 - budget["u, d quark masses"]) ** 2
    banner("6  Gravity in the lab: one-graviton exchange between design A's diamonds")
    print(f"   m = {m:.3e} kg, gap {gap * 1e6:.1f} um (stage 5): entangling phase {phi:.3f} rad")
    print(f"   the mass is {100 * budget['QCD field energy']:.0f}% QCD field energy (stage 4); with massless"
          f" u, d quarks the phase would be {light:.2f} rad")
    produce(st, "phase", phi)
    produce(st, "diamond mass", m)
    produce(st, "cryostat T", measured(st, "cryostat T", 0.15, "src/stur_gravity_full.py BASE_ENV (design)"))


# ------------------------------------------------------------------------------- stage 7
def gravity_as_gauge_theory():
    st = 7
    import sympy as sp
    import ladder_links as LL
    import macdowell_mansouri as MM
    G = use(st, "G")
    phi = use(st, "phase")
    Lam = measured(st, "Lambda", LL.LAMBDA_SI, "Planck 2018 with BAO")
    l = math.sqrt(3 / Lam)
    lp2 = 1.054571817e-34 * G / 2.99792458e8**3
    rel, _, _ = LL.lambda_correction_size()
    # the gauge theory's field equations, G_munu + (3/l^2) g_munu = 0, solved by Schwarzschild-de
    # Sitter (geometric units, M = G m / c^2); this f(r) is what stage 8 receives
    Mg, ls = sp.symbols("M l", positive=True)
    f_sds = 1 - 2 * Mg / MM.r - MM.r**2 / ls**2
    g = MM.static_spherical(f_sds)[1]
    solves = sp.simplify(MM.einstein_tensor(g) + 3 / ls**2 * g) == sp.zeros(4, 4)
    banner("7  Gravity as a broken de Sitter gauge theory: SO(4,1) -> SO(3,1)")
    print(f"   l = sqrt(3/Lambda) = {l:.3e} m; coupling 3/(G Lambda) in Planck units {3 / (lp2 * Lam):.2e}")
    print(f"   the Lambda term cancels in the entangling combination: {LL.lambda_cancels_in_entangling_phase()};"
          f" stage 6's {phi:.3f} rad changes at order {rel:.0e}")
    print(f"   its field equations are solved by Schwarzschild-de Sitter, f = 1 - 2GM/(c^2 r) - r^2/l^2: {solves}")
    produce(st, "l", l)
    produce(st, "f(r)", (f_sds, Mg, ls))


# ------------------------------------------------------------------------------- stage 8
def black_holes():
    st = 8
    import mpmath
    import sympy as sp
    import black_holes as BH
    import ladder_links as LL
    import macdowell_mansouri as MM
    l = use(st, "l")
    f_sds, Mg, ls = use(st, "f(r)")
    G = use(st, "G")
    m = use(st, "diamond mass")
    mpl = use(st, "M_Pl")
    m_ov = use(st, "neutron-star limit (free neutrons)")
    t_cryo = use(st, "cryostat T")
    mv = use(st, "M_V floor")
    resid = BH.surface_gravity_from_spin_connection()
    # Hawking temperature of Sgr A* from stage 7's f(r): kappa = c^2 f'(r_h)/2, T = hbar kappa / (2 pi c k_B),
    # against the Lambda = 0 formula hbar c^3 / (8 pi G M k_B)
    hbar, c, kB = 1.054571817e-34, 2.99792458e8, 1.380649e-23
    M_kg = BH.SGRA_VLTI[0] * BH.GM_SUN / G
    mpmath.mp.dps = 50
    fsym = sp.lambdify((MM.r, Mg, ls), f_sds, "mpmath")
    Mgeo = mpmath.mpf(G) * mpmath.mpf(M_kg) / mpmath.mpf(c) ** 2
    L = mpmath.sqrt(3 / mpmath.mpf(LL.LAMBDA_SI))
    assert abs(float(L) / l - 1) < 1e-15
    fn = lambda x: fsym(x, Mgeo, L)
    rh = mpmath.findroot(fn, 2 * Mgeo)
    hb, cm, kb = mpmath.mpf(hbar), mpmath.mpf(c), mpmath.mpf(kB)
    kappa = mpmath.diff(fn, rh) / 2 * cm**2
    T_sds_mp = hb * kappa / (2 * mpmath.pi * cm * kb)
    T_0_mp = hb * cm**3 / (8 * mpmath.pi * mpmath.mpf(G) * mpmath.mpf(M_kg) * kb)
    T_sds, T_0, dT = float(T_sds_mp), float(T_0_mp), float(T_sds_mp / T_0_mp - 1)
    e = BH.eht()
    a_i, a_f, _, _, _ = BH.area_law()
    labels = ("the diamond experiment's cryostat (stage 6)", "the CMB: above this mass a hole absorbs more",
              "electrons (the charges of stages 1 and 5)", "muons", "pions (stage 4's Goldstone bosons)",
              "QCD crossover: stage 4's condensate melts", "W and Z with their Goldstones (stage 1)", "top quark",
              "electroweak crossover (stage 1's breaking)", "3-3-1 content (stage 1)",
              "the Planck mass (stage 1's cutoff): semiclassics ends")
    rows = LL.evaporation_thresholds(t_cryo=t_cryo, mv=mv, m_pl_gev=mpl, labels=labels)
    banner("8  Black holes: the strong field, and evaporation back through every force")
    print(f"   surface gravity from stage 7's spin connection: omega^0_1t - f'/2 = {resid}")
    print(f"   Hawking temperature of Sgr A* from stage 7's f(r), measured Lambda: {T_sds:.6e} K"
          f" (Lambda = 0: {T_0:.6e} K; the measured Lambda changes it by {dT:.1e})")
    print(f"   the diamond is {m / (mpl * 1e9 * 1.602176634e-19 / c**2):.1e} Planck masses:"
          " too light to be a semiclassical black hole")
    print(f"   EHT: M87* {e['M87*'][2]:+.2f} sigma, Sgr A* {e['Sgr A*'][2]:+.2f} sigma;"
          f"  GW250114 area {a_i:.0f} -> {a_f:.0f} km^2 (it grew, as Hawking's area law requires)")
    print(f"   GW250114's holes, {BH.GW_M1:.1f} and {BH.GW_M2:.1f} solar masses, are {BH.GW_M2 / m_ov:.0f} to"
          f" {BH.GW_M1 / m_ov:.0f} times branch 7a's free-neutron limit: nothing could hold them up")
    print("   a shrinking hole's temperature, coldest first:")
    for lab, T, M, tau, f in rows:
        print(f"      {lab:52s} T = {T:9.2e} GeV, {tau:9.2e} s left, f = {f:5.2f}")
    last_T = rows[-1][1]
    print(f"   -> it ends at stage 1's Planck mass, T = {last_T:.4e} GeV = M_Pl/8 pi ({mpl / (8 * math.pi):.4e} GeV)")
    produce(st, "Sgr A* T_H", T_sds)
    produce(st, "end temperature", last_T)


# ------------------------------------------------------------------------------ branches
def w_mass():
    st = "2a"
    import chain_branches as CB
    import ladder_links as LL
    GF, a0 = use(st, "G_F"), use(st, "alpha(0)")
    lep, had = use(st, "Delta alpha (leptons, hadrons)")
    measured(st, "M_Z, m_t", (LL.M_Z, CB.M_TOP), "PDG 2024")
    measured(st, "M_W", CB.M_W_MEAS[0], "PDG 2024 (compared, not used)")
    w = CB.w_mass(a0, GF, dalpha=lep + had)
    banner("2a The W mass: what stage 2's running of alpha, and the top quark, do to it")
    for k, lab in (("tree", "tree level with stage 2's alpha(0)"), ("running", "with alpha run to M_Z (stage 2)"),
                   ("top", "with the top quark's loop"), ("top + QCD", "and its QCD correction")):
        print(f"   {lab:36s}: {w[k]:.3f} GeV  ({100 * (w[k] / CB.M_W_MEAS[0] - 1):+.2f}%)")
    print(f"   measured {CB.M_W_MEAS[0]} +- {CB.M_W_MEAS[1]} GeV; the remaining bosonic loops are not computed")
    produce(st, "M_W", w["top + QCD"])


def electron_moment():
    st = "2b"
    import chain_branches as CB
    a0 = use(st, "alpha(0)")
    measured(st, "QED series coefficients", CB.A_E_C5, "three to five loops, hadronic and weak terms (AUDIT.md)")
    measured(st, "a_e", CB.A_E_MEAS[0], "Fan et al. 2023")
    inv = CB.alpha_from_a_e()
    banner("2b The electron's magnetic moment: where stage 2's alpha comes from")
    print(f"   a_e from stage 2's alpha through the QED series: {CB.a_e(1 / a0):.9f}  (measured {CB.A_E_MEAS[0]:.14f})")
    print(f"   the measured a_e, inverted: 1/alpha = {inv:.9f}  (published {CB.AINV_FROM_AE[0]});"
          f" stage 2 has {1 / a0:.6f}")
    print("   a return trip, not a test: stage 1's alpha-hat(M_Z) was obtained from alpha(0) in the first place")
    produce(st, "1/alpha from a_e", inv)


def weak_angle():
    st = "2c"
    import chain_branches as CB
    lep, had = use(st, "Delta alpha (leptons, hadrons)")
    measured(st, "sin^2 theta_W(M_Z)", CB.S2_MZ[0], "PDG 2024 (MS-bar)")
    measured(st, "sin^2 theta_W at 157 MeV", CB.S2_QWEAK[0], "Qweak via PDG 2024 (compared, not used)")
    s0, dl, dh = CB.weak_angle_at_zero(lep, had)
    banner("2c The weak mixing angle at zero momentum: stage 2's loops also mix the photon with the Z")
    print(f"   leptons pull it toward 1/4 ({dl:+.5f}), quarks toward 21/44 ({dh:+.5f}):"
          f" {CB.S2_MZ[0]} at M_Z  ->  {s0:.5f} at zero")
    print(f"   full calculation {CB.S2_ZERO_PDG[0]} +- {CB.S2_ZERO_PDG[1]};  measured {CB.S2_QWEAK[0]} +- {CB.S2_QWEAK[1]}")
    produce(st, "sin^2 theta_W(0)", s0)


def neutron_lifetime():
    st = "3a"
    import chain_branches as CB
    GF, Vud = use(st, "G_F"), use(st, "|V_ud|")
    measured(st, "g_A", CB.G_A[0], "PDG 2024")
    measured(st, "m_n - m_p", CB.DM_NP, "CODATA 2018")
    measured(st, "radiative corrections to neutron decay", CB.MS_CONSTANT[0], "Marciano and Sirlin 2006")
    measured(st, "neutron lifetime", CB.TAU_N_MEAS[0], "PDG 2024 (compared, not used)")
    tree, tau, err = CB.neutron_lifetime(GF, Vud)
    banner("3a The neutron lifetime: the weak force acting on the strong force's nucleon")
    print(f"   phase space from m_n - m_p, computed: f = {CB.phase_space():.4f};  tree level {tree:.1f} s")
    print(f"   with the quoted radiative corrections: {tau:.1f} +- {err:.1f} s"
          f"  (measured {CB.TAU_N_MEAS[0]} +- {CB.TAU_N_MEAS[1]} s)")
    produce(st, "neutron lifetime", tau)


def primordial_helium():
    st = "4a"
    import chain_branches as CB
    tau, mpl, a0 = use(st, "neutron lifetime"), use(st, "M_Pl"), use(st, "alpha(0)")
    measured(st, "baryon-to-photon ratio", CB.ETA10[0] * 1e-10, "PDG 2024 (Planck)")
    measured(st, "deuteron binding, n + p and D + D cross sections", CB.B_DEUTERON, "nuclear data (AUDIT.md)")
    measured(st, "Y_p", CB.YP_MEAS[0], "PDG 2024 (compared, not used)")
    h = CB.helium(tau, mpl, a0)
    banner("4a Primordial helium: gravity's clock, the weak rates, the deuteron, the Coulomb barrier")
    print(f"   gravity (stage 1's M_Pl) sets the expansion: {h['t(T = 1 MeV)']:.2f} s at 1 MeV,"
          f" {h['t(T = 0.1 MeV)']:.0f} s at 0.1 MeV")
    print(f"   the weak rates, normalised to 3a's lifetime, freeze out with {100 * h['X_n at freeze-out']:.1f}% neutrons")
    print(f"   deuterium survives and burns through stage 2's Coulomb barrier at {h['T at half helium'] * 1e3:.0f} keV,"
          f" {h['t at half helium']:.0f} s; by then {100 * h['X_n when helium forms']:.1f}% neutrons are left")
    print(f"   helium mass fraction Y_p = {h['Y_p']:.4f}  (measured {CB.YP_MEAS[0]} +- {CB.YP_MEAS[1]});"
          " a minimal network, see chain_branches.py")
    produce(st, "Y_p", h["Y_p"])


def mass_difference():
    st = "4b"
    import chain_branches as CB
    GF, Vud, mpl, a0 = use(st, "G_F"), use(st, "|V_ud|"), use(st, "M_Pl"), use(st, "alpha(0)")
    tau, yp = use(st, "neutron lifetime"), use(st, "Y_p")
    L = CB.DM_NP_LATTICE
    measured(st, "lattice m_n - m_p and its QCD and QED parts", L["total"][0], "Borsanyi et al. 2015")
    rows = CB.splitting_consequences(GF, Vud, mpl, a0, (1.01 * CB.DM_NP, L["total"][0]))
    slope = (rows[0][3] - yp) / (0.01 * CB.DM_NP)
    banner("4b The neutron-proton mass difference: what 3a's lifetime and 4a's helium owe to it")
    print(f"   lattice QCD + QED: {L['QCD'][0]} MeV from m_d - m_u, {L['QED'][0]:+} MeV from electromagnetism:"
          f" {L['total'][0]} +- {L['total'][1]} MeV  (measured {CB.DM_NP:.4f}); not derived here")
    print(f"   at the measured value: lifetime {tau:.1f} s (3a), Y_p = {yp:.4f} (4a)")
    print(f"   at the lattice's central value: lifetime {rows[1][2]:.0f} s, Y_p = {rows[1][3]:.3f}")
    print(f"   dY_p/d delta = {slope:+.2f} per MeV: the measured helium fixes it to +- {abs(CB.YP_MEAS[1] / slope) * 1e3:.0f} keV")
    produce(st, "helium's sensitivity to m_n - m_p", slope)


def collapse():
    st = "7a"
    import black_holes as BH
    import chain_branches as CB
    mpl, G = use(st, "M_Pl"), use(st, "G")
    measured(st, "solar mass parameter, nucleon masses", BH.GM_SUN, "IAU 2015; CODATA 2018")
    measured(st, "heaviest neutron star", CB.M_NS_MEAS[0], "PSR J0740+6620 (compared, not used)")
    s = CB.collapse_limits(mpl, G, BH.GM_SUN)
    banner("7a When matter collapses: stage 1's Planck mass and the nucleon's mass")
    print(f"   M_Pl^3 / m_n^2 = {s['M_Pl^3/m_n^2']:.3f} solar masses, {s['nucleons']:.1e} nucleons")
    print(f"   electrons' Pauli pressure (Chandrasekhar): {s['Chandrasekhar number']:.3f}/mu_e^2 of it ="
          f" {s['M_Ch']:.3f} solar masses for carbon, the diamonds' element")
    print(f"   free neutrons in general relativity (Oppenheimer-Volkoff): {s['OV number']:.4f} of it ="
          f" {s['M_OV']:.3f} solar masses")
    print(f"   heaviest neutron star measured: {CB.M_NS_MEAS[0]} +- {CB.M_NS_MEAS[1]} solar masses,"
          f" {CB.M_NS_MEAS[0] / s['M_OV']:.1f} times that: stage 4's nuclear force, not Pauli pressure, carries it")
    produce(st, "Chandrasekhar mass", s["M_Ch"])
    produce(st, "neutron-star limit (free neutrons)", s["M_OV"])


STAGES = (unification, electroweak_to_photon, weak_to_strong, strong_force,
          electromagnetism_in_the_lab, gravity_in_the_lab, gravity_as_gauge_theory, black_holes)
BRANCHES = {"2a": w_mass, "2b": electron_moment, "2c": weak_angle, "3a": neutron_lifetime,
            "4a": primordial_helium, "4b": mass_difference, "7a": collapse}


def run():
    LEDGER.clear()
    INPUTS.clear()
    todo = [(i + 1, s) for i, s in enumerate(STAGES)] + list(BRANCHES.items())
    for _, s in sorted(todo, key=lambda x: order(x[0])):
        s()
    return LEDGER, INPUTS


def main():
    run()
    banner("Hand-offs: each value, the stage that produced it, the stages that used it")
    for name, _, made, used in LEDGER:
        print(f"   {name:34s} {made!s:>2}  ->  " + (", ".join(str(u) for u in used) if used else "(final)"))
    banner("Measured inputs, where they enter")
    for st, name, _, src in INPUTS:
        print(f"   {st!s:>2}: {name} ({src})")
    print("\n   Not derived anywhere in the chain: the values of these inputs, why the scales are")
    print("   so far apart, and gravity's unification with the gauge forces (stage 7 is an")
    print("   equivalent rewriting of general relativity, not a derivation from stage 1).")


if __name__ == "__main__":
    main()
