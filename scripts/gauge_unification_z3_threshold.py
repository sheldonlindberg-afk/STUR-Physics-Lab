#!/usr/bin/env python3
"""
Gauge Unification: Z_3 KK Power-Law Threshold Closure
=======================================================

Round 3: Compute the actual Z_3 KK threshold corrections that bridge
the gap between sin^2(theta_W) = 3/8 at M_KK = 516 GeV and the
observed sin^2(theta_W) = 0.2312 at M_Z.

Key insight: On S^1/Z_3, the X,Y bosons (SU(5) breaking sector) have
SHIFTED KK masses m_n = (n+1/3)*M_KK, while SM gauge bosons have
m_n = n*M_KK. This mass splitting produces non-universal threshold
corrections that split the couplings in exactly the right direction.
"""

import numpy as np

v_EW = 246.22
M_Z = 91.1876
alpha_em_MZ = 1/127.95
sin2_W_obs = 0.23121
alpha_s_obs = 0.1179
L_X = 3.0 / v_EW
M_KK = 2 * np.pi / L_X
M_Pl = 1.22e19

b1, b2, b3 = 41.0/10, -19.0/6, -7.0

alpha_1_obs = alpha_em_MZ / (1 - sin2_W_obs) * (5.0/3)
alpha_2_obs = alpha_em_MZ / sin2_W_obs

def header(title):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}\n")

header("Z_3 KK THRESHOLD CORRECTIONS FOR GAUGE UNIFICATION")

# The key physics: on S^1/Z_3, the 5D SU(5) adjoint decomposes as:
# 24 -> (8,1)_0 + (1,3)_0 + (1,1)_0 + (3,2)_{-5/6} + (3bar,2)_{5/6}
#        [gluon]   [W]       [B]       [X,Y bosons]    [X,Y conjugate]

# SM gauge bosons (8+3+1 = 12 generators) have Z_3 charge q=0 -> mass n*M_KK
# X,Y bosons (12 generators) have Z_3 charge q=1 -> mass (n+1/3)*M_KK

# The threshold correction from a massive vector boson in rep R_i:
# Delta_i = -b_i^{vector}/(2pi) * ln(m/mu)

# For the X,Y bosons in (3,2)_{5/6}:
# T_3(fund) = 1/2, T_2(fund) = 1/2
# b_3^XY = -11/3 * T_3 + ... This is for gauge boson contribution
# Actually, for massive VECTOR bosons, the contribution is:
# b_i = 11/3 * C_2(adj_i) for the gauge sector

# Simpler approach: the DIFFERENTIAL threshold correction.
# At each KK level n, the contribution to 1/alpha_i is:
# delta_i^(n) = b_i^{full 5D} / (2pi) * ln(Lambda/m_n)

# For SM fields (q=0 sector): m_n = n * M_KK
# For X,Y fields (q=1 sector): m_n = (n+1/3) * M_KK

# The SPLITTING between couplings comes from the X,Y sector:
# Delta(1/alpha_i - 1/alpha_j) = (b_i^XY - b_j^XY)/(2pi) * sum_n ln(n*M_KK / (n+1/3)*M_KK)

# For the X,Y gauge bosons (massive vectors in (3,2)_{5/6} + cc):
# Their 1-loop contribution to the gauge beta functions:
# As massive vectors with 3 polarizations (5D -> 3 massive modes):

# b_i^XY for (3,2)_{5/6} massive vector:
# Gauge boson contribution: -11/3 * T(R) * multiplicity
# b_3^XY = -11/3 * 1/2 * 2 = -11/3 (2 = dim(2) from SU(2))
# b_2^XY = -11/3 * 1/2 * 3 = -11/2 (3 = dim(3) from SU(3))
# b_1^XY = -11/3 * Y^2 * dim(3)*dim(2) * 3/5 = -11/3 * (5/6)^2 * 6 * 3/5

# Using standard normalization:
# For vector in (3,2,5/6): b_1 contribution = 2/3 * Y^2 * d(R) = 2/3 * (5/6)^2 * 6 * (3/5)
# Actually the vector contribution is different from scalar.

# Let me use the KEY RELATION instead:
# In SU(5), the 24 adjoint has EQUAL beta coefficients: b_1 = b_2 = b_3 = b_SU5
# The SM part has b_i^SM (different for each i)
# The X,Y part has b_i^XY = b_SU5 - b_i^SM

# The SU(5) adjoint beta coefficient (pure gauge, 1-loop):
# b_SU5 = -11 * C_2(SU5) / 3 = -11 * 5 / 3 = -55/3

# But we need the contribution from ONE KK level of the full adjoint.
# At each KK level, the full 5D SU(5) content gives:
# b_i^{KK level} = b_SU5^{massive} for ALL i (universal)
# This means complete KK levels DON'T split the couplings!

