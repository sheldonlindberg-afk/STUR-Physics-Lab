#!/usr/bin/env python3
"""v6.13 — Deep S₃ = Z₃⋊Z₂ orbifold optimization.
S¹/S₃ is the natural geometry upgrade: 3 gen = 2⊕1, NOT circulant.

Key advantage over Z₃:
  - V_CKM ≠ Identity by construction (different singlet vs doublet masses)
  - m₁ ≠ m₂ by construction (Z₂ splits the doublet via perturbations)
  - Only 2 perturbation params per sector (singlet + doublet), not 3
"""
import numpy as np
from scipy.linalg import eigh, svd
from scipy.optimize import differential_evolution, minimize
import sys, time

N_grid = 256
theta = np.linspace(0, 2*np.pi, N_grid, endpoint=False)
dtheta = 2*np.pi / N_grid
K = np.zeros((N_grid, N_grid))
for i in range(N_grid):
    K[i,i] = 2.0/dtheta**2
    K[i,(i+1)%N_grid] = -1.0/dtheta**2
    K[i,(i-1)%N_grid] = -1.0/dtheta**2

def solve_z3(alpha, perturbations):
    V = alpha * 3 * (1 - np.cos(3 * theta)) / 2
    ww = 3 * dtheta
    for k in range(3):
        tk = 2*np.pi*k/3
        d = np.abs(theta - tk); d = np.minimum(d, 2*np.pi - d)
        V += perturbations[k] * np.exp(-d**2 / (2*ww**2))
    H = K + np.diag(V)
    evals, evecs = eigh(H, subset_by_index=[0, 2])
    psi = []
    for m in range(3):
        p = evecs[:, m]; p /= np.sqrt(np.sum(p**2) * dtheta)
        psi.append(p)
    return evals, psi

def solve_higgs(alpha_H):
    V = alpha_H * 3 * (1 - np.cos(3 * theta)) / 2
    H = K + np.diag(V)
    _, evecs = eigh(H, subset_by_index=[0, 0])
    p = evecs[:,0]; p /= np.sqrt(np.sum(p**2) * dtheta)
    if p[0] < 0: p = -p
    return p

def s3_yukawa(alpha_f, alpha_H, du_sing, du_doub, dd_sing, dd_doub):
    _, psi_raw_L = solve_z3(alpha_f, [0, 0, 0])
    psi_L = [
        psi_raw_L[0],
        (psi_raw_L[1] + psi_raw_L[2]) / np.sqrt(2),
        (psi_raw_L[1] - psi_raw_L[2]) / np.sqrt(2),
    ]
    _, psi_raw_uR = solve_z3(alpha_f, [du_sing, du_doub, du_doub])
    psi_uR = [
        psi_raw_uR[0],
        (psi_raw_uR[1] + psi_raw_uR[2]) / np.sqrt(2),
        (psi_raw_uR[1] - psi_raw_uR[2]) / np.sqrt(2),
    ]
    _, psi_raw_dR = solve_z3(alpha_f, [dd_sing, dd_doub, dd_doub])
    psi_dR = [
        psi_raw_dR[0],
        (psi_raw_dR[1] + psi_raw_dR[2]) / np.sqrt(2),
        (psi_raw_dR[1] - psi_raw_dR[2]) / np.sqrt(2),
    ]
    pH = solve_higgs(alpha_H)
    Yu = np.zeros((3, 3)); Yd = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Yu[i,j] = np.sum(psi_L[i] * pH * psi_uR[j]) * dtheta
            Yd[i,j] = np.sum(psi_L[i] * pH * psi_dR[j]) * dtheta
    return Yu, Yd

print("="*78)
print("  v6.13 — S₃ = Z₃⋊Z₂ ORBIFOLD: DEEP OPTIMIZATION")
print("="*78)
sys.stdout.flush()

# ============================================================
# PART 1: Quark sector
# ============================================================
print("\nPART 1: S₃ QUARK SECTOR (6 params for 7 obs → 1 DOF)")
print("-"*78)
sys.stdout.flush()

