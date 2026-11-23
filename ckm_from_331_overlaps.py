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
# Demo: run this file (python3 ckm_from_331_overlaps.py) to see one worked case.
# Inputs: the nine localisation centres were chosen (Nelder-Mead) so that |V_us|,
# |V_cb| and |V_ub| come out at their measured values. Everything else is fixed by
# hand: widths, scalar profiles and phases, and every CG weight = 1. J and the mass
# ratios are then outputs, not inputs.
# ---------------------------------------------------------------------------

def _demo_inputs():
    """Quark sector of the beta = -1/sqrt(3) 3-3-1 model on y in [-6, 6].

    Left-handed quarks: Q_1, Q_2 in the antitriplet (X = 0), Q_3 in the triplet
    (X = +1/3). Right-handed u (X = +2/3) and d (X = -1/3) are SU(3)_L singlets.
    Scalars: eta (X = -1/3), rho (X = +2/3) and their conjugates. The U(1)_X rule
    alone decides which scalar couples each generation: rho* and eta* reach Q_1, Q_2;
    eta and rho reach Q_3. All Clebsch-Gordan weights are set to 1, so no mixing
    angle is put in by hand.
    """
    n = 481
    grid = [-6.0 + 12.0 * k / (n - 1) for k in range(n)]
    third = 1.0 / 3.0
    left = [
        FermionMultiplet331("Q1_L", 0, "L", "3bar", 0.0, -1.505, 0.55, 1.0),
        FermionMultiplet331("Q2_L", 1, "L", "3bar", 0.0, -1.422, 0.55, 1.0),
        FermionMultiplet331("Q3_L", 2, "L", "3", third, -2.155, 0.55, 1.0),
    ]
    u_right = [
        FermionMultiplet331("u_R", 0, "R", "1", 2 * third, -0.398, 0.5, 1.0),
        FermionMultiplet331("c_R", 1, "R", "1", 2 * third, 1.239, 0.5, 1.0),
        FermionMultiplet331("t_R", 2, "R", "1", 2 * third, 3.303, 0.5, 1.0),
    ]
    d_right = [
        FermionMultiplet331("d_R", 0, "R", "1", -third, -0.038, 0.5, 1.0),
        FermionMultiplet331("s_R", 1, "R", "1", -third, -0.857, 0.5, 1.0),
        FermionMultiplet331("b_R", 2, "R", "1", -third, 3.327, 0.5, 1.0),
    ]
    ones = [[1.0 + 0j] * 3 for _ in range(3)]
    eta = ScalarChannel331("eta", -third, 1.0, 0.3, 1.6, 0.35, 0.20, 1.3)
    rho_c = ScalarChannel331("rho*", -2 * third, 1.0, -1.2, 1.8, -0.25, 0.15, 0.9)
    rho = ScalarChannel331("rho", 2 * third, 1.0, 0.6, 1.6, 0.25, 0.15, 0.9)
    eta_c = ScalarChannel331("eta*", third, 1.0, -1.8, 1.8, -0.35, 0.20, 1.3)
    up_scalars = [(eta, ones), (rho_c, ones)]
    down_scalars = [(rho, ones), (eta_c, ones)]
    return grid, left, u_right, d_right, up_scalars, down_scalars


