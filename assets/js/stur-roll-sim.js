/*
 * STUR-ROLL roll simulator (browser + Node).
 *
 * A line-for-line port of stur_final.py step 5: the field theta obeys
 *   theta'' + (3 + dlnH/dN) theta' = (m/H)^2 sin theta,   N = ln a,
 * from z = 1e4 to today, in flat Lambda-CDM (Planck 2018). The rotation of
 * light emitted at redshift z is beta(z) = (k alpha / 2 pi) [theta(0) - theta(z)].
 * Integrator: adaptive Dormand-Prince 5(4). tests/web_sim.test.mjs checks it
 * against the Python output to 4 decimals.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.SturRoll = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const H_LITTLE = 0.6736;
  const H0_EV = 2.1332e-33 * H_LITTLE;               // H0 in eV
  const OM = 0.1430 / H_LITTLE ** 2;
  const OR = 4.18e-5 / H_LITTLE ** 2;
  const OL = 1 - OM - OR;
  const ALPHA = 1 / 137.035999;
  const Z_STAR = 1089.92;                            // recombination
  const Z_RE = 7.69;                                 // reionization midpoint
  const DEG = 180 / Math.PI;
  const HALF_DEG = (ALPHA / 2) * DEG;                // alpha/2 = 0.2091 deg
  const DATA = [
    { name: "ACT DR6 + Planck (2026)", beta: 0.277, sigma: 0.057 },
    { name: "ACT DR6", beta: 0.215, sigma: 0.074 },
    { name: "WMAP + Planck PR4", beta: 0.342, sigma: 0.0925 },
  ];

  function hubble(N) {
    const a = Math.exp(N);
    return H0_EV * Math.sqrt(OR / a ** 4 + OM / a ** 3 + OL);
  }

  function dlnH(N) {
    const a = Math.exp(N);
    const e2 = OR / a ** 4 + OM / a ** 3 + OL;
    return (-4 * OR / a ** 4 - 3 * OM / a ** 3) / (2 * e2);
  }

  // Dormand-Prince 5(4) tableau
  const C = [0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1, 1];
  const A = [
    [],
    [1 / 5],
    [3 / 40, 9 / 40],
    [44 / 45, -56 / 15, 32 / 9],
    [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
    [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656],
    [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84],
  ];
  const B5 = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0];
  const B4 = [5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40];

  function integrate(f, t0, t1, y0, rtol, atol, onStep) {
    let t = t0, y = y0.slice(), h = (t1 - t0) / 1000;
    const n = y.length;
    let steps = 0;
    while (t < t1) {
      if (t + h > t1) h = t1 - t;
      const k = [];
      for (let s = 0; s < 7; s++) {
        const ys = y.slice();
        for (let j = 0; j < s; j++) for (let i = 0; i < n; i++) ys[i] += h * A[s][j] * k[j][i];
        k.push(f(t + C[s] * h, ys));
      }
      const y5 = y.slice(), y4 = y.slice();
      for (let i = 0; i < n; i++)
        for (let s = 0; s < 7; s++) { y5[i] += h * B5[s] * k[s][i]; y4[i] += h * B4[s] * k[s][i]; }
      let err = 0;
      for (let i = 0; i < n; i++) {
        const sc = atol + rtol * Math.max(Math.abs(y[i]), Math.abs(y5[i]));
        err = Math.max(err, Math.abs(y5[i] - y4[i]) / sc);
      }
      if (err <= 1) {
        t += h; y = y5; steps++;
        if (onStep) onStep(t, y);
      }
      h *= Math.min(5, Math.max(0.2, 0.9 * Math.pow(err || 1e-10, -0.2)));
      if (steps > 2e6) throw new Error("too many steps");
    }
    return y;
  }

  /**
   * Run the roll. m: theta mass in eV. seed: starting offset theta_i (rad).
   * k: Chern-Simons level. Returns lands (theta_today/pi), beta_rec (deg),
   * z_roll (theta = pi/2 crossing, or null), and a sampled history.
   */
  function roll(m, seed, k = 1) {
    const rhs = (N, y) => {
      const H = hubble(N);
      return [y[1], -(3 + dlnH(N)) * y[1] + (m / H) ** 2 * Math.sin(y[0])];
    };
    const rtol = 1e-10, atol = Math.min(1e-13, 1e-3 * seed);
    const N0 = Math.log(1e-4), Nstar = -Math.log1p(Z_STAR);
    const hist = [[N0, seed]];
    const rec = (N, y) => hist.push([N, y[0]]);
    const yStar = integrate(rhs, N0, Nstar, [seed, 0], rtol, atol, rec);
    const yNow = integrate(rhs, Nstar, 0, yStar, rtol, atol, rec);
    const th0 = yNow[0];
    const kfac = (k * ALPHA) / (2 * Math.PI);
    let zRoll = null;
    for (let i = 1; i < hist.length; i++) {
      if (hist[i - 1][1] < Math.PI / 2 && hist[i][1] >= Math.PI / 2) {
        const [Na, ta] = hist[i - 1], [Nb, tb] = hist[i];
        const N = Na + ((Math.PI / 2 - ta) * (Nb - Na)) / (tb - ta);
        zRoll = Math.exp(-N) - 1;
        break;
      }
    }
    // thin the history to <= 600 points for plotting: beta(z_emit) in degrees
    const stride = Math.max(1, Math.floor(hist.length / 600));
    const curve = [];
    for (let i = 0; i < hist.length; i += stride) {
      const [N, th] = hist[i];
      curve.push({ z: Math.exp(-N) - 1, beta: kfac * (th0 - th) * DEG, theta: th });
    }
    return {
      lands: th0 / Math.PI,
      betaRec: kfac * (th0 - yStar[0]) * DEG,
      thetaStar: yStar[0],
      zRoll,
      curve,
    };
  }

  function pulls(beta) {
    return DATA.map((d) => ({ ...d, pull: (beta - d.beta) / d.sigma }));
  }

  /**
   * Tomography with opposite-sign domains (REFINEMENT_R7 A2):
   * beta_reio = (1 - f) beta_own + f (alpha - beta_own).
   */
  function deltaBeta(betaOwn, betaRec, fOpp) {
    const reio = (1 - fOpp) * betaOwn + fOpp * (2 * HALF_DEG - betaOwn);
    return reio - betaRec;
  }

  // Reionization-only projection (stur_final Reion, l = 2, seed 1e-4),
  // from src/checks/r2_distinct_prediction.py.
  const TOMO = [
    { m: 1e-31, rec: 0.2019, own: 0.1205 },
    { m: 2e-31, rec: 0.2144, own: 0.0679 },
    { m: 3e-31, rec: 0.2058, own: 0.0188 },
    { m: 1e-30, rec: 0.2080, own: -0.0009 },
    { m: 3e-30, rec: 0.2095, own: 0.0005 },
    { m: 1e-29, rec: 0.2091, own: 0.0001 },
    { m: 1e-28, rec: 0.2090, own: 0.0 },
  ];

  // Full beta(l) from the CLASS E-mode source (docs/PREDICTIONS.md), degrees.
  const BETA_L = {
    ells: [2, 3, 4, 6, 8, 10, 15, 20, 30],
    rows: {
      "1e-31": [0.1244, 0.1632, 0.1850, 0.2020, 0.2067, 0.2057, 0.2025, 0.2017, 0.2019],
      "3e-31": [0.0212, 0.0349, 0.0494, 0.0804, 0.0958, 0.1178, 0.1780, 0.2035, 0.2055],
      "1e-30": [0.0000, 0.0009, 0.0023, 0.0109, 0.0345, 0.0524, 0.1507, 0.2029, 0.2075],
    },
  };

  return {
    ALPHA, HALF_DEG, Z_STAR, Z_RE, DATA, TOMO, BETA_L,
    hubble, roll, pulls, deltaBeta,
  };
});