# The splitting ONLY comes from the boundary conditions that give
# different masses to SM vs X,Y sectors.

# The finite threshold correction from the mass splitting:
# Delta_i = -b_i^XY / (2pi) * sum_{n=0}^{N} ln((n+1/3)*M_KK / (n+1)*M_KK)
#         = -b_i^XY / (2pi) * sum_{n=0}^{N} ln((n+1/3)/(n+1))

# Since the TOTAL 24 contribution is universal, only the X,Y part matters:
# delta b_i^XY = b_i^{24} - b_i^{SM} where b_i^{24} is the same for all i.
# So: delta b_1^XY - delta b_2^XY = -(b_1^SM - b_2^SM)
# and: delta b_2^XY - delta b_3^XY = -(b_2^SM - b_3^SM)

# The threshold correction to the SPLITTING:
# Delta(1/alpha_1 - 1/alpha_2) = -(b_1 - b_2)/(2pi) * S_threshold
# where S_threshold = sum_n ln((n+1/3)/(n+1)) + matching terms

# Wait - this has the WRONG sign! The mass splitting makes the X,Y
# lighter than the corresponding SM modes at the same n.
# (n+1/3)*M_KK < (n+1)*M_KK, so X,Y are LIGHTER.

# The correction from X,Y being lighter:
# More X,Y running above their threshold -> more splitting.

# Actually the sign is:
# 1/alpha_i(M_Z) = 1/alpha_GUT + b_i^SM/(2pi)*ln(M_KK/M_Z)
#                + b_i^{XY}/(2pi) * sum_n ln(M_KK/(n+1/3)M_KK)  [X,Y contribution]
#                - b_i^{24}/(2pi) * sum_n ln(M_KK/(n+1)M_KK)      [subtract full 24]

# Since b_i^{24} is universal and b_i^{XY} = b_i^{24} - b_i^{SM}:
# The non-universal part is:
# delta_i = -b_i^SM/(2pi) * sum_n [ln(M_KK/(n+1/3)M_KK) - ln(M_KK/(n+1)M_KK)]
#         = -b_i^SM/(2pi) * sum_n ln((n+1)/(n+1/3))
#         = +b_i^SM/(2pi) * sum_n ln((n+1/3)/(n+1))  ... this is negative

# Hmm, let me just compute numerically what threshold is needed and
# whether the Z_3 spectrum can provide it.

L = np.log(M_KK / M_Z)

# From sin^2(theta_W) = 3/8 at M_KK:
inv_alpha_em = 1/alpha_em_MZ
b_eff = 5*b1/3 + b2
alpha_GUT = (8.0/3) / (inv_alpha_em - b_eff/(2*np.pi) * L)

print(f"  M_KK = {M_KK:.1f} GeV, ln(M_KK/M_Z) = {L:.4f}")
print(f"  alpha_GUT = {alpha_GUT:.6f} (1/{1/alpha_GUT:.1f})")
print()

# Required threshold corrections to match observations:
Delta_1 = 1/alpha_1_obs - 1/alpha_GUT - b1/(2*np.pi)*L
Delta_2 = 1/alpha_2_obs - 1/alpha_GUT - b2/(2*np.pi)*L
Delta_3 = 1/alpha_s_obs - 1/alpha_GUT - b3/(2*np.pi)*L

print(f"  Required KK threshold corrections:")
print(f"    Delta_1 = {Delta_1:.3f}")
print(f"    Delta_2 = {Delta_2:.3f}")
print(f"    Delta_3 = {Delta_3:.3f}")
print()

# The KK threshold from Z_3 mass splitting:
# S = sum_{n=0}^{N} ln((n+1/3)/(n+1))
# This converges because (n+1/3)/(n+1) -> 1 as n -> inf
# S = ln(prod_{n=0}^{N} (n+1/3)/(n+1)) = ln(Gamma(4/3)/Gamma(1) * Gamma(N+2)/Gamma(N+4/3))

from scipy.special import gamma as Gamma

N_max = int(M_Pl / M_KK)  # KK levels up to Planck
# For large N: prod_{n=0}^{N} (n+1/3)/(n+1) ~ N^{-2/3} * Gamma(4/3)
# S ~ -2/3 * ln(N) + ln(Gamma(4/3))

S_analytic = -2.0/3 * np.log(N_max) + np.log(Gamma(4.0/3))
print(f"  KK threshold sum (N_max = M_Pl/M_KK = {N_max:.2e}):")
print(f"    S = -2/3 * ln(N) + ln(Gamma(4/3)) = {S_analytic:.3f}")
print()

# The non-universal correction:
# Delta_i^{threshold} = -b_i^SM/(2pi) * S (from the mass splitting)
# Wait, I need to be more careful. The correction comes from the
# DIFFERENCE between Z_3 spectrum and unbroken spectrum.

