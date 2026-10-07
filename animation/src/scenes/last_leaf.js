// last_leaf.js: "The Last Leaf", a 15-second cartoon (see STORYBOARD.md).
//   Shot A (0–5 s):    the last leaf on a bare tree. A gust tears it off; Clawd nearly catches it; the wind snatches it.
//                      Whip pan right.
//   Shot B (5–9.6 s):  Clawd chases it, leaps and misses by a hair; it sails away. Clawd slumps. Brush wipe.
//   Shot C (9.6–15 s): Clawd sits, sad. The leaf drifts back on its own and lands on Clawd's head. Clawd beams. Iris out.
(() => {
  const LEAF = '#B93A2E', BARK = '#6E4B3E', GRASS = '#9FA45A', FAR = '#C9A270';
  const T_B = 5.0, T_C = 9.6;
  const skyCol = t => mixCol('#F3DCA8', '#EBAA92', seg(t, 1, 14.5));   // golden hour → dusky rose
  const WARM = [LEAF, PAL.ochre];                                       // brush-wipe colours, both sides of the cut

  // ---------- wind (video time) ----------
  const GUSTS = [[2.75, .45], [4.3, 1], [T_B + 1.55, 1]];
  const gust = t => GUSTS.reduce((s, [e, a]) => { const x = t - e; return s + (x < 0 ? 0 : a * (x < .2 ? ease(x / .2) : Math.exp(-(x - .2) * 2.5))); }, 0);
  const breeze = t => .25 * Math.sin(t * 1.7) + .15 * Math.sin(t * 2.9 + 1);

  // ---------- set pieces ----------
  function sky(t) {   // screen space, behind everything
    boilSeed('sky');
    const c = skyCol(t);
    paint(rectPts(-100, -100, W + 200, H + 200), { wash: c, ink: null });
    paint(ellPts(W * .5, H * .9, W * .8, H * .5, 30, 8), { fill: mixCol(c, PAL.rose, .5), fillOp: 80, bleed: .3, tex: .5, ink: null });
    for (let i = 0; i < 3; i++) {
      boilSeed('cloud' + i);
      const x = ((hash(i + 7) * W + t * 14 * (1 + i * .4)) % (W + 700)) - 350, y = 130 + i * 105;
      paint(ellPts(x, y, 220 - i * 35, 44, 22, 6), { fill: PAL.cream, fillOp: 150, bleed: .2, tex: .5, ink: null });
    }
  }
  // distant hills; px shifts them with the camera so they scroll slower than the ground (parallax)
  function farHills(px, G) {
    for (let i = 0; i < 7; i++) {
      boilSeed('far' + i);
      const cx = -500 + i * 640 + px * .55, ry = 120 + 90 * hash(i + 40);
      paint(ellPts(cx, G - 10, 430, ry, 30, 2), { wash: mixCol(FAR, skyCol(T), .35), fill: mixCol(FAR, PAL.rose, .3), fillOp: 70, bleed: .1, tex: .5, ink: mixCol(PAL.ink, FAR, .5), sw: .6 });
    }
  }
  function ground(x0, x1, G, t) {
    boilSeed('ground');
    paint(rectPts(x0, G - 30, x1 - x0, 760, 3), { wash: GRASS, fill: mixCol(GRASS, PAL.ochre, .5), fillOp: 90, bleed: .05, tex: .6, ink: null });
    for (let a = x0; a < x1; a += 1500) inkLine([[a, G - 28], [a + 760, G - 31], [Math.min(x1, a + 1520), G - 28]], 1, PAL.ink, 'ink', .5);
    for (let gx = Math.ceil(x0 / 110) * 110; gx < x1; gx += 110) {   // grass tufts lean with the breeze and the gusts
      boilSeed('tuft' + gx);
      const h = 16 + 18 * hash(gx), lean = (breeze(t + gx * .0007) + 2.2 * gust(t - gx * .0002)) * 14, bx = gx + 40 * hash(gx + 1);
      for (const k of [-1, 0, 1]) inkLine([[bx + k * 7, G - 26], [bx + k * 11 + lean, G - 28 - h - 6 * hash(gx + k)]], .7, mixCol(GRASS, PAL.ink, .4), 'inkfine', .4);
    }
  }
  // wind made visible: curling lines that sweep across the frame (screen space)
  function windLines(t, t0, y0, n) {
    const k = seg(t, t0, t0 + .8); if (k <= 0 || k >= 1) return;
    for (let i = 0; i < n; i++) {
      boilSeed('wind' + t0 + i);
      const hx = lerp(-300, W + 700, easeOut(k)) - i * 110 - hash(i + t0) * 160, y = y0 + i * 60 + hash(i * 3 + t0) * 40, len = 340;
      const P = []; for (let j = 0; j <= 6; j++) P.push([hx - len + len * j / 6, y + 9 * Math.sin(j * 1.1 + i)]);
      P.push([hx + 26, y - 14], [hx + 10, y - 34], [hx - 10, y - 18]);   // the curl at the head
      inkLine(P, .9, mixCol(PAL.ink, skyCol(t), .45), 'inkfine', .6);
    }
  }
  // whip-pan smear: horizontal bands of the scene's colours streak across; k = 1 covers the frame (cut there)
  function whip(k, t) {
    if (k <= .01) return;
    const n = 10, bh = H / n;
    for (let i = 0; i < n; i++) {
      boilSeed('whip' + i);
      const col = i < 6 ? mixCol(skyCol(t), PAL.cream, hash(i) * .4) : mixCol(GRASS, PAL.ochre, hash(i) * .5);
      paint(rectPts(-200, i * bh - 25, W + 400, bh + 50, 5), { wash: col, washOp: 255 * clamp(k * 1.3 - hash(i + 9) * .3), ink: null });
      if (k > .3) inkLine([[-100, i * bh + bh * (.3 + .4 * hash(i + 3))], [W + 100, i * bh + bh * (.3 + .4 * hash(i + 3)) + jit(6)]], .8, mixCol(col, PAL.ink, .15), 'inkfine', .2);
    }
  }

  // The leaf: base (stem end) at (x, y); rot = 0 hangs it straight down. s = length.
  function leafPts(s) {
    const R = [], L = [], n = 9;
    for (let i = 1; i < n; i++) {
      const v = i / n, w = s * .3 * Math.pow(Math.sin(Math.PI * Math.pow(v, .8)), .9) * (i % 2 ? 1 : .82);   // serrated edge
      R.push([w, s * .12 + v * s * .88]); L.push([-w, s * .12 + v * s * .88]);
    }
    return [[0, s * .12], ...R, [0, s], ...L.reverse()];
  }
  function leaf(x, y, s, rot) {
    boilSeed('leaf');
    const sw = clamp(s / 90, .35, 1.1);
    push(); translate(x, y); rotate(rot);
    inkLine([[0, 0], [jit(1), s * .14]], sw * 1.2, PAL.ink, 'ink', 0);
    paint(leafPts(s), { wash: LEAF, fill: PAL.ochre, fillOp: 70, bleed: .08, tex: .6, ink: PAL.ink, sw });
    inkLine([[0, s * .12], [s * .02, s * .55], [0, s * .9]], sw * .7, mixCol(LEAF, PAL.ink, .5), 'inkfine', .5);
    pop();
  }

  // ---------- shot A: the last leaf ----------
  const TIP_X = 1062, branchSway = t => (breeze(t) * .3 + gust(t) * 1.2) * 6;
  const tipY = t => 345 + branchSway(t);
  function tree(t) {
    boilSeed('tree');
    const s = branchSway(t), bark = { wash: BARK, fill: mixCol(BARK, PAL.ink, .3), fillOp: 90, bleed: .05, tex: .7, ink: PAL.ink, sw: .9 };
    paint(ribbon([[590, 440], [720, 380], [880, 342 + s * .3], [1000, 336 + s * .6], [TIP_X, tipY(t)]], 26, 6), bark);   // the leaf's branch
    paint(ribbon([[880, 344], [925, 285 + s * .3], [950, 250 + s * .5]], 9, 3), bark);
    paint(ribbon([[598, 330], [520, 232 - s * .3], [430, 172 - s * .5]], 20, 5), bark);
    paint(ribbon([[600, 300], [640, 190 + s * .2], [700, 118 + s * .4]], 18, 4), bark);
    paint(ribbon([[578, 560], [470, 505 - s * .2], [380, 486 - s * .4]], 18, 5), bark);
    paint(ribbon([[560, 915], [585, 700], [575, 480], [600, 290]], 80, 34), bark);   // trunk over the branch roots
    boilSeed('fallen');   // the leaves that already fell
    [[430, 0], [700, 1], [820, 2], [300, 3]].forEach(([fx, i]) => {
      push(); translate(fx, 892 + 10 * hash(i)); rotate(-1.4 + 2.8 * hash(i + 5));
      paint(leafPts(46), { wash: mixCol(LEAF, PAL.ochre, .3 + .4 * hash(i + 2)), ink: PAL.ink, sw: .45 }); pop();
    });
  }
  // the leaf's path: hanging → torn off by the first gust → fluttering down → snatched away by the second
  const tDrop = 3.0, tSnatch = 4.3;
  function fallA(tau) {
    const e = ease(seg(tau, 0, .5));
    return [TIP_X + 80 * Math.sin(2.6 * tau), tipY(tDrop) + 260 * tau - 60 * (1 - Math.exp(-4 * tau)), lerp(0, -1.6, e) + .5 * Math.cos(2.6 * tau) * e];
  }
  function leafA(t) {
    if (t < tDrop) return [TIP_X, tipY(t), .1 * Math.sin(t * 4.3) + gust(t) * .5 * Math.sin(t * 32)];
    if (t < tSnatch) return fallA(t - tDrop);
    const [x, y, r] = fallA(tSnatch - tDrop), k = seg(t - tSnatch, 0, .6);
    return [x + 1800 * easeIn(k), y - 280 * ease(k), r + 7 * easeIn(k)];
  }

  function shotA(t, lt, dur) {
    const G = 900, u = 24, x0 = 1090;
    const [lx, ly, lr] = leafA(lt), whipK = easeIn(seg(lt, 4.7, dur));
    const [cx, cy] = kf(lt, [[0, [1062, 410]], [1.3, [1062, 415]], [2.3, [930, 610]]]);
    sky(t);
    camBegin(cx + 1100 * easeIn(seg(lt, 4.6, dur)), cy, kf(lt, [[0, 2.3], [1.3, 2.2], [2.3, 1.2]]));
    farHills(0, G);
    ground(-600, 3400, G, t);
    tree(t);

    // Clawd: hopeful below the leaf → a take when it falls → bouncing under it, arms up → a take when it's snatched →
    // a turn to the right and off running after it
    const run = seg(lt, 4.75, dur), x = x0 + 420 * run * run;
    const mood = emotions(lt, [[0, 'hopeful', { lookY: -1 }], [tDrop + .05, 'surprised', { lookY: -1 }], [3.45, 'excited', { lookY: -.9, aL: 1.3, aR: 1.3 }],
                               [tSnatch + .08, 'surprised', { lookX: 1, lookY: -.4 }], [4.62, 'determined', { lookX: 1 }]]);
    if (lt < tSnatch + .1) mood.lookX = clamp((lx - x) / 220, -1, 1);
    if (lt > 3.45 && lt < tSnatch + .08) { mood.aL += .12 * Math.sin(lt * 17); mood.aR += .12 * Math.sin(lt * 17 + 2); }   // grabby
    const facing = lt < 4.6 ? {} : lt < 4.75 ? turn(lt, 4.6, 4.75, 0, .25) : { view: 'side', walk: (x - x0) / (4 * u) };
    clawd(x, G, u, { ...mood, ...facing });

    leaf(lx, ly, 86, lr);
    const at = toScreen(lx, ly + 46);
    camEnd();
    windLines(t, 2.75, 300, 2);
    windLines(t, tSnatch, 420, 5);
    if (lt < .5) iris(...at, lerp(0, 1500, easeIn(lt / .5)));   // open on the leaf
    whip(whipK, t);
  }

  // ---------- shot B: the chase ----------
  // The near miss is timed as reads: the leaf dips into reach (0.6–1.3) → crouch → leap (1.42) → the gust lifts it
  // (1.55) so it peaks just over the arm → landing (2.0) → the leaf sails away (2.0–2.9) → only then the slump.
  const V = 560, BX0 = 300;
  const xFree = lt => BX0 + V * lt;
  function leafB(lt) {
    if (lt < 1.55) {
      const flut = 25 * Math.sin(lt * 5.5) * (1 - seg(lt, 1, 1.4));
      return [xFree(lt) + kf(lt, [[0, 380], [1.3, 140], [1.55, 90]]), kf(lt, [[0, 520], [.6, 500], [1.3, 700], [1.55, 690]]) + flut, -1.6 + .5 * Math.cos(lt * 5.5)];
    }
    const [bx, by, br] = leafB(1.55 - 1e-6), s = lt - 1.55;
    return [bx + V * s + 900 * easeIn(seg(s, 0, 1.6)), by - 330 * easeOut(seg(s, 0, .85)) - 600 * easeIn(seg(s, .85, 1.9)), br + 5 * s];
  }

  function shotB(t, lt, dur) {
    const G = 880, u = 22, tUp = 1.42, tLand = 2.0;
    const x = lt < 1.95 ? xFree(lt) : xFree(1.95) + V * .3 * (1 - Math.exp(-(lt - 1.95) / .3));
    const camX = x + kf(lt, [[0, 260], [1.9, 200], [3.0, 40]]);
    sky(t);
    camBegin(camX, kf(lt, [[0, 660], [1.5, 640], [2.4, 600], [3.2, 650]]), kf(lt, [[0, 1.3], [2.6, 1.3], [dur, 1.38]]));
    farHills(camX - 960, G);
    ground(camX - 1300, camX + 1300, G, t);

    const hop = jump(lt, tUp, tLand, 6), running = lt < 2.4;
    const mood = emotions(lt, [[0, 'determined', { lookX: 1, lookY: -.6 }], [tLand + .05, 'surprised', { lookY: -1, lookX: .7 }],
                               [2.9, 'sad', { emote: null, lookX: .4, lookY: .3 }]]);
    let pose;
    if (lt < 2.5) pose = { view: 'side', walk: (x - BX0) / (4 * u), dy: lt < tUp - .15 || lt > tLand ? -Math.abs(Math.sin((x - BX0) / (4 * u) * Math.PI)) * .5 * (running ? 1 : 0) : 0 };
    else if (lt < 2.9) pose = turn(lt, 2.5, 2.62, .25, .125);
    else pose = turn(lt, 2.9, 3.02, .125, 0);
    const reach = ease(seg(lt, 1.3, 1.45)) * (1 - ease(seg(lt, tLand, 2.3)));   // the near arm stretches up for the leaf
    const slump = .13 * ease(seg(lt, 3.1, 3.5));
    clawd(x, G, u, { ...mood, ...pose,
      dy: (mood.dy || 0) * .3 + (pose.dy || 0) + hop.dy,
      sq: (mood.sq || 0) + hop.sq + slump,
      aL: lerp(mood.aL ?? .2, 1.5, reach), aR: lerp(mood.aR ?? .2, .6, reach) });

    const [lx, ly, lr] = leafB(lt);
    leaf(lx, ly, 76, lr);
    camEnd();
    windLines(t, T_B + 1.55, 330, 4);
    whip(1 - easeOut(seg(lt, 0, .3)), t);   // the whip pan's smear clears
    boilSeed('transition');
    if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, WARM);
  }

  // ---------- shot C: it comes back ----------
  const LEAF_ON = [-.6, -8.05], tLand = 3.0;   // where the leaf sits on Clawd's head (body units), and when it lands
  function shotC(t, lt, dur) {
    const G = 900, u = 30, x = 960, s = 3.2 * u;
    sky(t);
    camBegin(kf(lt, [[0, 960], [3.95, 960], [5.0, 975]]), kf(lt, [[0, 640], [3.95, 640], [5.0, 700]]), kf(lt, [[0, 1.15], [3.0, 1.2], [3.95, 1.22], [5.0, 1.75]]));
    farHills(0, G);
    ground(-600, 2600, G, t);

    const mood = emotions(lt, [[0, 'sad', { emote: null, lookY: .7 }], [3.35, 'surprised', { lookY: -1, lookX: -.25 }], [3.95, 'happy', { lookY: -.5, lookX: -.2 }]]);
    const slump = .12 * (1 - ease(seg(lt, 3.35, 3.6))), bump = .07 * spring(lt, tLand, 7, 26);
    const o = { ...mood, sq: (mood.sq || 0) + slump + bump };
    const settle = .25 * spring(lt, tLand, 5, 16);
    if (lt >= tLand) o.draw = (uu) => leaf(LEAF_ON[0] * uu, LEAF_ON[1] * uu, 3.2 * uu, -1.9 + settle);   // now it's a hat
    clawd(x, G, u, o);

    // before it lands, the leaf is in the world, drifting down to wherever that spot on Clawd's head is right now
    const sx = 1 + (o.sq || 0) * .6, sy = 1 - (o.sq || 0), r = o.rot || 0, px = LEAF_ON[0] * u * sx, py = LEAF_ON[1] * u * sy;
    const head = [x + (o.dx || 0) * u + px * Math.cos(r) - py * Math.sin(r), G + (o.dy || 0) * u + px * Math.sin(r) + py * Math.cos(r)];
    if (lt > .9 && lt < tLand) {
      const k = seg(lt, .9, tLand), kk = 1 - Math.pow(1 - k, 1.5), tau = lt - .9, fade = Math.pow(1 - k, .8);
      leaf(lerp(330, head[0], kk) + 110 * Math.sin(2.4 * tau) * fade, lerp(-120, head[1], kk) - 16 * Math.cos(4.8 * tau) * (1 - k), s, -1.9 + r + .7 * Math.sin(2.4 * tau + .3) * (1 - k));
    }
    const eye = toScreen(x, G - 6.5 * u);
    camEnd();
    boilSeed('transition');
    if (lt < .3) brushWipe(.5 + lt / .6, WARM);
    if (lt > 4.6) {   // iris closes on Clawd and the leaf, holds, shuts
      const ir = lt < 5.0 ? lerp(1500, 330, ease(seg(lt, 4.6, 5.0))) : lt < dur - .25 ? lerp(330, 310, seg(lt, 5.0, dur - .25)) : lerp(310, 0, easeIn(seg(lt, dur - .25, dur - .03)));
      iris(...eye, ir);
    }
  }

  shots([[0, shotA], [T_B, shotB], [T_C, shotC]]);
})();
