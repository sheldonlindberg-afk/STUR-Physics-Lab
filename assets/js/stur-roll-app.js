/* STUR-ROLL web app: reading mode, hero dial, simulator, charts, tomography. */
(function () {
  "use strict";
  const S = window.SturRoll;
  const $ = (id) => document.getElementById(id);
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- reading mode (plain / technical) ----------
  function setMode(mode) {
    document.body.dataset.mode = mode;
    document.querySelectorAll("[data-set-mode]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.setMode === mode)));
    try { localStorage.setItem("stur-mode", mode); } catch (e) { /* storage unavailable */ }
  }
  let initial = "plain";
  try { initial = localStorage.getItem("stur-mode") || initial; } catch (e) { /* ignore */ }
  const q = new URLSearchParams(location.search).get("mode");
  if (q === "plain" || q === "tech") initial = q;
  setMode(initial);
  document.querySelectorAll("[data-set-mode]").forEach((b) =>
    b.addEventListener("click", () => setMode(b.dataset.setMode)));

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

  // ---------- canvas helpers ----------
  function setupCanvas(cv) {
    const r = cv.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    cv.width = Math.round(r.width * dpr);
    cv.height = Math.round(r.height * dpr);
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx, w: r.width, h: r.height };
  }
  function axes(ctx, box, xTicks, yTicks, xLabel, yLabel) {
    const { l, t, r, b } = box;
    ctx.strokeStyle = css("--border");
    ctx.fillStyle = css("--muted");
    ctx.font = "12px " + css("--sans");
    ctx.lineWidth = 1;
    yTicks.forEach(([v, y, s]) => {
      ctx.beginPath(); ctx.moveTo(l, y); ctx.lineTo(r, y); ctx.stroke();
      ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillText(s, l - 6, y);
    });
    xTicks.forEach(([v, x, s]) => {
      ctx.beginPath(); ctx.moveTo(x, b); ctx.lineTo(x, b + 4); ctx.stroke();
      ctx.textAlign = "center"; ctx.textBaseline = "top"; ctx.fillText(s, x, b + 6);
    });
    ctx.strokeStyle = css("--border-strong");
    ctx.beginPath(); ctx.moveTo(l, b); ctx.lineTo(r, b); ctx.stroke();
    ctx.fillStyle = css("--muted");
    ctx.textAlign = "center"; ctx.textBaseline = "bottom";
    ctx.fillText(xLabel, (l + r) / 2, b + 36);
    ctx.save(); ctx.translate(4, (t + b) / 2); ctx.rotate(-Math.PI / 2);
    ctx.textBaseline = "top"; ctx.fillText(yLabel, 0, 0); ctx.restore();
  }
  function hline(ctx, box, y, color, label) {
    ctx.save();
    ctx.setLineDash([5, 4]); ctx.strokeStyle = color; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(box.l, y); ctx.lineTo(box.r, y); ctx.stroke();
    ctx.setLineDash([]); ctx.fillStyle = color; ctx.font = "12px " + css("--sans");
    ctx.textAlign = "right"; ctx.textBaseline = "bottom"; ctx.fillText(label, box.r - 4, y - 3);
    ctx.restore();
  }

  // ---------- hero dial ----------
  (function dial() {
    const svg = $("dial");
    if (!svg) return;
    const NS = "http://www.w3.org/2000/svg";
    const el = (tag, attrs, parent = svg) => {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      parent.appendChild(e);
      return e;
    };
    el("circle", { cx: -45, cy: 0, r: 52, fill: "none", stroke: "var(--border-strong)", "stroke-width": 2 });
    el("text", { x: -45, y: -62, "text-anchor": "middle", "font-size": 10, fill: "var(--muted)" }).textContent = "hidden field θ";
    el("text", { x: -45, y: 4, "text-anchor": "middle", "font-size": 11, fill: "var(--muted)" }).textContent = "0 → π";
    const arc = el("path", { fill: "none", stroke: "var(--accent)", "stroke-width": 5, "stroke-linecap": "round" });
    const dot = el("circle", { r: 7, fill: "var(--accent)" });
    el("circle", { cx: 55, cy: 0, r: 46, fill: "none", stroke: "var(--border)", "stroke-width": 1.5, "stroke-dasharray": "3 4" });
    el("text", { x: 55, y: -56, "text-anchor": "middle", "font-size": 10, fill: "var(--muted)" }).textContent = "polarization ×200";
    const bar = el("g", {});
    el("line", { x1: 55, y1: -38, x2: 55, y2: 38, stroke: "var(--blue)", "stroke-width": 4, "stroke-linecap": "round" }, bar);
    el("line", { x1: 55, y1: -38, x2: 55, y2: 38, stroke: "var(--faint)", "stroke-width": 1, "stroke-dasharray": "2 3" });
    const lab = el("text", { x: 55, y: 66, "text-anchor": "middle", "font-size": 12, fill: "var(--text)", "font-family": "var(--mono)" });
    function draw(th) {
      const R = 52, cx = -45;
      const x = cx + R * Math.sin(th), y = -R * Math.cos(th);
      arc.setAttribute("d", `M ${cx} ${-R} A ${R} ${R} 0 0 1 ${x.toFixed(2)} ${y.toFixed(2)}`);
      dot.setAttribute("cx", x.toFixed(2)); dot.setAttribute("cy", y.toFixed(2));
      const beta = (S.ALPHA / (2 * Math.PI)) * th * (180 / Math.PI);
      bar.setAttribute("transform", `rotate(${(beta * 200).toFixed(2)} 55 0)`);
      lab.textContent = "β = " + beta.toFixed(4) + "°";
    }
    if (reduceMotion) { draw(Math.PI - 1e-6); return; }
    let t0 = null;
    function frame(ts) {
      if (t0 === null) t0 = ts;
      const t = ((ts - t0) / 1000) % 7;           // 1 s rest, 4 s roll, 2 s hold
      const u = Math.min(1, Math.max(0, (t - 1) / 4));
      const ease = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
      draw(Math.max(1e-6, ease * (Math.PI - 1e-6)));
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();

  // ---------- simulator ----------
  const state = { logm: -30, logs: -4, k: 1, result: null };
  const fmtE = (v) => { const e = Math.floor(Math.log10(v)); const m = v / 10 ** e; return `${m.toFixed(1)}e${e}`; };

  function drawRoll() {
    const cv = $("roll-chart");
    if (!cv || !state.result) return;
    const { ctx, w, h } = setupCanvas(cv);
    const box = { l: 72, t: 16, r: w - 12, b: h - 44 };
    const half = state.k * S.HALF_DEG;
    const yMax = half * 1.18;
    const X = (z) => box.l + (1 - Math.log10(1 + z) / 4) * (box.r - box.l);   // 1e4 -> 0
    const Y = (b) => box.b - (Math.max(-0.05 * yMax, Math.min(b, yMax)) / yMax) * (box.b - box.t);
    const step = 0.05 * state.k;
    const yt = [];
    for (let v = 0; v <= yMax + 1e-9; v += step) yt.push([v, Y(v), v.toFixed(2) + "\u00b0"]);
    const xt = [[1e4, "10⁴"], [1e3, "1000"], [100, "100"], [10, "10"], [1, "1"], [0, "0"]].map(([z, s]) => [z, X(z), s]);
    axes(ctx, box, xt, yt, "redshift when the light was emitted  (earlier ← → later)", "rotation today");
    // epochs
    const mark = (z, label) => {
      const x = X(z);
      ctx.save(); ctx.strokeStyle = css("--faint"); ctx.setLineDash([2, 4]);
      ctx.beginPath(); ctx.moveTo(x, box.t); ctx.lineTo(x, box.b); ctx.stroke();
      ctx.restore(); ctx.fillStyle = css("--muted"); ctx.font = "11px " + css("--sans");
      ctx.textAlign = "center"; ctx.textBaseline = "top"; ctx.fillText(label, x, box.t);
    };
    mark(S.Z_STAR, "CMB released");
    mark(S.Z_RE, "first stars");
    hline(ctx, box, Y(half), css("--accent"), (state.k === 1 ? "α/2" : state.k + "α/2") + " = " + half.toFixed(4) + "°");
    // curve
    ctx.strokeStyle = css("--blue"); ctx.lineWidth = 2.4; ctx.lineJoin = "round";
    ctx.beginPath();
    state.result.curve.forEach((p, i) => {
      const x = X(p.z), y = Y(p.beta * state.k);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    });
    ctx.stroke();
    // CMB point
    const bx = X(S.Z_STAR), by = Y(state.result.betaRec * state.k);
    ctx.fillStyle = css("--accent"); ctx.beginPath(); ctx.arc(bx, by, 5, 0, 2 * Math.PI); ctx.fill();
  }

  function renderSim() {
    const r = state.result, k = state.k;
    const beta = r.betaRec * k, half = k * S.HALF_DEG;
    $("r-beta").textContent = beta.toFixed(4) + "°";
    $("r-ratio").textContent = (beta / half).toFixed(4);
    $("r-lands").textContent = r.lands.toFixed(4);
    $("r-zroll").textContent = r.zRoll === null ? "not yet" : r.zRoll < 10 ? r.zRoll.toFixed(1) : r.zRoll.toFixed(0);
    const v = $("verdict");
    const dev = Math.abs(beta / half - 1);
    let cls = "warn", plain, tech;
    if (r.lands < 0.9) {
      plain = "The field has not finished rolling today, so the CMB is rotated by less than the full amount. This mass is too light.";
      tech = `Roll incomplete: θ(0)/π = ${r.lands.toFixed(3)}; m is below the derived-amplitude window.`;
    } else if (r.thetaStar - 10 ** state.logs > 0.05) {
      plain = "The field started rolling before the CMB was released, so part of the rotation is missing.";
      tech = `θ(z*) − θ_i = ${(r.thetaStar - 10 ** state.logs).toFixed(3)} > 0.05: the roll began before recombination.`;
    } else if (dev < 0.03) {
      cls = "ok";
      plain = `The derived amplitude holds: the CMB is rotated by ${(100 * beta / half).toFixed(1)}% of ${k === 1 ? "α/2" : k + "α/2"}.`;
      tech = `|β/(kα/2) − 1| = ${(100 * dev).toFixed(2)}% < 3%; z_roll ≈ ${r.zRoll ? r.zRoll.toFixed(1) : "—"}.`;
    } else if (Math.abs(r.lands - 1) > 0.025) {
      plain = `The rotation is ${(100 * beta / half).toFixed(1)}% of the ideal value: the field is still swinging around its new resting point today. This mass sits at the edge of the allowed window.`;
      tech = `|β/(kα/2) − 1| = ${(100 * dev).toFixed(1)}% ≥ 3%: θ(0)/π = ${r.lands.toFixed(3)}, not yet settled at π.`;
    } else {
      plain = `The rotation is ${(100 * beta / half).toFixed(1)}% of the ideal value: the starting nudge is too large, so the field rolls less than half a turn.`;
      tech = `|β/(kα/2) − 1| = ${(100 * dev).toFixed(1)}% ≥ 3%.`;
    }
    if (k > 1 && cls === "ok") {
      cls = "warn";
      plain += ` But k = ${k} sits well above the measurements.`;
      tech += ` k = ${k} is disfavoured by the data (see pulls).`;
    }
    v.className = "verdict " + cls;
    v.innerHTML = `<span class="plain">${plain}</span><span class="tech">${tech}</span>`;
    const box = $("pulls");
    box.innerHTML = "";
    S.pulls(beta).forEach((p) => {
      const pos = 50 + Math.max(-4, Math.min(4, p.pull)) * 12.5;
      const row = document.createElement("div");
      row.className = "pull-row";
      row.innerHTML = `<span>${p.name}</span><span class="pull-track"><span class="band2"></span><span class="band1"></span><span class="mid"></span><span class="dot" style="left:${pos}%"></span></span><span class="v">${p.pull >= 0 ? "+" : ""}${p.pull.toFixed(2)}σ</span>`;
      box.appendChild(row);
    });
    drawRoll();
  }

  let timer = null;
  function compute(delay = 120) {
    clearTimeout(timer);
    $("busy").classList.add("on");
    timer = setTimeout(() => {
      state.result = S.roll(10 ** state.logm, 10 ** state.logs);
      $("busy").classList.remove("on");
      renderSim();
    }, delay);
  }
  function syncLabels() {
    $("m-out").textContent = fmtE(10 ** state.logm) + " eV";
    $("s-out").textContent = fmtE(10 ** state.logs) + " rad";
    $("k-out").textContent = "k = " + state.k;
  }
  $("m-in").addEventListener("input", (e) => { state.logm = +e.target.value; syncLabels(); compute(); });
  $("s-in").addEventListener("input", (e) => { state.logs = +e.target.value; syncLabels(); compute(); });
  document.querySelectorAll("[data-k]").forEach((b) => b.addEventListener("click", () => {
    state.k = +b.dataset.k;
    document.querySelectorAll("[data-k]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    syncLabels();
    if (state.result) renderSim();
  }));
  document.querySelectorAll("[data-preset]").forEach((b) => b.addEventListener("click", () => {
    const [lm, ls] = b.dataset.preset.split(",").map(Number);
    state.logm = lm; state.logs = ls;
    $("m-in").value = lm; $("s-in").value = ls;
    syncLabels(); compute(0);
  }));
  syncLabels();
  compute(0);

  // ---------- beta(l) chart ----------
  const LEGEND = { "1e-31": "1×10⁻³¹ eV", "3e-31": "3×10⁻³¹ eV", "1e-30": "1×10⁻³⁰ eV" };
  function drawEll() {
    const cv = $("ell-chart");
    if (!cv) return;
    const { ctx, w, h } = setupCanvas(cv);
    const box = { l: 72, t: 16, r: w - 12, b: h - 44 };
    const { ells, rows } = S.BETA_L;
    const lx = (l) => box.l + (Math.log(l / 2) / Math.log(15)) * (box.r - box.l);
    const yMax = 0.24;
    const Y = (b) => box.b - (b / yMax) * (box.b - box.t);
    axes(ctx, box, [2, 3, 5, 10, 20, 30].map((l) => [l, lx(l), String(l)]),
      [0, 0.05, 0.1, 0.15, 0.2].map((b) => [b, Y(b), b.toFixed(2) + "°"]),
      "multipole ℓ  (big patches ← → fine patterns)", "rotation β(ℓ)");
    hline(ctx, box, Y(S.HALF_DEG), css("--accent"), "α/2");
    const colors = [css("--blue"), css("--violet"), css("--warn")];
    Object.entries(rows).forEach(([m, vals], i) => {
      ctx.strokeStyle = colors[i]; ctx.fillStyle = colors[i]; ctx.lineWidth = 2.2;
      ctx.beginPath();
      vals.forEach((v, j) => (j ? ctx.lineTo(lx(ells[j]), Y(v)) : ctx.moveTo(lx(ells[j]), Y(v))));
      ctx.stroke();
      vals.forEach((v, j) => { ctx.beginPath(); ctx.arc(lx(ells[j]), Y(v), 2.8, 0, 2 * Math.PI); ctx.fill(); });
      ctx.font = "12px " + css("--sans"); ctx.textAlign = "left"; ctx.textBaseline = "middle";
      ctx.fillText("m = " + LEGEND[m], box.l + 8, box.t + 14 + i * 16);
    });
  }
  drawEll();

  // ---------- tomography ----------
  const SIG = 0.05;
  function drawTomo() {
    const i = +$("t-m").value, f = +$("t-f").value;
    const row = S.TOMO[i];
    const db = S.deltaBeta(row.own, row.rec, f);
    $("t-m-out").textContent = fmtE(row.m) + " eV";
    $("t-f-out").textContent = f.toFixed(3);
    $("t-db").textContent = (db >= 0 ? "+" : "") + db.toFixed(3) + "°";
    $("t-sig").textContent = (Math.abs(db) / SIG).toFixed(1) + "σ";
    const svg = $("numline");
    const lo = -0.25, hi = 0.07, L = 30, R = 570;
    const X = (v) => L + ((v - lo) / (hi - lo)) * (R - L);
    const ticks = [-0.25, -0.2, -0.15, -0.1, -0.05, 0, 0.05];
    svg.innerHTML =
      `<rect x="${X(-0.209)}" y="34" width="${X(-0.122) - X(-0.209)}" height="28" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"/>` +
      `<rect x="${X(-SIG)}" y="34" width="${X(SIG) - X(-SIG)}" height="28" rx="6" fill="var(--surface-2)" stroke="var(--border-strong)"/>` +
      `<line x1="${L}" y1="48" x2="${R}" y2="48" stroke="var(--border-strong)"/>` +
      ticks.map((t) => `<line x1="${X(t)}" y1="62" x2="${X(t)}" y2="68" stroke="var(--border-strong)"/><text x="${X(t)}" y="84" text-anchor="middle" font-size="12" fill="var(--muted)">${t === 0 ? "0" : t.toFixed(2)}°</text>`).join("") +
      `<text x="${(X(-0.209) + X(-0.122)) / 2}" y="26" text-anchor="middle" font-size="12" fill="var(--accent)">STUR-ROLL</text>` +
      `<text x="${X(0)}" y="26" text-anchor="middle" font-size="12" fill="var(--muted)">miscalibration</text>` +
      `<circle cx="${X(Math.max(lo, Math.min(hi, db)))}" cy="48" r="8" fill="var(--blue)" stroke="var(--surface)" stroke-width="2"/>` +
      `<text x="${X(Math.max(lo, Math.min(hi, db)))}" y="108" text-anchor="middle" font-size="12" fill="var(--blue)">Δβ = ${db.toFixed(3)}°</text>`;
  }
  $("t-m").addEventListener("input", drawTomo);
  $("t-f").addEventListener("input", drawTomo);
  drawTomo();

  // ---------- redraw on resize or theme change ----------
  let rz = null;
  const redraw = () => { clearTimeout(rz); rz = setTimeout(() => { drawRoll(); drawEll(); }, 100); };
  window.addEventListener("resize", redraw);
  window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", redraw);
})();