def obj_s3_quark(params):
    du_s, du_d, dd_s, dd_d, alpha_f, alpha_H = params
    if alpha_f < 0.5 or alpha_f > 30 or alpha_H < 5 or alpha_H > 2000: return 1e10
    try:
        Yu, Yd = s3_yukawa(alpha_f, alpha_H, du_s, du_d, dd_s, dd_d)
    except: return 1e10
    UuL, su, _ = svd(Yu); UdL, sd, _ = svd(Yd)
    su = np.sort(su)[::-1]; sd = np.sort(sd)[::-1]
    V = np.abs(UuL.T @ UdL)
    if su[1] < 1e-15 or sd[1] < 1e-15 or su[2] < 1e-30 or sd[2] < 1e-30: return 1e10
    return ((V[0,1]-0.225)/0.003)**2 + ((V[1,2]-0.041)/0.003)**2 + \
           ((V[0,2]-0.004)/0.0005)**2 + \
           ((np.log10(su[0]/su[1])-np.log10(271))/0.2)**2 + \
           ((np.log10(su[1]/su[2])-np.log10(477))/0.2)**2 + \
           ((np.log10(sd[0]/sd[1])-np.log10(51))/0.2)**2 + \
           ((np.log10(sd[1]/sd[2])-np.log10(20))/0.2)**2

bounds = [(-500, 500)]*4 + [(0.5, 30), (5, 2000)]
t0 = time.time()
result = differential_evolution(obj_s3_quark, bounds, maxiter=300,
                                  seed=42, tol=0.05, popsize=20,
                                  mutation=(0.5, 1.5), recombination=0.9)
print(f"  DE: χ² = {result.fun:.2f} in {time.time()-t0:.0f}s", flush=True)
result2 = minimize(obj_s3_quark, result.x, method='Nelder-Mead',
                   options={'maxiter':10000, 'fatol':0.01})
if result2.fun < result.fun:
    result = result2; print(f"  Polished: χ² = {result.fun:.2f}", flush=True)

du_s, du_d, dd_s, dd_d, af, aH = result.x
Yu, Yd = s3_yukawa(af, aH, du_s, du_d, dd_s, dd_d)
UuL, su, _ = svd(Yu); UdL, sd, _ = svd(Yd)
su = np.sort(su)[::-1]; sd = np.sort(sd)[::-1]
V = np.abs(UuL.T @ UdL)
print(f"\n  BEST S₃ QUARK (χ² = {result.fun:.2f}, 6 params for 7 obs → 1 DOF):")
print(f"    α_f = {af:.3f}, α_H = {aH:.1f}")
print(f"    δ_u = [{du_s:.1f}(singlet), {du_d:.1f}(doublet)]")
print(f"    δ_d = [{dd_s:.1f}(singlet), {dd_d:.1f}(doublet)]")
print(f"    mt/mc = {su[0]/su[1]:.1f} (obs 271)")
print(f"    mc/mu = {su[1]/max(su[2],1e-30):.1f} (obs 477)")
print(f"    mb/ms = {sd[0]/sd[1]:.1f} (obs 51)")
print(f"    ms/md = {sd[1]/max(sd[2],1e-30):.1f} (obs 20)")
print(f"    |V_CKM|:")
for row in V:
    print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
print(f"    |δ|/α_f = {max(abs(du_s),abs(du_d),abs(dd_s),abs(dd_d))/af:.1f}")
sys.stdout.flush()

# ============================================================
# PART 2: Lepton sector
# ============================================================
print("\n" + "="*78)
print("PART 2: S₃ LEPTON SECTOR (6 params for 6 obs → 0 DOF)")
print("-"*78)
sys.stdout.flush()

def obj_s3_lepton(params):
    de_s, de_d, dn_s, dn_d, alpha_l, alpha_H = params
    if alpha_l < 0.5 or alpha_l > 30 or alpha_H < 5 or alpha_H > 2000: return 1e10
    try:
        Ye, Yn = s3_yukawa(alpha_l, alpha_H, de_s, de_d, dn_s, dn_d)
    except: return 1e10
    UeL, se, _ = svd(Ye); UnL, sn, _ = svd(Yn)
    se = np.sort(se)[::-1]; sn = np.sort(sn)[::-1]
    U = np.abs(UeL.T @ UnL)
    if se[1] < 1e-15 or sn[1] < 1e-15: return 1e10
    s12sq = U[0,1]**2 / (1 - U[0,2]**2) if U[0,2] < 0.99 else 1
    s23sq = U[1,2]**2 / (1 - U[0,2]**2) if U[0,2] < 0.99 else 1
    s13sq = U[0,2]**2
    return ((s12sq - 0.303)/0.015)**2 + ((s23sq - 0.572)/0.02)**2 + \
           ((s13sq - 0.02195)/0.003)**2 + \
           ((np.log10(max(se[0]/se[1],1))-np.log10(16.8))/0.2)**2 + \
           ((np.log10(max(se[1]/max(se[2],1e-30),1))-np.log10(206.8))/0.2)**2 + \
           ((np.log10(max(sn[0]/sn[1],1))-np.log10(5.8))/0.3)**2

bounds_l = [(-500, 500)]*4 + [(0.5, 30), (5, 2000)]
t0 = time.time()
result_l = differential_evolution(obj_s3_lepton, bounds_l, maxiter=300,
                                    seed=123, tol=0.05, popsize=20)
