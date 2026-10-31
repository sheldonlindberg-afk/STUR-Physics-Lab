// Checks the website's roll simulator against stur_final.py (step 5) and
// REFINEMENT_R7 A2.  Run: node --test tests/
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const S = require("../assets/js/stur-roll-sim.js");

// (m [eV], seed) -> (lands/pi, beta_rec [deg]) from results/stur_final_output.txt
const EXPECTED = [
  [3e-31, 1e-2, 0.9927, 0.2069],
  [3e-31, 1e-4, 0.9843, 0.2058],
  [1e-30, 1e-2, 0.9962, 0.2076],
  [1e-30, 1e-4, 0.9951, 0.2080],
  [3e-30, 1e-2, 1.0016, 0.2087],
  [3e-30, 1e-4, 1.0023, 0.2095],
];

test("alpha/2 is 0.2091 deg", () => {
  assert.ok(Math.abs(S.HALF_DEG - 0.20905) < 1e-5);
});

for (const [m, seed, lands, beta] of EXPECTED) {
  test(`roll m=${m} seed=${seed} matches stur_final`, () => {
    const r = S.roll(m, seed);
    assert.ok(Math.abs(r.lands - lands) < 6e-5, `lands ${r.lands} vs ${lands}`);
    assert.ok(Math.abs(r.betaRec - beta) < 6e-5, `beta ${r.betaRec} vs ${beta}`);
  });
}

test("pulls match the scoreboard", () => {
  const p = S.pulls(0.2080).map((x) => +x.pull.toFixed(2));
  assert.deepEqual(p, [-1.21, -0.09, -1.45]);
});

test("tomography with opposite domains (R7 A2)", () => {
  const row = S.TOMO.find((t) => t.m === 2e-31);
  assert.ok(Math.abs(S.deltaBeta(row.own, row.rec, 0) + 0.1465) < 1e-4);
  assert.ok(Math.abs(S.deltaBeta(row.own, row.rec, 0.085) + 0.1225) < 1e-4);
});
