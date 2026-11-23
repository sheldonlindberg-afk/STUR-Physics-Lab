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

        phase = apq / abs_apq
        phase_conj = phase.conjugate()
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
                akp, akq = a[k][p], a[k][q]
                new_kp = c * akp + s * phase * akq
                new_kq = -s * phase_conj * akp + c * akq
                a[k][p] = new_kp
                a[p][k] = new_kp.conjugate()
                a[k][q] = new_kq
                a[q][k] = new_kq.conjugate()

        a[p][p] = complex(app + t * abs_apq, 0.0)
        a[q][q] = complex(aqq - t * abs_apq, 0.0)
        a[p][q] = 0j
        a[q][p] = 0j

        for i in range(n):
            uip, uiq = u[i][p], u[i][q]
            u[i][p] = c * uip + s * phase * uiq
            u[i][q] = -s * phase_conj * uip + c * uiq

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
