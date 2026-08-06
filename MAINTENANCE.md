# Maintenance & Update Schedule

What keeps this report accurate, who updates it (automatic vs manual), and how often.

## 1. Automatic — no action required

| Data | Source | Frequency | Where |
|---|---|---|---|
| BTC price, drawdown, cycle-4 chart lines, cycle low | Binance public API | On page load + every 60s | client-side JS |
| Price indicators (Mayer Multiple, 200D MA, Pi Cycle Top, weekly RSI, 200-week MA) | Computed from Binance daily closes | On page load | client-side JS |
| Fear & Greed | alternative.me API | On page load | client-side JS |
| Funding rate (7-day avg of 8-hourly BTCUSDT perpetual funding) | Binance Futures API (`fapi/v1/fundingRate`) | On page load | client-side JS (`fetchFunding()`) |
| On-chain metrics (Realized Price, **MVRV ratio + MVRV Z-Score**, NUPL, SOPR, Puell) | bitcoin-data.com (BGeometrics) → `data.json` + `history.json` | **Daily 06:00 UTC** | GitHub Action → `scripts/build_data.py` |
| Macro (US M2 + y/y, Fed assets, TGA, RRP, net liquidity, 10y & 2y nominal, 10y real, HY/IG OAS, broad USD index) | FRED keyless CSV → `data.json` | **Daily 06:00 UTC** | same Action |
| US spot ETF net flows (5d / 20d / 60d / YTD / cumulative / AUM) | SoSoValue → `data.json` | **Daily 06:00 UTC** | same Action |
| Live checklist rows (tagged `LIVE`, incl. funding rate, macro composite and ETF flows), macro-table rows tagged `LIVE`, on-chain floor card, 200W MA card, buy-ladder highlight, family/stage banner, expert & equal readiness, retro-calibration chart, cycle-clock & drawdown-progress thesis stats | Derived from the above | On page load | client-side JS |

**Health check (monthly):** confirm the GitHub Action is green (repo → Actions → "Update on-chain data"), that `data.json`'s `updated` field is recent, and that **`data.json`'s `stale` array is empty** — it lists any source that failed and kept its previous value. `scripts/build_data.py` never fails the build on a bad source, so a silently degraded feed shows up there and nowhere else.

**Data-pipeline facts worth not rediscovering:**
- Everything is **keyless**. `BGEOMETRICS_TOKEN` only lifts bitcoin-data.com's anonymous rate limit (**10 requests/hour** — easy to trip when testing locally) and may widen the history window.
- **FRED sends no CORS header**, so its series can never be fetched from the page; they must come through the Action. Verified 2026-08-06.
- The **SoSoValue ETF endpoint is undocumented** (`POST api.sosovalue.xyz/openapi/v2/etf/historicalInflowChart`, body `{"type":"us-btc-spot"}`). It works keyless and happens to echo any `Origin`, but it is an internal endpoint and may change without notice — which is why it is routed through the Action and why its failure only marks `etf` stale.
- **`mvrv` and `mvrv-zscore` are different endpoints.** The ratio is ~1.24 today; the Z-score ~0.39. Both are published. Do not collapse them again — that bug lived in the report for its whole life until Aug 2026.
- `history.json` (~60KB) holds the daily on-chain series and exists **only** for the retro-calibration section. If it is missing or malformed the section hides itself and nothing else breaks.
- The free history window is exactly **1,461 days**, so the calibration can reach the Nov 2022 bottom and not the Dec 2018 one. If the token ever widens that window, `calibTrace()` will pick it up automatically — check whether cycle 2 becomes scoreable.

## 2. Manual — research snapshot (tagged `research: Jul 24, 2026` in the UI)

**Frequency: every 2–4 weeks.** Tighten to **weekly** when either happens:
- we enter the projected bottom window (**Sep–Nov 2026**), or
- BTC closes below **$57K** (probe band reached), or
- a 2nd crypto-native catalyst fires (exchange failure, stablecoin depeg, >$500M exploit).

What to refresh (all live in the `L.en` / `L.pt` i18n objects in `index.html`):

