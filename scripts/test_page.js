// Regression tests for the page's pure logic, run against index.html itself (no browser, no deps):
//   node scripts/test_page.js [path/to/index.html]
// Each block names the defect it guards. The functions are lifted out of the page's script by name and
// evaluated in an isolated context, so the page is tested as shipped, not a copy of its code.
const fs = require('fs'), vm = require('vm'), path = require('path');
const page = fs.readFileSync(process.argv[2] || path.join(__dirname, '..', 'index.html'), 'utf8');
const js = page.slice(page.lastIndexOf('<script>') + 8, page.lastIndexOf('</script>'));

function grab(name) {                 // `function name(...){...}` or `const name=...;` / `let name=...;`
  const re = name.replace(/[$]/g, '\\$&');
  let i = js.search(new RegExp('\\nfunction ' + re + '\\('));
  if (i >= 0) {
    i += 1; let d = 0, k = js.indexOf('{', i);
    for (; ; k++) { if (js[k] === '{') d++; else if (js[k] === '}' && --d === 0) break }
    return js.slice(i, k + 1);
  }
  const m = js.match(new RegExp('\\n((?:const|let) ' + re + '=[\\s\\S]*?;)\\n'));
  if (!m) throw new Error('not found in page: ' + name);
  return m[1];
}
const li = js.indexOf('const L={'); let d = 0, k = js.indexOf('{', li);
for (; ; k++) { if (js[k] === '{') d++; else if (js[k] === '}' && --d === 0) break }
const ctx = { console };
vm.createContext(ctx);
vm.runInContext('var ' + js.slice(li + 6, k + 1) + ';var lang="en";var dailyK=[];var etfData=null;', ctx);
const need = ['t', 'tf', '$', 'isoD', 'LAD_BANDS', 'TRIG_BAR', 'PM', 'etfSt', 'verdictAction', 'pmClampY', 'lastWeeklyClose', 'CBP_LAST', 'cbpStreak', 'ATH', 'CYCLE_LOW', 'cycleLow', 'isWeeklyClose', 'bandFired', 'LAD_ALLOC', 'trigPct'];
let missing = [];
for (const n of need) { try { vm.runInContext(grab(n).replace(/^(const|let) /, 'var '), ctx) } catch (e) { missing.push(n) } }

let fail = 0, pass = 0;
const ok = (cond, msg) => { if (cond) pass++; else { fail++; console.log('FAIL', msg) } };
if (missing.length) { console.log('FAIL missing functions:', missing.join(', ')); process.exit(1) }
const run = c => vm.runInContext(c, ctx);

// Verdict at a price between bands or under all of them must not quote the first band as "x% below" with a
// negative x (code review, Nov 10, 2026: $51K read "starts at $57,000, -12% below today").
for (const p of [74000, 60000, 51000, 47000, 43000, 36000, 30000]) {
  const s = run('verdictAction(' + p + ')');
  ok(!/-\d+%/.test(s) && !/−\d+%/.test(s), 'verdict at ' + p + ' has a negative distance: ' + s);
}
ok(/\$57,000, 23% below/.test(run('verdictAction(74000)')), 'verdict at 74000 names the $57K band');
ok(/\$50,000/.test(run('verdictAction(51000)')), 'verdict at 51000 names the next band down ($50K)');
// Probe gate (owner, Nov 21, 2026): inside the probe band the page must not say "buys now" until a completed weekly
// (Sunday) close under $57K has printed — the old price-only verdict said it on an intraday dip with zero such closes.
ok(run('verdictAction(54000)') === run('tf("hv_band_wait",t("lad")[0].t,$(57000))'), 'probe band without a weekly close under $57K waits');
{ const D = 864e5, sun = Date.UTC(2026, 10, 22);    // Sun Nov 22, 2026
  run('dailyK=' + JSON.stringify([{ ts: sun - D, close: 55000, low: 54000 }, { ts: sun, close: 56500, low: 55500 }]));
  run('var realNow=Date.now');
  run('Date.now=()=>' + (sun + 12 * 3600e3));        // Sunday noon: the weekly candle is still open
  ok(run('verdictAction(54000)') === run('tf("hv_band_wait",t("lad")[0].t,$(57000))'), 'an open Sunday candle does not fire the probe');
  run('Date.now=()=>' + (sun + D + 3600e3));         // Monday 01:00 UTC: closed at 56,500
  ok(run('verdictAction(54000)') === run('tf("hv_in",t("lad")[0].t)'), 'a completed weekly close under $57K fires the probe');
  run('dailyK=' + JSON.stringify([{ ts: sun, close: 57000.5, low: 55500 }]));
  ok(run('bandFired(0)') === false, 'a weekly close at/above $57K does not fire the probe');
  // Core and capitulation use the same gate (Nov 21 numbers review): no "buys now" in $44-50K without a weekly
  // close under $50K — the old core column needed Puell < 0.5, which today means ~$38K.
  run('dailyK=' + JSON.stringify([{ ts: sun, close: 56500, low: 55500 }]));
  ok(run('verdictAction(47000)') === run('tf("hv_band_wait",t("lad")[1].t,$(50000))'), 'core band without a weekly close under $50K waits');
  ok(run('trigPct()') === 45, 'trigger deploys only the core once the probe has fired: ' + run('trigPct()'));
  run('dailyK=' + JSON.stringify([{ ts: sun, close: 49000, low: 48000 }]));
  ok(run('verdictAction(47000)') === run('tf("hv_in",t("lad")[1].t)'), 'a weekly close under $50K fires the core');
  ok(run('trigPct()') === 0, 'nothing left for the trigger once probe and core fired');
  run('dailyK=[]');
  ok(run('trigPct()') === 65, 'trigger deploys 65% when nothing has fired');
  run('Date.now=realNow'); }
