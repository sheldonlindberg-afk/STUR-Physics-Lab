/* "From the quantum level up" page: which-path fringes and the two-diamond entanglement
   calculator. Reading mode and nav highlighting come from stur-resistance.js. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  // ---------- 1. Double slit with a which-path detector: V = |<E1|E2>| = |cos theta| ----------
  const thIn = $("wp-in");
  const cv = $("wp-fringes");

  function drawWP() {
    if (!cv || !thIn) return;
    const th = parseFloat(thIn.value) * Math.PI / 180;
    const V = Math.abs(Math.cos(th));
    const D = Math.abs(Math.sin(th));
    const r = cv.getBoundingClientRect();
    if (!r.width) return;
    const dpr = window.devicePixelRatio || 1;
    cv.width = Math.round(r.width * dpr);
    cv.height = Math.round(r.height * dpr);
    const g = cv.getContext("2d");
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = r.width, H = r.height;
    g.clearRect(0, 0, W, H);
    const accent = css("--accent") || "#4ade80";
    const muted = css("--muted") || "#8b949e";
    // intensity bars
    for (let x = 0; x < W; x++) {
      const u = (x / W - 0.5) * 12;
      const env = Math.exp(-u * u / 18);
      const I = env * (1 + V * Math.cos(2.2 * u)) / 2;
      g.globalAlpha = Math.min(1, 0.08 + 0.92 * I);
      g.fillStyle = accent;
      g.fillRect(x, 0, 1, H * 0.62);
    }
    g.globalAlpha = 1;
    // profile
    g.strokeStyle = muted;
    g.lineWidth = 1.5;
    g.beginPath();
    for (let x = 0; x < W; x++) {
      const u = (x / W - 0.5) * 12;
      const env = Math.exp(-u * u / 18);
      const I = env * (1 + V * Math.cos(2.2 * u)) / 2;
      const y = H - 8 - I * (H * 0.32);
      if (x === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
    g.stroke();
    $("wp-out").textContent = Math.round(parseFloat(thIn.value)) + "°";
    $("wp-v").textContent = V.toFixed(3);
    $("wp-d").textContent = D.toFixed(3);
    $("wp-s").textContent = (V * V + D * D).toFixed(3);
  }
  if (thIn) {
    thIn.addEventListener("input", drawWP);
    document.querySelectorAll("[data-wp]").forEach((b) =>
      b.addEventListener("click", () => { thIn.value = b.dataset.wp; drawWP(); }));
    let rt;
    window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(drawWP, 120); });
    document.querySelectorAll("[data-set-mode]").forEach((b) => b.addEventListener("click", drawWP));
    drawWP();
  }

  // ---------- 2. Two diamonds: negativity of the branch state, exact ----------
  // rho_{(ij),(kl)} = 1/4 exp(-i(phi_ij - phi_kl)) exp(-gt * ((i!=k) + (j!=l))),
  // with phi = lambda * dphi/2 on |00> and |11>, 0 on |01>, |10> (parallel geometry).
  // Negativity = -sum of negative eigenvalues of the partial transpose (Hermitian 4x4,
  // diagonalised as the equivalent real symmetric 8x8 by Jacobi rotations).
  function jacobiEig(A) {
    const n = A.length;
    const a = A.map((r) => r.slice());
    for (let sweep = 0; sweep < 60; sweep++) {
      let off = 0;
      for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += a[p][q] * a[p][q];
      if (off < 1e-24) break;
      for (let p = 0; p < n; p++) {
        for (let q = p + 1; q < n; q++) {
          if (Math.abs(a[p][q]) < 1e-300) continue;
          const th = (a[q][q] - a[p][p]) / (2 * a[p][q]);
          const t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1));
          const c = 1 / Math.sqrt(t * t + 1), s = t * c;
          for (let k = 0; k < n; k++) {
            const akp = a[k][p], akq = a[k][q];
            a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq;
          }
          for (let k = 0; k < n; k++) {
            const apk = a[p][k], aqk = a[q][k];
            a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk;
          }
        }
      }
    }
    return a.map((r, i) => r[i]);
  }

  function negativity(dphi, gt) {
    const ph = [dphi / 2, 0, 0, dphi / 2];          // |00>, |01>, |10>, |11>
    const bits = [[0, 0], [0, 1], [1, 0], [1, 1]];
    const re = [], im = [];
    for (let a = 0; a < 4; a++) {
      re.push([]); im.push([]);
      for (let b = 0; b < 4; b++) {
        const d = (bits[a][0] !== bits[b][0]) + (bits[a][1] !== bits[b][1]);
        const amp = 0.25 * Math.exp(-gt * d);
        re[a].push(amp * Math.cos(-(ph[a] - ph[b])));
        im[a].push(amp * Math.sin(-(ph[a] - ph[b])));
      }
    }
    // partial transpose on the second qubit
    const idx = (i, j) => 2 * i + j;
    const pr = [], pi = [];
    for (let a = 0; a < 4; a++) { pr.push([0, 0, 0, 0]); pi.push([0, 0, 0, 0]); }
    for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++)
      for (let k = 0; k < 2; k++) for (let l = 0; l < 2; l++) {
        pr[idx(i, l)][idx(k, j)] = re[idx(i, j)][idx(k, l)];
        pi[idx(i, l)][idx(k, j)] = im[idx(i, j)][idx(k, l)];
      }
    // real 8x8 embedding [[Re, -Im], [Im, Re]]: each eigenvalue appears twice
    const M = [];
    for (let a = 0; a < 8; a++) {
      M.push([]);
      for (let b = 0; b < 8; b++) {
        const ra = a % 4, rb = b % 4;
        if (a < 4 && b < 4) M[a].push(pr[ra][rb]);
        else if (a < 4) M[a].push(-pi[ra][rb]);
        else if (b < 4) M[a].push(pi[ra][rb]);
        else M[a].push(pr[ra][rb]);
      }
    }
    const ev = jacobiEig(M);
    let neg = 0;
    ev.forEach((e) => { if (e < -1e-12) neg -= e; });
    return neg / 2;
  }

  const lamIn = $("lam-in"), gtIn = $("gt-in");
  const DPHI = 2.187;            // design A entangling phase (GRAVITY_ENTANGLEMENT.md)

  function updateLam() {
    if (!lamIn || !gtIn) return;
    const lam = parseFloat(lamIn.value), gt = parseFloat(gtIn.value);
    const dp = lam * DPHI;
    const N = negativity(dp, gt);
    $("lam-out").textContent = lam.toFixed(2);
    $("gt-out").textContent = gt.toFixed(2);
    $("q-dphi").textContent = dp.toFixed(3) + " rad";
    $("q-conc").textContent = Math.abs(Math.sin(dp / 2)).toFixed(3);
    $("q-neg").textContent = N.toFixed(4);
    $("q-verdict").textContent = N > 1e-6 ? "entangled" : "not entangled";
    $("q-verdict").className = N > 1e-6 ? "ok" : "bad";
  }
  if (lamIn) {
    [lamIn, gtIn].forEach((el) => el.addEventListener("input", updateLam));
    document.querySelectorAll("[data-lam]").forEach((b) =>
      b.addEventListener("click", () => { lamIn.value = b.dataset.lam; gtIn.value = b.dataset.gt; updateLam(); }));
    updateLam();
  }
})();