| Item | i18n keys | What to look up |
|---|---|---|
| Static checklist rows | `bs` entries `puell`*, `hash`, `lth`, `resv`, `sthmvrv`, `cbp` (fields `r` + `st`) | Hash Ribbons cross status, LTH supply, exchange reserves + SSR, **STH-MVRV + short-term-holder realized price**, Coinbase Premium streak |
| Macro & flow table | `mac` — **only the rows WITHOUT a `k:` field** (fields `r` + `e`) | Fed rate path & FOMC outcomes, tariffs/legal status, recession odds, catalyst watch, geopolitics, **Strategy holdings / mNAV / BTC sales**, scheduled events, BTC-vs-equities. Rows carrying `k:` (`rates`, `netliq`, `dxy`, `credit`, `etf`) prepend a live figure — refresh only their narrative tail, never restate the number in prose |
| Polymarket card | `cvp[3]` (fields `v` + `d`) | P(BTC < $55K / $50K / $40K) for 2026, plus P(BTC tags $70K) as the market's counter-read |
| Trigger cards' current readings | `trig` (field `d`) | Coinbase Premium, ETF streak, hash ribbons, Fed pricing. Lead each with its status in bold (`FIRED` / `PARTIAL` / `NOT FIRED`) and keep the tally in `trig_n` in sync |
| Cycle-phase timeline (C4) | `PHASES.c4` const (Distribution / Early Decline / projected Capitulation dates) + phase table totals row in `renderPhases()` | Refine the C4 phase boundaries as new price action confirms them; the Capitulation segment stays `proj:true` (striped bar, "(proj.)" label, NOW marker) until the bottom is confirmed |
| Snapshot date badge | `an_asof` (EN + PT) | set to the new research date |

\* The `fed` (macro liquidity) and `etf` rows are now **fully LIVE** and need no research refresh — do not hand-edit their `r`/`st`. `puell` auto-switches to LIVE if `data.json` provides it — only its static fallback text needs the date kept honest. The `fund` (funding rate) row is normally LIVE from Binance Futures; only its static fallback text (`bs` entry `fund`, field `r`) matters when the Futures API is unreachable — keep the date honest there too.

**Procedure:** run a research pass (web search: each item above), edit the i18n arrays in `index.html`, bump `an_asof`, verify locally, commit & push.

**All three languages are now full translations.** ES stopped being an EN fallback in Aug 2026 (it was 81 of 173 keys, so the entire analysis rendered in English for Spanish readers). **EN, PT-BR and ES must all stay at key parity** — a missing key silently falls back to English and nobody notices. PT/ES values are stored `\uXXXX`-escaped; EN is mostly literal. Verify parity after any i18n change:

```
node -e "const fs=require('fs');let s=fs.readFileSync('index.html','utf8');
let i=s.indexOf('const L={'),d=0,k=s.indexOf('{',i),st=k;
while(true){if(s[k]==='{')d++;else if(s[k]==='}'){d--;if(d===0)break}k++}
const L=eval('('+s.slice(st,k+1)+')');const en=Object.keys(L.en);
for(const lg of ['pt','es'])console.log(lg,Object.keys(L[lg]).length,'/',en.length,
  'missing:',en.filter(x=>!(x in L[lg])).join(',')||'none');
for(const lg of ['pt','es'])L.en.bs.forEach((o,ix)=>{if(o.k!==L[lg].bs[ix].k||o.st!==L[lg].bs[ix].st)
  console.log('BS MISMATCH',lg,ix)});"
```

`k:`, `st:` and the `mac` `e:`/`k:` fields are **logic, not text** — they must be byte-identical across languages. Notes that contain markup (`bs_n`, `trig_n`, `s2n`) must be assigned with `innerHTML`, not `textContent`; getting that wrong renders the tags literally.

## 2b. Signal & trigger conventions

Rules that keep the checklist honest over time. **Never retro-edit a threshold because you dislike the reading it just produced** — change the spec prospectively and record it here.

This section holds *conventions*. The derivations, tested counter-arguments and data
limitations behind each conclusion go in [`ANALYSIS-LOG.md`](ANALYSIS-LOG.md); add an
entry there whenever a research pass changes a threshold, a weight or the thesis.

