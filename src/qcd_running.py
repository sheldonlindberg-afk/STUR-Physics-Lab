#!/usr/bin/env python3
"""Two-loop MS-bar running of the strong coupling, used by the 3-3-1 scripts."""
import numpy as np
from scipy.integrate import solve_ivp


def alpha_s_run(mu_to, mu0=91.1876, a0=0.1180, thresholds=(1.27, 4.18, 172.69)):
    """2-loop MSbar running with continuous matching at the quark masses."""
    def nf(mu):
        return 3 + sum(mu > m for m in thresholds)

    def rhs(lnmu2, a):
        n = nf(np.exp(lnmu2 / 2))
        b0, b1 = 11 - 2 * n / 3, 102 - 38 * n / 3
        return -(b0 / (4 * np.pi)) * a**2 - (b1 / (16 * np.pi**2)) * a**3
    sol = solve_ivp(rhs, [2 * np.log(mu0), 2 * np.log(mu_to)], [a0], rtol=1e-10, atol=1e-14,
                    max_step=0.5)
    return sol.y[0, -1]