print(f"  DE: χ² = {result_l.fun:.2f} in {time.time()-t0:.0f}s", flush=True)
result_l2 = minimize(obj_s3_lepton, result_l.x, method='Nelder-Mead',
                     options={'maxiter':10000, 'fatol':0.01})
if result_l2.fun < result_l.fun:
    result_l = result_l2; print(f"  Polished: χ² = {result_l.fun:.2f}", flush=True)

de_s, de_d, dn_s, dn_d, al, aH_l = result_l.x
Ye, Yn = s3_yukawa(al, aH_l, de_s, de_d, dn_s, dn_d)
UeL, se, _ = svd(Ye); UnL, sn, _ = svd(Yn)
se = np.sort(se)[::-1]; sn = np.sort(sn)[::-1]
U = np.abs(UeL.T @ UnL)
s12sq = U[0,1]**2 / (1 - U[0,2]**2) if U[0,2] < 0.99 else 1
s23sq = U[1,2]**2 / (1 - U[0,2]**2) if U[0,2] < 0.99 else 1
s13sq = U[0,2]**2
print(f"\n  BEST S₃ LEPTON (χ² = {result_l.fun:.2f}, 6 params for 6 obs → 0 DOF):")
print(f"    α_f(l) = {al:.3f}, α_H = {aH_l:.1f}")
print(f"    δ_e = [{de_s:.1f}, {de_d:.1f}]  δ_ν = [{dn_s:.1f}, {dn_d:.1f}]")
print(f"    sin²θ₁₂ = {s12sq:.4f} (obs 0.303)")
print(f"    sin²θ₂₃ = {s23sq:.4f} (obs 0.572)")
print(f"    sin²θ₁₃ = {s13sq:.5f} (obs 0.02195)")
print(f"    mτ/mμ = {se[0]/se[1]:.1f} (obs 16.8), mμ/me = {se[1]/max(se[2],1e-30):.1f} (obs 206.8)")
print(f"    mν₃/mν₂ = {sn[0]/sn[1]:.2f} (obs 5.8)")
print(f"    |δ|/α_f = {max(abs(de_s),abs(de_d),abs(dn_s),abs(dn_d))/al:.1f}")
sys.stdout.flush()

# ============================================================
# PART 3: Combined (shared α_H, α_f floats)
# ============================================================
print("\n" + "="*78)
print("PART 3: S₃ COMBINED (10 params for 13 obs → 3 DOF)")
print("-"*78)
sys.stdout.flush()

def obj_s3_combined(params):
    du_s,du_d,dd_s,dd_d,de_s,de_d,dn_s,dn_d,alpha_f,alpha_H = params
    if alpha_f < 0.5 or alpha_f > 30 or alpha_H < 5 or alpha_H > 2000: return 1e10
    try:
        Yu, Yd = s3_yukawa(alpha_f, alpha_H, du_s, du_d, dd_s, dd_d)
        Ye, Yn = s3_yukawa(alpha_f, alpha_H, de_s, de_d, dn_s, dn_d)
    except: return 1e10
    UuL,su,_ = svd(Yu); UdL,sd,_ = svd(Yd)
    su = np.sort(su)[::-1]; sd = np.sort(sd)[::-1]
    Vckm = np.abs(UuL.T @ UdL)
    UeL,se,_ = svd(Ye); UnL,sn,_ = svd(Yn)
    se = np.sort(se)[::-1]; sn = np.sort(sn)[::-1]
    Up = np.abs(UeL.T @ UnL)
    if su[1]<1e-15 or sd[1]<1e-15 or su[2]<1e-30 or sd[2]<1e-30: return 1e10
    if se[1]<1e-15 or sn[1]<1e-15: return 1e10
    s12sq = Up[0,1]**2/(1-Up[0,2]**2) if Up[0,2]<0.99 else 1
    s23sq = Up[1,2]**2/(1-Up[0,2]**2) if Up[0,2]<0.99 else 1
    s13sq = Up[0,2]**2
    chi2 = ((Vckm[0,1]-0.225)/0.005)**2 + ((Vckm[1,2]-0.041)/0.005)**2
    chi2 += ((Vckm[0,2]-0.004)/0.001)**2
    chi2 += ((np.log10(su[0]/su[1])-np.log10(271))/0.3)**2
    chi2 += ((np.log10(su[1]/max(su[2],1e-30))-np.log10(477))/0.3)**2
    chi2 += ((np.log10(sd[0]/sd[1])-np.log10(51))/0.3)**2
    chi2 += ((np.log10(sd[1]/max(sd[2],1e-30))-np.log10(20))/0.3)**2
    chi2 += ((s12sq-0.303)/0.03)**2 + ((s23sq-0.572)/0.04)**2
    chi2 += ((s13sq-0.02195)/0.008)**2
    chi2 += ((np.log10(max(se[0]/se[1],1))-np.log10(16.8))/0.3)**2
    chi2 += ((np.log10(max(se[1]/max(se[2],1e-30),1))-np.log10(206.8))/0.3)**2
    chi2 += ((np.log10(max(sn[0]/sn[1],1))-np.log10(5.8))/0.5)**2
    return chi2