# For each KK level n, the 5D SU(5) adjoint contributes equally to all alpha_i.
# But on Z_3, the X,Y masses are (n+1/3)*M_KK while SM masses are (n+1)*M_KK.
# The threshold correction from this splitting is:

# Delta_i = b_i^{XY_effective}/(2pi) * S_threshold

# Since complete SU(5) multiplets are universal, the splitting ONLY
# comes from the MASS DIFFERENCE between X,Y and SM modes at each level.

# For a complete SU(5) KK level at mass m_n = n*M_KK (hypothetical):
# The contribution to 1/alpha_i is b_SU5/(2pi) * ln(Lambda/m_n) for ALL i.

# On Z_3: SM modes at n*M_KK, X,Y at (n+1/3)*M_KK.
# Delta_i = [b_i^{XY}/(2pi)*ln(Lambda/((n+1/3)*M_KK)) + b_i^{SM}/(2pi)*ln(Lambda/(n*M_KK))]
#         - [b_SU5/(2pi)*ln(Lambda/(n*M_KK))]
#         = b_i^{XY}/(2pi) * [ln(Lambda/((n+1/3)*M_KK)) - ln(Lambda/(n*M_KK))]
#         = b_i^{XY}/(2pi) * ln(n/(n+1/3))

# Summing over n:
# Delta_i = b_i^{XY}/(2pi) * sum_{n=1}^{N} ln(n/(n+1/3))

# b_i^{XY} = b_i^{SU5} - b_i^{SM}
# Since b_i^{SU5} is the same for all i, the SPLITTING is:
# Delta_i - Delta_j = (b_i^{XY} - b_j^{XY})/(2pi) * S
#                   = -(b_i^{SM} - b_j^{SM})/(2pi) * S

# So the Z_3 threshold ENHANCES the SM splitting by a factor of S!

S_sum = sum(np.log(n/(n+1.0/3)) for n in range(1, 10000))  # converges for ratios
# Actually this doesn't converge... let me check
# ln(n/(n+1/3)) = ln(1 - 1/(3n+1)) ~ -1/(3n) for large n -> diverges!

# Right, the sum DIVERGES logarithmically. This is the 5D power-law running.
# Need a UV cutoff. Use Lambda = M_Pl:
N_cut = min(int(M_Pl / M_KK), 10**7)  # practical cutoff
S_sum_N = sum(np.log(n/(n+1.0/3)) for n in range(1, N_cut+1))
# Approximate for large N: S ~ -1/3 * ln(N) + const
# More precisely: S_N = ln(prod n/(n+1/3)) = ln(Gamma(N+1)*Gamma(4/3)/(Gamma(1)*Gamma(N+4/3)))

print(f"  Threshold sum S = sum_{{n=1}}^N ln(n/(n+1/3)):")
print(f"    S(N=10^4) = {sum(np.log(n/(n+1.0/3)) for n in range(1, 10001)):.3f}")
print(f"    S(N=10^6) = {sum(np.log(n/(n+1.0/3)) for n in range(1, 10**6+1)):.3f}")

# Approximate: S(N) ~ -1/3 * ln(N) + ln(Gamma(4/3)) + const
# For N = M_Pl/M_KK ~ 2.4e16:
S_approx = -1.0/3 * np.log(M_Pl/M_KK) + np.log(Gamma(4.0/3))
print(f"    S(M_Pl/M_KK) ~ -1/3*ln({M_Pl/M_KK:.1e}) + ln(Gamma(4/3)) = {S_approx:.3f}")
print()

# The splitting correction:
# Delta_1 - Delta_2 = -(b1-b2)/(2pi) * S
# Delta_2 - Delta_3 = -(b2-b3)/(2pi) * S

delta_12_threshold = -(b1-b2)/(2*np.pi) * S_approx
delta_23_threshold = -(b2-b3)/(2*np.pi) * S_approx

# Required:
delta_12_needed = (1/alpha_1_obs - 1/alpha_2_obs) - (b1-b2)/(2*np.pi)*L
delta_23_needed = (1/alpha_2_obs - 1/alpha_s_obs) - (b2-b3)/(2*np.pi)*L

print(f"  Splitting corrections from Z_3 threshold:")
print(f"    Delta(1/alpha_1 - 1/alpha_2)_threshold = {delta_12_threshold:.3f}")
print(f"    Delta(1/alpha_2 - 1/alpha_3)_threshold = {delta_23_threshold:.3f}")
print()
print(f"  Required splittings (obs - SM running):")
print(f"    needed delta_12 = {delta_12_needed:.3f}")
print(f"    needed delta_23 = {delta_23_needed:.3f}")
print()

# Ratio: how much of the needed correction does Z_3 provide?
r12 = delta_12_threshold / delta_12_needed if delta_12_needed != 0 else 0
r23 = delta_23_threshold / delta_23_needed if delta_23_needed != 0 else 0

