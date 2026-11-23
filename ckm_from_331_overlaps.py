from __future__ import annotations

import cmath
from dataclasses import dataclass
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ScalarChannel331:
    """Represents a scalar/background channel carrying U(1)_X charge and profile."""
    name: str
    x_charge: float
    vev_scale: float
    center_y: float
    sigma_y: float
    phase_slope: float
    phase_osc_amp: float
    phase_osc_freq: float


@dataclass(frozen=True)
class FermionMultiplet331:
    """Minimal 3-3-1 metadata for a fermion state on the internal coordinate y."""
    label: str
    generation: int  # 0, 1, 2
    chirality: str   # "L" or "R"
    su3_rep: str     # e.g. "3", "3bar", "1"
    x_charge: float
    potential_center: float
    potential_width: float
    profile_sign: float  # +1.0 or -1.0 in d(ln psi)/dy


def _trapz_complex(grid: Sequence[float], vals: Sequence[complex]) -> complex:
    total = 0j
    for i in range(len(grid) - 1):
        dy = grid[i + 1] - grid[i]
        total += 0.5 * dy * (vals[i] + vals[i + 1])
    return total


def normalize_wavefunction(grid: Sequence[float], raw: Sequence[complex]) -> List[complex]:
    norm_sq = _trapz_complex(grid, [abs(z) * abs(z) for z in raw]).real
    if norm_sq <= 0.0 or not math.isfinite(norm_sq):
        raise ValueError("Wavefunction norm must be positive and finite")
    inv_norm = 1.0 / math.sqrt(norm_sq)
    return [z * inv_norm for z in raw]


def solve_localized_wavefunction(
    grid: Sequence[float],
    center: float,
    width: float,
    sign: float,
) -> Tuple[List[complex], Dict[str, float]]:
    """
    Derives a normalized profile from a first-order localization equation
    d(ln psi)/dy = -sign * ((y - center) / width^2) and returns both the
    wavefunction and its emergent mean/RMS width on the internal coordinate.
    """
    w_safe = max(float(width), 1e-4)
    inv_var = 1.0 / (w_safe * w_safe)
    s_val = float(sign)
    raw = [
        complex(
            math.exp(max(-150.0, min(150.0, -0.5 * s_val * ((y - center) ** 2) * inv_var))),
            0.0,
        )
        for y in grid
    ]
    psi = normalize_wavefunction(grid, raw)
    prob = [abs(p) * abs(p) for p in psi]
    y_mean = _trapz_complex(grid, [complex(y * pr, 0.0) for y, pr in zip(grid, prob)]).real
    y_var = _trapz_complex(
        grid, [complex(((y - y_mean) ** 2) * pr, 0.0) for y, pr in zip(grid, prob)]
    ).real
    return psi, {
        "emergent_center_y": y_mean,
        "emergent_rms_width_y": math.sqrt(max(0.0, y_var)),
    }


def build_scalar_profile(grid: Sequence[float], channel: ScalarChannel331) -> List[complex]:
    sigma = max(float(channel.sigma_y), 1e-4)
    inv_2var = 0.5 / (sigma * sigma)
    out: List[complex] = []
    for y in grid:
        amp = float(channel.vev_scale) * math.exp(
            max(-150.0, min(150.0, -((y - channel.center_y) ** 2) * inv_2var))
        )
        phase = channel.phase_slope * y + channel.phase_osc_amp * math.sin(
            channel.phase_osc_freq * y
        )
        out.append(amp * cmath.exp(1j * phase))
    return out


def is_331_coupling_allowed(
    left: FermionMultiplet331,
    scalar: ScalarChannel331,
    right: FermionMultiplet331,
    tol: float = 1e-9,
) -> bool:
    """
    Checks U(1)_X charge neutrality for psi_L^dagger * Phi * psi_R:
    -X(L) + X(Phi) + X(R) = 0, and checks basic SU(3)_L contraction compatibility.
    """
    charge_ok = abs((-float(left.x_charge)) + float(scalar.x_charge) + float(right.x_charge)) <= tol
    if not charge_ok:
        return False
    l_rep = left.su3_rep
    r_rep = right.su3_rep
    if r_rep == "1":
        return l_rep in ("3", "3bar", "1")
    return l_rep in ("3", "3bar") and r_rep in ("3", "3bar")