bounds_c = [(-500,500)]*8 + [(0.5,30), (5,2000)]
t0 = time.time()
result_c = differential_evolution(obj_s3_combined, bounds_c, maxiter=300,
                                    seed=77, tol=0.1, popsize=20)
print(f"  DE: χ² = {result_c.fun:.2f} in {time.time()-t0:.0f}s", flush=True)
result_c2 = minimize(obj_s3_combined, result_c.x, method='Nelder-Mead',
                     options={'maxiter':10000, 'fatol':0.1})
if result_c2.fun < result_c.fun:
    result_c = result_c2; print(f"  Polished: χ² = {result_c.fun:.2f}", flush=True)

du_s,du_d,dd_s,dd_d,de_s,de_d,dn_s,dn_d,af_c,aH_c = result_c.x
Yu, Yd = s3_yukawa(af_c, aH_c, du_s, du_d, dd_s, dd_d)
Ye, Yn = s3_yukawa(af_c, aH_c, de_s, de_d, dn_s, dn_d)
UuL,su,_ = svd(Yu); UdL,sd,_ = svd(Yd)
su = np.sort(su)[::-1]; sd = np.sort(sd)[::-1]
Vckm = np.abs(UuL.T @ UdL)
UeL,se,_ = svd(Ye); UnL,sn,_ = svd(Yn)
se = np.sort(se)[::-1]; sn = np.sort(sn)[::-1]
Up = np.abs(UeL.T @ UnL)
s12sq = Up[0,1]**2/(1-Up[0,2]**2) if Up[0,2]<0.99 else 1
s23sq = Up[1,2]**2/(1-Up[0,2]**2) if Up[0,2]<0.99 else 1
s13sq = Up[0,2]**2

print(f"\n  BEST S₃ COMBINED (χ² = {result_c.fun:.2f}, 10 params for 13 obs → 3 DOF):")
print(f"    α_f = {af_c:.3f}, α_H = {aH_c:.1f}")
print(f"    δ_u=[{du_s:.1f},{du_d:.1f}] δ_d=[{dd_s:.1f},{dd_d:.1f}]")
print(f"    δ_e=[{de_s:.1f},{de_d:.1f}] δ_ν=[{dn_s:.1f},{dn_d:.1f}]")
print(f"  QUARKS:")
print(f"    mt/mc={su[0]/su[1]:.1f}(271) mc/mu={su[1]/max(su[2],1e-30):.1f}(477)")
print(f"    mb/ms={sd[0]/sd[1]:.1f}(51) ms/md={sd[1]/max(sd[2],1e-30):.1f}(20)")
print(f"    |V_CKM|:")
for row in Vckm:
    print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
print(f"  LEPTONS:")
print(f"    mτ/mμ={se[0]/se[1]:.1f}(16.8) mμ/me={se[1]/max(se[2],1e-30):.1f}(206.8)")
print(f"    mν₃/mν₂={sn[0]/sn[1]:.2f}(5.8)")
print(f"    sin²θ₁₂={s12sq:.4f}(0.303) sin²θ₂₃={s23sq:.4f}(0.572) sin²θ₁₃={s13sq:.5f}(0.022)")
print(f"    |δ|/α_f = {max(abs(du_s),abs(du_d),abs(dd_s),abs(dd_d),abs(de_s),abs(de_d),abs(dn_s),abs(dn_d))/af_c:.1f}")

print("\n" + "="*78)
print("  S₃ vs Z₃: VERDICT")
print("="*78)
print(f"  Z₃ quark (8 params, -1 DOF): χ² = 0.20 (overfitting)")
print(f"  Z₃ combined (11 params, 2 DOF): χ² = 93 (FAILS)")
print(f"  S₃ quark (6 params, 1 DOF): χ² = {result.fun:.2f}")
print(f"  S₃ lepton (6 params, 0 DOF): χ² = {result_l.fun:.2f}")
print(f"  S₃ combined (10 params, 3 DOF): χ² = {result_c.fun:.2f}")
print(f"\n  S₃ wins if combined χ² < ~7.8 (p=0.05 for 3 DOF)")
print("="*78)
