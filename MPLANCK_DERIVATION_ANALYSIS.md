# Can a Dimensional Constant Be Derived from Pure Mathematics?

**Document Type:** Foundational analysis (dimensional analysis / philosophy of physics)
**Status:** Standard argument, self-contained

---

## The Question

Can a dimensionful physical constant — the Planck mass, Newton's constant G, or any
other quantity with units — ever be derived purely from dimensionless mathematics
(pure numbers, integers, topological invariants), or must every physical theory take at
least one dimensional quantity as an irreducible input?

## The Dimensional Barrier

**To "derive" a dimensional constant like G would mean** expressing it as a function of
pure numbers (π, e, integers), other dimensionless constants, or logical/geometric
necessities alone. But G has dimensions of [length³/(mass·time²)]. You cannot construct
a dimensional quantity from dimensionless inputs — there is nothing in a pure number to
tell you what unit of length, mass, or time it refers to.

**Theorem (Buckingham π):** Any physical law relating n dimensional quantities involving
k independent fundamental dimensions can be rewritten as a relationship among (n−k)
dimensionless groups.

**Corollary:** To determine a dimensional quantity in absolute terms (not merely relative
to another dimensional quantity), at least one dimensional input must be supplied
somewhere in the theory. No amount of internal self-consistency, topological structure,
or discrete symmetry can substitute for it, because those objects only ever supply
integers and ratios — dimensionless numbers — never units.

## What This Rules Out

Three commonly-proposed routes for avoiding a dimensional input each fail for a specific,
identifiable reason:

**1. Topological/discrete structure alone.** A discrete symmetry group, orbifold, or
winding number provides only integers and ratios (like 1/3, 2/3). It can fix *relations
between* scales, but never an absolute scale itself — the ratio of two lengths can be a
pure number, but a single length cannot be.

**2. Self-consistency conditions.** Anomaly cancellation, moduli stabilization, vacuum
stability, and similar consistency requirements fix dimensionless coupling relations and
gauge-group structure. None of them supply a dimensional scale on their own; any apparent
scale-fixing calculation that uses such conditions can be checked for where a dimensional
input was smuggled in (usually via a coefficient in a potential, or a normalization
condition that secretly refers to an external scale).

**3. Dimensional transmutation.** In QCD, the proton mass arises dynamically from
renormalization-group running (e.g. $m_p \sim \Lambda_{QCD} \sim M_Z \exp(-8\pi^2/g_s^2)$),
which looks like it generates a scale "for free." But this always requires (a) a starting
scale at which to begin running and (b) a coupling value at that scale — both of which are
themselves dimensional or scale-referenced inputs. The mechanism *converts* one scale
(and a dimensionless coupling) into another; it does not eliminate the need for a scale.

## The Logical Structure

```
Q: Why does G have the value it has?
A: Because M_Planck = sqrt(hbar c / G) has the value it has.
Q: Why does M_Planck have that value?
A: Any answer either (a) invokes another dimensional scale, displacing the question,
   or (b) is a dimensionless self-consistency statement, which — by the Buckingham-π
   corollary above — cannot fix an absolute scale, or (c) invokes anthropic/selection
   reasoning, which explains why observers see that value without deriving the value
   itself from first principles.
```

The regress must terminate somewhere with an irreducible dimensional input. This is not
a defect of any particular theory; it is a structural fact about what "dimensional"
means.

## Why This Matters for Evaluating Any "Unification" Claim

Any theory that claims to reduce a set of physical constants to "zero free parameters"
should be checked against this bound: **at least one dimensional input is logically
required**, no matter how much dimensionless structure (topology, discrete symmetries,
group-theoretic selection rules) the theory contains upstream of it. A claim to have
derived *every* dimensional constant, including the very last one, from pure numbers
is provably impossible by the Buckingham-π argument above — not merely difficult, but
outside what mathematics permits.

A more modest and checkable claim is: "this theory needs only N dimensional inputs,"
for some small N, with everything else following as dimensionless ratios or
consistency conditions. That claim is falsifiable in the ordinary way (count the actual
independent dimensional inputs the calculation uses) and is the right standard to hold
any such framework to, rather than the impossible standard of zero dimensional inputs.

## References

1. Buckingham, E. (1914). "On physically similar systems: illustrations of the use of
   dimensional equations." Physical Review 4(4), 345.
2. Dirac, P. A. M. (1937). "The Cosmological Constants." Nature 139, 323.
3. Bekenstein, J. D. (1973). "Black holes and entropy." Phys. Rev. D 7, 2333 (for the
   related point that even information-theoretic bounds like the Bekenstein bound are
   stated in terms of a pre-existing length scale, not derivations of one).
</content>