def overlap_integral_331(
    grid: Sequence[float],
    psi_l: Sequence[complex],
    phi: Sequence[complex],
    psi_r: Sequence[complex],
    cg_factor: complex = 1.0 + 0j,
) -> complex:
    integrand = [
        cg_factor * psi_l[k].conjugate() * phi[k] * psi_r[k] for k in range(len(grid))
    ]
    return _trapz_complex(grid, integrand)


def build_derived_yukawa_331(
    grid: Sequence[float],
    left_states: Sequence[FermionMultiplet331],
    right_states: Sequence[FermionMultiplet331],
    scalars_and_cg: Sequence[Tuple[ScalarChannel331, List[List[complex]]]],
) -> Tuple[List[List[complex]], Dict[str, Any]]:
    """
    Constructs a 3x3 Yukawa matrix from derived wavefunctions, scalar profiles,
    and 3-3-1 selection/CG weights without hardcoding mixing angles.
    """
    n_l = len(left_states)
    n_r = len(right_states)
    yukawa: List[List[complex]] = [[0j for _ in range(n_r)] for _ in range(n_l)]
    allowed_count = 0
    forbidden_count = 0
    left_diag: List[Dict[str, float]] = []
    right_diag: List[Dict[str, float]] = []

    l_waves = [solve_localized_wavefunction(grid, s.potential_center, s.potential_width, s.profile_sign) for s in left_states]
    r_waves = [solve_localized_wavefunction(grid, s.potential_center, s.potential_width, s.profile_sign) for s in right_states]

    for s, info in l_waves:
        _ = s
        left_diag.append(info)
    for s, info in r_waves:
        _ = s
        right_diag.append(info)

    for scalar, cg_mat in scalars_and_cg:
        phi_vec = build_scalar_profile(grid, scalar)
        for i, l_st in enumerate(left_states):
            for j, r_st in enumerate(right_states):
                if not is_331_coupling_allowed(l_st, scalar, r_st):
                    forbidden_count += 1
                    continue
                allowed_count += 1
                yukawa[i][j] += overlap_integral_331(
                    grid, l_waves[i][0], phi_vec, r_waves[j][0], cg_factor=cg_mat[i][j]
                )

    return yukawa, {
        "allowed_couplings": allowed_count,
        "forbidden_by_u1x_or_rep": forbidden_count,
        "left_profile_moments": left_diag,
        "right_profile_moments": right_diag,
    }