**Scoring structure (Aug 2026).** The headline is an **ordinal**, not a percentage: 15 signals in four families (`BS_FAM` — Valuation / Capitulation / Supply & flows / Macro), a family lights on a **strict majority** of active signals (PARTIAL counts a half), and lit-family count maps to TOO EARLY / APPROACHING / BOTTOM ZONE / CONFIRMED. Rules to preserve:
- The majority test must stay **strict (`> n/2`)**. With `>=`, a family of all-PARTIAL signals sums to exactly `n/2` and lights with nothing active — this shipped briefly and rendered "BOTTOM ZONE" on 2 of 15 active signals.
- **Both** the expert-weighted and equal-weighted scores are published, permanently. They currently agree to within ~3 points and agreed to within 1 at the 2022 bottom. If a change ever makes them diverge materially, that divergence is a finding to investigate, not a number to pick between.
- `BS_W` must still sum to **100**, now across **15** keys.
- **Every computable threshold lives in the `RULE` object** and nowhere else, because the live checklist and the retro-calibration both call it. Never inline a threshold at a call site — the whole value of the calibration is that both eras are scored by identical code.

**Latched vs live signals.** Some checklist rows are state ("is it true right now"), others are events ("has it happened this cycle"). The 200W MA row is an *event*: once a weekly close prints below the line, the signal has fired for the cycle even if price reclaims it. The row keeps rendering LIVE state — the latch lives in its tooltip and must be kept there.
- Latched so far in cycle 4: **200W MA — week of Jun 22–28, 2026 closed $59,577 vs a $62,414 200W MA** (−4.5%; first since 2022; reclaimed after).
  Figures are Binance-derived, matching what the page computes — prefer those over news-reported values from other indices.
- **Cycle-phase anchoring:** the capitulation phase is dated from the *flush*, not the low, matching C2 (2018-06-22) and C3 (2022-06-13). C4 is anchored on the Jun 22–28, 2026 breakdown week. Whenever `PHASES.c4` boundaries move, re-check that each `d` still equals its date span and that the ~140–150-day capitulation estimate still lands inside the stated window.

**Trigger changelog.**

