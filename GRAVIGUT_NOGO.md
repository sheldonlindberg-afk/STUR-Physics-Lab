# Can stage 1's gauge theory give stage 7's gravity? A no-go for orthogonal graviGUTs

*Whether the 3-3-1 gauge theory of the merged simulation's stage 1 and the broken de Sitter
gauge theory of gravity in stage 7 can be derived one from the other, or from one common
group. Independent work, not peer reviewed.*

Run it: `python3 src/m331_gravigut_nogo.py` (standard library only, about 3 s; output in
[results/m331/gravigut_nogo.txt](results/m331/gravigut_nogo.txt)). It takes stage 1's
fermions from the blind build's own functions in
[`src/chain_first_principles.py`](src/chain_first_principles.py). Pinned by
[`tests/test_331_gravigut_nogo.py`](tests/test_331_gravigut_nogo.py), with a positive
control showing that the scan finds a chiral content when an embedding has it.

## The result in one paragraph

Breaking SU(3)_C × SU(3)_L × U(1)_X cannot leave SO(1,4) or the Lorentz group behind. A
compact group has no non-compact subgroups. The only published way to derive gravity's gauge
group and internal forces together puts both in a larger orthogonal group SO(1, 3 + N), with
the fermions in one Majorana–Weyl spinor. That route does not work for stage 1. Three facts
together force SO(N) to be at least SO(30): chirality forbids zero weights and needs an odd
dim R, triality makes dim R a multiple of 3, and Majorana–Weyl needs N ≡ 6 mod 8. Every
embedding there, all 115, carries at least 49 chiral exotic multiplets (colour sextets,
15-plets), and none has stage 1's chiral content. So stage 7 is not derived from stage 1, and
no orthogonal graviGUT derives both. This confirms what [FORCE_CHAIN.md](FORCE_CHAIN.md)
already says: the step from 6 to 7 is a change of language, not of physics.

## The steps

| | Result | Label |
|---|---|---|
| N1 | so(1,4) has 4 generators with tr(XX) > 0 (three boosts and the time translation); su(3)+su(3)+u(1) and all its subalgebras have tr(XX) ≤ 0. No breaking leaves gravity's group | CHECK |
| N2 | Stage 1 has 66 Weyl components (β = −1/√3), 69 (β = +1/√3). One quark family is an SU(3)_L triplet, two are antitriplets: the families are not copies of one representation, so the content must come whole from one representation | CHECK |
| N3 | Zero weights in the vector of SO(N) make the spinor vectorlike; with V = R + R̄, conj Λᵏ R = Λ^{d−k} R, so chirality needs d odd; no zero weight means non-zero triality, so d ≡ 0 mod 3; Majorana–Weyl in SO(1, 3+N) needs N ≡ 6 mod 8. Hence d ≡ 3 mod 12: SO(30) at least. The minimal embedding, 6 = (3,1) + (1,3) in SO(12) or SO(14), is vectorlike | CHECK (conditions LIT: Majorana–Weyl at p − q ≡ 0 mod 8) |
| N4 | All 115 embeddings at d = 15 (SO(30)) and all 13 at d = 9 (SO(18), no Majorana condition, so every fermion comes twice): none with stage 1's chiral index; at least 49 (SO(30)) and 4 (SO(18)) chiral exotic multiplets | CHECK |
| N5 | Supersymmetry is the one loophole in Coleman–Mandula. N = 8 supergravity's SU(8) contains SU(3) × SU(3) × U(1), but it has 56 spin-½ states, fewer than stage 1's 66 | CHECK (count); LIT (the multiplet) |

## What this does not cover

- Parents that are not orthogonal. For E8, Distler and Garibaldi prove that no real form
  holds gravity and chiral matter together (arXiv:0905.2658). Other exceptional real forms
  are not checked here.
- Supergroups beyond N5's count, and Kaluza–Klein constructions.
- Gravity that is not unified with 3-3-1 but fixes its couplings (asymptotic safety,
  [`src/m331_gravity_fixed_point.py`](src/m331_gravity_fixed_point.py)) or is induced by its
  matter (Sakharov), tested in [INDUCED_GRAVITY_PREREG.md](INDUCED_GRAVITY_PREREG.md).

## Sources

1. F. Nesti and R. Percacci, Phys. Rev. D 81, 025010 (2010), [arXiv:0909.4537](https://arxiv.org/abs/0909.4537): SO(3,11) → SO(3,1) × SO(10), one Majorana–Weyl 64.
2. F. Nesti and R. Percacci, [arXiv:0706.3307](https://arxiv.org/abs/0706.3307): gravi-weak unification; the larger symmetry exists only where there is no metric, which is how Coleman–Mandula is respected.
3. S. Konitopoulos, D. Roumelioti and G. Zoupanos, Fortschr. Phys. 2023, 2300226, [arXiv:2309.15892](https://arxiv.org/abs/2309.15892): SO(1,17) → SO(1,3) × SO(14) → SO(10).
4. D. Roumelioti, S. Stefas and G. Zoupanos, [arXiv:2403.17511](https://arxiv.org/abs/2403.17511): SO(2,16), with the (A)dS and conformal gravity sub-chain.
5. R. Percacci, [arXiv:0803.0303](https://arxiv.org/abs/0803.0303): mixing internal and spacetime transformations.
6. J. Distler and S. Garibaldi, Commun. Math. Phys. 298, 419 (2010), [arXiv:0905.2658](https://arxiv.org/abs/0905.2658).
