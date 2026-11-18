# CANARY-060158c59f054784-higgs_rho: planted so a builder transcript that contains this string has read the oracle
"""Hidden oracle for the higgs_rho campaign.

Target: the m_H dependence of Delta rho (equivalently of the Peskin-Takeuchi T parameter, alpha T = Delta rho) from the Higgs sector at one
loop, for m_H >> M_W:  Delta rho = -(3 alpha / (16 pi c^2)) ln(m_H^2 / M_W^2) + const   ("Veltman screening": the logarithm is proportional to
the hypercharge coupling g'^2 = 4 pi alpha / c^2, so it vanishes in the custodial limit). LIT: Peskin and Takeuchi, PRD 46, 381 (1992);
PDG electroweak review, Delta rho ~ (3 G_F M_W^2 / 8 sqrt2 pi^2)[m_t^2/M_W^2 - (s^2/c^2) ln(m_H^2/M_W^2)]  (same coefficient with
G_F M_W^2 = pi alpha / (sqrt2 s^2)). Not an independent derivation; the builds are the derivation."""
import math

MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
C2 = (MW / MZ) ** 2
LINT_TARGETS = [3 / (16 * math.pi), 0.0597, 3 * ALPHA / (16 * math.pi * C2)]
LINT_EXACT = [3 * ALPHA / (16 * math.pi * C2), 3 / (16 * math.pi)]


def target(MW_, MZ_, alpha):
    return -3 * alpha / (16 * math.pi * (MW_ / MZ_) ** 2)


def coeff_check(m):
    worst = 0.0
    for MW_, MZ_, al in ((80.38, 91.19, 1 / 128.0), (80.0, 92.0, 1 / 130.0), (75.0, 91.19, 1 / 125.0)):
        for xi in (1.0,):
            worst = max(worst, abs(m.log_coefficient(MW_, MZ_, al, xi) / target(MW_, MZ_, al) - 1))
    return worst < 1e-8, f"worst relative deviation of log_coefficient from -3 alpha/(16 pi c^2): {worst:.1e}"


def xi_check(m):
    vals = [m.log_coefficient(MW, MZ, ALPHA, xi) for xi in (1.0, 0.3, 4.0)]
    return max(abs(v / vals[0] - 1) for v in vals) < 1e-8, f"log_coefficient at xi = 1, 0.3, 4: {vals}"


def slope_check(m):
    f = lambda mh: m.rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
    h1, h2 = 3e4 * MW, 3e5 * MW
    slope = (f(h2) - f(h1)) / math.log((h2 / MW) ** 2 / (h1 / MW) ** 2)
    return abs(slope / target(MW, MZ, ALPHA) - 1) < 1e-4, f"measured slope {slope:.6e}, target {target(MW, MZ, ALPHA):.6e}"


ORACLE = [("log_coefficient = -3 alpha/(16 pi c^2)", coeff_check),
          ("log_coefficient independent of the gauge parameter xi", xi_check),
          ("measured large-mH slope of rho_higgs_rel = -3 alpha/(16 pi c^2)", slope_check)]