| Date | Trigger | Change |
|---|---|---|
| Aug 6, 2026 (coherence pass) | Falsifier #6 | **Tightened before ever firing.** The deploy-anyway trigger ("reclaims Realized Price + 200W MA, 30 days, positive flows") was nearly satisfied at ~$64K with 0 of 7 core signals — price never traded below Realized Price this cycle, so the reclaim was vacuous. Now uses the thesis paragraph's own counter-scenario confirmation (weekly close &gt; ~$70K + Coinbase Premium positive + 4-week ETF ≥ $1.5B), so the same event has one confirmation, not a weak and a strong one. Old wording preserved inside the falsifier text. |
| Aug 6, 2026 (coherence pass) | Cycle clock | ~368 → **~370**: (363+376)/2 = 369.5. Arithmetic slip in the stated derivation, not a reading-driven change. |
| Aug 6, 2026 | `mvrv` row | **Bug, not a threshold change.** The pipeline had been writing the MVRV *ratio* under the `mvrv_zscore` key since inception, so a Z-score threshold was being scored against a ratio and the row read a false OFF. Both series are now fetched and displayed. Because `< 0.5` had never once been evaluated against a Z-score, the threshold was **specified** rather than retro-edited, from the measured precedent: **ACTIVE at Z < 0** (2022 bottom closed at −0.32, troughed −0.36; 2018 ≈ −0.3), **PARTIAL below 0.5**. Today's 0.39 is PARTIAL. Note this is *stricter* than a literal reading of the old text would have been. |
| Aug 6, 2026 | ETF inflows | The **v2 spec adopted Jul 24 is now in force and computed**: 4-week net ≥ +$1.5B is ACTIVE, merely-positive is PARTIAL. Under it the trigger reads **not fired** (+$0.34B) where the retired "3 consecutive positive weeks" wording had it *fired — low conviction*. The July reading stays on the record; it is not revised away. |
| Aug 6, 2026 | Checklist grew 14 → **15 signals** | Added `etf` (weight 5, live from SoSoValue) and converted `fed` from a narrative row to a **computed macro-liquidity composite** (M2 y/y accelerating · USD below 200d · real 10y below 200d; 3 of 3 ACTIVE, 2 PARTIAL). `BS_W` rebalanced to keep the sum at 100 by taking 5 points from rows the new ones partly duplicate: `sopr` 6→5, `hash` 7→6, `lth` 6→5, `cbp` 5→3. **Deliberately rejected:** adding Global M2, Fed balance sheet, real rates, credit spreads and DXY as separate rows — they are one collinear factor and would have silently taken macro to ~40% of the score. Credit spreads are kept out of the score entirely and used in the macro table as a drawdown-**depth** modifier. |
| Jul 24, 2026 | ETF inflows 3+ weeks | Fired on the letter of the spec (+$197M / +$76M / +$274M) but with ~7% of the outflow recovered. Marked *fired — low conviction*; magnitude stated inline rather than moving the goalposts. **v2 spec, applies from the next firing:** require cumulative net inflows ≥ $1.5–2B, or ≥ 25% of the preceding outflow streak, alongside the 3-week condition. |
| Jul 24, 2026 | Capitulation tranche gate | Stays strictly crypto-native, but gained a documented parallel **macro gate** (Fed hike odds repriced + DXY breaks 103 + 200W MA lost again) so an oil-shock → CPI-reacceleration path to $38–44K is not silently uncovered. |
| Jul 24, 2026 | Checklist grew 13 → **14 signals** | Added `sthmvrv` (short-term-holder MVRV, coins under 155 days). Rationale: it is the only valuation signal not diluted by permanently-held supply — ancient coins, Strategy's treasury, ETF holdings — so it reads the cohort that actually capitulates. `BS_W` was rebalanced to keep the total at **100**: it took 7 points from the aggregate signals it partly supersedes (`rp` 10→9, `nupl` 10→9, `mvrv` 8→6, `hash` 8→7, `fund` 8→7, `resv` 4→3). Readiness moved 31% → 33% at the time of the change — verify the sum is still 100 if you ever touch these. |
| Jul 24, 2026 | Capitulation gate marked **partially armed** | Strategy began selling BTC to fund preferred dividends (3,588 BTC / $216M, Jun 29–Jul 5; $1.25B authorised). That is genuine non-discretionary selling, so the `mac` catalyst row moved `m` → `h` and its wording from "not fired" to "emerging, not fired". It is a drip, not a cascade — the tranche still requires funding z < −2. Do not promote it to fired without an accelerating, forced sale. |

## 3. Event-driven — rewrite, not refresh