def _self_checks(y_u, y_d, result) -> List[Tuple[str, bool]]:
    """Checks the numerics: V unitary, H = U diag U^dagger, J matches its definition."""
    checks: List[Tuple[str, bool]] = []
    for name, y in (("up", y_u), ("down", y_d)):
        h = _mat_mul(y, _mat_hermitian(y))
        ev, u = jacobi_hermitian_eig(h)
        rebuilt = _mat_mul(_mat_mul(u, [[ev[i] if i == j else 0.0 for j in range(3)] for i in range(3)]), _mat_hermitian(u))
        scale = max(abs(x) for row in h for x in row) or 1.0
        err = max(abs(h[i][j] - rebuilt[i][j]) for i in range(3) for j in range(3)) / scale
        checks.append((f"H_{name} = U diag(ev) U^dagger (rel. err {err:.1e})", err < 1e-10))
        checks.append((f"H_{name} eigenvalues non-negative", min(ev) > -1e-12 * scale))
    _, u_u = jacobi_hermitian_eig(_mat_mul(y_u, _mat_hermitian(y_u)))
    _, u_d = jacobi_hermitian_eig(_mat_mul(y_d, _mat_hermitian(y_d)))
    v = _mat_mul(_mat_hermitian(u_u), u_d)
    vv = _mat_mul(_mat_hermitian(v), v)
    uerr = max(abs(vv[i][j] - (1.0 if i == j else 0.0)) for i in range(3) for j in range(3))
    checks.append((f"V_CKM unitary (max |V^dagger V - 1| = {uerr:.1e})", uerr < 1e-10))
    rows = [sum(m * m for m in row) for row in result["abs_v_ckm"]]
    checks.append(("each row of |V|^2 sums to 1", all(abs(r - 1.0) < 1e-10 for r in rows)))
    checks.append(("|J| <= 1/(6 sqrt 3), the largest a 3x3 unitary allows", abs(result["jarlskog_j"]) <= 1.0 / (6.0 * math.sqrt(3.0)) + 1e-12))
    return checks


def main() -> int:
    grid, left, u_right, d_right, up_scalars, down_scalars = _demo_inputs()
    y_u, info_u = build_derived_yukawa_331(grid, left, u_right, up_scalars)
    y_d, info_d = build_derived_yukawa_331(grid, left, d_right, down_scalars)
    res = diagonalize_ckm_from_yukawas(y_u, y_d)

    print("CKM from 3-3-1 wavefunction overlaps")
    print("inputs: 9 localisation centres chosen to reproduce |V_us|, |V_cb|, |V_ub|; J and mass ratios are outputs")
    print(f"grid: {len(grid)} points on y in [{grid[0]:.1f}, {grid[-1]:.1f}]")
    print(f"up sector:   {info_u['allowed_couplings']} couplings allowed, {info_u['forbidden_by_u1x_or_rep']} forbidden by U(1)_X / SU(3)_L")
    print(f"down sector: {info_d['allowed_couplings']} couplings allowed, {info_d['forbidden_by_u1x_or_rep']} forbidden by U(1)_X / SU(3)_L")
    print("\nmass ratios from sqrt(eigenvalues of Y Y^dagger), heaviest = 1:")
    for name, ev in (("up  ", res["h_u_eigenvalues_asc"]), ("down", res["h_d_eigenvalues_asc"])):
        # An eigenvalue below ~1e-14 of the largest is round-off: that mass is not resolved.
        cells = [
            f"{math.sqrt(e / ev[-1]):.3e}" if e > 1e-14 * ev[-1] else "unresolved"
            for e in ev
        ]
        print(f"  {name}: " + "  ".join(cells))
    print("\n|V_CKM|:")
    for row in res["abs_v_ckm"]:
        print("  " + "  ".join(f"{x:.4f}" for x in row))
    o = res["observables"]
    print(f"\n|V_us| = {o['V_us']:.4f}   |V_cb| = {o['V_cb']:.4f}   |V_ub| = {o['V_ub']:.5f}   J = {o['J']:.3e}")
    print("measured (PDG 2024): |V_us| = 0.2243, |V_cb| = 0.0408, |V_ub| = 0.00382, J = 3.08e-05")
    print("(the sign of J flips if every scalar phase is conjugated; the demo does not fix that convention)")

    print("\nself-checks:")
    checks = _self_checks(y_u, y_d, res)
    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    n_pass = sum(ok for _, ok in checks)
    print(f"\n{n_pass}/{len(checks)} checks passed")
    return 0 if n_pass == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
