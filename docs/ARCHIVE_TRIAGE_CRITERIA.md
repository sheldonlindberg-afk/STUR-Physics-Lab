# Archive triage: criteria (fixed before screening)

Committed before any archive claim was screened. Results go in
[`ARCHIVE_TRIAGE.md`](ARCHIVE_TRIAGE.md).

> **In plain terms.** The archive holds the older, much broader version of
> this project. Before reading it for anything salvageable, we write down the
> test every claim must pass, so that the answer is not shaped by what we
> hope to find.

## Scope

Every claim that the archive itself presents as a prediction or a derived
number, starting from `archive/v7-toe/HIGH_PRECISION_PREDICTIONS.md`,
`archive/v7-toe/FALSIFICATION_PROTOCOL.md` and the scripts they cite, plus
`archive/genesis-v10-stur-b/`.

## The four gates (all required to survive)

| Gate | Question | Fails if |
|---|---|---|
| **G1 Reproduces** | Does the cited script run and print the claimed number? | it crashes, is missing, or prints a different number |
| **G2 Not a fit** | Are there fewer adjustable inputs than predicted outputs? | an input was chosen to match the output it claims to predict, or the count of tuned inputs is at least the count of outputs |
| **G3 Agrees with data** | Does the number match current measurements within the stated error? | it is off by more than 3&sigma; of the combined uncertainty, or the claimed precision exceeds what the inputs allow |
| **G4 Compatible** | Is it consistent with STUR-ROLL's frozen core and with the GR precision tests? | it requires modified gravity at tested scales, or contradicts a STUR-ROLL result (rounds 1&ndash;8) |

A claim that passes all four is a **candidate**. Candidates are not adopted:
each becomes a round-9 module with its own preregistration, as in round 8.

## Gate order and stopping

Gates are applied in order; the first failure is recorded with a one-line
reason and the claim is not examined further. A claim whose script cannot be
located is marked G1-fail ("not reproducible"), not assumed correct.

## Shortlist checked regardless of order

Four ideas use the same mechanism as STUR-ROLL and are checked fully even if
the archive presents them weakly: generation splitting via Hosotani
(Wilson lines), KK-triality dark matter, holonomy baryogenesis, and the
swampland checks.