| Event | Action |
|---|---|
| **2nd crypto-native catalyst fires** | Update `mac` catalyst row + checklist; capitulation tranche ($38–44K) becomes actionable — reflect in thesis if bands shift |
| **Strategy escalates** (sales beyond the $1.25B programme, mNAV holding below 1, a dividend cut/suspension, or forced deleveraging) | This is the leading 2nd-catalyst candidate. Update the `Strategy / corporate treasuries` and catalyst rows in `mac`, promote the capitulation gate from *partially armed*, and re-check the counter-scenario probability in `th_p` — it is the main thing that can invalidate "the low is already in". Track: holdings, average cost ($75,476), mNAV, preferred dividend run-rate ($1.76B/yr), USD reserve, and whether weekly filings show equity raises with no BTC bought |
| **A falsifier fires** (see the "What would prove this wrong" section in `index.html`, key `fal`) | These are pre-registered and must be honoured, not reinterpreted. In particular: if a bottom is confirmed with **fewer than 8 of 15 signals ever firing**, the thresholds belong to a regime that has ended — rebuild them on damped levels and say so; do not keep scoring against 2018 values. And if the symmetric-error trigger fires (price reclaims Realized Price **and** the 200-week MA, holds 30 days, 4-week ETF flows positive), **deploy the remaining probe and core tranches regardless of the readiness reading** |
| **Bottom confirmed** (8+ checklist signals active, price reclaims Realized Price and holds) | Rewrite thesis banner (`th_*` keys) from "projected bottom" to "bottom in / accumulation"; fill Cycle 4 row in the "Post-ATH bear market" table (low, date, weeks, drawdown); retire or archive the buy ladder; in the **cycle-phase timeline** (`PHASES.c4` const) set the projected Capitulation segment's real end date and remove the `proj:true` flag (fill `d`/`r`), so the bar, NOW marker and phase table reflect the confirmed bottom |
| **Thesis invalidated** (e.g. sustained reclaim of ~$90K+ with bottom signals still inactive, or new ATH) | Re-derive the whole convergence analysis — bands and window are no longer valid |
| **Price bands/window revised by new research** | Update in ALL places at once: `LAD_BANDS` const, `lad` rows, ch2 band plugin price levels (`[57000,50000,44000,38000]` + window weeks 50–60), `th_core` value in thesis HTML, `cvp` cards, `th_p` text |
| **New halving date estimate** | `H5` const in `index.html` |
| **Window or thesis changed (any of the above)** | Also update the OG/Twitter meta descriptions in the `<head>` of `index.html` (they cite the Sep–Nov 2026 window, the $44–50K zone, the signal count **and the retro-calibration figures — 100% at the 2022 bottom vs the current reading**) and regenerate the share image: edit `og-card.html`, then run<br>`google-chrome --headless --disable-gpu --hide-scrollbars --window-size=1200,630 --screenshot=og.png og-card.html`<br>The card also carries the **checklist signal count**, so changing the number of signals requires a regeneration too. Its C4 chart line stays a static snapshot — the `now · −N%` label drifts from the live drawdown by design |

## 4. Fixed — never touch

Cycles 1–3 historical data (`D1`/`D2`/`D3` arrays, halving & bear-market tables), ATH reference ($126,296 / Oct 6, 2025 — `ATH`/`ATHD` consts), phase history.

## 5. Standing analytical cautions

Recorded so a future pass does not have to rediscover them, and does not quietly drop them.

- **The report contradicts itself and knows it.** A −65% damped target sits alongside checklist thresholds calibrated on −78%-and-deeper capitulations. If the damping thesis holds, the checklist may top out near 70% at the real low. This is falsifier #5, stated in `bs_n` in the UI. Do not resolve it by inventing damped thresholds — there is no observation to calibrate them against.
- **The −65% is an assumption, not an extrapolation.** From −85% → −84% → −78%, repeating cycle 3 gives −78% and the linear trend gives −75%; both land *below* the $35K black-swan tranche. The ladder is priced entirely for damping being right.
- **The four timing methods are not independent** — they are re-parameterisations of the same three cycle lengths. Describe their agreement as internal consistency, never as corroboration.
- **The calibration is N=1.** One confirmed bottom sits inside the free on-chain window. It is an anchor, not a validated model, and the UI says so. Do not let repeated citation harden it into more than that.
- **The checklist identifies a zone, not a date** — cycle 3 held above 80% for roughly four months. This is the standing argument for the price ladder over the calendar.
- **Verify by rendering, not by simulating.** Both scoring bugs found in Aug 2026 (the family-lighting rule, the MVRV series) were invisible in the source and obvious in the DOM:
  `google-chrome --headless --disable-gpu --no-sandbox --virtual-time-budget=25000 --dump-dom http://localhost:8931/index.html`

---
**Last research snapshot: Aug 6, 2026** · next manual refresh due: **late Aug 2026** (switch to **weekly** from September — projected bottom window)

Carry into the next pass: the **Sep 15–16 FOMC with a dot plot** (the July meeting dissented 3–0 toward a *hike*, so this is the live risk to the liquidity-turn assumption), the **Aug 12 CPI** and **Aug 7 payrolls**, the **Aug 11–13 Treasury refunding** against a drained reverse repo, and — inside the window itself — the **Mt. Gox creditor deadline on Oct 31** and the **US midterms on Nov 3**. Also re-source the Polymarket card, which went stale this pass and is labelled as such.