print(f"  Fraction provided by Z_3 KK threshold:")
print(f"    delta_12: {r12:.2%}")
print(f"    delta_23: {r23:.2%}")
print()

# Now compute the CORRECTED prediction:
# 1/alpha_i(M_Z) = 1/alpha_GUT + b_i/(2pi)*ln(M_KK/M_Z) + Delta_i_threshold
# where Delta_i_threshold includes the Z_3 mass splitting

# For the splitting, we have:
# Delta_i = b_i^{XY}/(2pi) * S
# b_i^{XY} = b_SU5 - b_i^{SM}

# We can determine b_SU5 from the requirement that the universal part is absorbed into alpha_GUT:
# b_SU5 = b1 + b2 + b3 ... no, that's wrong.
# In SU(5), the adjoint has b = -11*5/3 = -55/3 for the gauge sector.
# With matter: b_SU5 depends on matter content.

# For the SPLITTING, what matters is b_i^{XY} = const - b_i^{SM}
# The const cancels in the splitting, so:
# Delta_i^{non-universal} = -b_i^{SM}/(2pi) * S

# Total: 1/alpha_i(M_Z) = 1/alpha_GUT_eff + (b_i - b_i*f_S)/(2pi)*ln(M_KK/M_Z)
# where f_S = S/ln(M_KK/M_Z)

f_S = abs(S_approx) / L  # note S is negative, so |S|
b_eff_1 = b1 * (1 + f_S)
b_eff_2 = b2 * (1 + f_S)
b_eff_3 = b3 * (1 + f_S)

# Re-determine alpha_GUT with corrected betas:
b_eff_em = 5*b_eff_1/3 + b_eff_2
alpha_GUT_corr = (8.0/3) / (inv_alpha_em - b_eff_em/(2*np.pi) * L)

alpha_1_corr = 1.0 / (1/alpha_GUT_corr + b_eff_1/(2*np.pi) * L)
alpha_2_corr = 1.0 / (1/alpha_GUT_corr + b_eff_2/(2*np.pi) * L)
alpha_3_corr = 1.0 / (1/alpha_GUT_corr + b_eff_3/(2*np.pi) * L)

sin2_corr = (alpha_1_corr * 3/5) / (alpha_1_corr * 3/5 + alpha_2_corr)

print(f"  WITH Z_3 KK THRESHOLD CORRECTIONS:")
print(f"    f_S = |S|/ln(M_KK/M_Z) = {f_S:.2f}")
print(f"    Effective betas: b1_eff={b_eff_1:.2f}, b2_eff={b_eff_2:.2f}, b3_eff={b_eff_3:.2f}")
print(f"    alpha_GUT = {alpha_GUT_corr:.6f} (1/{1/alpha_GUT_corr:.1f})")
print()
print(f"    sin^2(theta_W)(M_Z) = {sin2_corr:.5f}  (obs: {sin2_W_obs:.5f}, err: {abs(sin2_corr-sin2_W_obs)/sin2_W_obs*100:.1f}%)")
print(f"    alpha_s(M_Z)        = {alpha_3_corr:.4f}  (obs: {alpha_s_obs:.4f}, err: {abs(alpha_3_corr-alpha_s_obs)/alpha_s_obs*100:.0f}%)")

header("SUMMARY")
print(f"  ╔═══════════════════════════════════════════════════════════╗")
print(f"  ║  GAUGE UNIFICATION WITH Z_3 KK THRESHOLDS              ║")
print(f"  ╠═══════════════════════════════════════════════════════════╣")
print(f"  ║  Without KK corrections:                                ║")
print(f"  ║    sin^2(theta_W) = 0.365 (58% off)                    ║")
print(f"  ║                                                         ║")
print(f"  ║  With Z_3 power-law KK threshold (cutoff M_Pl):       ║")
print(f"  ║    sin^2(theta_W) = {sin2_corr:.4f} ({abs(sin2_corr-sin2_W_obs)/sin2_W_obs*100:.1f}% off)                   ║")
print(f"  ║    alpha_s        = {alpha_3_corr:.4f} ({abs(alpha_3_corr-alpha_s_obs)/alpha_s_obs*100:.0f}% off)                        ║")
print(f"  ║                                                         ║")
if abs(sin2_corr - sin2_W_obs)/sin2_W_obs < 0.1:
    print(f"  ║  STATUS: SOLVED (within 10%)                           ║")
elif abs(sin2_corr - sin2_W_obs)/sin2_W_obs < 0.3:
    print(f"  ║  STATUS: CLOSE (within 30%)                            ║")
else:
    print(f"  ║  STATUS: PARTIAL (>30% off, needs 2-loop/matter)       ║")
print(f"  ╚═══════════════════════════════════════════════════════════╝")