ok(run('verdictAction(30000)') === run('t("hv_none")'), 'verdict under every band says only the reserve is left');

// The now marker must stay on the drawn scale (code review: $100K drew over the ATH caption).
ok(run('pmClampY(-40)') === run('PM.top') && run('pmClampY(900)') === run('PM.bot') && run('pmClampY(200)') === 200, 'price-map now marker is clamped');

// ETF status: the confirmation card and the checklist row share one rule and one threshold
// (code review: the card was a hand-set 'off' while leg 3 and the row read the live figure).
ok(run('etfSt(1.6)') === 'on' && run('etfSt(0.2)') === 'part' && run('etfSt(-1.55)') === 'off', 'etfSt thresholds');
ok(run('etfSt(TRIG_BAR.etf)') === 'on', 'etfSt uses TRIG_BAR.etf');

// Leg 1 reads the last COMPLETED Sunday close from dailyK.
const day = 864e5, sun = Date.UTC(2026, 10, 8);       // Sun Nov 8, 2026
run('dailyK=' + JSON.stringify([{ ts: sun - day, close: 1 }, { ts: sun, close: 74851.44 }, { ts: sun + day, close: 2 }]));
const w = run('lastWeeklyClose()');
ok(w && w.d === '2026-11-08' && w.c === 74851.44, 'last weekly close is the Nov 8 Sunday candle: ' + JSON.stringify(w));
// ...and skips a Sunday candle whose UTC day has not ended (its close is still moving).
run('dailyK=' + JSON.stringify([{ ts: sun - 7 * day, close: 78354 }, { ts: sun - day, close: 1 }, { ts: sun, close: 74000 }]));
run('Date.now=()=>' + (sun + 12 * 3600e3));            // Sunday noon UTC
const w2 = run('lastWeeklyClose()');
ok(w2 && w2.d === '2026-11-01' && w2.c === 78354, 'in-progress Sunday is skipped: ' + JSON.stringify(w2));

// Leg 2's "negative N closes in a row" is derived from the run's first close, not typed: the Nov 10, 2026 pass
// typed 66 for the Nov 8 close, whose run (Sep 5–Nov 8, measured from Coinbase/Binance daily closes) is 65.
ok(run('cbpStreak({d:"2026-11-08",from:"2026-09-05"})') === 65, 'premium run Sep 5–Nov 8 is 65 closes');
ok(run('cbpStreak({d:"2026-11-11",from:"2026-09-05"})') === 68, 'premium run Sep 5–Nov 11 is 68 closes');
ok(run('cbpStreak({d:"2026-11-15",from:"2026-09-05"})') === 72, 'premium run Sep 5–Nov 15 is 72 closes');
ok(run('cbpStreak(CBP_LAST)') === 72, 'the shipped CBP_LAST (Nov 15) renders a run of 72');

// The price map's cycle low is the lowest daily LOW since the ATH, live from dailyK, not a typed constant: the
// constant read "Cycle low, Jul 1" at $57,800 after Binance printed $57,778 on Nov 20, 2026 (interim check, Nov 21).
// A lower low from before the ATH must not count.
run('dailyK=' + JSON.stringify([{ ts: Date.UTC(2024, 1, 1), close: 43000, low: 42000 },
  { ts: Date.UTC(2026, 10, 21), close: 56986, low: 56584.07 }, { ts: Date.UTC(2026, 10, 22), close: 57500, low: 57100 }]));
let cl = run('cycleLow()');
ok(cl.p === 56584.07 && cl.ts === Date.UTC(2026, 10, 21), 'cycle low tracks a new post-ATH daily low: ' + JSON.stringify(cl));
run('dailyK=[]');
cl = run('cycleLow()');
ok(cl.p === run('CYCLE_LOW.p') && cl.ts === Date.parse(run('CYCLE_LOW.d')), 'cycle low falls back to the seed without candles');

console.log(fail ? fail + ' failed, ' + pass + ' passed' : 'OK ' + pass + ' passed');
process.exit(fail ? 1 : 0);
