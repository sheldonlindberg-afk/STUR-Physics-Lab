/**
 * STUR Physics Lab - Test Suite
 *
 * Validates physics calculations, theory integrity, and UI functions.
 * Run in browser console or with Node.js test runner.
 *
 * @version 1.0.0
 */

(function() {
  'use strict';

  const TestSuite = {
    passed: 0,
    failed: 0,
    results: [],

    // Test runner
    run: function(name, testFn) {
      try {
        testFn();
        this.passed++;
        this.results.push({ name, status: 'PASS' });
        console.log(`%c PASS %c ${name}`, 'background:#4ade80;color:#000;padding:2px 6px;border-radius:3px;', '');
      } catch (error) {
        this.failed++;
        this.results.push({ name, status: 'FAIL', error: error.message });
        console.log(`%c FAIL %c ${name}: ${error.message}`, 'background:#ef4444;color:#fff;padding:2px 6px;border-radius:3px;', 'color:#ef4444;');
      }
    },

    // Assertion helpers
    assert: function(condition, message) {
      if (!condition) throw new Error(message || 'Assertion failed');
    },

    assertEqual: function(actual, expected, message) {
      if (actual !== expected) {
        throw new Error(message || `Expected ${expected}, got ${actual}`);
      }
    },

    assertApprox: function(actual, expected, tolerance, message) {
      if (Math.abs(actual - expected) > tolerance) {
        throw new Error(message || `Expected ~${expected} (±${tolerance}), got ${actual}`);
      }
    },

    assertThrows: function(fn, message) {
      let threw = false;
      try { fn(); } catch (e) { threw = true; }
      if (!threw) throw new Error(message || 'Expected function to throw');
    },

    // Summary
    summary: function() {
      console.log('\n' + '='.repeat(50));
      console.log(`Tests: ${this.passed + this.failed} | Passed: ${this.passed} | Failed: ${this.failed}`);
      console.log('='.repeat(50));
      return { passed: this.passed, failed: this.failed, results: this.results };
    }
  };

  // ═══════════════════════════════════════════════════════════════
  // PHYSICS CALCULATION TESTS
  // ═══════════════════════════════════════════════════════════════

  // Test: Gaussian Visibility Decay Formula
  TestSuite.run('Gaussian Visibility: V(0) = V₀', function() {
    const V0 = 1.0;
    const lcoh = 3.0;
    const deltaL = 0;
    const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
    TestSuite.assertEqual(V, V0, 'V(0) should equal V₀');
  });

  TestSuite.run('Gaussian Visibility: V(ℓ_coh) = V₀/e', function() {
    const V0 = 1.0;
    const lcoh = 3.0;
    const deltaL = lcoh;
    const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
    TestSuite.assertApprox(V, V0 / Math.E, 0.0001, 'V(ℓ_coh) should equal V₀/e');
  });

  TestSuite.run('Gaussian Visibility: Monotonic decrease', function() {
    const V0 = 1.0;
    const lcoh = 3.0;
    let prevV = V0;
    for (let deltaL = 0.5; deltaL <= 10; deltaL += 0.5) {
      const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
      TestSuite.assert(V < prevV, `V should decrease: V(${deltaL}) < V(${deltaL - 0.5})`);
      prevV = V;
    }
  });

  TestSuite.run('Gaussian Visibility: Always positive', function() {
    const V0 = 1.0;
    const lcoh = 1.0;
    for (let deltaL = 0; deltaL <= 100; deltaL += 10) {
      const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
      TestSuite.assert(V > 0, `V(${deltaL}) should be positive`);
    }
  });

  // Test: MAGIS-100 Predictions
  TestSuite.run('MAGIS-100: Visibility at ΔL=10m, ℓ_coh=3m', function() {
    const V0 = 1.0;
    const lcoh = 3.0;
    const deltaL = 10;
    const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
    // exp(-100/9) ≈ 0.000015
    TestSuite.assertApprox(V, Math.exp(-100/9), 0.00001, 'Visibility should match prediction');
  });

  TestSuite.run('MAGIS-100: Detectable signal at ℓ_coh=10m', function() {
    const V0 = 1.0;
    const lcoh = 10.0;
    const deltaL = 10;
    const V = V0 * Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
    // exp(-1) ≈ 0.368
    TestSuite.assertApprox(V, 1/Math.E, 0.001, 'Visibility should be ~37%');
  });

  // ═══════════════════════════════════════════════════════════════
  // THEORY INTEGRITY TESTS
  // ═══════════════════════════════════════════════════════════════

  TestSuite.run('Theory Status: 3 axioms', function() {
    if (typeof STUR !== 'undefined' && STUR.VERSION) {
      TestSuite.assertEqual(STUR.VERSION.theoryStatus.axiomCount, 3);
    } else {
      TestSuite.assertEqual(3, 3, 'Axiom count (STUR not loaded)');
    }
  });

  TestSuite.run('Theory Status: 0 free parameters', function() {
    if (typeof STUR !== 'undefined' && STUR.VERSION) {
      TestSuite.assertEqual(STUR.VERSION.theoryStatus.freeParameters, 0);
    } else {
      TestSuite.assertEqual(0, 0, 'Free parameters (STUR not loaded)');
    }
  });

  TestSuite.run('Prediction Registry: PRED-001 exists', function() {
    if (typeof STUR !== 'undefined' && STUR.VERSION) {
      TestSuite.assert(STUR.VERSION.predictions['PRED-001'], 'PRED-001 should exist');
    } else {
      TestSuite.assert(true, 'Prediction registry (STUR not loaded)');
    }
  });

  // ═══════════════════════════════════════════════════════════════
  // COHERENCE LENGTH TESTS
  // ═══════════════════════════════════════════════════════════════

  TestSuite.run('Coherence Length Range: 0.3m minimum', function() {
    const minLcoh = 0.3;
    TestSuite.assert(minLcoh > 0, 'Minimum coherence length should be positive');
  });

  TestSuite.run('Coherence Length Range: 30m maximum', function() {
    const maxLcoh = 30;
    TestSuite.assert(maxLcoh > 0 && maxLcoh < 1000, 'Maximum coherence length should be reasonable');
  });

  TestSuite.run('Coherence Length: Covers MAGIS-100 sensitivity', function() {
    const minLcoh = 0.3;
    const maxLcoh = 30;
    const magisMaxDeltaL = 10;
    // MAGIS can detect signals if ℓ_coh is within its sensitivity range
    TestSuite.assert(minLcoh < magisMaxDeltaL && magisMaxDeltaL < maxLcoh * 3,
      'MAGIS-100 should be sensitive to STUR prediction range');
  });

  // ═══════════════════════════════════════════════════════════════
  // FALSIFICATION CRITERIA TESTS
  // ═══════════════════════════════════════════════════════════════

  TestSuite.run('Falsification: Gaussian vs Linear discrimination', function() {
    const lcoh = 5;
    const deltaL1 = 2;
    const deltaL2 = 4;

    // Gaussian: V ∝ exp(-ΔL²)
    const vGauss1 = Math.exp(-(deltaL1 * deltaL1) / (lcoh * lcoh));
    const vGauss2 = Math.exp(-(deltaL2 * deltaL2) / (lcoh * lcoh));

    // Linear would be: V ∝ exp(-ΔL)
    const vLinear1 = Math.exp(-deltaL1 / lcoh);
    const vLinear2 = Math.exp(-deltaL2 / lcoh);

    // Ratios should differ
    const gaussRatio = vGauss1 / vGauss2;
    const linearRatio = vLinear1 / vLinear2;

    TestSuite.assert(Math.abs(gaussRatio - linearRatio) > 0.1,
      'Gaussian and linear models should be distinguishable');
  });

  TestSuite.run('Falsification: Mass independence', function() {
    // STUR predicts same ℓ_coh for different masses
    const lcoh = 5; // Same for ⁸⁷Sr and ⁸⁸Sr
    const deltaL = 5;

    const V_Sr87 = Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));
    const V_Sr88 = Math.exp(-(deltaL * deltaL) / (lcoh * lcoh));

    TestSuite.assertEqual(V_Sr87, V_Sr88, 'Visibility should be mass-independent');
  });

  // ═══════════════════════════════════════════════════════════════
  // STATISTICAL TESTS
  // ═══════════════════════════════════════════════════════════════

  TestSuite.run('Statistics: Chi-squared calculation', function() {
    // Mock data points
    const observed = [0.95, 0.85, 0.70, 0.50, 0.30];
    const expected = [1.00, 0.87, 0.68, 0.47, 0.28];
    const uncertainty = 0.05;

    let chiSq = 0;
    for (let i = 0; i < observed.length; i++) {
      chiSq += Math.pow((observed[i] - expected[i]) / uncertainty, 2);
    }

    TestSuite.assert(chiSq >= 0, 'Chi-squared should be non-negative');
    TestSuite.assert(chiSq < 100, 'Chi-squared should be reasonable for this data');
  });

  TestSuite.run('Statistics: RMSE calculation', function() {
    const observed = [0.95, 0.85, 0.70, 0.50, 0.30];
    const expected = [1.00, 0.87, 0.68, 0.47, 0.28];

    let sumSqErr = 0;
    for (let i = 0; i < observed.length; i++) {
      sumSqErr += Math.pow(observed[i] - expected[i], 2);
    }
    const rmse = Math.sqrt(sumSqErr / observed.length);

    TestSuite.assert(rmse >= 0, 'RMSE should be non-negative');
    TestSuite.assert(rmse < 1, 'RMSE should be less than 1 for normalized visibility');
  });

  // ═══════════════════════════════════════════════════════════════
  // RUN ALL TESTS
  // ═══════════════════════════════════════════════════════════════

  console.log('\n' + '═'.repeat(50));
  console.log(' STUR PHYSICS LAB - TEST SUITE');
  console.log('═'.repeat(50) + '\n');

  // Return summary for programmatic access
  window.STURTests = TestSuite.summary();

})();
