#!/usr/bin/env python3
"""
Unifying-equation search, front 4: ONE twist that gives both spin-1/2 and the thirds.

Question: is there a single gauge 'twist' g that acts on every field as (-1)^{2J}
(-1 on fermions, +1 on bosons)?  If so, a fold carrying g gives statistics from charge
(a 'spin-charge relation').  Then: does it force charges in thirds?

Fields (one generation; Q = T3 + Y; triality = colour Z3 charge; B-L).
Literature attributions marked LIT were recalled, not retrieved in this session.
"""
import itertools
from fractions import Fraction as Fr
import numpy as np

F = Fr
FIELDS = [  # name, triality, 2T (0 or 1), Y, B-L, 2J
    ("Q_L", 1, 1, F(1, 6), F(1, 3), 1),
    ("u_R", 1, 0, F(2, 3), F(1, 3), 1),
    ("d_R", 1, 0, F(-1, 3), F(1, 3), 1),
    ("L_L", 0, 1, F(-1, 2), F(-1), 1),
    ("e_R", 0, 0, F(-1), F(-1), 1),
    ("nu_R", 0, 0, F(0), F(-1), 1),
    ("H", 0, 1, F(1, 2), F(0), 0),
    ("S(B-L=2)", 0, 0, F(0), F(2), 0),        # scalar giving nu_R a Majorana mass
]
# gauge bosons sit in adjoints: every centre element acts trivially on them (and B-L = 0)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def phase(f, a, b, c, th):
    """centre element (omega^a, (-1)^b, exp(2 pi i c Y)) x exp(i th (B-L)) acting on field f."""
    _, t, twoT, Y, BL, _ = f
    return np.exp(2j * np.pi * a * t / 3) * (-1) ** (b * twoT) * np.exp(2j * np.pi * c * float(Y)) \
        * np.exp(1j * th * float(BL))


def mismatch(a, b, c, th, fields):
    return max(abs(phase(f, a, b, c, th) - (-1) ** f[5]) for f in fields)


