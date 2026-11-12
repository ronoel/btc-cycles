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
const need = ['t', 'tf', '$', 'isoD', 'LAD_BANDS', 'TRIG_BAR', 'PM', 'etfSt', 'verdictAction', 'pmClampY', 'lastWeeklyClose', 'CBP_LAST', 'cbpStreak'];
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
ok(run('verdictAction(54000)') === run('tf("hv_in",t("lad")[0].t)'), 'verdict inside the probe band says it is buying');
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
ok(run('cbpStreak(CBP_LAST)') === 65, 'the shipped CBP_LAST (Nov 8) renders a run of 65');

console.log(fail ? fail + ' failed, ' + pass + ' passed' : 'OK ' + pass + ' passed');
process.exit(fail ? 1 : 0);