def _mat_mul(a: List[List[complex]], b: List[List[complex]]) -> List[List[complex]]:
    n = len(a)
    out = [[0j for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            if aik == 0j:
                continue
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def _mat_hermitian(a: List[List[complex]]) -> List[List[complex]]:
    n = len(a)
    return [[a[j][i].conjugate() for j in range(n)] for i in range(n)]


def jacobi_hermitian_eig(
    h: List[List[complex]], max_sweeps: int = 120, tol: float = 1e-14
) -> Tuple[List[float], List[List[complex]]]:
    n = len(h)
    a = [[h[i][j] for j in range(n)] for i in range(n)]
    u = [[1.0 + 0j if i == j else 0j for j in range(n)] for i in range(n)]

    for _ in range(max_sweeps):
        p, q = 0, 1
        max_val = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                val = abs(a[i][j])
                if val > max_val:
                    max_val = val
                    p, q = i, j
        if max_val < tol:
            break

        app, aqq = a[p][p].real, a[q][q].real
        apq = a[p][q]
        abs_apq = abs(apq)
        if abs_apq < tol:
            continue

        # Rotate in the (p, q) plane: first remove the phase of a_pq by rephasing
        # column/row q (D = diag(..., e^{-i phi} at q, ...)), then apply the real
        # Jacobi rotation with t = tan(theta) the smaller root of t^2 + 2 tau t - 1 = 0.
        phase_conj = (apq / abs_apq).conjugate()
        tau = (aqq - app) / (2.0 * abs_apq)
        t = (
            1.0 / (tau + math.sqrt(1.0 + tau * tau))
            if tau >= 0.0
            else -1.0 / (-tau + math.sqrt(1.0 + tau * tau))
        )
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c

        for k in range(n):
            if k != p and k != q:
                akp, akq = a[k][p], a[k][q] * phase_conj
                new_kp = c * akp - s * akq
                new_kq = s * akp + c * akq
                a[k][p] = new_kp
                a[p][k] = new_kp.conjugate()
                a[k][q] = new_kq
                a[q][k] = new_kq.conjugate()

        a[p][p] = complex(app - t * abs_apq, 0.0)
        a[q][q] = complex(aqq + t * abs_apq, 0.0)
        a[p][q] = 0j
        a[q][p] = 0j

        for i in range(n):
            uip, uiq = u[i][p], u[i][q] * phase_conj
            u[i][p] = c * uip - s * uiq
            u[i][q] = s * uip + c * uiq

    evals = [a[i][i].real for i in range(n)]
    order = sorted(range(n), key=lambda idx: evals[idx])
    return [evals[idx] for idx in order], [[u[row][col] for col in order] for row in range(n)]


def diagonalize_ckm_from_yukawas(
    y_u: List[List[complex]], y_d: List[List[complex]]
) -> Dict[str, Any]:
    """
    Diagonalizes H_u = Y_u Y_u^dagger and H_d = Y_d Y_d^dagger to extract
    V_CKM = U_u^dagger U_d, |V_ij| magnitudes, and Jarlskog invariant J.
    """
    ev_u, u_u = jacobi_hermitian_eig(_mat_mul(y_u, _mat_hermitian(y_u)))
    ev_d, u_d = jacobi_hermitian_eig(_mat_mul(y_d, _mat_hermitian(y_d)))
    v_ckm = _mat_mul(_mat_hermitian(u_u), u_d)

    mags = [[abs(v_ckm[i][j]) for j in range(3)] for i in range(3)]
    j_cp = (
        v_ckm[0][1]
        * v_ckm[1][2]
        * v_ckm[0][2].conjugate()
        * v_ckm[1][1].conjugate()
    ).imag

    return {
        "h_u_eigenvalues_asc": ev_u,
        "h_d_eigenvalues_asc": ev_d,
        "abs_v_ckm": mags,
        "observables": {
            "V_us": mags[0][1],
            "V_cb": mags[1][2],
            "V_ub": mags[0][2],
            "J": j_cp,
        },
        "jarlskog_j": j_cp,
    }


# ---------------------------------------------------------------------------
# Self-consistent calculation: nothing is fitted.
#
# Every field's profile on y is a mode of one operator,
#     H_f = -d^2/dy^2 + y^2 + g_X X_f A(y),
# where y^2 is the localizing domain-wall background (it sets the unit of y) and
# A(y) is the U(1)_X background sourced by every fermion of the model:
#     -A''(y) = g_X * sum_f n_f X_f |psi_f(y)|^2.
# Fields with identical quantum numbers are the successive orthogonal modes of the
# same operator, so generations are not placed by hand. A is recomputed from the
# modes and the loop repeats until A stops changing (it "locks in").
#
# External numbers, all measured and none adjusted toward quark data:
#   alpha(M_Z), sin^2 theta_W(M_Z)  ->  g_L, g_X   (beta = -1/sqrt(3) matching)
#   v = 246 GeV and the 3-3-1 scale w (only sets how heavy the exotic quarks are).
# ---------------------------------------------------------------------------

ALPHA_MZ = 1.0 / 127.95
SIN2W_MZ = 0.23122
V_EW_GEV = 246.22
W_331_GEV = 5000.0  # exotic-quark scale; light-quark results are checked to be insensitive to it

THIRD = 1.0 / 3.0

# beta = -1/sqrt(3) model, one entry per field species:
# (name, X, multiplicity per generation (colour x SU(3)_L components), number of generations).
# Leptons and exotic quarks are included because they source A(y); the total X is zero.
SPECIES: List[Tuple[str, float, int, int]] = [
    ("Q_a  (3, 3bar, 0)", 0.0, 9, 2),         # (d, -u, D)_L, generations 1 and 2
    ("Q_3  (3, 3, +1/3)", THIRD, 9, 1),       # (u, d, U)_L, generation 3
    ("up_R (3, 1, +2/3)", 2 * THIRD, 3, 4),   # u_R, c_R, t_R and the exotic U_R: same charges
    ("dn_R (3, 1, -1/3)", -THIRD, 3, 5),      # d_R, s_R, b_R and the exotics D_1R, D_2R
    ("L    (1, 3, -1/3)", -THIRD, 3, 3),      # (nu, e, N)_L
    ("e_R  (1, 1, -1)", -1.0, 1, 3),
]
# Scalars are probes of A (their condensates are not counted as sources).
SCALARS: Dict[str, float] = {"eta": -THIRD, "rho": 2 * THIRD, "chi": -THIRD}


def gauge_couplings() -> Tuple[float, float]:
    """g_L and g_X from alpha and sin^2 theta_W at M_Z for beta = -1/sqrt(3):
    t^2 = g_X^2/g_L^2 = s^2 / (1 - (1 + beta^2) s^2)."""
    g_l = math.sqrt(4.0 * math.pi * ALPHA_MZ / SIN2W_MZ)
    t2 = SIN2W_MZ / (1.0 - (4.0 / 3.0) * SIN2W_MZ)
    return g_l, math.sqrt(t2) * g_l


def _sturm_count(diag: Sequence[float], off2: float, lam: float) -> int:
    """Number of eigenvalues below lam of a symmetric tridiagonal matrix."""
    count, q = 0, 1.0
    for i, d in enumerate(diag):
        q = d - lam - (off2 / q if i else 0.0)
        if q == 0.0:
            q = 1e-300
        if q < 0.0:
            count += 1
    return count


def _thomas(diag: Sequence[float], off: float, rhs: Sequence[float]) -> List[float]:
    n = len(diag)
    c, d = [0.0] * n, [0.0] * n
    c[0], d[0] = off / diag[0], rhs[0] / diag[0]
    for i in range(1, n):
        m = diag[i] - off * c[i - 1]
        c[i] = off / m
        d[i] = (rhs[i] - off * d[i - 1]) / m
    x = [0.0] * n
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def lowest_modes(grid: Sequence[float], potential: Sequence[float], k: int) -> Tuple[List[float], List[List[float]]]:
    """Lowest k eigenpairs of -d^2/dy^2 + V(y) with psi = 0 at the ends (finite differences,
    Sturm bisection for the eigenvalues, inverse iteration for the modes)."""
    h = grid[1] - grid[0]
    diag = [2.0 / (h * h) + v for v in potential]
    off = -1.0 / (h * h)
    lo_all, hi_all = min(diag) - 4.0 / (h * h), max(diag) + 4.0 / (h * h)
    evals: List[float] = []
    modes: List[List[float]] = []
    for j in range(k):
        lo, hi = lo_all, hi_all
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if _sturm_count(diag, off * off, mid) > j:
                hi = mid
            else:
                lo = mid
            if hi - lo < 1e-13 * max(1.0, abs(mid)):
                break
        lam = 0.5 * (lo + hi)
        shift = lam - 1e-9 * max(1.0, abs(lam))
        vec = [1.0 + 0.01 * math.sin(7.0 * i) for i in range(len(grid))]
        for _ in range(6):
            vec = _thomas([d - shift for d in diag], off, vec)
            for prev in modes:  # keep exact orthogonality to lower modes
                dot = sum(a * b for a, b in zip(vec, prev)) * h
                vec = [a - dot * b for a, b in zip(vec, prev)]
            nrm = math.sqrt(sum(a * a for a in vec) * h)
            vec = [a / nrm for a in vec]
        if max(vec) < -min(vec):  # sign convention: largest lobe positive
            vec = [-a for a in vec]
        evals.append(lam)
        modes.append(vec)
    return evals, modes


def solve_self_consistent(
    n_grid: int = 401, half_width: float = 8.0, mixing: float = 0.5, tol: float = 1e-12, max_iter: int = 500
) -> Dict[str, Any]:
    """Iterates modes <-> U(1)_X background until the background stops changing."""
    _, g_x = gauge_couplings()
    grid = [-half_width + 2.0 * half_width * i / (n_grid - 1) for i in range(n_grid)]
    h = grid[1] - grid[0]
    a_field = [0.0] * n_grid
    history: List[float] = []
    modes: Dict[str, List[List[float]]] = {}
    for it in range(1, max_iter + 1):
        density = [0.0] * n_grid
        for name, x, mult, ngen in SPECIES:
            pot = [y * y + g_x * x * a for y, a in zip(grid, a_field)]
            _, modes[name] = lowest_modes(grid, pot, ngen)
            if x != 0.0:
                for psi in modes[name]:
                    for i, p in enumerate(psi):
                        density[i] += mult * x * p * p
        # -A'' = g_X rho with A = 0 at the ends.
        rhs = [g_x * r * h * h for r in density]
        a_new = _thomas([2.0] * n_grid, -1.0, rhs)
        change = max(abs(p - q) for p, q in zip(a_new, a_field))
        history.append(change)
        a_field = [(1.0 - mixing) * p + mixing * q for p, q in zip(a_field, a_new)]
        if change < tol:
            break
    scalars = {}
    for name, x in SCALARS.items():
        pot = [y * y + g_x * x * a for y, a in zip(grid, a_field)]
        scalars[name] = lowest_modes(grid, pot, 1)[1][0]
    net_charge = sum(mult * x * ngen for _, x, mult, ngen in SPECIES)
    return {"grid": grid, "A": a_field, "modes": modes, "scalars": scalars,
            "iterations": len(history), "history": history, "converged": history[-1] < tol,
            "net_x_charge": net_charge, "g_x": g_x}


def _overlap(grid: Sequence[float], a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    return _trapz_complex(grid, [complex(p * q * r, 0.0) for p, q, r in zip(a, b, c)]).real


def build_mass_matrices(sol: Dict[str, Any], w_gev: float = W_331_GEV) -> Tuple[List[List[complex]], List[List[complex]]]:
    """Up (4x4) and down (5x5) mass matrices, rows = left-handed components, columns =
    right-handed modes. The scalar in each row is fixed by which SU(3)_L component of the
    multiplet its vev sits in; U(1)_X neutrality of every term is asserted.

    up rows:   u in Q_1, u in Q_2 (via rho*), u in Q_3 (via eta), U in Q_3 (via chi)
    down rows: d in Q_1, d in Q_2 (via eta*), d in Q_3 (via rho), D in Q_1, D in Q_2 (via chi*)
    v_eta = v_rho = v / sqrt(2) (no information in the model prefers either)."""
    grid, m, s = sol["grid"], sol["modes"], sol["scalars"]
    v_eta = v_rho = V_EW_GEV / math.sqrt(2.0)
    qa, q3 = m["Q_a  (3, 3bar, 0)"], m["Q_3  (3, 3, +1/3)"][0]
    up_r, dn_r = m["up_R (3, 1, +2/3)"], m["dn_R (3, 1, -1/3)"]
    up_rows = [(qa[0], 0.0, "rho*", -2 * THIRD, v_rho), (qa[1], 0.0, "rho*", -2 * THIRD, v_rho),
               (q3, THIRD, "eta", -THIRD, v_eta), (q3, THIRD, "chi", -THIRD, w_gev)]
    dn_rows = [(qa[0], 0.0, "eta*", THIRD, v_eta), (qa[1], 0.0, "eta*", THIRD, v_eta),
               (q3, THIRD, "rho", 2 * THIRD, v_rho), (qa[0], 0.0, "chi*", THIRD, w_gev),
               (qa[1], 0.0, "chi*", THIRD, w_gev)]

    def assemble(rows, right, x_right):
        out = []
        for psi_l, x_l, sname, x_s, vev in rows:
            assert abs(-x_l + x_s + x_right) < 1e-12, (sname, x_l, x_right)
            prof = s[sname.rstrip("*")]
            out.append([complex(vev * _overlap(grid, psi_l, prof, psi_r), 0.0) for psi_r in right])
        return out

    return assemble(up_rows, up_r, 2 * THIRD), assemble(dn_rows, dn_r, -THIRD)


def light_ckm(m_u: List[List[complex]], m_d: List[List[complex]]) -> Dict[str, Any]:
    """CKM among the three light states. W links row k of the up matrix to row k of the
    down matrix for k = 0, 1, 2 (the SU(2)_L doublet inside each SU(3)_L multiplet)."""
    ev_u, u_u = jacobi_hermitian_eig(_mat_mul(m_u, _mat_hermitian(m_u)))
    ev_d, u_d = jacobi_hermitian_eig(_mat_mul(m_d, _mat_hermitian(m_d)))
    v = [[sum(u_u[k][i].conjugate() * u_d[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    mags = [[abs(x) for x in row] for row in v]
    j_cp = (v[0][1] * v[1][2] * v[0][2].conjugate() * v[1][1].conjugate()).imag
    return {"masses_up_gev": [math.sqrt(max(e, 0.0)) for e in ev_u],
            "masses_down_gev": [math.sqrt(max(e, 0.0)) for e in ev_d],
            "v": v, "abs_v": mags, "J": j_cp}


def main() -> int:
    g_l, g_x = gauge_couplings()
    sol = solve_self_consistent()
    m_u, m_d = build_mass_matrices(sol)
    res = light_ckm(m_u, m_d)
    res_w = light_ckm(*build_mass_matrices(sol, w_gev=4.0 * W_331_GEV))

    print("CKM from 3-3-1 wavefunction overlaps, solved self-consistently (no fitted inputs)")
    print(f"inputs: alpha(M_Z) = 1/{1 / ALPHA_MZ:.2f}, sin^2 theta_W = {SIN2W_MZ}, v = {V_EW_GEV} GeV, w = {W_331_GEV:.0f} GeV")
    print(f"derived couplings: g_L = {g_l:.4f}, g_X = {g_x:.4f}")
    print(f"net U(1)_X charge of all fermion fields: {sol['net_x_charge']:+.1e}")
    print(f"self-consistency: {sol['iterations']} iterations, last change in A = {sol['history'][-1]:.1e}, converged = {sol['converged']}")

    grid, hh = sol["grid"], sol["grid"][1] - sol["grid"][0]
    print("\nderived profile centres <y> (unit = width of the localizing background):")
    for name, _, _, _ in SPECIES:
        cs = ["%+.4f" % (sum(y * p * p for y, p in zip(grid, psi)) * hh) for psi in sol["modes"][name]]
        print(f"  {name}: modes " + ", ".join(cs))
    for name, prof in sol["scalars"].items():
        print(f"  scalar {name}: {sum(y * p * p for y, p in zip(grid, prof)) * hh:+.4f}")

    mu, md = res["masses_up_gev"], res["masses_down_gev"]
    print("\nmasses (GeV), light three then exotic:")
    print("  up:   " + "  ".join(f"{x:.4g}" for x in mu))
    print("  down: " + "  ".join(f"{x:.4g}" for x in md))
    print(f"  m_c/m_t = {mu[1] / mu[2]:.4g}   m_u/m_t = {mu[0] / mu[2]:.4g}")
    print(f"  m_s/m_b = {md[1] / md[2]:.4g}   m_d/m_b = {md[0] / md[2]:.4g}")
    print("  measured at M_Z (approx.): m_c/m_t = 3.6e-3, m_u/m_t = 7e-6, m_s/m_b = 1.9e-2, m_d/m_b = 9.6e-4")

    print("\n|V_CKM| (light 3 x 3 block):")
    for row in res["abs_v"]:
        print("  " + "  ".join(f"{x:.4f}" for x in row))
    a = res["abs_v"]
    print(f"\n|V_us| = {a[0][1]:.4f}   |V_cb| = {a[1][2]:.4f}   |V_ub| = {a[0][2]:.5f}   J = {res['J']:.3e}")
    print("measured (PDG 2024): |V_us| = 0.2243, |V_cb| = 0.0408, |V_ub| = 0.00382, J = 3.08e-05")
    n0u = sum(1 for x in mu[:3] if x < 1e-6 * mu[2])
    n0d = sum(1 for x in md[:3] if x < 1e-6 * md[2])
    if n0u > 1 or n0d > 1:
        print(f"note: {n0u} up and {n0d} down light masses vanish; mixing among degenerate massless states is not defined,")
        print("      so the corresponding entries of |V| are basis artefacts, not results.")
    print("why: the self-consistent background is even in y (a lopsided seed decays back to it), so every")
    print("     profile is centred at y = 0, each mode has definite parity, and overlaps of odd total parity vanish.")

    checks: List[Tuple[str, bool]] = []
    checks.append(("self-consistent loop converged", sol["converged"]))
    checks.append(("total U(1)_X charge of the fermion content is zero", abs(sol["net_x_charge"]) < 1e-12))
    worst = 0.0
    for modes in sol["modes"].values():
        for i, p in enumerate(modes):
            for j, q in enumerate(modes):
                worst = max(worst, abs(sum(a1 * b1 for a1, b1 in zip(p, q)) * hh - (1.0 if i == j else 0.0)))
    checks.append((f"modes of each operator orthonormal (max error {worst:.1e})", worst < 1e-9))
    vv = [[sum(res["v"][k][i].conjugate() * res["v"][k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    uerr = max(abs(vv[i][j] - (1.0 if i == j else 0.0)) for i in range(3) for j in range(3))
    checks.append((f"light CKM block unitary to O(v^2/w^2) (max |V^dagger V - 1| = {uerr:.1e})", uerr < 1e-2))
    dw = max(abs(p - q) for r1, r2 in zip(res["abs_v"], res_w["abs_v"]) for p, q in zip(r1, r2))
    checks.append((f"|V| insensitive to the exotic scale (w x4 changes it by {dw:.1e})", dw < 1e-2))
    checks.append(("J = 0 exactly, as it must be when no complex number enters", res["J"] == 0.0))
    odd = max(abs(sol["A"][i] - sol["A"][-1 - i]) for i in range(len(grid))) / 2
    checks.append((f"converged background is parity-even (odd part {odd:.1e})", odd < 1e-10))

    print("\nself-checks:")
    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    n_pass = sum(ok for _, ok in checks)
    print(f"\n{n_pass}/{len(checks)} checks passed")
    return 0 if n_pass == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
