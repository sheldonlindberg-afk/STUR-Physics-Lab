/* Research notes page: reading mode and fringe visibility. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  // ---------- reading mode (plain / technical) ----------
  function setMode(mode) {
    document.body.dataset.mode = mode;
    document.querySelectorAll("[data-set-mode]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.setMode === mode)));
    try { localStorage.setItem("stur-mode", mode); } catch (e) { /* storage unavailable */ }
  }
  let initial = "tech";
  try { initial = localStorage.getItem("stur-mode") || initial; } catch (e) { /* ignore */ }
  const q = new URLSearchParams(location.search).get("mode");
  if (q === "plain" || q === "tech") initial = q;
  setMode(initial);
  document.querySelectorAll("[data-set-mode]").forEach((b) =>
    b.addEventListener("click", () => { setMode(b.dataset.setMode); drawFringes(); }));

  // ---------- active nav link ----------
  const links = [...document.querySelectorAll(".nav a")];
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((a) => a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id));
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    document.querySelectorAll("main section[id]").forEach((s) => io.observe(s));
  }

  // ---------- fringe visibility ----------
  const sigIn = $("sig-in");
  const cv = $("fringes");
  const visibility = (s) => Math.exp(-0.5 * s * s);

  function drawFringes() {
    if (!cv) return;
    const s = parseFloat(sigIn.value);
    const V = visibility(s);
    const r = cv.getBoundingClientRect();
    if (!r.width) return;
    const dpr = window.devicePixelRatio || 1;
    cv.width = Math.round(r.width * dpr);
    cv.height = Math.round(r.height * dpr);
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = r.width, h = r.height, band = h * 0.52;
    const periods = 5.5;
    // stripes: what a screen would show
    for (let x = 0; x < w; x++) {
      const I = 0.5 * (1 + V * Math.cos((2 * Math.PI * periods * x) / w));
      const g = Math.round(255 * I);
      ctx.fillStyle = `rgb(${Math.round(g * 0.29)},${Math.round(g * 0.87)},${Math.round(g * 0.5)})`;
      ctx.fillRect(x, 0, 1, band);
    }
    // intensity curve below
    const top = band + 12, bot = h - 10;
    ctx.strokeStyle = css("--border-strong");
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    [0, 1].forEach((v) => { const y = bot - v * (bot - top); ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); });
    ctx.setLineDash([]);
    ctx.strokeStyle = css("--accent");
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x <= w; x += 2) {
      const I = 0.5 * (1 + V * Math.cos((2 * Math.PI * periods * x) / w));
      const y = bot - I * (bot - top);
      x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.stroke();
  }

  function updateVis() {
    const s = parseFloat(sigIn.value);
    const V = visibility(s);
    $("sig-out").textContent = s.toFixed(2) + " rad";
    $("r-v").textContent = V.toFixed(4);
    $("r-s").textContent = (0.5 * s * s).toFixed(3);
    $("r-e").textContent = (0.5 * s * s).toFixed(3);
    $("r-d").textContent = Math.sqrt(Math.max(0, 1 - V * V)).toFixed(3);
    $("mc-out").textContent = "";
    drawFringes();
  }
  if (sigIn) {
    sigIn.addEventListener("input", updateVis);
    document.querySelectorAll("[data-sig]").forEach((b) =>
      b.addEventListener("click", () => { sigIn.value = b.dataset.sig; updateVis(); }));
    let rt;
    window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(drawFringes, 120); });
    updateVis();
  }

  // Seeded Monte Carlo: |<exp(i phi)>| for phi ~ N(0, s^2)
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const mcBtn = $("mc-btn");
  if (mcBtn) mcBtn.addEventListener("click", () => {
    const s = parseFloat(sigIn.value);
    const n = 200000, rnd = mulberry32(1);
    let re = 0, im = 0;
    for (let i = 0; i < n; i += 2) {
      const u = Math.max(rnd(), 1e-12), v = rnd();
      const rad = Math.sqrt(-2 * Math.log(u));
      const a = s * rad * Math.cos(2 * Math.PI * v), b = s * rad * Math.sin(2 * Math.PI * v);
      re += Math.cos(a) + Math.cos(b);
      im += Math.sin(a) + Math.sin(b);
    }
    const mc = Math.hypot(re, im) / n;
    const ex = visibility(s);
    $("mc-out").innerHTML = `Monte Carlo V = <b class="mono">${mc.toFixed(4)}</b> &nbsp;vs&nbsp; e<sup>&minus;s&sup2;/2</sup> = <b class="mono">${ex.toFixed(4)}</b> &nbsp;(difference ${Math.abs(mc - ex).toFixed(4)}; statistical error &lesssim; ${(1 / Math.sqrt(n)).toFixed(4)})`;
  });
})();