def main():
    banner("S1  CHECK: the Standard Model's Z6 generator acts trivially on every field")
    print("    (omega, -1, exp(2 pi i Y)):  " + ", ".join(
        f"{f[0]} {abs(phase(f, 1, 1, 1, 0) - 1):.0e}" for f in FIELDS if f[0] != "S(B-L=2)"))

    banner("S2  Without B-L: is (-1)^F a gauge twist of SU(3) x SU(2) x U(1)_Y?")
    sm = [f for f in FIELDS if f[0] not in ("S(B-L=2)",)]
    cs = np.linspace(0, 6, 60001)
    best = min((mismatch(a, b, c, 0.0, sm), a, b, c) for a in range(3) for b in range(2) for c in cs)
    print(f"   best over all centre elements and hypercharge angles: max |phase - (-1)^2J| = {best[0]:.3f}")
    print("   (nu_R has Y = 0 and no colour or isospin: nothing in this group can flip its sign.)")
    sm_no_nuR = [f for f in sm if f[0] != "nu_R"]
    best2 = min((mismatch(a, b, c, 0.0, sm_no_nuR), a, b, c) for a in range(3) for b in range(2) for c in cs)
    print(f"   even without nu_R: best mismatch = {best2[0]:.3f}  (e_R needs exp(-2 pi i c) = -1, so c is")
    print("    half-integer, and then the Higgs picks up +-i instead of +1)")
    print("   -> NO spin-charge twist exists in the Standard Model gauge group.")

    banner("S3  With gauged B-L (plus nu_R and the B-L = 2 scalar)")
    ths = np.linspace(0, 12 * np.pi, 12001)
    sols = sorted({(round(th / np.pi, 3), a, b, c) for th in ths for a in range(3) for b in range(2)
                   for c in [0, 0.5, 1] if mismatch(a, b, c, th, FIELDS) < 1e-9})
    print("   (theta/pi, colour omega^a, isospin (-1)^b, hypercharge c) giving (-1)^2J on ALL fields:")
    for sol in sols[:8]:
        print(f"     theta = {sol[0]:.0f} pi   a = {sol[1]}  b = {sol[2]}  c = {sol[3]}")
    print("   theta = pi needs the COLOUR CENTRE (a = 1): omega x exp(i pi/3) = -1 on quarks -")
    print("   one combined twist carries both the colour 1/3 and the fermion sign.")
    print("   minimal: theta = 3 pi:  (-1)^{2J} = exp(3 pi i (B-L))   (KNOWN: spin-charge relation,")
    print("   realised in SO(10), where it is the centre element -1 of Spin(10))")
    for f in FIELDS:
        print(f"     {f[0]:9s} B-L = {str(f[4]):4s}  exp(3 pi i (B-L)) = {phase(f, 0, 0, 0, 3*np.pi).real:+.0f}"
              f"   (-1)^2J = {(-1)**f[5]:+d}")

    banner("S4  The fold carrying that twist: J = x Phi / 4 pi with x = B-L")
    xs = [f[4] for f in FIELDS]
    # minimal Dirac flux: exp(i x Phi) = 1 for every B-L charge present
    Phi = next(k * np.pi for k in range(1, 50) if all(abs(np.exp(1j * k * np.pi * float(x)) - 1) < 1e-9 for x in xs))
    print(f"   minimal Dirac-consistent B-L flux: Phi = {Phi/np.pi:.0f} pi   (quark B-L = 1/3 forces 6 pi; leptons alone: 2 pi)")
    print("   field-angular-momentum shift J = x Phi / 4 pi = 3x/2  (mod 1) for anything bound to the fold:")
    for name, x, stat in [("quark", F(1, 3), "fermion"), ("lepton", F(-1), "fermion"), ("Higgs", F(0), "boson"),
                          ("meson q qbar", F(0), "boson"), ("diquark qq", F(2, 3), "boson"),
                          ("baryon qqq", F(1), "fermion"), ("pentaquark", F(1), "fermion")]:
        J = (F(3, 2) * x) % 1
        print(f"     {name:13s} B-L = {str(x):4s}  J mod 1 = {str(J):4s}  -> "
              f"{'half-integer' if J == F(1, 2) else 'integer':12s} ({stat})")
    print("   -> ONE twist (B-L flux 6 pi) assigns the right statistics to every particle and hadron.")

    banner("S4b  Minimal COMBINED fold: colour-centre twist k (Z3) + B-L flux 2 pi m")
    print("   Dirac consistency: quark n_q = (k + m)/3 must be an integer; lepton n_l = -m; S: n = 2m.")
    print("   Correct statistics: n_q odd, n_l odd, n_S even.  Smallest solutions (|k| <= 2, |m| <= 6):")
    rows = []
    for m in range(1, 7):
        for k in range(0, 3):
            if (k + m) % 3:
                continue
            nq, nl = (k + m) // 3, -m
            ok = nq % 2 == 1 and nl % 2 != 0
            rows.append((m, k, nq, nl, ok))
    for m, k, nq, nl, ok in rows[:5]:
        print(f"     m = {m}, k = {k}:  quark J = {F(nq,2)}, lepton J = {F(abs(nl),2)}   statistics {'OK' if ok else 'wrong'}")
    print("   -> minimal: B-L flux 2 pi with colour twist k = 2: quarks AND leptons both get J = 1/2")
    print("      exactly. The colour-centre twist is what makes the 1/3 B-L charge Dirac-consistent.")
    print("   This object is KNOWN: the minimal grand-unified monopole carries colour-magnetic flux that")
    print("   compensates fractional charges (LIT, recalled: SU(5) Dokos-Tomaras 1980; SO(10) analogous).")

    banner("S5  Does the twist force the thirds?  (anomaly cancellation, KNOWN)")
    print("   S3 allows quark B-L = (2m+1)/3 for any integer m: 1/3 OR 1 OR 5/3 ...: allowed, not forced.")
    print("   What forces 1/3 is the number of colours, via [SU(2)]^2 U(1)_Y: N_c Y_Q + Y_L = 0:")
    for Nc in [1, 2, 3, 4, 5]:
        YQ = F(1, 2) / Nc
        print(f"     N_c = {Nc}:  Y_Q = {str(YQ):5s}  -> Q_u = {str(F(1,2)+YQ):5s}  Q_d = {str(F(-1,2)+YQ):5s}")
    print("   -> the thirds come from N_c = 3, not from the twist. The twist only RESPECTS them.")

    banner("S6  If the quark IS the fold: the baryon no-go of front 3 survives")
    print("   quark spin 1/2 needs J = k/2 with k odd (k = units of 6 pi flux); a baryon's three folds")
    odd = [c for c in itertools.product(range(-7, 8, 2), repeat=3) if sum(c) == 0]
    print(f"   must cancel: {len(odd)} solutions among odd k in [-7, 7]. B-L flux is confined in the")
    print("   broken phase, so an uncancelled fold would drag an infinite string.")


if __name__ == "__main__":
    main()
