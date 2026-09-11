# Analysis Log

Dated record of the analytical work behind the report: what was found, how it was
verified, and what changed as a result. Newest first.

**Why this file exists.** The report's credibility rests on not quietly retro-editing
thresholds and conclusions. That only works if there is a durable record of what was
concluded, when, and on what evidence — including findings that never reached the UI
and calculations that only became a single tooltip sentence.

**Where knowledge lives:**

| File | Holds |
|---|---|
| `index.html` (i18n objects + `?` tooltips) | the conclusions, thresholds and methodology as the reader sees them |
| `MAINTENANCE.md` | how to keep it accurate: refresh cadence, per-key checklists, signal conventions, trigger changelog, event-driven rewrite rules |
| **`ANALYSIS-LOG.md`** (this file) | why the conclusions are what they are: the calculations, the numbers behind them, rejected hypotheses, data limitations |
| git history | the diffs, one commit per analytical change, with the reasoning in the message |

Rule of thumb: a **conclusion** goes in `index.html`; a **procedure or convention**
goes in `MAINTENANCE.md`; the **derivation, the counter-argument you tested, or the
thing you decided *not* to change** goes here.

---

## 2026-09-11 — CPI day: a September hike went from coin-flip to priced, ETFs bled three sessions, and the provider went backwards

Same-day check (~13:30–14:30 UTC), not a research pass. `an_asof` stays Sep 7; no `index.html`
row edited; no threshold or trigger touched.

**Pipeline defect, found first because it changes what the page shows.** The Sep 11 06:14 build
published `realized_price`, `mvrv`, `nupl` and `sopr` dated **Sep 4**, after the Sep 10 builds had
them at **Sep 9**, and `history.json` shrank 1,483 → 1,478 days on those four series. Cause is
provider-side: bitcoin-data.com `/v1/sopr` fetched at ~14:00 UTC returns 1,455 rows, 2022-09-11 →
**2026-09-04**, with Sep 2–4 identical to what we stored — the tail was withdrawn, not restated.
Two builder bugs turned that into data loss: `extend_series` ended the merged series at
`max(new)`, and `data.json` took each series' latest from the fresh fetch unconditionally. The
page did say so (`feed stale — showing 2026-09-04`, via the 3-day freshness rule), so the reader
was not misled about age; the five history days were simply deleted. Fixed in
`scripts/build_data.py`: both ends of `extend_series` take the wider series (the start had the
mirror bug — a token-widened window starting earlier than `history.json` would have lost its new
head, and a fresh series wholly *before* the stored one came back **empty**, `v: []`); a new
`merge_latest()` never moves a reading backwards and marks `onchain` stale when the source
regresses, as the module docstring already promised. `scripts/test_build_data.py`: 3 tests, all
pass on the fix, **all 3 fail on the old code** (checked with `git stash`). Restoring Sep 5–9 is a
re-merge of `0df559b:history.json` with the current file through the fixed `extend_series` →
1,483 days on all four, tails back to Sep 9 (dry run only; not applied in this entry).

**Readings, verified by rendering** (Chrome headless, 06:14 data + live Binance): **TOO EARLY,
0 of 4 families lit** — Valuation 0/4, Capitulation 0 + 3 PARTIAL, Supply & flows 1 + 2 PARTIAL,
Macro 0 + 1 PARTIAL. The 21% headline is §5's noise case twice over: SOPR is the stale Sep 4 1.004
and Puell 0.8894 sits 0.0106 under its bar.

**Price.** Sep 10 closed **$76,568.72** (−2.22%). Sep 11: low **$76,047** in the 12:00 UTC hour (CPI
at 12:30), then **$79,4xx** by 14:00 (3,531 and 2,452 BTC in those two hours against ~300–500
typical). CoinDesk's live blog has the immediate reaction as a dip to $76.7K erased within minutes;
the extension to $79K is not explained by any source retrieved — oil falling on Sep 11 is
coincident, not established as the cause. Bounce peak unchanged at **+42.4%** ($82,300, Sep 3); gap
to the +45.7%/~$84.2K marker still 3.3 points.

**Falsifier #6, four days before the Sep 14 window.** Leg 1: Sep 7–13 candle in progress at ~$79.3K,
far above ~$70K. Leg 2 moved **away**: raw premium **−0.0420%** on the Sep 10 close (adjusted
−0.0020%), the widest of the window, after −0.0287% Sep 9; no positive raw close since Sep 4. Leg 3
still fires but is weakening: SoSoValue has Sep 9 **−$120.24M** and Sep 10 **−$282.56M** — three
straight outflow sessions, −$449.45M — and `etf.d20` fell **3.54 → 3.19**. The +$23.05M Sep 9 figure
carried in news (Sep 10 entry) is contradicted by the source; so is a MEXC-attributed "+$757M" for
Sep 10. `d5` +$0.46B is almost all Sep 3's +$730.87M, which rolls off with the next session. Base
case for Sep 14: **2 of 3 a fourth time**, on leg 2.

**Macro.** August CPI (CoinDesk): headline 0.4% m/m / 3.4% y/y, in line; **core 0.3% m/m vs 0.2%**,
2.4% y/y in line — the Sep 10 "core consensus unverified" item is closed. Polymarket September FOMC:
**+25bp 80.5% / hold 18.5%** (from 53.5% / 45.5% on Sep 10); CoinDesk puts futures at ~23bp, i.e.
essentially fully priced. 2-year +6bp to 4.61% on the print. FRED 10-year **4.83 on Sep 9**, a new
`hi2y` again; the tape was ~4.95% on Sep 10 (Bloomberg, "highest since 2023"). Brent ~$108 on Sep 10
on Houthi–Saudi escalation (EnergyConnects), falling Sep 11 (CNBC headline; body not retrieved;
aggregator levels inconsistent, $103.78–$106.74). Treasury's Sep 10 buyback took **$5.19B of the $6B
max** on $10.5B offered — the carry item from Sep 10 is closed. Capitulation tranche's macro gate:
hike-repricing leg now plainly met; dollar leg not (`DTWEXBGS` Sep 4 print still under its 200-day);
200W MA not lost. 1 of 3.

**Other.** Liquid: blocks resumed Sep 10 (Elements v23.3.4, Sep 9), peg-outs still disabled, 598.5 BTC
outstanding, Blockstream refusing the ransom (The Block, Sep 11) — under the $500M bar, no gate moves.
Strategy: preferred buyback raised to $2B (TechTimes, Sep 8), no BTC purchase found Sep 8–11. No
Anthropic public S-1 found. Polymarket BTC (Gamma API, ~14:00 UTC): ↓$60K 27.5%, ↓$55K 18.5% →
no-new-low **~76.5%** (flat vs ~77% Sep 7); ↑$85K 64.5%, ↑$90K **45.5%** (49.5% Sep 7). F&G 69 → 56.
Funding 7d +0.0044%/8h. mempool.space hashrate 30d/60d +0.76%, next retarget est +3.03%.

**Counter-scenario not re-scored** — that is the Sep 14 pass's call. The ledger this week leans
against it (premium further from positive, ETF flows reversing, a hike becoming certain) while price
and the prediction market held.

---

## 2026-09-10 — The headline moved 3 points on a row whose threshold sits inside its own daily noise

Not an adjudication and not a research pass — a same-day check of what changed since the Sep 9
entry, prompted by "how did the BTC and ETH ETFs do today, update the data, and did anything happen
that could move the price?". `an_asof` stays at Sep 7 and **no `index.html` row was edited**.

**`data.json` rebuilt at 03:25 UTC, `stale` empty.** On-chain advances to **Sep 9**: Realized Price
$52,760.15 → **$52,794.62**, MVRV-Z 0.8725 → **0.8495**, MVRV 1.4873 → **1.4808**, NUPL 0.3276 →
**0.3247**, SOPR 1.0022 → **1.0034**, Puell 0.8901 → **1.0825**, STH-MVRV 1.10 flat, STH cost basis
$70,955.89 → **$71,088.01**. Macro advances to **Sep 8**: the nominal 10-year prints **4.80**, and
because `hi2y` stood at 4.79 the build **reset the two-year high in the report's own series** — the
thing the Sep 9 carry list said tonight's FRED print might do, now done. The 2-year is 4.39, the
real 10-year 2.43 against a 2.47 high, `DTWEXBGS` unchanged at 118.0732 and still 1.18% under its
200-day. Net liquidity, M2 and HY OAS unmoved. **The ETF block did not advance: `etf.d` still reads
2026-09-08**, `d20` +$3.54B — see the ETF section below. `history.json` grew by exactly one day on
all eight series with the 2022-08-19 head intact.

**The finding of this pass, and it is about the instrument rather than the market.** Rendering the
page against three consecutive builds, holding today's price constant, gives **18% → 21% → 18%
ready** for the Sep 7, Sep 8 and Sep 9 on-chain data. Every point of that swing is one row: **Puell
0.9389 (NOT YET) → 0.8901 (PARTIAL) → 1.0825 (NOT YET)**, crossing its own 0.9 PARTIAL bar and
crossing back. Nothing else changed status; families read 0 of 4 lit at all three builds and the
stage stays TOO EARLY. Measured over the series itself, that is not an accident: over the last 30
days Puell has **mean 0.8994** — sitting *on* the bar — with **σ 0.1188** and a **median absolute
one-day move of 0.0647**, and it changed status **9 times in 30 days**; over 365 days, 52 times.
**SOPR is in the same position from the other side**: at 1.0034 it is **0.0016** from its 1.005 bar
while its median one-day move is **0.0036**, more than twice the remaining distance. So two of the
fifteen rows currently sit inside a single day's noise of their own thresholds, and together they
carry 11 of the 100 weight points.

This is recorded, not acted on. **No threshold was changed and none should be changed on this
evidence** — §2b's rule is that a threshold is never retro-edited because of the reading it just
produced, and 0.9 was specified long before this week. What the measurement establishes is narrower:
**a same-day reading of the headline percentage is not information when the marginal row is Puell.**
The daily entries should quote the family count and the stage, which did not move, rather than the
percentage, which moved 3 points on noise; that is now a bullet in `MAINTENANCE.md` §5. If the
ladder owner ever wants the percentage to be day-to-day meaningful, the prospective fix is to score
Puell on a smoothed value — its 7-day mean, say — rather than the daily print. That would be a spec
change, decided in advance of a reading, with the derivation logged here and the calibration re-run;
it was not made today.

**Correction to the Sep 9 entry.** It called SOPR "the checklist's single PARTIAL" (the carry list in
`MAINTENANCE.md` said "still the only PARTIAL"). On the Sep 8 build both were quoting, **Puell at
0.8901 was also PARTIAL** — the entry listed the 0.9389 → 0.8901 move without noticing it had crossed
the bar. That build carried **six** PARTIAL rows (SOPR, Puell, Hash Ribbons, LTH supply, exchange
reserves, macro composite) against one ACTIVE (ETF), and its headline was 21%. Today's build carries
five, Puell having dropped out.

**ETF flows — and the reason this section is shorter than the question asked for.** The
question was about "today", meaning the Sep 9 US session. **SoSoValue does not have it.** Queried
directly at 03:5x UTC on the same undocumented endpoint `build_data.py` uses
(`POST api.sosovalue.xyz/openapi/v2/etf/historicalInflowChart`), the latest session in **both**
`us-btc-spot` and `us-eth-spot` is **2026-09-08**. That is the structural lag the 19:00 UTC run was
added for, seen from the other side of it: the Sep 9 session will land in the 06:00 or 19:00 run
today. Web coverage does carry provisional Sep 9 figures — a BTC net **inflow of ~$23.05M** (IBIT
+$169M, ARKB −$72.29M) and an ETH net **inflow of ~$44.16M** (all of it ETHA), both attributed to
the SoSoValue dashboard — but they are single-sourced, the API contradicts them by omission, and the
BTC per-fund figures given do not reconcile to the stated total. **They are not written into
anything and did not adjudicate anything.**

What the source does support, as of the **Sep 8** session:

| | US spot BTC | US spot ETH |
|---|---|---|
| Sep 8 net flow | **−$46.65M** | **−$24.29M** |
| 5 sessions | +$0.72B | +$0.11B |
| 20 sessions | **+$3.54B** | +$1.73B |
| 60 sessions | +$2.03B | +$1.98B |
| Cumulative net inflow | +$55.57B | +$13.17B |
| Net assets | $99.5B | $15.72B |

The BTC column is what `data.json` publishes. **The ETH column is computed here from the same
endpoint and is not a project series** — ETH is not tracked in `data.json`, is not in `CORE`, and
nothing in the checklist scores it; it is reported because it was asked for. Wiring it up would be
the four-edit change §2b describes plus a `CORE` question nobody has asked, and was not started.

**This resolves a disagreement the research surfaced.** Coverage of the Sep 8 ETH session carried
three incompatible totals — −$24.29M in headlines, −$96.69M attributed to SoSoValue in body text,
and a per-fund breakdown summing to ≈−$106.5M. The endpoint says **−$24.29M**, so the headline
figure is the one on this source and the other two are not reproducible from it.

Two notes on reading the table. **Sep 7 was Labor Day** — there is no session, which is why "the
first outflow day in five sessions" on Sep 8 counts Sep 1, 2, 3, 4 and 8. And **`etf.d20` will move
when Sep 9 lands**: the window is rolling, so the direction depends on which day rolls off (around
Aug 11) as much as on Sep 9 itself. Leg 3 clears its +$1.5B bar by a wide enough margin that this is
not in doubt for Sep 14, but the published figure will not stay 3.54.

**Same-source deltas, Sep 9 → Sep 10** (measured 03:25–03:50 UTC, same sources as the Sep 9 entry).
**The Sep 9 bounce did not hold.** Binance `BTCUSDT` closed Sep 9 at **$78,306.43**, −0.19% on the
day, after trading $77,770–$79,760 — the Sep 9 entry caught it intraday at $79,480.93 and +1.31%,
and it gave all of that back by the close. **−38.0% from the ATH**, **+35.5%** above the Jul 1
intraday low ($57,800.19). The bounce's peak-to-peak measurement is **unchanged at +42.4%** (Jul 1
low → Sep 3 high $82,300), so the gap to the +45.7% 2018 precedent stays **3.3 p.p.** — no new high
printed, and per §5 that comparison, not the day's percentage, is the measurement that speaks to the
bottom. The weekly candle in progress (Sep 7–13) opened $80,341.83 and sits at $78,306.61: leg 1 of
the deploy trigger clears with room. Funding 7d +0.0048% → **+0.0047%/8h** (last print +0.0036%).
Fear & Greed 66 → **69**, back to the Sep 8 level, still Greed. Next difficulty retarget re-estimated
+2.07% → **+2.80%** at 31.4% of the epoch, dated **Sep 19 11:55 UTC** — hashrate accelerating again,
the direction the Hash Ribbons row already reads as PARTIAL.

**Coinbase Premium, leg 2 of the deploy trigger: it went the wrong way.** Raw daily close **−0.0287%
on Sep 9**, against −0.0111% on Sep 8 — **the widest negative raw close of the Sep 7–13 window so
far**, wider than Sep 7's −0.0253%. USDT-adjusted **+0.0003%**, barely positive and not the
adjudicating convention. The method reproduces the Sep 6 (−0.0034%), Sep 7 (−0.0253%) and Sep 8
(−0.0111%) figures the last two entries published, which is the check that it is the same
measurement. The Sep 10 day in progress is worse still at −0.0828% raw. **Four days to the Sep 14
00:15 UTC adjudication: legs 1 and 3 clear, and leg 2 has moved away from its bar rather than
toward it.**

**Polymarket** (Gamma, `what-price-will-bitcoin-hit-before-2027`, `closed:false`, 03:40 UTC):
↓$70K 54.5 → **55.5**, ↓$65K **38.5**, ↓$60K flat at **25.5**, ↓$55K flat at **17.5**, ↓$50K
**14.5**, ↓$45K **8.5**; ↑$85K 69 → **64.5**, ↑$90K 49 → **45.5**, ↑$95K **28.5**. The downside rungs
below $60K did not move at all while the upside rungs gave back 3.5–4.5 points — the market marked
down the bounce without marking up the bottom.

**Macro and events, Sep 9–10.** Sourcing note: the research pass that produced these was told to
collect rather than conclude, and several items came back with the disagreements intact. They are
carried that way.

- **Oil stayed through $100.** Brent **$100.71** on Sep 9 (TradingEconomics, +2.85% on the day) and
  above $101 in Asian trade Sep 10 (Bloomberg, Sep 10 dateline; CoinDesk Daybook Sep 9 has "above
  $101, up 2% over 24 hours"). WTI is **not resolved** — $97.19 and $96.70 from two contexts, no
  single settle corroborated twice.
- **The driver has a second track the Sep 8–9 entries did not name.** CNBC's Sep 9 headline is
  "Brent crude tops $100 as **U.S.-Iran tit-for-tat strikes** stoke oil supply worries"
  (`cnbc.com/2026/09/09/oil-prices-today-wti-brent-us-iran-hormuz-attacks.html`); the body was not
  fetched (CNBC 403s). The report already carries the Hormuz war in its narrative rows, so this is
  background rather than a new mechanism — but the last two entries attributed the oil move to the
  Sep 8 Houthi strikes alone, and at least one Sep 9 outlet attributes it to the Iran–US exchange.
  **No row was edited on a headline.** For scale, and *not* as a Sep 9 delta: Al Jazeera's Aug 27
  headline reports **Hormuz traffic down ~95%** from ~100 ships/day pre-war; search synthesis around
  it adds Gulf crude exports ~9M bpd against ~17M in 2025 and **direct via-strait crude ~2.2M bpd**,
  neither traced to a fetched article. Those last two are different measures, and a summary that runs
  "9M → under 2M" conflates them.
- **"Saudi retaliation" is not supportable and the Sep 8 entry's claim should be treated as
  withdrawn.** Everything found traces to Houthi spokesmen — 32 strikes (Amer, via AP/KSAT, Sep 9),
  54 and 121 in other Houthi-attributed accounts — plus a coalition statement that it "will take all
  necessary operational measures to deter the terrorist Houthi militia" (Al Jazeera, Sep 8). AP:
  "Saudi authorities didn't immediately respond to a request for comment." **No independent
  confirmation of a Saudi retaliatory strike.** The Sep 9 entry flagged this; it now resolves
  against the Sep 8 wording.
- **The Treasury buyback conflation is resolved, and it went the other way from the carry note.**
  `sb0607` is a **policy floor**: "This change is effective September 9, 2026 and will be in effect
  for the remainder of this refunding quarter (through November 4, 2026)", doubling operations from
  $2B to at least $4B, with no operation date given. Separately, **Treasury announced on Sep 9 a
  buyback of up to $6B in 10–20y nominals to be conducted Sep 10** — announced Sep 9, not conducted
  Sep 9. So "the first enlarged Treasury buyback on Sep 9" was indeed a conflation of an effective
  date with an operation date, and the operation is **today**. Reporting ties the yield move to it:
  TradingEconomics has the 10-year "around 4.85% on Thursday" citing "Treasury buyback announcements
  ($6 billion, triple the usual amount)" among the drivers. The $6B figure is search-synthesis
  sourced; **the TreasuryDirect results page was not published yet and was not read.**
- **The 10-year kept climbing.** ~**4.83%** Sep 9 and ~**4.85%** Sep 10 on the tape, against the
  4.786% close / 4.812% intraday high of Sep 8. `data.json` carries the FRED print at 4.80 with
  `hi2y` reset to match; the tape is above the series. The 2-year could not be isolated for Sep 9
  separately from Sep 8's 4.39.
- **Equities fell again.** S&P **7,636.36** (−0.48%), Nasdaq **26,253.34** (−0.64%), Dow
  **52,380.66** (−0.77%), two sources in agreement, "as rising Treasury yields and oil prices
  continued to rattle investors". The S&P is now **~1.6% under the 7,757.64 record** the
  `Equities divergence` row quotes — a row untouched since Aug 19, which widens the case for the
  Sep 14 pass to reach it.
- **Liquid Network: confirmed, and the date in the last two entries is wrong.** The exploit was
  **Sep 6, 2026**, not Sep 7 or Sep 8 — `index.html` says Sep 7. TRM Labs puts the drain at ~**$319M**
  and the return at 85%. The ~86% backing figure the Sep 9 entry single-sourced is now corroborated:
  ~**3,597 BTC** in the identified reserve against ~**4,200 L-BTC** outstanding, ~**598.5 BTC
  (~$47M) still outstanding**, the network **still paused** with deposits and withdrawals halted,
  and **no full technical post-mortem published**. So the Sep 8 entry's "closed" was the optimistic
  reading and the Sep 9 entry was right to reopen it. It stays **under the $500M 2nd-catalyst bar**
  either way, so no gate moves.
- **August CPI, Sep 11, 8:30 ET.** Release date and time confirmed twice. Headline consensus
  **3.4% y/y / 0.4% m/m** confirmed on 2026 sources (Nowflation, which also carries its own 3.36%
  call; Kiplinger). **The 2.4% core consensus this report carries was not verified** — no sourced
  core figure was found this pass. It is not contradicted either; it is simply unconfirmed, and the
  Sep 9 entry's dissolved 2025-article conflict does not cover it.
- **Fed pricing is flat, and the two markets disagree.** Polymarket September hike **53.5%**
  (unchanged from Sep 9), hold 44.5% → **45.5%**, read off `fed-decision-in-september-762`. CME
  FedWatch was **58.7%** on Sep 7; one outlet frames the futures-implied figure as low as 32%. A
  5–6 point prediction-market/futures divergence is itself the finding; nothing here moves the
  `Fed` row. **No Fed speaker on Sep 9 or Sep 10** — Waller on Sep 3 is still the last word, so the
  Sep 11 CPI remains the input his conditional rule points at.
- **Strategy: nothing.** No 8-K, purchase, sale or dividend news dated Sep 9–10. Two stories that
  surfaced are older and do not conflict with the Sep 8 8-K: the 4,603 BTC purchase is the Sep 2
  report of an Aug 24–30 buy, and Phong Le's "minuscule" defence of a 7,000 BTC sale is a Sep 1
  Bloomberg interview about a sale predating the Aug 31–Sep 7 window.
- **No crypto-native loss event above the $500M bar on Sep 9–10.** Liquid (~$319M, Sep 6) remains
  the largest and is under it. Liquidation totals disagree across sources again — $264M (Sep 8,
  verified date), $196M, and a $231M rolling-24h snapshot near query time with BTC $60.3M / ETH
  $36.9M. **None adopted**, as on Sep 8.
- **ETH, for context.** Closed ~**$2,507** Sep 9 in a ~$2,486–$2,560 range. Bitwise amended its ETH
  ETF S-1 for staking mechanics (Sep 7); BlackRock's staked-ETH ETHB held ~$851M in late August at a
  ~1.72% 30-day rate. None of this touches the report, which does not track ETH.

**Read.** The tape and the inputs point the same way today, which is the change from Sep 9, when they
pointed opposite ways: the bounce gave back its gain into the close, sentiment is flat, the premium
widened negative, upside prediction rungs came off 3.5–4.5 points, equities fell a second day, and
oil and the long end both held their highs. Nothing crossed a threshold. Stage TOO EARLY, 0 of 4
families lit, one ACTIVE row, ladder unfilled.

**Not changed:** thresholds, weights, `BS_W`/`BS_FAM`/`BS_SPEED`, the ladder, probabilities, the
counter-scenario at 40%, every `mac` row, `an_asof`, and every `index.html` string. **Not checked
this pass:** Hash Ribbons state beyond the difficulty estimate, LTH supply, exchange reserves, the
`Trade & tariffs` and `Equities divergence` narrative rows, the core-CPI consensus, and the
TreasuryDirect result of today's $6B operation.

---

## 2026-09-09 — Tape quiet, inputs loud: oil through $100, and a stale checkout corrected

Not an adjudication and not a research pass — a same-day check of what changed since the Sep 8
entry, prompted by the question "what are the next events, and did anything move?". `an_asof` stays
at Sep 7 and **no `index.html` row was edited**; what this entry carries is the delta set, four
items that read against what the report currently says, and one conflict that dissolved on checking.

**Same-source deltas, Sep 8 → Sep 9** (measured 12:32–12:40 UTC, the same sources the Sep 8 entry
used): BTC $78,455.80 close → **$79,480.93** intraday (+1.31%), day range $78,455.79–$79,760,
**−37.1% from the ATH**, +37.5% above the Jul 1 low, day 338 of ~370 on the cycle clock. The weekly
candle in progress (Sep 7–13) opened $80,341.83 and sits at $79,507 — leg 1 of the deploy trigger
(> ~$70K) would fire with room. Coinbase Premium
raw daily closes: Sep 6 −0.0034%, Sep 7 −0.0253%, **Sep 8 −0.0111%** — the method reproduces the
Sep 6 and Sep 7 figures the last two entries published, which is the check that it is the same
measurement. Funding 7d +0.0049% → **+0.0048%/8h** (last print +0.009%). Fear & Greed 69 → **66**,
still Greed. Polymarket ↓$70K 57 → **54.5**, ↓$60K flat at 25.5, ↓$55K 20.5 → **17.5**, ↑$85K
67.5 → **69**, ↑$90K 45 → **49**; the low-is-in interpolation at $57.8K moves ~77% → **~78%**.
September hike 54.5% → **53.5%** (hold 44.5%) on the same Gamma event; October hike 30.5%. Next
difficulty retarget re-estimated **+3.7% → +2.07%** at 26.7% of the epoch, dated Sep 19 14:20 UTC.
**Correction made during this pass:** it was first written up against a stale local checkout and
said `data.json` was still the Sep 8 19:10 build with the checklist unchanged "by construction".
It is not — the **06:14 UTC Action ran and did move the scoring inputs**, and the claim was wrong
before it was corrected. The build carries every on-chain series forward to **Sep 8**: Realized
Price $52,777.74 → **$52,760.15**, MVRV-Z 0.9116 → **0.8725**, MVRV 1.4997 → **1.4873**, NUPL
0.3332 → **0.3276**, **SOPR 1.0019 → 1.0022** (the checklist's single PARTIAL, moving *away* from
its 1.005 bar), Puell 0.9389 → **0.8901**, STH-MVRV 1.11 → **1.10**, STH cost basis $70,966.91 →
**$70,955.89**. ETF advances from Sep 4 to **Sep 8** and absorbs the outflow day: `d5` 0.99 →
**0.72**, `d60` 2.06 → **2.03**, YTD −1.0 → **−1.04**, AUM 101.3 → **99.5** (price, not
redemptions) — but **`d20` rises 3.44 → 3.54**, because a larger outflow rolled out of the
twenty-day window than the −$46.65M that rolled in. So **leg 3 of the deploy trigger reads +$3.54B
against its +$1.5B bar**, firing by more than it did on Sep 7; with leg 1 clear on the weekly, the
Sep 14 window is again a question about leg 2 alone. Macro advances from the Aug 28 prints to
**Sep 4**: nominal 10-year **4.78** (1bp under `hi2y` 4.79, so the two-year high still stands in the
report's own series), real 10-year **2.43** vs 2.47, 2-year **4.37**. **`DTWEXBGS` is 118.0732
against a 119.48 200-day — 1.18% below it, not the 0.67% the carry list recorded**: the dollar
moved *further* from a crossing, which strengthens the one macro condition working for the thesis.
Net liquidity, M2 and HY OAS are unmoved. Stage TOO EARLY, 0 of 4 families lit, ladder unfilled.

The lesson is the one this file already carries in another form: **`git fetch` before reading
`data.json`, because the Action pushes and the working copy does not follow.** A same-day check that
reads a stale checkout will report "nothing moved" with total confidence and be wrong about the only
file that scores the page.

**Macro of the day, dated Sep 8–9, and it is the whole story.** Brent **$98.61 → $102.05**
(Sep 9 ~11 UTC), through $100 after Houthi strikes on Abha, Khamis Mushait, Jizan and Najran on
Sep 8 — including the **Jizan refinery, ~400,000 bpd** — with ≥73 injured. The 10-year **closed
4.786% with a 4.812% intraday high**, above the 4.80% Aug 31 high the `rates` row cites and above
`nom10y.hi2y` (4.79) in `data.json`, so tonight's FRED print may set a new two-year high in the
report's own series; the 2-year is 4.396%. US spot ETFs took their **first outflow day in five
sessions, −$46.65M on Sep 8** (GBTC −$65.51M, FBTC −$17.05M, BTCO −$4.68M against BITB +$14.47M and
IBIT +$10.66M; SoSoValue via an aggregator, Farside 403'd). Equities: S&P 7,673.52 (−0.58%), Nasdaq
26,421.41 (−0.32%), with Sep 9 futures Dow −0.6% / S&P −0.2% / NDX +0.1%. **No Fed speakers on
Sep 8 or Sep 9** — Waller on Sep 3 is still the last word, and his conditional rule makes the Sep 11
CPI the input. Coverage attributed Sep 8 to oil, yields and long liquidations; the liquidation
figures disagree ($264M total crypto with $79M in BTC, against $55M in BTC elsewhere) and neither
was adopted.

So the read the tape gives and the read the inputs give point opposite ways: a +1.3% bounce with
sentiment cooling three points, against oil through $100 and the long end at a new high for the
move. Oil is the route to the CPI-reacceleration scenario the capitulation tranche's macro gate was
written for, which makes it the live variable rather than a headline.

**Four items that read against what the report currently says.** None was written into `index.html`
this pass; they are recorded here so the Sep 14 pass can act on them rather than rediscover them.

1. **The Liquid Network row is less closed than the Sep 8 entry says.** That entry concluded "under
   the bar, closed the way the 2nd-catalyst row expected". One source dated Sep 9 (Archyde, citing
   TRM Labs) reports ~3,597 BTC in the identified reserve against ~4,200 L-BTC outstanding — an
   **implied backing ratio of ~86%** — with L-BTC deposits and withdrawals **still halted,
   including at centralised exchanges**, no post-mortem published, and no statement from the
   federation on how the shortfall is covered. Single-sourced, so it is not written as fact and the
   row is left alone; but "closed" was the optimistic reading and the Sep 14 pass should confirm or
   drop this before the row stands.
2. **Anthropic's $15B pre-IPO credit facility (Bloomberg, Sep 3) is in no file in this repo** —
   verified by grep across `index.html`, `MAINTENANCE.md` and this log. It is a funding step, not a
   filing, so it does not satisfy the "Anthropic public filing" carry item; it is corroboration for
   the mid-October listing the scheduled-events row now reports (CNBC, Sep 5, which the report does
   carry).
3. **"Saudi retaliation" may be overstated in the Sep 8 entry.** Today's sources show the foreign
   minister saying "the road to diplomacy is not closed" alongside a pledge to defend the kingdom,
   and coalition language about deterrent measures — **no confirmed retaliatory strike**. Flagged
   for checking, not corrected: the Sep 8 entry may have had a source this pass did not see.
4. **The Treasury buyback: effective date, possibly not operation date.** The press release
   (`home.treasury.gov/news/press-releases/sb0607`) says the ≥$4B size is *effective* Sep 9 through
   Nov 4. Nothing found confirms an operation is *scheduled* for Sep 9, and no result was published
   as of 12:40 UTC. The scheduled-events row and the carry list both say "the first enlarged
   Treasury buyback on Sep 9", which may conflate the two. Worth pinning against the TreasuryDirect
   operation calendar before it is restated.

**One conflict, checked and dissolved.** The research pass surfaced an August CPI consensus of
2.9% headline / 3.1% core against the 3.4% / 2.4% this report has carried since Sep 8, which would
have been a material error going into the print. It came from a **2025** article: July **2026** CPI
printed **3.4% headline / 2.5% core** on Aug 12, which is what the `Fed` row already states (BLS
release; CNBC Aug 12, 2026). The contradiction is therefore not real. Note what this does and does
not establish — it removes the challenge to the 3.4% / 2.4% August consensus; it does not
independently re-verify it.

**Not changed:** thresholds, weights, ladder, probabilities, the counter-scenario at 40%, every
`mac` row including the 2nd-catalyst and Strategy rows, `an_asof`. **Not checked this pass:** Hash
Ribbons, Sep 9 yield levels and closes, independent confirmation of a Saudi strike, and `Trade &
tariffs` / `Equities divergence` — still untouched since Aug 19, though the S&P at 7,673.52 is now
~1.1% under the 7,757.64 record that row quotes. No crypto-native loss event above the $500M bar
occurred on Sep 8–9; Liquid (~$320M) remains the largest and is under it.

---

## 2026-09-08 — Two carry items landed; nothing else moved, and only one row was edited

Not an adjudication and not a research pass — a same-day check of what changed since the Sep 7
entry, 16 hours after it. `an_asof` stays at Sep 7 because only one narrative row was refreshed.

**Strategy's 8-K for Aug 31–Sep 7 was filed Sep 8** (EDGAR accession 0001193125-26-384402, read
from the filing itself): **no bitcoin bought or sold**, no ATM shares sold, **$176.3M of STRC bought
back** from USD Cash (1,810,885 shares), and the digital-credit repurchase authorisation doubled from
$1B to $2B with $1.19B still available. Holdings 845,050 BTC at $75,412 average. USD Reserve $5.10B,
USD Cash $1.44B (from $1.61B in the Aug 31 8-K, the STRC buyback). **The $5.10B reserve is not new**
— checked against the Aug 31 8-K, which carried the same figure as of Aug 30 — but it had never
entered the report, whose last recorded reserve was the $2.55B of July. Read: the Aug 24–30 purchase
was a one-off, but the third consecutive filing shows no sale, and retiring 12% paper lowers the
dividend run-rate the capitulation gate depends on. The gate's status (armed in name only) does not
change; the `mac` Strategy row's "no 8-K filed yet" sentence was replaced in all three languages.

**Liquid Network:** 3,400 of the ~4,000 BTC were returned on Sep 7; ~598 BTC (~$47M) outstanding as of
Sep 8; the network stays paused for fixes; no exchange reported a solvency problem. Under the bar,
closed the way the 2nd-catalyst row expected. Sources disagree on whether the exploit was Sep 6 or
Sep 7; the row keeps Sep 7 (first reports) and is otherwise left as written.

**Same-source deltas, Sep 7 → Sep 8:** BTC ~$78.9K → $78.35K (day low $77,620, 4.8% under the Sep 3
high); Coinbase Premium raw −0.024% intraday at ~20:00 UTC (informational — the leg reads the Sunday
close); funding 7d +0.0047% → +0.0049%/8h; Fear & Greed 69 → 69; Hash Ribbons no new day (Sep 7 still
+0.47% Up), next retarget estimated +3.7% at 22% of the epoch; Polymarket ↓$70K 52.5 → 57, ↓$60K
24.5 → 25.5, ↓$55K flat 20.5, ↑$85K 71.5 → 67.5, ↑$90K 49.5 → 45, low-is-in interpolation ~77%
unchanged; September hike 51.5% → 54.5% on the same Gamma event. `data.json`'s 19:10 UTC build
brought only HY OAS 2.65 → 2.68 (Sep 7) and RRP 0.7 → 0.6; every on-chain series is still Sep 7, so
the checklist state is the Sep 7 state by construction (not re-rendered for scoring today). Sep 8 ETF
flows are not published anywhere yet; by the measured lag they reach `data.json` at the Sep 9 19:00
UTC run. The bounce marker is unchanged (+42.4% peak vs +45.7%, gap 3.3), because it is measured at
the peak.

**Macro of the day, dated Sep 8:** Brent to $98 after Houthi strikes on Saudi energy facilities and
Saudi retaliation; Iran announced a maritime "exclusion zone" outside Hormuz; 10-year ~4.77–4.79%;
Treasury confirmed the enlarged buyback (≥$4B per operation) from Sep 9; August CPI consensus 3.4%
headline / 2.4% core for Sep 11. Coverage attributed the day's decline to oil, hike odds and long
liquidations. Nothing dated Sep 7–8 on the Anthropic filing or the MSCI consultation.

**Not changed:** thresholds, weights, ladder, probabilities, the counter-scenario at 40%, the
2nd-catalyst row, `an_asof`. The MAINTENANCE carry list was updated for the two landed items.

---

## 2026-09-07 — The Sep 7 adjudication: 2 of 3 a third time, the miss is now inside the noise, and the market finally moved

The third scheduled adjudication of falsifier #6. The pinned window was **Monday Sep 7, 00:15 UTC**
(MAINTENANCE §2b); this pass ran on the evening of Sep 7 in Brazil (≈03:00–05:00 UTC Sep 8), about
27 hours late. As on Sep 1 it is still a clean adjudication, because every input the window uses was
fixed before it opened: the Aug 31–Sep 6 weekly candle, the Sep 6 daily closes, and the ETF figure
`data.json` carried at 00:15 UTC Monday — the Sep 6 19:08 UTC build, through Sep 4, which every
build since has carried unchanged because Sep 7 was Labor Day and there was no US session.

BTC **~$78.9K**, **−37.5%** from the ATH, day 337 of ~370 on the cycle clock (week 48.1), week ~9.9
off the Jul 1 low of $57,800.19 and **+36.6%** above it. The window has been open a week; the cadence
is weekly.

**The recommendation is unchanged. Stage TOO EARLY, 0 of 4 families lit, ladder unfilled, nothing
deployed.** The probe (20%, $52–57K) and core (45%, $44–50K) tranches remain empty. Next
adjudication: **Monday Sep 14, 00:15 UTC**.

### Falsifier #6 at the Sep 7 window: 2 of 3, not fired

| Leg | Bar | Reading at the window | |
|---|---|---|---|
| 1 — weekly close | > ~$70K | **$80,341.83** (Aug 31–Sep 6 candle: $77,682 open, $82,300 high, $76,264 low) | **FIRED**, by 15% |
| 2 — Coinbase Premium | positive | **−0.0034%** raw, Sep 6 daily close (Coinbase $80,339.13 vs Binance $80,341.83); **+0.0026%** USDT-adjusted (tether 0.99994) | **NOT FIRED** |
| 3 — ETF 4-week net | > +$1.5B | **+$3.44B** (`etf.d20` through Sep 4, the figure live at 00:15 UTC) | **FIRED** |

Same configuration for the third Monday running, same leg missing. Two things about leg 1 are worth
having on the record without making anything of them: $80,342 is the **highest weekly close since the
week of May 4** ($82,210), and the Sep 3 high of $82,300 came $550 under the May 8 high of $82,850 —
the last lower high of the decline from January. A weekly close above ~$82.2K would be the first
higher high on the weekly chart since the top. Noted as structure, not written as a marker: the report
already has one marker for this rally and does not need a second one chosen while looking at the tape.

### Leg 2: three Mondays inside the noise — the design review's input, measured rather than argued

Daily closes for the adjudicated week and the two days after, raw convention (Coinbase `BTC-USD` ÷
Binance `BTCUSDT` − 1) with USDT-adjusted alongside:

| | Aug 31 | Sep 1 | Sep 2 | Sep 3 | **Sep 4** | Sep 5 | **Sep 6** | Sep 7 |
|---|---|---|---|---|---|---|---|---|
| raw | −0.0236 | −0.0521 | −0.0422 | −0.0079 | **+0.0180** | −0.0002 | **−0.0034** | −0.0253 |
| USDT-adj | +0.0134 | +0.0019 | −0.0012 | −0.0049 | −0.0020 | −0.0052 | **+0.0026** | −0.0083 |

One positive raw close in the week, on the Friday; the adjudicated Sunday missed by **0.34 basis
points** and was positive on the adjusted convention — the Aug 23 configuration again. The Sep 1 entry
said the streak-break was "the first evidence for the deferred design review" and deferred the review
because that pass was a reactive moment. This one is too, so the review is still not run. What this
pass does instead is measure every form of the leg that has been proposed, over all three windows, so
that whoever runs the review has numbers rather than a narrative:

| Window | Pinned: raw, Sunday close | USDT-adjusted, Sunday close | Any positive raw close in the week | Weekly mean, raw | Weekly mean, adjusted |
|---|---|---|---|---|---|
| Aug 24 (Aug 17–23) | **−0.0060** · no | +0.0070 · *yes* | 0 of 7 · no | −0.0370 · no | +0.0078 · *yes* |
| Aug 31 (Aug 24–30) | **−0.0217** · no | −0.0187 · no | 3 of 7 · *yes* | −0.0028 · no | −0.0006 · no |
| Sep 7 (Aug 31–Sep 6) | **−0.0034** · no | +0.0026 · *yes* | 1 of 7 · *yes* | −0.0159 · no | +0.0007 · *yes* |

The Aug 17–23 row was measured from the candles for this table, not inferred from the streak; it
reproduces the −0.0060% / +0.0070% the Aug 24 entry published. The dispersion of the raw daily
closes is **σ = 0.021%** over Aug 24–Sep 7 (n = 15, mean −0.010%) and 0.026% over Aug 17–Sep 7
(n = 22, mean −0.019%). The three Sunday readings — −0.60, −2.17 and −0.34 basis points — all sit
inside one standard deviation of zero; the Sep 6 miss is a sixth of one.

Read the table by column. The pinned form and its smoothed version (weekly mean, raw) agree on all
three Mondays: 0 of 3. The forms that disagree are the ones that either change the *convention*
(adjusted: 2 of 3, and the second of those a positive 0.07 basis points, which is noise on any
reading) or take the *best day* (any positive close: 2 of 3). So the pinned form is not producing a
different answer from a noise-robust version of itself; it is producing the same answer with no
margin. That is the finding. Whether a leg that governs 65% of the ladder should be read at the
resolution of ±2 basis points is the design question, and it is a decision, not a measurement:

- **Keep as pinned.** Raw Sunday close. Has read not-fired three times by margins that a daily σ
  covers three times over.
- **Weekly mean of raw closes > 0.** The noise-robust form of the *same* convention. It would have
  changed nothing so far — which is exactly why it is the one form that could be adopted prospectively
  without being a retro-edit.
- **USDT-adjusted convention.** The Aug 19 entry declined to switch to it when it flattered the
  reading and §2b says why. Its measured cost, stated as the Aug 21 pinning asked for: on it, the
  trigger would have fired on **two of three Mondays** and 65% of the ladder would be deployed.

Any change applies from the window after the decision, never to a window already adjudicated. Nothing
here is changed in this pass; the table is the standing input.

### The checklist did not move

`CORE` rescored through the same `RULE` object the calibration replays, on-chain values as of
**Sep 7** (`data.json`, built locally at 03:00 UTC Sep 8), spot ~$78.9K:

| Rule | Sep 1 | Today | |
|---|---|---|---|
| Puell | 1.0045 | **0.9389** | NOT YET (bar 0.9; it printed 1.1183 on Sep 6) |
| MVRV-Z | 0.8514 | 0.9116 | NOT YET |
| SOPR | 1.0046 | **1.0019** | **PARTIAL** (bar < 1.005) |
| Price ÷ 200W MA | +19% | +21.7% ($64,888) | NOT YET |
| Price ÷ Realized Price | 1.46 | 1.50 ($52,778) | NOT YET |
| NUPL | 0.3295 | 0.3332 | NOT YET |
| STH-MVRV | 1.10 | 1.11 (basis $70,967) | NOT YET |
| Drawdown | −38.9% | −37.5% | NOT YET |

**Expert 4%, equal 6%** — the same single PARTIAL as Sep 1, against 95% at the confirmed Nov 21,
2022 bottom. Puell's path this week is worth one line because it will keep doing this: 1.0045 (Aug 31)
→ 1.1183 (Sep 6) → 0.9389 (Sep 7). The denominator is a 365-day average and barely moves; the
numerator is a day's issuance value plus fees, so the ratio swings ±15% day to day around its slow
trend and now sits 4 basis points over the PARTIAL bar. When it flickers PARTIAL the `CORE` figure will
read ~9% and it will mean nothing.

Across all 15 rows: **expert 18%, equal 23%**, 1 ACTIVE (`etf`), 5 PARTIAL (`hash`, `sopr`, `lth`,
`resv`, `fed`), **0 of 4 families lit → TOO EARLY**. Families: Valuation 0 of 4; Capitulation 0 active
· 2 partial (1.0 of 5, needs > 2.5); Supply & flows 1 active · 2 partial (2.0 of 5, needs > 2.5);
Macro 0 active · 1 partial (0.5 of 1). Identical to Sep 1 in every cell. Rendered headless (Chrome,
`--dump-dom`) and read off the page, not recomputed by hand; stderr carried no console errors.

### Hash Ribbons: seven days Up, the retarget went the right way, the row stays PARTIAL

The BGeometrics `hashribbons` series since the Aug 31 whipsaw:

| | Aug 31 | Sep 1 | Sep 2 | Sep 3 | Sep 4 | **Sep 5** | Sep 6 | **Sep 7** |
|---|---|---|---|---|---|---|---|---|
| 30d (EH/s) | 908.1 | 907.5 | 904.3 | 911.0 | 912.3 | 916.4 | 918.0 | 917.4 |
| 60d (EH/s) | 909.0 | 907.2 | 903.9 | 907.5 | 909.5 | 909.6 | 911.9 | 913.1 |
| gap | −0.10% | +0.03% | +0.04% | +0.39% | +0.31% | **+0.75%** | +0.68% | **+0.47%** |
| state | Down | Up | Up | Up | Up | Up | Up | Up |

Seven consecutive Up days, the gap widening rather than hovering. The **Sep 5 retarget printed
+1.31%** — mempool.space's `previousRetarget` field reads 1.3065%, and difficulty went 125.81T →
127.45T at block 965,664 — against the +1.10% mempool.space estimated on Sep 1 and the −0.94%
CoinWarz had. That is the first projection this log has quoted to land on the right side, by 0.2 of a
point; the next retarget is due ~Sep 19 and mempool.space estimates **+3.8%** with 17% of the epoch
elapsed. A second provider agrees in sign: mempool.space's own 3-month hashrate series reads 911.0 vs
907.6 EH/s (+0.38%) on 30d/60d — a different measurement kept as a cross-check, not spliced.

**The row stays PARTIAL.** The Sep 1 entry tested persistence as a rule and rejected it because a
28-day Up in Feb–Mar 2026 still preceded the July low; seven days does not clear a test that 28
failed, and the field is still a memoryless sign(30d − 60d). The cross is proving itself; it has not
proven itself. The stage would not move at ACTIVE either (Capitulation would read 1.5 of 5).

### Macro: a hike became the modal outcome, and the composite's dollar leg is still 0.7% away

The Fed trigger card had been carrying a Kalshi/FedWatch mix from different dates. This pass replaces
it with a **same-day Polymarket snapshot** (Gamma API, Sep 7 — the same method the BTC card uses):
the Sep 15–16 meeting at **51.5% hike / 47.5% hold / 0.45% cut**, a hike by the October meeting at
62%, at least one hike in 2026 at **70.5%**, no cut in 2026 at 92.7%, an emergency cut at 6.1%. It is
the first snapshot in which a hike is the modal outcome rather than "even money in one market".

What moved it, dated. **August payrolls on Sep 4: +162K against +53K expected**, unemployment 4.1%,
participation 61.6%, June–July revised up 55K, earnings +3.1% y/y. **Waller on Sep 3**, the day before:
willing to hold if progress toward 2% continues, would consider a hike if inflation comes in hot, the
decision "heavily influenced" by the August inflation data — which makes **CPI on Sep 11** the print
that decides the meeting, and it goes into the calendar as such. **Brent above $95** after two tankers
were struck leaving the Strait of Hormuz, following the Aug 30–31 exchange of fire (the strikes are
dated "early September" by the coverage collected, not to a day). ISM manufacturing
54.6 on Sep 2 (from 55.6). The Sep 3 rally to $82,300 was attributed in coverage to Waller's remarks,
the +$731M ETF day and ~$250M of short liquidations; the Sep 4 payrolls print reversed it.

FRED, as carried in `data.json`: 10-year **4.77%** (Sep 3) against a 4.79% two-year high and a 4.36%
200-day; 2-year 4.34%; real 10-year **2.42%** against a 2.05% 200-day and a 2.47% two-year high; HY
OAS 2.65% against a 2.59% two-year low. Broad dollar 118.75 (Aug 28 — FRED's `DTWEXBGS` lags a week)
against a 119.55 200-day: **0.67% below**, the composite's fragile leg, unchanged. M2 y/y 5.41%
against 4.53% (3m) and 4.06% (6m). Composite **2 of 3, PARTIAL**, unchanged.

Net liquidity **$5,768.7B** on Sep 2, below its 4-week ($5,839.6B), 13-week ($5,833.7B) and 52-week
($5,986.6B) averages, and $11B lower than the Aug 26 reading; the TGA rose $17B to **$967.9B** ahead
of the first enlarged buyback on Sep 9; RRP $0.7B. US recession odds on Polymarket 6.5% (from 8% on
Aug 19). Every macro axis the report tracks moved against the liquidity turn again, except the dollar,
which held.

### Geopolitics row moved to headwind

The `mac` geopolitics row still read "De-escalating" with a tooltip about Hormuz calm and Brent at
$76, two passes after this log recorded the Aug 30–31 exchange of fire and one after Brent crossed
$90. It contradicted the Fed and Rates rows on the same page. Refreshed to **re-escalating** and moved
`e:` from `m` to `h` in all three languages (the `e:` field is logic, byte-identical across
languages). Found by a second opinion reading the rendered page rather than by the stale-number sweep — a row
can be stale without containing a number, which the sweep cannot catch.

### ETF flows: third Monday over the bar, and the largest day since January

`etf.d20` **+$3.44B** through Sep 4 (SoSoValue), 5-day +$0.99B, **60-day +$2.06B** (from +$0.58B
on Sep 1), YTD −$1.00B, cumulative $55.6B, AUM $101.3B. Daily, per Farside via coverage: Aug 31
+$217M, **Sep 1 −$236M** (the first outflow day since Aug 28; IBIT −$201M), Sep 2 +$101M, **Sep 3
+$731M — the largest single day since January** (IBIT +$454M), Sep 4 +$175M with only IBIT and FBTC
positive going into the holiday. Week of Aug 31–Sep 4: ~+$987M. The Farside daily figures and the
SoSoValue 20-day arbiter are different sources with different windows and are not spliced; the
arbiter is the one that adjudicates.

### The bounce outlasted both precedents in time, not in size

**+42.4%** at $82,300 on Sep 3, **64 days (week 9.1)** off the low. The 2022 bear rally topped in week
8.3 and the 2018 one in week 3.9, so this bounce has now run longer than either — a comparison the
Sep 1 entry could not make, when the peak sat exactly on the 2022 week. In amplitude it is still under
both (+43.1% and +45.7%), and the pre-registered marker is +45.7% (~$84.2K): the gap closed from 4.7
to **3.3 points**, and price has since retraced to ~$78.9K, 4.1% under the high. The duration
comparison is new evidence and goes into the ledger below. The marker is an amplitude marker and does
not move: it was written on Aug 24 so that it would not be re-derived at whatever level price reached.

### Strategy: the second week is unfiled, and a dated route back to selling appeared

No 8-K covering Aug 31–Sep 6 has been filed — Sep 7 was Labor Day, so it is due once the US session
returns. Checked on EDGAR: the filings in September so far are the Aug 31 8-K (filed Sep 1, the
purchase) and a second Sep 1 8-K that only sets the preferred dividend rates (STRC 12.00%, paid
semi-monthly; STRF/STRK/STRD/STRE quarterly). So whether the Aug 24–30 purchase was a one-off is still
open, and the `mac` row says so. A public tracker quotes mNAV ~1.12× on the EV definition.

**New and dated inside the window:** MSCI has reopened its consultation on excluding "non-operating"
digital-asset treasury companies from its investable-market indexes — comments open to the end of
September, a decision expected mid-October, effective at the November index review. Coverage estimates
~$2.8B of passive outflow from MSTR; Strategy's public response called the proposal a pretext. This is
the re-arming route the Strategy row had not named: forced index selling widens the discount, a wider
discount makes the ATM dearer, and the dividend still has to be paid. Added to the scheduled-events
row at all three dates and to the Strategy row's tooltip. It is not a catalyst yet; it is a calendar.

### The second-catalyst bar was tested for the first time since July

**The Liquid Network — a Bitcoin sidechain exchanges use to move coins — was exploited for ~$320M
(~4,000 BTC) on Sep 7** (Bloomberg, CoinDesk). The attackers claim to be white-hat and to intend
returning the funds for a fee; that is unverified and is labelled so in the row. It is the largest
crypto-native event since the Coldcard exploit (~$120–140M) and about two-thirds of the $500M bar.
Under the bar, and not a solvency event unless a custodian turns out to be uncovered; watch whether
the funds come back. No stablecoin left 12bp of par in the week. Also dated: the FTX cash
distribution starts Sep 30 (record date Aug 15); Mt. Gox holds ~34,504 BTC with the Oct 31 deadline
and moved nothing in the week.

Two calendar corrections from the research. The SEC's Regulation Crypto Assets was **published in
the Federal Register on Aug 21**, so its 60-day comment period closes **Oct 20** — the row had
deliberately left this "mid-to-late October" until the publication date was known, and it is pinned
now. And the Anthropic listing is now reported for **October** rather than late September, with a
raise above $60B; still trade-press, still not company-confirmed, and the row moves it to October and
says so.

### Polymarket: the first move in four reads, and it went toward the counter-scenario

Gamma API snapshot at the time of this pass, open contracts only, Sep 1 in parentheses: ↓$60K
**24.5%** (28.5), ↓$55K **20.5%** (23.5), ↓$50K 14% (15.5), ↓$45K 8.5% (7.5), ↓$40K 6.5% (6.5);
interpolated at the $57,800 low, ~23%, so the low-is-in read is **~77%**, from ~74% on Aug 24, Aug
26 and Sep 1. The revisit rungs eased — ↓$65K 33.5%, ↓$70K **52.5%** (59), ↓$75K 77.5% (86.5) — so
the market's median path still touches $70K, leg 1's bar, but only just. Upside repriced *up*: ↑$85K
**71.5%** (61.5), ↑$90K **49.5%** (44.5), ↑$95K 32% (31.5), ↑$100K 24.5% (22). The $90K rung —
falsifier #2's level — is now a coin flip.

### The counter-scenario is held at 40%, for a different reason than last week

For it, since Sep 1: the market moved, +3 points, after three flat reads; the rally outlasted both
precedents in duration; the highest weekly close since May; the ribbons Up seven days with a positive
retarget; the ETF leg over its bar for a third Monday with the 60-day at +$2.06B; the adjusted premium
positive on the adjudicated day. Against it: a September hike is now the modal outcome and payrolls
beat by 109K; Brent above $95; a $320M exploit; the premium negative on seven of the last eight
closes; the valuation rows did not move by a single state; price is 4% off the high; and the strongest
possible "for" item — a second week of Strategy buying — is not in hand because the 8-K is not filed.

Held at **40%**. Last week's reason was "the market has not moved", and that is no longer true, so the
reason is stated differently: the ledger is two-sided in a different way, and the marker is uncrossed
at 3.3 points. The market is at ~77% and the report at 40%; the gap is the report's stated
disagreement, and it narrows when the marker is crossed or the valuation rows move, not when a week
tilts.

### Supporting reads

- **Funding** 7-day average **+0.0047%/8h** (~+5.2% annualised), last +0.0045%; down from +0.0081%
  on Sep 1, still positive against the row's −0.005% bar. Funding z < −2 is not in sight.
- **Fear & Greed** 73 (Sep 5) → 71 → 69 (Sep 7). Greed on every print.
- **Aggressive-buy triggers**: still **1 fired · 1 partial · 2 not fired**. ETF fired and extended;
  hash PARTIAL with seven days Up; premium NOT FIRED by 0.3bp; Fed moved further away.

### Other falsifiers, cross-checked

**#1** (new ATH) — $126,296, far off. **#2** (above ~$90K for eight consecutive weeks with fewer than
three families lit) — high $82,300, not in play; the market now prices ↑$90K at 49.5%. **#3** (week
70 = Feb 2027) — not due. **#4** (low below $30K) — not in play; its named mechanism gained a dated
route (MSCI) and no event. **#5** (bottom confirmed on fewer than 8 of 15) — not in play.

### What was deliberately not changed

- **No threshold, no weight, no `BS_W`, no `CORE` membership, no ladder band, no probability.**
- **The premium convention and window.** Raw governs, Monday close adjudicates. The three-window
  table above is the input to the design review; the review is a decision for the owner of the ladder
  and was not run in the pass in which two of its candidate outcomes would fire the trigger.
- **`hash` stays PARTIAL** and no persistence rule was pinned, for the reasons measured above.
- **`sthmvrv`'s ≤0.80 threshold** stays under prospective review, unchanged.
- **`lth` and `resv`** carry their Aug 19 readings; SLOW rows, nothing dated to this week found.
- **The bottom window and ladder bands.** Nothing this week touched them.
- **`mac_h` still reads "Reading (Aug 19, 2026)".** Refreshed this pass: Fed policy, Geopolitics,
  US recession odds, 2nd catalyst, Strategy, Scheduled events. Carrying a live figure and refreshed
  only in their narrative tail or not at all: Rates, Liquidity, US dollar, Credit spreads, Spot ETF
  flows. **Not refreshed since Aug 19: Trade & tariffs, Equities divergence.** The header moves when
  those two are re-checked, not before.

### Stale-number sweep, per the Aug 26 procedure

Searched `index.html`, `README.md`, `MAINTENANCE.md` and `og-card.html` for the previous pass's
headline figures — `1.0046`, `ten days at zero`, `week 47`, `46% above Realized Price`, `+41.0%`,
`81,479`, `~74%`, `3.35B`, `−0.022%`, `next adjudication is Mon Sep 7`, `Sep 1` tags — and checked
each hit is a dated statement or a fix. Fixed: the thesis paragraph's SOPR figure, "week 47" and
"1.10" (×3); `ph_notes[2].tip`'s "46% above Realized Price" (the DOM renders 50%) and its bounce
sentence (×3) — the key MAINTENANCE names as a repeat offender, stale again; the replacement is
*dated* ("50% on Sep 7") rather than re-typed as a present-tense reading, because the page already
computes the live ratio in the thesis paragraph; README line 5. Two figures were re-typed as
present-tense and will need the weekly cadence to carry them: "week 48" in `th_p` (×3) and the
"37% rally" gloss next to it. The
`og-card.html` stat reads 4%, matching `cal_sum`'s "4% today", so the card is not regenerated. The
research tag moves to **Sep 7, 2026** in all three languages, because narrative rows were refreshed
and not only the trigger cards.

**Carry into the next pass (Sep 14 window):** Strategy's 8-K for Aug 31–Sep 6, due Sep 8 — a second
buying week makes the de-arming a pattern, a sale re-arms the gate; **August CPI on Sep 11** and what
the Sep 15–16 pricing does after it; the first enlarged buyback on Sep 9 against the TGA ($967.9B) and
net liquidity; `DTWEXBGS` against its 200-day (0.67% away; FRED's latest print is Aug 28, so the
Sep 14 pass will see the Sep 4 week at best); whether the premium prints positive on a *Sunday*
close, or the owner decides the leg-2 form from the table above; ribbon persistence (14 days would
still be under the rejected 28); the bounce against the +45.7% marker and against $82,210, the last
higher weekly close; whether the Liquid Network funds come back; the MSCI comment close at end-Sep;
an Anthropic public filing; and `mac_h`, which needs Trade & tariffs and Equities divergence
re-checked before it can move.

---

## 2026-09-04 — A dated IPO calendar entered the window row, with the one price measurement that justifies it

**Why an IPO is on a bottom-window calendar at all.** A reader asked whether BTC fell around the
SpaceX IPO. It did, and the shape of the fall is specific enough to be worth writing down before
the next one, because the next one is scheduled inside this report's own projected window.

**What was measured, from Binance daily closes rather than from press accounts.** SpaceX priced
after the close on Jun 11, 2026 and debuted Jun 12 on Nasdaq (SPCX, $135, ~$75B raised — the
largest listing on record; sources put the valuation at $1.75–1.77T and disagree at that
precision). Around it:

| | | |
|---|---|---|
| May 31 | $73,674 | the day before |
| Jun 1–6 | $73,674 → **$60,885** | **−17.4% in six sessions** |
| Jun 11 | $63,626 | priced |
| **Jun 12** | **$63,580** | **debut — −0.1% on the day** |
| Jun 15 | $66,329 | **+4.3%** three sessions later |
| Jul 10 | $64,162 | **+0.9%** four weeks later |

**The finding is a timing correction, not a confirmation.** The entire drawdown happened *before*
the listing, during book-building; the debut day itself was a non-event and BTC rose for three
sessions after it. The cycle low ($57,800, Jul 1) came 19 days later but only −5.6% below the
IPO-day price. That ordering is *more* consistent with the capital-rotation mechanism than the
naive version — allocating into an offering requires selling first — which is exactly why it is
worth recording: the naive version would have watched the wrong fortnight.

**The confound is real and is published with the claim.** The Mt. Gox trustee moved 10,422 BTC on
Jun 3 and ~$1.86B of leverage was liquidated inside the same 72 hours. Two candidate causes, one
observation, N=1. Contemporaneous press had already reached the same place from the other
direction: crypto.news ran the question on **Jun 8, four days before the debut**, and concluded
the IPO did not trigger the fall — which is itself evidence the fall preceded the listing.

**What went into the row, and what was deliberately kept out of it.** Company-confirmed and
stated as such: Anthropic's confidential S-1 on Jun 1, the Morgan Stanley / Goldman Sachs /
JPMorgan mandate on Jun 3, and the $65B round at a $965B valuation on May 28. *Not*
company-confirmed, and labelled in the row as trade-press and aggregator reporting: a public
filing targeted at end-August and a Nasdaq listing in late September or early October. There is
no date, no ticker and no price range, so the entry is explicitly undated inside the month rather
than pinned to a day — the same treatment the SEC comment-period deadline already gets in that
row.

**An attempted verification that failed, recorded so it is not repeated as fact.** An EDGAR
company search for a public Anthropic S-1 returned an empty feed. It was **not** treated as
evidence: the identical query returns an empty feed for SpaceX, which demonstrably completed an
IPO, so the query is broken rather than the answer negative. Nothing in the row rests on it.

**What this does not do.** It does not move the window, which is derived from cycle structure and
not from a catalyst calendar — the row's own tooltip already says so and that is the reason the
row exists. The value of the entry is pre-registration: if a bottom forms in the second half of
September it will be attributed to whatever was in the news that week, and this is the record that
the book-building fortnight was expected in advance, along with the honest note that one
observation cannot tell it apart from a Mt. Gox distribution.

---

## 2026-09-03 — The overlaid-cycles chart was drawn by hand, and the run-up was wrong by up to 59 points

**What prompted it.** A reader question — how does cycle 4's drawdown so far compare with the
others at the same week — ran into the fact that the report answers it twice, from two different
sources, and the answers disagree. The same-week table reads `D1`/`D2`/`D3`, three hardcoded
arrays; the click-to-compare panel calls `calcAtWeek()`, which computes from Binance history.
At week 47 the table read **C1 −67 / C2 −68 / C3 −71**. Measured closes say **−69.7 / −67.4 /
−70.8**. Not a large gap, but it **inverted the C1/C2 ordering**, and the report cites that
ordering when it argues successive bear markets are getting shallower.

**What the arrays actually were.** Not low-resolution — wrong. Sampled every 2–6 weeks, rounded
to whole percent, and read by `da()`, a step lookup that returns the last point at or before the
week asked for, so a week-47 query was answered with a week-44 value. Diffed against exchange
closes, week by week, on the weeks they had in common:

| | mean abs. error, pre-ATH | mean abs. error, post-ATH | worst point |
|---|---|---|---|
| C1 | 17.0 p.p. | 5.9 p.p. | week −4: drawn −25%, real **−82.2%** |
| C2 | 19.4 p.p. | 7.1 p.p. | week −5: drawn −12%, real **−70.6%** |
| C3 | 13.8 p.p. | 6.6 p.p. | week −16: drawn −15%, real **−53.4%** |

The pre-ATH half is where it is worst, and the failure is systematic rather than random: each
array draws the run-up as a smooth ramp easing into the top, when every cycle actually spent the
final weeks in a near-vertical leg. Cycle 1 was **70% below its own ATH three weeks before
printing it**, and 82% below four weeks before. Two specific distortions matter because the report reasons about them:

- **C3's April-2021 double top was erased.** Week −30 was drawn at −42%; the real reading is
  **−8.8%**. The chart showed a deep mid-cycle trough where there was a local high 8% from the
  eventual ATH — i.e. it drew away the single most-cited structural feature of cycle 3.
- **C2's COVID crash was drawn at the wrong week and the wrong depth.** Week 114 was drawn at
  −80%; real −49.8%. The real low, −72.9%, came three weeks later at week 117 (Mar 15, 2020).

**Why this was worth fixing rather than annotating.** The chart is the report's opening exhibit
and the run-up is half of it. `cvp_sum` argues cycle 4's amplitude was compressed "on the way up
as much as on the way down" — an argument about exactly the segment that was fabricated. The
numbers behind that claim come from the Pi Cycle, not from these arrays, so the conclusion
stands; but the picture offered as its illustration was not evidence for it.

**What replaced them.** `scripts/build_cycles.py`, in the pattern of `build_data.py`: it fetches
daily closes and rewrites the three `const` lines in place, one point per week from −82 to +140,
one decimal, using the **same definition the runtime uses** — `close / ATH_const − 1`, the close
being the last one at or before `ATH_date + 7w`, which is what `calcAtWeek()` does and what
`processKlines()` builds cycle 4 from. Three artefacts of the old arrays are gone with them: the
step-lookup error (every week is now present, so `da()` lands exactly), the whole-percent
rounding, and the disagreement between the chart and the click panel.

**Sources, and why they are mixed.** Binance BTCUSDT wherever it reaches, Bitstamp BTC/USD to
backfill what predates it — Binance's pair starts Aug 17, 2017, which is *after* cycle 2's
window opens (week −82 = May 22, 2016). That is presumably why the arrays were hand-drawn in the
first place: the report's own data source cannot draw C2's left half. So C1 is all Bitstamp, C3
all Binance, C2 carries one seam at week −17. The seam is placed in the run-up deliberately: the
feeds are not identical to the decimal — through the Oct–Nov 2018 Tether scare USDT traded at a
discount and BTCUSDT ran ~1.5% above BTC/USD, so C2's week 47 reads −67.9% on Bitstamp against
**−67.4%** on Binance. Half a point, but it is basis rather than noise, so it belongs on the side
of the chart where nothing is quantified. The post-ATH half — the part every table and claim
reads — is Binance throughout, matching the retro-calibration.

**A trap worth recording, because it nearly shipped silently.** The first run of the generator
produced C1 week 47 = −69.1% where a hand check said −69.7%. The cause was
`datetime.date.fromtimestamp()`, which reads a candle's 00:00 UTC open in **local** time; at
UTC−03 that labels every single day one early. Nothing errors, nothing looks wrong, and all three
series shift by a day. It was caught only because one value had been computed independently
beforehand. `--verify` exists for this class of failure: it refetches and exits 1 if the
committed arrays drift more than 0.15 p.p. from the sources. It was run against the old arrays
first, and failed at 58.6 p.p. — that number is the regression this change fixes.

**Two things deliberately left alone.**

- **The `PRIOR_LOWS` markers now sit 0.3–2.4 p.p. below their own lines** (C1 −85 marker vs a
  −82.6 line at week 59). This is correct and must not be reconciled: the marker is the true low
  day, the series samples one close every 7 days, and C1 bottomed on Jan 14, 2015 — three days
  before week 59's sample, after which price had already bounced. Re-sampling the series to
  weekly *minima* would close the gap and destroy comparability with cycle 4, which is built
  from point-in-time closes at runtime. Noted in the code so a future pass does not "fix" it.
- **Week 0 is pinned to y=0 in all three arrays.** No cycle closes at its own intraday ATH, so an
  honest week 0 reads −4% to −6% for cycles 1–3 (C3 closed $64,995 against a $69,000 ATH
  constant) against a hard 0 for cycle 4, whose series is seeded `{x:0,y:0}` by `processKlines()`.
  The four lines would miss each other at the one point the chart exists to align them on. The
  pin costs one week of fidelity per cycle and is documented rather than silent.

**What did not change.** No threshold, no conclusion, no table. The bear-market table's
−85/−84/−78 and the low dates are measured on the actual low day and were independently
confirmed correct in passing (C1's Jan 14, 2015 close of $171 against a $1,150 ATH is −85.1%).
The same-week comparison table will now print different numbers, but it prints them because they
are the measured ones — the direction of the report's argument is unaffected, and cycle 4 is if
anything *further* from precedent than the old arrays implied.

---

## 2026-09-02 — The window got a calendar: recurring macro prints added to the scheduled-events row

**What changed and why now.** Until today the `Scheduled events in the window` row listed only
structural, one-off items — the Treasury buybacks, the September FOMC, Mt. Gox, the midterms —
and deliberately left out the recurring macro releases on the grounds that CPI-and-payroll
noise is not cycle evidence. **That exclusion was correct while the Fed row read cut-versus-hold
and stopped being correct when it flipped to hold-versus-hike.** With a September hike at least
even money in one market (Kalshi ~59% on Aug 31 against CME ~58.6% *hold* on Aug 25), every
inflation and labour print between now and Sep 16 is a direct input to the one dated event the
report itself calls "a genuine shock to the window". The row now carries the full Sep→Dec
calendar in all three languages.

**Dates, and where each came from.** Not from memory — the BLS and BEA schedule pages were
fetched on Sep 2, 2026:

| Item | Date | Source |
|---|---|---|
| Employment Situation (Aug / Sep / Oct) | Sep 4 · Oct 2 · Nov 6 | `bls.gov/schedule/news_release/empsit.htm` |
| CPI (Aug / Sep / Oct) | **Sep 11** · Oct 14 · Nov 10 | `bls.gov/schedule/2026/09_sched.htm`, `.../news_release/cpi.htm` |
| PPI (Aug) | Sep 10 | `bls.gov/schedule/2026/09_sched.htm` |
| Personal Income & Outlays (PCE) | Sep 30 · **Oct 29** · Nov 25 | `bea.gov/news/schedule` |
| Q3 GDP advance | Oct 29 | `bea.gov/news/schedule` |

Two of those placements matter more than their being on a calendar. **August CPI lands Sep 11,
four days before the FOMC** — the last inflation print the committee sees. And **September PCE
and Q3 GDP advance both land Oct 29, the morning after the Oct 27–28 FOMC**, so the October
meeting is decided without them and repriced by them within a day.

**Derived rather than sourced, and labelled as such on the page:** the quarterly options expiry
(Sep 25 — last Friday of the quarter, stated that way in the row so the derivation is visible),
the cycle clock crossing the ~370-day C2/C3 average around **Oct 11** (ATH 2025-10-06 + 370),
and week 60 = **Nov 30**, which the report already uses as the window's close.

**One date was deliberately *not* printed.** The Aug 19 SEC Regulation Crypto Assets proposal
carries a 60-day comment period, and the obvious arithmetic gives Oct 18 — which is both a
Sunday and, more importantly, wrong in kind: the clock runs from **Federal Register publication**,
which lags a proposal by days to weeks. The row says "mid-to-late October" and states the
reason. Pinning it to a day is a Sep 7 to-verify.

**Recorded here, not on the page: $70K now does double duty.** Falsifier #6's leg 1 asks for a
weekly close above ~$70K; short-term-holder cost basis is **$70,148.64** as of Aug 31. The two
numbers arrived independently — leg 1 was set from the bear-rally structure, the STH basis is
computed — and they have converged on the same level. A weekly close below it would un-fire the
deploy trigger and put the STH cohort underwater in the same candle, which is the cleanest
single level on the chart right now. Left out of the UI on purpose: it is an observation about
two thresholds, not a new threshold, and inventing a rule out of a coincidence in the pass that
notices it is the failure mode this log exists to prevent.

**`an_asof` deliberately not bumped.** MAINTENANCE §Procedure bumps the snapshot badge for a
research pass; this was one row plus a calendar lookup. Moving it to Sep 2 would assert that
Fed policy, Strategy, tariffs and geopolitics were re-researched today, which they were not.
It stays **Sep 1, 2026**.

**Two pieces of drift found while in the file:**
- **Fixed:** `MAINTENANCE.md`'s footer read "Last research snapshot: Aug 19, 2026" against
  `an_asof`'s Sep 1 — two research passes stale, and unambiguous, so it moved to Sep 1.
  Its `an_asof` row also said "(EN + PT)" when there have been three keys since the Spanish
  translation shipped; now "(EN + PT + ES)", with the don't-bump-on-a-targeted-edit rule
  written into the same cell so the next pass does not have to re-derive it from this log.
- **Flagged for Sep 7, not fixed:** `mac_h` still reads "Reading (Aug 19, 2026)" in all three
  languages while the rows underneath it were rewritten on Aug 31 and Sep 1. Fixing it honestly
  requires knowing which rows each pass actually refreshed — a pass decision, not an edit.

**Verified by rendering**, per the standing rule: script block extracted and `node --check`ed,
then `google-chrome --headless --dump-dom` against `localhost:8931` — 426KB of DOM, no
`INFO:CONSOLE` lines, the new row present. The check was not ceremonial: the row is a
single-quoted JS string literal and every apostrophe in the new text had to be a curly `’`, or
all three languages would have gone dark at once. **Rendered in EN only** — Portuguese and
Spanish were checked by `node --check` and by the replacement being the same string-value
substitution with no key added or removed, which is weaker and is stated as such.

**And a self-correction on the same rule, caught after the commit.** The first version of this
entry said the render confirmed "the stage still reading TOO EARLY". It did not: what had been
grepped was a count of the four stage names in the DOM, which matches the ladder *legend* inside
`th_stage_tip`, not the live headline. Re-rendered against the Sep 2 06:00 UTC `data.json`
(on-chain through Sep 1: SOPR 1.0024, Puell 0.9361, STH basis $70,269.54; `etf.d20` 2.90) and
read the headline element itself: **"Too early", 0 of 4 families lit, 1/15 active, 5 partial,
expert 18% · equal 23%** — unchanged from the Sep 1 pass. The claim was true; the evidence
offered for it was not the evidence. Exactly the failure this file exists to make expensive.

## 2026-09-01 — The Aug 31 adjudication, run two days late: 2 of 3 again, and the premium had already flipped on days the window does not look at

The second scheduled adjudication of falsifier #6. The pinned window was **Monday Aug 31, 00:15 UTC**
(MAINTENANCE §2b); this pass ran on the evening of Sep 1 in Brazil (≈02:30 UTC Sep 2), about 50
hours late. It is still a clean adjudication, because every input the window uses was fixed before it
opened and none of them can be affected by looking later: the Aug 24–30 weekly candle, the Aug 30
daily closes, and the ETF figure that `data.json` carried at 00:15 UTC Monday (the Aug 30 19:08 UTC
build, through Aug 28). Nothing here was measured on the incomplete Sep 2 candles.

BTC **~$77.1K**, **−38.9%** from the ATH, day 330 of ~370 on the cycle clock (week 47 post-ATH),
week ~8.9 off the Jul 1 low of $57,800.19 and **+33.5%** above it. The Sep–Nov bottom window opened
today, which under MAINTENANCE §2 moves the research cadence to **weekly**.

**The recommendation is unchanged. Stage TOO EARLY, 0 of 4 families lit, ladder unfilled, nothing
deployed.** The probe (20%, $52–57K) and core (45%, $44–50K) tranches remain empty. Next
adjudication: **Monday Sep 7, 00:15 UTC**.

### Falsifier #6 at the Aug 31 window: 2 of 3, not fired

| Leg | Bar | Reading at the window | |
|---|---|---|---|
| 1 — weekly close | > ~$70K | **$77,682.00** (Aug 24–30 candle: $77,734 open, $81,478.87 high, $76,670.01 low) | **FIRED**, by 11% |
| 2 — Coinbase Premium | positive | **−0.0217%** raw, Aug 30 daily close (Coinbase $77,665.14 vs Binance $77,682.00); −0.0187% USDT-adjusted | **NOT FIRED** |
| 3 — ETF 4-week net | > +$1.5B | **+$3.31B** (`etf.d20` through Aug 28, the figure live at 00:15 UTC) | **FIRED** |

Same configuration as Aug 24, same leg missing, and this time the miss is not marginal: Aug 30 is
negative on both conventions and by more than three times the Aug 23 gap.

### Leg 2: the streak broke on Aug 26, and the window never saw it

Daily closes, raw convention (Coinbase `BTC-USD` ÷ Binance `BTCUSDT` − 1), USDT-adjusted alongside:

| | Aug 24 | Aug 25 | **Aug 26** | **Aug 27** | Aug 28 | **Aug 29** | Aug 30 | Aug 31 | Sep 1 |
|---|---|---|---|---|---|---|---|---|---|
| raw | −0.0141 | −0.0157 | **+0.0031** | **+0.0321** | −0.0086 | **+0.0050** | **−0.0217** | −0.0236 | −0.0521 |
| USDT-adj | +0.0109 | −0.0077 | +0.0001 | +0.0181 | −0.0076 | +0.0010 | −0.0187 | +0.0134 | +0.0019 |

**The ~99-day negative streak ended on Aug 26.** Three of the seven closes in the adjudicated week
printed positive on the governing convention — Aug 26, Aug 27 (+0.032%, the widest positive print
since May) and Aug 29 — and CoinDesk reported the flip on Aug 28 ("after nearly 100 consecutive days
underwater"). None of the three fell on the one day the window reads, the completed UTC day before
Monday. The leg therefore did not fire, and under the conventions pinned on Aug 21 that is the
correct result: the threshold text is *sustained* > 0, the window is the Monday close, and a
Wednesday–Thursday–Saturday scatter with negative prints between them is neither.

It is, however, the concrete case the deferred design review was waiting for. On Aug 21 this log
recorded that leg 1 is price, leg 3 chases price, and leg 2 is the only leg that measures a distinct
cohort; on Aug 24 and Aug 26 it deferred re-specifying the trigger because those were maximally
reactive moments. This pass is one too — re-specifying the leg to "any positive close in the week"
would fire it retroactively — so the design review **stays deferred**, and the fact that the
Monday-pinned form and a plausible weekly form now give different answers is recorded here as the
first evidence for that review rather than acted on.

Two further reads on the same table. Sep 1 printed **−0.052% raw**, the most negative close since
Aug 18 (−0.0681%), and **+0.002% adjusted**, because Coinbase `USDT-USD` closed at 0.99946 — the whole gap fits
inside the tether discount again, exactly the Aug 19 finding. And the adjusted column is positive on
six of the nine days, so on the convention that does *not* govern, the US bid has been level or
slightly ahead of the offshore one for most of a fortnight.

### The checklist moved off zero, by four ten-thousandths of SOPR

`CORE` rescored through the same `RULE` object the calibration replays, on-chain values as of
**Aug 31** (`data.json`), spot $77,142:

| Rule | Aug 26 | Today | |
|---|---|---|---|
| Puell | 0.9454 | **1.0045** | NOT YET (crossed back above 1.0) |
| MVRV-Z | 0.8757 | 0.8514 | NOT YET |
| SOPR | 1.0103 | **1.0046** | **PARTIAL** (bar < 1.005) |
| Price ÷ 200W MA | +21.8% | +19% ($64,633) | NOT YET |
| Price ÷ Realized Price | 1.49 | 1.46 ($52,672) | NOT YET |
| NUPL | 0.3302 | 0.3295 | NOT YET |
| STH-MVRV | 1.13 | 1.10 (basis $70,149) | NOT YET |
| Drawdown | −37.9% | −38.9% | NOT YET |

**Expert 4%, equal 6%** — one PARTIAL of eight after ten consecutive days at zero, against 95% at
the confirmed Nov 21, 2022 bottom. Read it for what it is: SOPR sits 0.0004 under a bar it will
recross on any up day, so this is the instrument twitching, not turning. It did break two pieces of
prose that had hard-coded the zero — the thesis paragraph's "zero, not merely low" and the README's
"0% today" — which is the drift MAINTENANCE §5 warns about; both fixed, the first by removing the
word rather than by re-typing a number the page already computes.

Across all 15 rows: **expert 18%, equal 23%**, 1 ACTIVE (`etf`), 5 PARTIAL (`hash`, `lth`, `resv`,
`fed`, `sopr`), **0 of 4 families lit → TOO EARLY**. Families: Valuation 0 of 4; Capitulation 1.0 of 5
(needs > 2.5); Supply & flows 2.0 of 5 (needs > 2.5); Macro 0.5 of 1. Rendered headless and read off
the page, not recomputed by hand.

**The expert/equal gap is now 5 points**, breaching the ~3-point note in §2b for the second pass
running. Re-derived rather than copied: the six lit rows carry weights 5, 6, 5, 3, 7 and 5 against a
mean of 6.67, so five of six sit below it and one (`fed`, 7) marginally above; their weighted mass is
18 of 100 while their count is 3.5 of 15. The sentence written on Aug 24 ("every lit row at or below
average") is no longer literally true, but the mechanism is the same: which rows happen to be lit,
not the weights. **Recorded, not acted on.**

### Hash Ribbons crossed on Aug 26 — and the row stays PARTIAL, with the reasons written down

The BGeometrics `hashribbons` series (the source the Aug 18 and Aug 24 measurements used) reads:

| | Aug 25 | **Aug 26** | Aug 27 | Aug 28 | Aug 29 | Aug 30 | **Aug 31** | **Sep 1** |
|---|---|---|---|---|---|---|---|---|
| 30d (EH/s) | 906.8 | 910.2 | 914.1 | 910.8 | 910.0 | 909.7 | 908.1 | 907.5 |
| 60d (EH/s) | 909.4 | 907.2 | 907.9 | 907.2 | 905.8 | 907.0 | 909.0 | 907.2 |
| gap | −0.29% | **+0.34%** | +0.68% | +0.40% | +0.46% | +0.29% | **−0.10%** | **+0.03%** |
| state | Down | **Up** | Up | Up | Up | Up | **Down** | **Up** |

So the 30-day average did cross above the 60-day on Aug 26, for the first time since Jun 3 — the row's
threshold text, "30d > 60d after capitulation", is literally met on seven of the last eight days. Three
things were checked on the full 1,461-day series before deciding what that is worth:

1. **The state field carries no memory.** It equals `sign(sma_30 − sma_60)` on every one of 1,461
   days, zero exceptions. "After capitulation" is the analyst's judgement, not the field's; a naive
   rule on it would have read ACTIVE for 278 straight days through 2023–24.
2. **The preceding Down stretch is the longest in the window.** Jun 3 – Aug 25 is **84 days**; the next
   longest are 52 (Jan 5 – Feb 25, 2026) and 48 (Nov 27, 2022 – Jan 13, 2023, the one that bracketed
   the last confirmed bottom). By duration this is a real capitulation. By depth it is not much of one:
   the 60-day average fell from ~925 to ~907 EH/s, about 2%.
3. **The 2022 parallel is close in timing and shape-different.** The Jan 14, 2023 cross came 54 days
   after the Nov 21 low with price +33.6% above it ($20,872 vs $15,617). The Aug 26 cross came 56 days
   after the Jul 1 low with price +36.7% above it ($79,024 vs $57,800). But 2022's Down began on Nov 27,
   *after* the low, and this one began on Jun 3, four weeks *before* it — the ribbons capitulated into
   the low in 2026 and out of it in 2022. The parallel belongs in the counter-scenario ledger below;
   it does not settle the row.

Persistence was tested as a candidate rule and **rejected**: the Feb 26 – Mar 25, 2026 Up held 28
days and still preceded the July low by three months, while the Jan 3–4 Up (two days, +0.01%) is the
known misfire. No run length in the series separates the crosses that held from the ones that did
not, so no prospective rule is pinned this pass. The row stays **PARTIAL** on a reading the tooltip
already anticipated — the state whipsawed on Aug 31 and sits +0.03% from flipping again — and the
card now says the cross printed rather than "precondition converging". Note the stage would not move
even at ACTIVE: Capitulation would read 1.5 of 5 against a strict 2.5. The decision is not
load-bearing, which is the right kind of decision to leave on the conservative side.

Difficulty: the next retarget is estimated for ~Sep 5 at **+1.10%** (mempool.space, read at the time
of this pass), against −0.94% on CoinWarz. The card's last projection (+0.45% for Aug 23) printed
−1.31%, so the figure is quoted with its source and not leaned on.

### Strategy resumed buying, which reverses the Jul 24 finding

Verified against the 8-Ks, not the coverage. **Aug 24 8-K:** no bitcoin bought or sold Aug 17–23,
holdings 840,447 BTC. **Aug 31 8-K:** **4,603 BTC bought for $369.7M at $80,318** between Aug 24 and
30, funded from the ATM (4,531,421 MSTR shares, ~$602.8M), taking holdings to **845,050 BTC** at an
aggregate cost of $63.73B, average $75,412. Coverage adds that $151.8M of the same proceeds bought
STRC back and $50.7M paid STRC dividends; a public tracker quotes mNAV ~1.02× on the EV definition
(basic mNAV, which this report last measured at ~0.66× on Aug 19, was not re-measured).

This is the first purchase since the selling began in late June, at a price above the treasury's own
average, in a week when the equity traded at a premium again. The Jul 24 entry named Strategy "a
structural seller" and armed the capitulation gate on it; the Aug 19 entry recorded the first paused
week as "the first evidence the sales are discretionary rather than forced". A $370M purchase is the
second piece of that evidence and the stronger one. Consequences:

- The `mac` catalyst row moves from *headwind / emerging* to **mixed / de-armed for now**. The
  dividend run-rate ($1.76B annualised) has not changed and the mechanism has not gone away, but a
  forced seller does not buy at $80K.
- The capitulation tranche's crypto-native gate steps back a second time: **partially armed → armed
  in name only** until a forced sale reappears. It still requires funding z < −2, which is nowhere
  near (see below).
- Falsifier #4's named mechanism, leveraged corporate-treasury liquidation, is **less live** than at
  any point since June.
- This cuts toward the counter-scenario and is entered in its ledger as such.

Also checked and rejected as catalysts: the ~$15B August contraction in stablecoin supply (USDT
~$189B → $183.2B, USDC ~$80B → $72.1B, attributed to the GENIUS Act yield ban pushing balances into
tokenised Treasuries). Both stayed within 12bp of par; that is redemption, not a depeg. No exchange
failure, no exploit above the $500M bar, no Mt. Gox movement in the week.

### Macro moved against liquidity, and the composite's dollar leg is the fragile one

The composite still reads **2 of 3, PARTIAL**, re-derived from `data.json`: M2 y/y 5.41% against
4.53% (3m) and 4.06% (6m), accelerating ✓; broad USD 118.75 vs a 119.55 200-day, below ✓; real 10-year
2.42% vs a 2.04 200-day, above ✗. Two things about that reading:

- **The dollar leg is 0.7% from flipping.** If `DTWEXBGS` closes above its 200-day the composite goes
  to 1 of 3 and `fed` goes OFF — the Macro family's only row.
- **The real 10-year is 5bp from its two-year high** (2.47%). The nominal 10-year hit 4.73% on Aug 28
  in FRED and, per Bloomberg, **topped 4.75% on Aug 31 with a 4.80% high, the highest since January
  2025**; the 2-year is 4.34% against a 3.82 200-day and a 4.40 two-year high.

What moved it, dated: **July PCE on Aug 26** — headline 3.7% y/y, core 3.3%, income and spending both
above forecast. **BLS preliminary benchmark on Aug 28: −79K** (−0.1%), private payrolls −178K — the
revision flagged in advance as large turned out small. **Brent above $90 on Aug 31** after the first
exchange of fire in the Strait of Hormuz in about a month (a US strike on an island; Iranian attacks
on the UAE and Jordan). Sep 15–16 FOMC pricing is now **source-dependent**: Kalshi on Aug 31 prices a
25bp hike at ~59% and a hold at ~38%; CME FedWatch on Aug 25 read a hold at ~58.6%. Those are
different instruments six days apart across an oil-driven yield spike and are not spliced into the
"~62% → ~38% → ~32%" series the Fed trigger card was carrying — that series is retired from the card
and the card now says a hike is at least an even-money proposition in one market. Whatever the exact
number, the direction is the opposite of the last three passes: the Fed trigger moved **further away**.

Net liquidity: $5,779.5B on Aug 26, below its 4-week ($5,824.8B), 13-week ($5,872.2B) and 52-week
($5,978.6B) averages, with the TGA at $950.7B ahead of the Sep 9 buyback enlargement. Credit: HY OAS
2.63% against a 2.59% two-year low — still no stress, still a depth signal only.

### ETF flows: the quarter turned positive

At the window `etf.d20` was +$3.31B; it is **+$3.35B** now (through Aug 31), with the 5-day at +$0.80B.
**The 60-day is +$0.58B, positive for the first time since the outflow regime began** — the "sharp
reversal inside a still-negative quarter" caveat of Aug 24 and 26 no longer holds and is removed from
the ETF trigger card. YTD −$1.77B, cumulative $54.8B, AUM $99.6B. The daily texture: Aug 25 +$314M,
a nine-session inflow run ended by **−$202M on Aug 28** (the day of the intraday reversal), +$217M on
Aug 31 with IBIT +$206M. Week of Aug 24–28: +$925M.

### The bounce peaked at +41.0% in week 8.3 — the exact week the 2022 rally topped

$81,478.87 on Aug 28, **+40.96%** off $57,800.19, 58 days (week 8.3) off the low. The 2022 bear rally
topped at +43.1% in week 8.3; 2018's at +45.7% in week 3.9. The pre-registered marker is +45.7%
(~$84.2K) and the gap to it is **4.7 points**, from 5.1 on Aug 26. Aug 28 was also an outside
reversal: $80,250 open, $81,479 high, $76,888 low, $77,846 close (−3.0%), which coverage attributed to
a short squeeze into Jackson Hole and profit-taking out of it. The Aug 24–30 week closed flat, −0.07%.

**Not called a top.** Four sessions after a spike is not enough to say the rally has ended, and the
Aug 24 entry's rule is that the marker governs in both directions: the number does not go up because
price approaches it, and it does not go down because price backs away from it.

### The counter-scenario is held at 40%, and this time the ledger is two-sided

For the counter-scenario since Aug 26: Strategy back as a buyer (the strongest item); three positive
premium closes; the ribbon cross with its 2022 timing parallel; the 3-month ETF figure turning
positive; the trigger reading 2 of 3 for a second Monday. Against it: the rally peaked at the
precedent week and reversed intraday; macro tightened on every axis the report tracks (nominal and
real yields, oil, hike odds); the premium is back to its most negative raw close since Aug 18;
Polymarket is flat at ~74% for the third read with the upside rungs repriced *down*; the checklist's
only movement was toward the base case, and that by a rounding error.

The market: Gamma API snapshot at the time of this pass, open contracts only — ↓$60K **28.5%** (29.5),
↓$55K **23.5%** (22.5), ↓$50K 15.5% (16.5), ↓$45K 7.5% (9.5), ↓$40K 6.5% (7.5); interpolated at the
$57,800 low, ~26%, so the low-is-in read is **~74%**, unchanged from Aug 24 and Aug 26. Upside: ↑$85K
**61.5%** (68.5), ↑$90K **44.5%** (48.5), ↑$95K 31.5% (37.5), ↑$100K 22%. Two rungs not quoted before
are worth having: ↓$70K **59%** and ↓$75K **86.5%** — the market's median path for the rest of 2026
revisits $70K, which is the leg-1 bar.

Held at **40%**. The arguments roughly cancel, the marker is uncrossed, and the market has not moved.
Re-deriving the number on a mixed week would be the drift the Aug 24 entry was written to prevent.

### Supporting reads

- **Funding** 7-day average **+0.0081%/8h** (~+8.8% annualised), last +0.0080%; still at or near the
  cap, still on the wrong side of the row's −0.005% bar by nearly three times its magnitude. Funding
  z < −2, the capitulation tranche's second condition, is not in sight.
- **Fear & Greed** 73 (Aug 24) → 74 → 65 → 71 → 73 (Aug 28) → 68 → 69 → 62 (Aug 31) → 69 (Sep 1).
  Greed on every print.
- **Aggressive-buy triggers**: still **1 fired · 1 partial · 2 not fired**. ETF fired and extended;
  hash PARTIAL with the cross now printed; premium NOT FIRED but no longer a streak; Fed moved away.

### Other falsifiers, cross-checked

**#1** (new ATH) — $126,296, far off. **#2** (above ~$90K for eight consecutive weeks with fewer than
three families lit) — high $81,479, not in play; Polymarket ↑$90K 44.5%. **#3** (week 70 = Feb 2027)
— not due. **#4** (low below $30K) — not in play, and its named mechanism weakened this week (above).
**#5** (bottom confirmed on fewer than 8 of 15) — not in play.

### What was deliberately not changed

- **No threshold, no weight, no `BS_W`, no `CORE` membership, no ladder band, no probability.**
- **The premium convention and window.** Raw governs, Monday close adjudicates. The streak-break is
  evidence for the deferred design review, not a reason to run it now.
- **`hash` stays PARTIAL** and no persistence rule was pinned, for the reasons measured above.
- **`sthmvrv`'s ≤0.80 threshold** stays under prospective review, unchanged.
- **`lth` and `resv`** carry their Aug 19 readings; nothing dated to this week was found for either,
  and they are SLOW rows on a 2–4 week cadence. `resv` is still blocked on the paywalled endpoint.
- **The bottom window and ladder bands.** The one vector on the window still points later, not
  earlier (Jul 25 entry); nothing this week touched it.

### Stale-number sweep, per the Aug 26 procedure

Searched the file for the previous pass's headline figures — `+40.6%`, `81,273`, `3.03B`, `−0.016%`,
`Aug 25`, `next adjudication is Monday Aug 31`, `−1.30B`, `still negative`, `~32%`, `week to Aug 16`,
`840,447`, `0% today`, `not merely low` — and checked each hit is a dated statement or a fix. The
research tag moves to **Sep 1, 2026** in all three languages, because this pass refreshed narrative
rows (Strategy, Fed pricing, rates, events) and not only the trigger cards.

**Carry into the next pass (Sep 7 window):** whether the ribbon state holds Up through the week or
whipsaws again; whether the premium prints positive on a *Sunday* close; the ~Sep 5 retarget against
the +1.10% estimate; the Sep 9 buyback start and its effect on the TGA and net liquidity; whether
`DTWEXBGS` crosses its 200-day (the composite's fragile leg); the Sep 15–16 FOMC as the first dated
event inside the window, with a hike now a live outcome; and Strategy's Sep 8 8-K — a second week of
buying makes the de-arming a pattern.

---

## 2026-08-26 — Interim check: the two live legs moved in opposite directions, and nothing changed

Not an adjudication. The pinned window for falsifier #6 is Monday 00:15 UTC (MAINTENANCE §2b);
the next one is **Aug 31**. This is the between-Mondays read the Aug 24 entry's cadence implies
now that the Sep–Nov bottom window is six days out, and it is written down mainly to record two
things that moved and one thing that deliberately did not.

BTC **~$78.4K**, **−37.9%** from the ATH, week 46 post-ATH, week ~7.9 off the Jul 1 low of
$57,800.19 and **+35.6%** above it.

**The recommendation is unchanged. Stage TOO EARLY, 0 of 4 families lit, ladder unfilled,
nothing deployed.** The probe (20%, $52–57K) and core (45%, $44–50K) tranches remain empty.

### Falsifier #6: still 2 of 3, but not the same 2-of-3

| Leg | Bar | Aug 24 | Aug 26 | |
|---|---|---|---|---|
| 1 — weekly close | > ~$70K | $77,734.00 | $77,734.00 (Aug 17–23 still the last closed week) | **FIRED** |
| 2 — Coinbase Premium | positive | −0.0060% (Aug 23) | **−0.0157%** (Aug 25 close) | **NOT FIRED** |
| 3 — ETF 4-week net | > +$1.5B | +$2.32B | **+$3.03B** | **FIRED** |

**Leg 3 extended and is no longer near its bar at all.** `etf.d20` is **+$3.03B**, twice the
+$1.5B threshold, with the 5-day at +$2.08B. The 60-day roughly halved its deficit in two days,
−$2.31B → **−$1.30B**, and YTD −$2.91B → −$2.25B. The quarter is still negative; the month is
emphatically not.

**Leg 2 moved away, which is the finding.** Daily closes on the raw convention:

| | Aug 21 | Aug 22 | Aug 23 | Aug 24 | Aug 25 | Aug 26* |
|---|---|---|---|---|---|---|
| raw | −0.0159 | −0.0266 | **−0.0060** | −0.0141 | **−0.0157** | −0.0113 |
| USDT-adj | −0.0019 | +0.0034 | +0.0070 | +0.0109 | **−0.0077** | −0.0073 |

\* Aug 26 is an incomplete candle and does not count for anything; shown so the direction is not
read off one day.

Aug 23 was the closest to a flip in ~96 days and it has not been beaten since. Note **Aug 25 is
negative on *both* conventions** — only the second such day in this streak (Aug 21 was the
first). Two days ago the interesting fact about this leg was that the two conventions disagreed
by 1.3bp and the pinning decided the call; today they agree, in the direction of not firing.

**Method validated before use, as on Aug 24.** The same measurement reproduces every figure this
log has published: raw −0.0743 (Aug 17), −0.0681 (Aug 18), −0.0502 (Aug 19), −0.0182 (Aug 20),
−0.0060 (Aug 23); adjusted +0.0198, +0.0089, +0.0108, +0.0068, +0.0070 on the same days.

### A wording error found in the process: *divide* should be *multiply*

MAINTENANCE §2b and the Aug 24 entry both describe the USDT-adjusted premium as "the Binance leg
**divided** by Coinbase `USDT-USD`". Reproducing the table above shows that only **multiplying**
gives the published numbers — which is also the economically correct conversion, since a
`BTCUSDT` price times the USD value of a tether is a BTC price in dollars:

> Aug 23: 77,734.00 × 0.99987 = 77,723.90 USD; 77,729.36 ÷ 77,723.90 − 1 = **+0.0070%** ✓
> Dividing instead gives 77,744.10, and the premium reads **−0.0189%** — wrong sign.

Nothing material turns on it: raw governs, adjusted is context, and adjusted has never
adjudicated anything. But it is the same class of error as the +48% precedent corrected on Aug 24
— *a number, or here a formula, repeated across passes is not thereby verified* — and the arithmetic
was always being done correctly while the prose described something else. §2b is corrected
prospectively; the Aug 24 entry is left unedited as the dated record of what was written then.

### The checklist has not moved

`CORE` rescored through the same `RULE` object the calibration replays, on-chain values as of
**Aug 25** (the published date in `data.json`), at spot $78,399:

| Rule | Aug 24 | Today | |
|---|---|---|---|
| Puell | 0.9562 | 0.9454 | NOT YET |
| MVRV-Z | 0.8611 | 0.8757 | NOT YET |
| SOPR | 1.0076 | 1.0103 | NOT YET |
| Price ÷ 200W MA | +20.9% | +21.8% ($64,344) | NOT YET |
| Price ÷ Realized Price | 1.48 | 1.49 ($52,548) | NOT YET |
| NUPL | 0.3188 | 0.3302 | NOT YET |
| STH-MVRV | 1.13 | 1.13 (basis $69,205) | NOT YET |
| Drawdown | −38.5% | −37.9% | NOT YET |

**Expert 0%, equal 0%** — zero ACTIVE, zero PARTIAL of eight, a fifth consecutive day, against 95%
at the confirmed Nov 21, 2022 bottom. Six of the eight drifted *further* from their thresholds;
only Puell moved toward one, and it is still above its PARTIAL bar. Across all 15 rows: **expert
16%, equal 20%**, 1 ACTIVE (`etf`), 4 PARTIAL (`hash`, `lth`, `resv`, `fed`), **0 of 4 families lit
→ TOO EARLY**. The expert/equal gap is still 4 points, still the small-numbers artefact diagnosed
Aug 24; nothing was changed.

The macro composite was re-derived rather than assumed: M2 y/y 5.41% against 4.53% (3m) and 4.06%
(6m) — accelerating ✓; broad USD 118.06 vs a 119.63 200-day — below ✓; real 10-year 2.38% vs a
2.03% 200-day — **above ✗**. Two of three, PARTIAL, unchanged.

### The counter-scenario is held at 40%, and the reason is the marker

The bounce peak rose from **+37.5%** (Aug 21 high, $79,500) to **+40.6%** ($81,272.62 on Aug 25,
week ~7.9 off the low). Against the precedent envelope — +45.7% by week ~3.9 in 2018, +43.1% by
week ~8.3 in 2022 — we are now level with the week the 2022 rally topped and **2.5 points below
its magnitude**. That is the tightest this comparison has been, and the gap to the pre-registered
marker has closed from **8.2 points to 5.1** in two days.

**It still does not move the number, and that is the point.** The Aug 24 entry wrote the marker
down "prospectively, so it is not re-derived later at whatever level price happens to be." A
probability that ratchets up every time price makes a marginal new high *is* that re-derivation,
performed two days at a time. The marker is +45.7% (~$84.2K) and it has not been cleared. When it
is, the number goes most of the way to the market's; until then it is 40%.

Three further reasons not to move it this pass, none of which is the checklist:

1. **The market did not move either.** Polymarket, same-day snapshot Aug 26, Gamma API, open
   contracts only: ↓$60K **29.5%** (was 30%) and ↓$55K **22.5%** (was 21.5%), which interpolates at
   the $57,800 cycle low to ~26.4% — so the market prices the low already being in at **~74%**,
   the same ~74% as Aug 24 after moving ~12 points in the five days before that. Price printed a
   new rally high on Aug 25 and the read did not budge.
2. **Underneath that flat headline the deep rungs moved *against* the counter-scenario.**
   P(<$50K) went 11.5% → **16.5%** and P(<$45K) 8.5% → 9.5%. This report's $44–50K core zone is
   priced slightly *more* likely than it was two days ago. Upside: ↑$80,000 settled YES on Aug 24
   (so it leaves the card, like ↑$70K and ↑$75K before it); the nearest open rung ↑$85,000 is
   68.5%, ↑$90,000 **48.5%**, ↑$95,000 37.5%.
3. **The one leg of the trigger that measures institutional demand rather than price moved the
   wrong way.** Leg 1 is price and leg 3 is a flow confirmation that chases price — the Aug 21
   entry established both, before either fired. Leg 2 is the discriminating one, and it is
   further from firing than it was on Monday.

Symmetrically, the 0% checklist is again **not** counted as evidence for the base case, for the
reason recorded Aug 24: every one of those eight rules is a function of price or of a realized-cap
ratio that price moves, so a rally that argues for the counter-scenario also darkens the
checklist. Counting both would be counting one price move twice.

### Supporting reads

- **Funding** 7-day average **+0.0090%/8h** (~+9.9% annualised), from +0.0079% on Aug 24 — still
  pinned at or near the +0.0100% cap, and still on the wrong side of the row's −0.005% bar by
  nearly three times the threshold's magnitude.
- **Fear & Greed** 73 (Aug 24) → 74 (Aug 25) → **65** (Aug 26). Greed throughout; the pullback
  from the high is the only supporting read that moved toward the base case.
- **Puell** 0.9562 → **0.9454**, still above the 0.9 PARTIAL bar.
- **Aggressive-buy triggers** unchanged at **1 fired · 1 partial · 2 not fired**; the two halves
  moved in opposite directions (ETF extended, premium retreated) without changing the tally.

### Other falsifiers, cross-checked

**#1** (new ATH) — $126,296, far off. **#2** (above ~$90K for eight consecutive weeks with fewer
than three families lit) — high $81,273, not in play, and still the one to watch if the rally
extends, since families lit is 0 and Polymarket puts ↑$90K at 48.5%. **#3** (week 70 = Feb 2027) —
not due. **#4** (low below $30K) and **#5** (bottom confirmed on fewer than 8 of 15 signals) — not
in play.

### What was deliberately not changed

- **No threshold, no weight, no `BS_W`, no `CORE` membership, no ladder band, no probability.**
- **The premium convention.** Raw governs; the two conventions now agree anyway.
- **The trigger's design review** stays deferred, per Aug 21 and Aug 24. Two days after it missed
  and then moved away is no better a moment to re-specify it than the day it missed.
- **`sthmvrv`'s ≤0.80 threshold** stays under prospective review, unchanged.
- **Not a full research refresh.** The narrative `mac` rows, `lth`, `resv` and `hash` carry their
  Aug 19/24 snapshots; they are on a 2–4 week cadence and are not due. Refreshed here: `cbp`,
  `fund`, `puell`, the ETF and premium trigger cards, `trig_n`, the Polymarket card, `th_p`, the
  bear-rally calibration note in `ph_notes[2]` and the adjudication line in `fal[5]`.
  `hash` was **not** re-measured — its Aug 24 reading (30d 910.3 EH/s vs 60d 916.1, −0.63%) stands
  and the card says so.

### A sweep the Aug 24 pass should have run, and this one did

Two keys outside the ones being edited still carried the bounce peak as **+34% / +37.5% / $79,500
intraday Aug 21** presented as the *current* reading: `ph_notes[2].tip` (the bear-rally calibration
note, which the Aug 24 pass corrected for peak-to-peak form but left at the old level) and, less
seriously, a prose "48% above Realized Price" that is now 49%. `fal[5]` told the reader the trigger
stood where it did on Aug 24 while `th_p` said otherwise two paragraphs away. All three fixed.

Generalising the Aug 21 doc-sync finding and the Aug 24 +48% correction into something runnable:
**after editing the keys a pass is about, grep the file for the previous pass's headline numbers**
— here `+34%`, `37.5%`, `79,500`, `2.32B` — and check each hit is a *dated* statement rather than a
current one. Dated references ("peaked at +37.5% on Aug 21", "P(<$55K) was 37.5% on Aug 19") are
correct and must stay; the same digits presented as today's reading are the bug. The four searches
took a minute and found two real staleness bugs, one of them in the exact note the previous pass
had touched.

---

## 2026-08-24 — The adjudication: two legs fired, the third missed by 0.6 basis points

The scheduled check the Aug 21 entry deferred to. Run at **00:15 UTC Monday Aug 24**, the
window that entry pinned, against the measurement conventions it wrote down *before* the
answer was visible (MAINTENANCE §2b). BTC ~$77.7K, **−38.5%** from the ATH, week 46
post-ATH, week ~7.7 off the Jul 1 low of $57,800 and **+34.5%** above it.

**Result: 2 of 3 legs. Falsifier #6 does not fire. Nothing is deployed.** The probe (20%,
$52–57K) and core (45%, $44–50K) tranches remain unfilled, as before.

### The three legs, measured

| Leg | Bar | Reading | |
|---|---|---|---|
| 1 — weekly close | > ~$70K | **$77,734.00** (Aug 17–23 candle, $62,900 open, $79,500 high) | **FIRED**, by 11% |
| 2 — Coinbase Premium | positive | **−0.0060%** raw, daily close Aug 23 | **NOT FIRED** |
| 3 — ETF 4-week net | > +$1.5B | **+$2.32B** (`etf.d20`, through Aug 21) | **FIRED** |

Leg 1 is not a squeaker: the candle closed 11% above the bar, and the report's own
$70,000 level was tagged, cleared and held for five sessions.

Leg 3 is no longer marginal either, which is the change from Friday. On Aug 21 it read
**+$1.77B** with ~$1.12B of that two days old, and the entry recorded that a rolling
window barely over its bar can fall back under as large days roll off. It did the
opposite: **+$2.32B**, with the 5-day at +$1.92B. The 60-day is still **−$2.31B** and YTD
**−$2.91B**, so this is a sharp reversal inside a still-negative quarter, not a trend.

### Leg 2 is the whole adjudication, and it turned on the convention pinned Friday

Coinbase `BTC-USD` daily close Aug 23 **$77,729.36** against Binance `BTCUSDT` daily close
**$77,734.00**: **−0.0060%** on the raw convention. Six thousandths of one percent — $4.64
on a $77.7K coin.

On the **USDT-adjusted** convention (Binance leg divided by Coinbase `USDT-USD` close,
0.99987) the same day reads **+0.0070%** — *positive*. Reported as context, and it does
not adjudicate.

So the pinning did exactly the work it was written to do, and it is worth stating plainly
because this is the case it was written for. The Aug 21 entry said: *"Switching now, when
adjusted is the side closer to firing, would be that same retro-edit pointed the other
way."* Two days later the adjusted convention is the one that fires and the raw one is not,
and the gap between them is 1.3bp. Had the convention not been fixed in advance, 65% of the
ladder would have been deployed on a choice made while looking at the answer.

**Method validation.** The same measurement reproduces the figures this log has quoted all
along: −0.0681% (Aug 18) against the −0.068% published, −0.0502% (Aug 19) against −0.050%,
−0.0182% (Aug 20) against −0.018%. The streak, on daily closes:

| | Aug 17 | Aug 18 | Aug 19 | Aug 20 | Aug 21 | Aug 22 | Aug 23 |
|---|---|---|---|---|---|---|---|
| raw | −0.0743 | −0.0681 | −0.0502 | −0.0182 | −0.0159 | −0.0266 | **−0.0060** |
| USDT-adj | +0.0198 | +0.0089 | +0.0108 | +0.0068 | −0.0019 | +0.0034 | **+0.0070** |

~96 days negative on the raw convention. Note Aug 21 is negative on *both* — the two
conventions do not simply sit on opposite sides of zero, they cross each other.

### The checklist went to zero

Rescoring the 8-rule `CORE` subset through the same `RULE` object the calibration replays,
on-chain values as of **Aug 22** (the published date in `data.json`) at spot:

| Rule | Aug 21 | Today | |
|---|---|---|---|
| Puell | 0.8743 | **0.9562** | PARTIAL → NOT YET |
| MVRV-Z | 0.6907 | 0.8611 | NOT YET |
| SOPR | 1.0181 | 1.0076 | NOT YET |
| Price ÷ 200W MA | +20.9% | +20.9% ($64,219) | NOT YET |
| Price ÷ Realized Price | 1.50 | 1.48 ($52,415) | NOT YET |
| NUPL | 0.3314 | 0.3188 | NOT YET |
| STH-MVRV | 1.15 | 1.13 (basis $68,327) | NOT YET |
| Drawdown | −38.0% | −38.5% | NOT YET |

**Expert 5% → 0%, equal 6% → 0%.** Zero ACTIVE, zero PARTIAL, against 95% at the confirmed
Nov 21, 2022 bottom. Puell crossing 0.9 on Aug 22 took the last PARTIAL. The full daily
trace: 44% (Aug 13–16) → 36% (17–18) → 21% (19) → 5% (20–21) → **0% (22–24)**.

**This is not the first 0% and that was checked rather than assumed.** The same eight rules
printed 0% on Oct 7–9 and Oct 26–28, 2025. The honest statement is therefore the sharper
one: *the checklist reads exactly the same today, at $77.7K and −38.5% in week 46, as it did
at $114K and −10% in week 3.* Every rule is a function of price or of a realized-cap ratio
that price moves, so a 34% rally erases the whole signal. That is a property of the
instrument, and the reason the report publishes an ordinal stage rather than this number.

Across all 15 rows: **expert 16%, equal 20%**, 1 ACTIVE (`etf`), 4 PARTIAL (`hash`, `lth`,
`resv`, `fed`), **0 of 4 families lit → TOO EARLY**.

### A finding MAINTENANCE asks to investigate: expert and equal now differ by 4 points

§2b says the two scores "currently agree to within ~3 points" and that material divergence
"is a finding to investigate, not a number to pick between." At 16 vs 20 it is 4. Checked:
it is a small-numbers artefact, not a structural break. The mean weight is 6.67; the single
ACTIVE row (`etf`) carries 5, and three of the four PARTIALs carry 5, 3 and 6. Every row
that is lit at all is at or below average weight, so equal-weighting flatters by
construction. With one active signal out of fifteen there is no arrangement of weights that
would not produce a gap of this order. **Recorded, not acted on** — no weight changed.

### Supporting reads, all moving the same way

- **Fear & Greed 31 (Aug 17) → 73 (Aug 24)**, Greed. Seven days.
- **Funding pinned at the +0.0100%/8h cap** for six consecutive intervals; 7-day average
  +0.0079%/8h, ~+8.6% annualised. The `fund` row's bar is *−0.005%*; it is on the wrong side
  of zero by nearly three times the threshold's magnitude.
- **Hash ribbons re-measured** (BGeometrics, same source and method as Aug 18, which
  reproduces at 911.8/925.6): as of Aug 22, 30-day **910.3 EH/s** against 60-day **916.1**,
  gap **−0.63%**. Still no cross; row stays PARTIAL.
- **A correction:** the trigger card projected the ~Aug 22 retarget at **+0.45%**. It printed
  **−1.31%** on Aug 23 (125.807T from 127.480T, mempool.space). Hashrate fell over the epoch.
  This is the one supporting read that moved *toward* the base case, and it is small.

### Polymarket, refreshed — and the card has been measuring the wrong level

Gamma API, same-day snapshot Aug 24 (`what-price-will-bitcoin-hit-before-2027`, open
contracts only, per the sourcing procedure in MAINTENANCE §2):

| | Aug 19 | Aug 24 |
|---|---|---|
| P(dip < $55K) | 37.5% | **21.5%** |
| P(dip < $50K) | 25% | **11.5%** |
| P(dip < $45K) | 17.5% | **8.5%** |
| P(dip < $40K) | 12.5% | **6.5%** |
| P(dip < $60K), re-listed | ~53% | **30%** |
| P(reach $80K) | 54% | **89.5%** |
| P(reach $85K) | 38% | **69.5%** |
| P(reach $90K) | 24% | **49%** |

`↑ $75,000` settled YES on Aug 21, so it leaves the card the way `↑ $70,000` did on Aug 19;
the nearest still-open upside rung is now `↑ $80,000`.

**Methodology fix.** The card and `th_p` have been quoting the market's no-new-low read as
`1 − P(<$55K)`, which today would be 78.5%. That measures the wrong level: the cycle low is
**$57,800**, so a new low needs the price below $57.8K, not below $55K. The two rungs that
bracket it are ↓$60K at 30% and ↓$55K at 21.5%; interpolating to $57.8K gives **~26%**, so
the market prices "the low is already in" at **~74%**, not 78.5%. The old figure overstated
the market by ~4 points in the direction of the counter-scenario. Corrected on the card.

### The counter-scenario moves 30% → 40%

The legs govern capital and they did not complete. The probability tracks evidence and it
has to move, on the Aug 19 precedent — that pass moved 25% → 30% with *zero* legs fired.

What is new since:

1. **Two of the three pre-registered legs are fired**, and neither marginally. The weekly
   close cleared its bar by 11%; the flow leg went from $1.77B (barely over, two days of it)
   to $2.32B (no longer one roll-off from failing). This report wrote those legs down as its
   own definition of what would confirm the counter-scenario. Two thirds of that definition
   is now satisfied.
2. **The market moved ~12 points** on the same evidence, from ~62% to ~74% on the corrected
   measure above.
3. **The `resv`/`lth` supply story has not recovered** to argue against it, and the Fed is
   still not the source of the liquidity impulse — both noted Aug 19, both unchanged.

What holds it at 40% rather than at the market's 74% is one thing, and it is measured
rather than argued, and it is measured **peak-to-peak**, which is the only apples-to-apples
form: **this bounce peaked at +37.5% on Aug 21 (week ~7.3), against +45.7% by week ~3.9
($5,827 on Jun 28 → $8,492 on Jul 25, 2018) and +43.1% by week ~8.3 ($17,622 on Jun 18 →
$25,211 on Aug 15, 2022)** — the two bear rallies that preceded lower lows. We are inside
that envelope and at almost exactly the point on the clock where the 2022 rally topped. The
envelope has not broken — but note the peak-to-peak comparison is *tighter* than the
spot-to-peak form used on Aug 21: +37.5% against +43.1% is much closer than +34% against
+43% made it look.

Two things deliberately **not** counted in the derivation:

- **The 0% checklist is not evidence for the base case here.** It is a mechanical
  consequence of the same rally, as the section above shows. Reading it as independent
  confirmation would be counting one price move twice, in opposite directions.
- **The trigger's own weakness is not counted against the counter-scenario either.** The
  Aug 21 entry established that leg 1 is price (a bear rally is a price move) and leg 3 is a
  lagging confirmation untestable against 2018/2022 because spot ETFs did not exist. That
  argument was recorded *before* the legs fired and it still stands — but it is a reason not
  to treat 2-of-3 as decisive, which is why the number is 40% and not 60%, rather than a
  reason to ignore the legs.

**The gap between 40% and the market's ~74% is now the thing to watch.** Its entire content
is the precedent envelope. If this bounce clears **+45.7%** — roughly **$84.2K** — without a
lower low, that argument is spent and the probability should go most of the way to the
market's.
Written down now, prospectively, so it is not re-derived later at whatever level price
happens to be.

### What was deliberately not changed

- **The trigger's design.** The Aug 21 entry recorded that falsifier #6 is a weak
  discriminator and that a later pass should revisit its *design* prospectively. The pass in
  which it missed by 0.6bp is the maximally reactive moment to do that, in either direction.
  Deferring again is the discipline, not an oversight.
- **The premium convention.** Raw governs. Adjusted is context. See above.
- **No threshold, no weight, no `BS_W`, no `CORE` membership, no ladder band.**
- **`sthmvrv`'s ≤0.80 threshold** stays under prospective review, unchanged, per §2b.
- **Not a full research refresh.** The narrative `mac` rows and the `lth`/`resv` readings
  carry their Aug 19 snapshot; they are on a 2–4 week cadence and are not due. Refreshed here
  only: the four trigger cards, `cbp`, `hash`, the Polymarket card and `th_p`.

### A rendering bug found while verifying this entry

`th_p` needed to state the drawdown twice — once in the opening sentence and again in the
sentence about the checklist reading the same now as it did at $114K. The second one
rendered as a literal **`{1}`** on the live page. Cause: `tf()` substituted placeholders
with `String.replace` and a *string* pattern, which replaces only the first match, so any
key reusing a placeholder silently printed the raw token. No existing key had ever reused
one, so the bug had never fired.

Fixed at the helper rather than by rewording, because rewording would have left the trap
for the next pass. `tf()` now uses `split`/`join`, which also removes a second latent
problem: `replace()` gives `$&`, `` $` `` and `$'` special meaning **in the replacement
value**, and several of the values passed here are prices like `$77,448`. Verified by
rendering the page headless and confirming zero `{n}` tokens survive anywhere outside the
inline script source.

### Correction, same day: the +48% precedent figure is not reproducible

The derivation above was first written against **+48% at week ~4½** for the 2018 bear rally,
the figure this log and `index.html` have carried since before this pass. It was checked
against the sources rather than inherited, because it had just been promoted from background
colour into a **pre-registered prospective marker** ("if the bounce clears +48% (~$85.5K)…"),
and a marker measured wrong is worse than no marker.

Measured interim-low to rally-high, on one consistent index at a time:

| | Binance `BTCUSDT` | Coinbase `BTC-USD` |
|---|---|---|
| 2018 | $5,827 (Jun 28) → $8,492 (Jul 25) = **+45.7%**, 3.9 wk | $5,777 (Jun 24) → $8,488 (Jul 24) = **+46.9%**, 4.3 wk |
| 2022 | $17,622 (Jun 18) → $25,211 (Aug 15) = **+43.1%**, 8.3 wk | $17,567 (Jun 18) → $25,215 (Aug 15) = **+43.5%**, 8.3 wk |

**No single index produces +48%.** The origin is visible in the report's own wording: the
"precedent is exact" passage read *"the Jun 2018 flush to $5,750 rallied 48% to $8,492"*.
$8,492 is Binance's high, but $5,750 is neither venue's low. A low from one source divided
into a high from another gives +47.7%, rounded to 48%. 2022 was never wrong — all four of its
figures reproduce on both venues.

Two things changed as a result, and both cut **against** the report's own base case, which is
the test of whether a correction is motivated:

1. **The marker drops to +45.7% (~$84.2K)** from +48% (~$85.5K). The level at which the base
   case's last argument is declared spent is now **$1.3K closer**, not further away.
2. **The comparison is now peak-to-peak.** Setting cycle 4's *current* price against the
   precedents' *peaks* flattered the base case: +34% against +43% reads like room left, while
   +37.5% (the Aug 21 high) against +43.1% is most of the way there. Corrected in `th_p` and
   in the bear-rally calibration note, both of which carried the spot-to-peak form.

Older entries keep +48% on the record, unedited — they are the dated statement of what was
concluded then. `index.html`, `MAINTENANCE.md` and this entry carry the measured figures.
Process note, generalising the Aug 21 doc-sync finding: **a number repeated across passes is
not thereby verified.** This one survived several passes as prose and was only checked when it
was asked to carry weight.

### Other falsifiers, cross-checked

Checked so this pass does not adjudicate one condition while another quietly fires.
**#1** (new ATH) — $126,296, far off. **#2** (above ~$90K for eight consecutive weeks with
fewer than three families lit) — price $77.7K, high $79,500; not in play, and it is the one
to watch if the rally extends, since families lit is 0. **#3** (week 70 = Feb 2027) — not
due. **#4** (low below $30K) and **#5** (bottom confirmed with fewer than 8 of 15 signals)
— not in play. Aggressive-buy triggers: **ETF flows moved NOT FIRED → FIRED** at +$2.32B,
so that tally goes from 0 fired · 1 partial · 3 not fired to **1 fired · 1 partial · 2 not
fired** — the first of the four ever to fire.

---

## 2026-08-21 — The first leg of the deploy trigger fired, and the checklist went almost fully dark

Unscheduled pass, prompted by the size of the move. BTC ran to **$79,500** intraday and
sits ~$77.5K, **−38.6%** from the ATH and **+34%** above the Jul 1 low of $57,800. Week
~46 post-ATH; week ~7.3 off the flush. Two days ago this file recorded +21% and −45%.

Almost all of this entry is about keeping two questions apart: *is the bottom thesis in
trouble* (the checklist answers that, and it says less than ever) and *has the
pre-registered escape hatch fired* (falsifier #6 answers that, and one leg has).

### The checklist did not just fail to improve — it collapsed

Rescoring the 8-rule `CORE` subset with the Aug 20 on-chain values at spot, using the
same `RULE` object the calibration replays:

| Rule | Aug 19–20 | Today | |
|---|---|---|---|
| MVRV-Z | 0.4146 | **0.5638** | PARTIAL → NOT YET |
| SOPR | 1.0012 | **1.0125** | PARTIAL → NOT YET |
| Price vs 200W MA | +8.1% | **+20.9%** | PARTIAL → NOT YET |
| Price ÷ Realized Price | 1.33 | 1.48 | NOT YET |
| NUPL | 0.245 | 0.285 | NOT YET |
| STH-MVRV (spot ÷ cost basis) | 1.03 | 1.15 | NOT YET |
| Drawdown | −45% | −38.6% | NOT YET |
| Puell | 0.676 | 0.754 | PARTIAL (the only one left) |

**Expert readiness 21% → 5%, equal 25% → 6%**, against 95% at the confirmed Nov 21, 2022
bottom. One PARTIAL out of eight. Supporting reads move the same way: Fear & Greed
**29 → 72 (Greed)** in eight days, weekly RSI 38.8 → 56.5, Mayer 1.124 (200D MA
$69,009), perp funding back positive at +0.006%/8h (~+6.5% annualised).

This is not a contradiction with the section below and it is worth saying why plainly:
the checklist measures *proximity to a capitulation bottom*, falsifier #6 measures *the
counter-scenario*. In a world where the Jul 1 low was the bottom, these two are supposed
to move in opposite directions. They just did, hard. `BS_SPEED` exists because that is
normally a fast-vs-slow artefact; this time it is not — the slow valuation rows moved
too, and they moved *away*.

### The three legs: one fired, one pending, one not

| Leg | Bar | Reading |
|---|---|---|
| 1 — weekly close | > ~$70K | **pending.** The Aug 17–23 candle is at ~$77.5K against a $62,900 open; it needs ~−10% in two days to fail. Closes 00:00 UTC Mon Aug 24 |
| 2 — Coinbase Premium | positive | **not fired.** Daily closes: −0.068% (Aug 18), −0.050% (Aug 19), **−0.018% (Aug 20)**. Intraday Aug 21 raw −0.038%…−0.048%, USDT-adjusted −0.011%…−0.022% — **negative on both conventions** |
| 3 — ETF 4-week net | > +$1.5B | **fired: +$1.77B.** +$517M Aug 19 and **+$606M Aug 20**, the two largest days in ~3.5 months; 5d alone +$1.55B. 60d still −$3.35B |

Leg 3 is the one that matters and it deserves separating from the price. The Aug 20
entry set up the 2018/2022 bear-rally analogy as the reason not to react to +21%. Those
rallies are the reason the trigger requires *institutional* confirmation and not just
price — and this is the first time the flow leg has actually cleared its bar. That is a
genuine divergence from the analogy, not another restatement of it.

**Nothing is deployed.** Leg 2 is negative on both conventions and leg 1 cannot resolve
before Monday, so the question of which premium convention governs is not even
load-bearing today. +34% at week ~7.3 remains inside the precedent envelope (+48% at
week ~4½ in 2018, +43% at week ~8 in 2022, both followed by lower lows 5–6 months on).

### Recorded before the adjudication: the trigger is a weak discriminator

This is the part that has to be written now rather than after Monday, following the
Aug 19 precedent of recording the Fed-trigger gap instead of patching it mid-move.
Falsifier #6 was designed to tell "the bottom is already in" apart from "this is a bear
rally". Examined leg by leg, it is not well built for that:

- **Leg 1 is price.** A bear rally is a price move. It cannot discriminate by construction.
- **Leg 3 is a lagging confirmation.** The report's own ETF tooltip calls the row a
  confirmation rather than a leading signal, one that mostly chases price — and it is
  **untested against the precedent**, because spot ETFs did not exist in 2018 or 2022.
  There is no way to check what this leg would have printed at the +48%/+43% rally highs.
  It is also *rolling*, not latched: +$1.77B is barely over the bar and ~$1.12B of it
  arrived in two days, so it can fall back under as those roll off.
- **Leg 2 is the only genuinely independent one**, and the Aug 19 pass established that
  it is measured within noise of a documented stablecoin artifact.

So two of three legs are things a bear rally does, and the third is the one sitting in
the noise. **The trigger is not being changed** — it was tightened once already, on
Aug 6, and re-specifying it in the pass where it is about to adjudicate is exactly what
the no-retro-edit rule forbids, in either direction. What is recorded is that if it
fires, it fires on evidence weaker than its own framing implies, and a later pass should
revisit its *design* prospectively rather than its thresholds reactively.

### Leg-2 measurement pinned prospectively, while the outcome is unknown

The scheduled Monday check compared instantaneous tickers. The gap oscillates ±5bp
intraday and 00:15 UTC Monday is the thinnest liquidity of the week, so an instantaneous
reading adjudicates 65% of the ladder on a coin flip. Fixed by writing the procedure
down **before** anyone can see the answer (MAINTENANCE §2b): **daily-close figure, raw
convention**, USDT-adjusted reported as context only.

This is adjudication procedure, not a spec change: daily closes reproduce the figures the
log has always quoted (−0.108% on Aug 12, and −0.018% for Aug 20 against the −0.016%
published that day). Keeping the raw convention is likewise not merely discipline — the
Aug 19 pass adjudicated **this exact configuration**, adjusted positive and raw negative,
and left the row NOT YET on the standard convention. Switching now, when adjusted is the
side closer to firing, would be that same retro-edit pointed the other way.

### A doc-sync bug: the repo held two live specs for falsifier #6

`MAINTENANCE.md` §3 still carried the **pre-Aug-6 draft** of the trigger — "price
reclaims Realized Price and the 200-week MA, holds 30 days, 4-week ETF flows positive" —
15 days after the Aug 6 entry retired that draft as near-vacuous and `index.html`
replaced it. The file that instructs "falsifiers must be honoured, not reinterpreted"
was the one holding the retired wording. Restated to the current spec, with a note; this
is a restatement, not a re-derivation, and the direction is fixed and dated.

**The retired wording does not read fired today**, which was checked rather than assumed:
it requires a 30-day hold above the 200-week MA, and price closed **below** the 200W MA
on six consecutive days, Aug 11–16 (low close $62,900 on Aug 16 against a $63,955 line),
five days ago. The bug is real; the alarm is not. Process note for next time: when a
falsifier is re-specified, grep the whole repo for the old wording in the same pass.

### The probability moves Monday either way

Deferring `th_p` to the scheduled check is right; treating "trigger not fired" as
"evidence unchanged" would not be. Two of three pre-registered legs at or near their
bars, price 10%+ above the $70K level, and Polymarket's no-new-low side around 65% is
this report's own definition of counter-scenario evidence, and the Aug 19 pass moved the
number 25% → 30% with *no* leg fired at all. The legs govern capital; the probability
tracks evidence. **Nothing is moved today** — no threshold, no weight, and not the 30% —
because the point of deferring to a scheduled adjudication is not to pre-empt it.

Also noted: the trigger has no expiry. Leg 1 re-resolves every Monday. Monday is when
this configuration is adjudicated, not the trigger's last chance.

### Data-source notes

- **The ETF row lags the leg it adjudicates.** The committed `data.json` read
  `etf.d20 = +0.94` (through Aug 19) while the live SoSoValue series was already at
  **+$1.77B** (through Aug 20) — i.e. the published arbiter showed leg 3 *under* its bar
  after it had cleared it. The 06:00 UTC Action runs before SoSoValue publishes the prior
  US session. Not a failure and not flagged stale, because the fetch succeeds; it is a
  one-day phase offset that happens to land on the one row a pre-registered trigger reads.
  Refreshed by hand this pass. Check `etf.d` before reading a sub-bar `d20` as real.
- **`stale: ["onchain"]` was self-inflicted.** Five of eight bitcoin-data.com series
  returned HTTP 429 on the manual re-run: this pass had already spent the anonymous
  10-req/hour budget pulling the same endpoints directly to verify them. The merge kept
  the correct Aug 20 values, so the flag was conservative rather than wrong; a retry once
  the rolling window reset cleared it, and that second run also extended all eight series
  in `history.json` (1461d → 1462–1463d) rather than the three the throttled run reached.
  Setting `BGEOMETRICS_TOKEN` locally is the fix if a pass needs both hand-verification and
  a run in the same hour.

### Second opinion

The pass was reviewed by a second model given the same data and the opposite brief
(disagree where warranted). It confirmed the `CORE` rescore to 5%/6% by hand, measured
the premium independently (raw −0.048%, adjusted −0.022% via a different USDT venue —
negative both ways), and produced three of the corrections above: that leg 3 is rolling
rather than latched, that leg-2 measurement needed pinning before the outcome was
visible, and that the probability must move on evidence regardless of what the trigger
does. It found the `MAINTENANCE.md` doc-sync bug. Its one claim that did not survive
checking was that the retired wording would read fired today — the 30-day hold fails, as
above. Recorded because a review that changed four things in the entry is part of how the
entry got its numbers.

---

## 2026-08-19 — The week the counter-scenario got its best evidence, and the checklist did not move

Scheduled refresh (the cadence said late Aug). It landed on the most eventful day of
the drawdown so far, so most of this entry is about telling a large price move apart
from a change in the evidence. Live state read from the rendered page: BTC $69.3K,
**−45%**, week 45, stage **Too early — 0 of 4 families lit**, 0 of 15 active, 9 partial,
expert 27% · equal 30%. On Aug 12 the same page read −50%, 1 of 15 active,
expert 41% · equal 40%.

**What happened on Aug 19.** The US Treasury announced it will at least **double its
long-end liquidity-support buybacks, from $2B to ≥$4B per operation** in the 10–20y and
20–30y sectors, effective Sep 9 and running through Nov 4. The 30-year fell 9bp to
5.196%, the dollar weakened, and BTC ran from an intraday $64,112 to **$70,022** — a
+9.2% day, ~$1.44B of short liquidations, and the **first daily close above the 200-day
MA since Dec 4, 2025** — 258 days below it, Mayer 1.004, measured from Binance closes. Two smaller tailwinds landed the same day: the SEC proposed
*Regulation Crypto Assets* (offering exemptions plus a token safe harbour), and the 50%
Section 338 tariff on Canadian goods was **paused three days at its deadline** pending a
USMCA deal.

Worth being precise about the causal chain, because the report had this scenario
half-written already. The Aug 12 pass noted that reverse repo is drained so refunding
lands directly on reserves, and recorded that the 3y and 10y legs cleared without
stress. The **30y leg did not**: on Aug 13 it cleared at 5.216%, the highest yield the
US has paid on 30-year debt since 2001, with a 2.39 bid-to-cover against a 2.43 average,
a 0.4bp tail, and dealers taking 11.6% versus a 10.6% norm. A long-end selloff followed.
The buyback expansion is the policy response to that. So the liquidity turn this report
has been waiting for did begin — from **debt management rather than monetary policy**,
which is why the `netliq` macro row moves from headwind to *mixed* while the Fed row
stays a headwind. It is a duration swap, not reserve creation; it is also a deliberate
intervention landing inside the projected bottom window.

**The counter-scenario is raised 25% → 30%, and the derivation matters more than the
number.** Three arguments for a larger increase, and one against that caps it:

1. *The market's own counter-read resolved in its favour.* The Aug 12 pass quoted
   Polymarket pricing a $70K retag at 68%. That contract **settled YES on Aug 19** when
   BTC tagged exactly $70,000. This is the first time this report has recorded a
   prediction-market disagreement and then watched it resolve, and it resolved against
   the report.
2. *The market moved hard.* Same-day Gamma snapshot, Aug 19, $54.5M event volume:
   P(<$55K) **57% → 37.5%**, P(<$50K) 36% → 25%, P(<$45K) 22.5% → 17.5%, P(<$40K)
   15% → 12.5%. The no-new-low side is now ~62.5% against this report's 30%. The
   re-listed sub-$60K contract prices a *return* below $60K at ~53% — the cleanest
   statement of the disagreement: the market thinks a revisit is a coin flip and a new
   low is not.
3. *The supply-floor damage stopped — but only stopped.* Pulling the LTH series
   directly (see below) shows the Coldcard-migration drawdown ended on Aug 11 and supply
   has risen every week since. It also shows the recovery is small: +40,279 BTC (+0.24%)
   against a −249,798 BTC (−1.48%) fall, still **1.24% below the Jul 24 record**. This
   argument was drafted as "fully reversed" on the strength of one data point matching a
   figure the Aug 12 pass had quoted from news reports; the series says otherwise, and
   the leg is weaker than it first looked.
4. *Against all three — the measured size of the bounce.* This is +21% off the $57,800
   low. The two precedent bear rallies inside a capitulation phase ran **+48%**
   (Jun→Jul 2018, $5,750 → $8,492) and **+43%** (Jun→Aug 2022, $17,622 → $25,211), and
   both were followed by lower lows 5–6 months later. At +21% both prior cycles were not
   even halfway through their relief rally. A price move of this size is inside the
   distribution of what a bear rally does; it is not evidence about the bottom.

Net: +5 points, not +20. The number moved because the *evidence* moved (a resolved
contract, a reversed supply series, a liquidity intervention), and was held down by the
one measurement that directly addresses the question being asked.

**The checklist did not move, and that is the finding.** A +9% day, a $70,000 tag, a
Treasury liquidity intervention, a tariff pause and a regulatory-clarity proposal
produced: zero triggers fired (third consecutive pass at 0 fired · 1 partial · 3 not
fired), zero families lit, and a readiness reading that went *down*. Valuation is why —
price at 33% above Realized Price, NUPL 0.19, MVRV-Z 0.41, against −0.28 and −0.32 at
the confirmed 2022 bottom. Everything that improved was fast; nothing slow moved.

**Short-term-holder MVRV crossed above 1.00 — PARTIAL → NOT YET.** 0.84 (Jun 30) → 0.96
(Aug 18) → 1.03 (Aug 19), against an STH cost basis of $67,244. The cohort that
actually capitulates is back in profit. This is the single clearest statement available
that no flush is underway, and it is worth separating from the shallow-bottom argument:
it says the bottom is not happening *now*, not that it already happened.

### Data-source work: four manual rows examined, one converted

The user asked whether indicators should be added or removed. The answer is neither: no
row was added or removed, and the useful finding was that **rows already in the
checklist could stop being hand-quoted**. The BGeometrics OpenAPI spec
(`https://api.bitcoin-data.com/v3/api-docs`, 688 paths) was read for the first time.

| Row | Endpoint | Verdict |
|---|---|---|
| `sthmvrv` | `sth-mvrv` + `realized-price-sth` | **Adopted — now LIVE**, and added to `CORE` |
| `hash` | `hashribbons` (free; `{sma_30, sma_60, state}`) | Deferred — numbers quoted, not scored. See below |
| `lth` | `long-term-hodler-supply-btc` | Used to settle this pass's reading and correct two published figures; left manual |
| `resv` | `exchange-reserve-btc` | **Impossible — HTTP 403, subscription only** |

- **`sthmvrv` went live and joined the calibration.** The series carries the full
  1,461-day free window, which reaches back past the Nov 2022 bottom, so it satisfies
  both `CORE` membership tests: clean daily history in *both* eras, and a threshold
  fixed **before** the series was in hand (≤0.80 ACTIVE / <1.00 PARTIAL, specified
  Jul 24, 2026 when the row was added). The order of operations was deliberate:
  membership was decided on those grounds and the historical reading was looked at
  afterwards, because conditioning inclusion on what a signal does to the 2022 figure is
  precisely how a calibration turns into a fit. The calibration subset is therefore
  **8 rules, not 7**, and the published pair is now 95% at the Nov 2022 bottom
  against 21% today — *not* 100%, for the reason below. The live row is built as spot ÷ published cohort cost basis,
  the same construction as the Realized Price row, so it reads against spot rather than
  lagging a day on the published ratio.
- **`hashribbons` deliberately not scored yet.** It is free and it works, and it
  independently confirms the hand-computed figures (BGeometrics Aug 18: sma30 911.8 EH/s,
  sma60 925.6 EH/s, state "Down"; blockchain.info over the same window: 912.2 / 918.5).
  But the classic signal is *stateful* — a cross **after** a capitulation — and a naive
  `sma_30 > sma_60` rule reads ACTIVE through any ordinary bull market. Before wiring it
  into `RULE`, its state field has to be checked against Jan 2026 (the known misfire,
  followed by a further 20%+ decline) and Nov 2022. Recorded in MAINTENANCE §2b.
- **`resv` stays manual on missing data, not on a reading.** The reserve endpoint is now
  paywalled. `exchange-supply-ratio` is free (14.04% of circulating supply, Aug 18) but
  measures something adjacent, and substituting it would be a spec change dressed as a
  data upgrade. The row says the data is missing instead.
- **Rejected, again:** adding any new row. Nothing in this pass's evidence is
  un-represented. The Treasury buyback is the closest call — it is a genuine liquidity
  mechanism the macro composite does not test — but macro is deliberately one composite
  row, and a second macro row would re-inflate exactly the collinear factor the families
  exist to collapse. It is recorded in the `netliq` narrative and in the Fed-trigger card
  instead.

### The calibration's first act was to fail one of the checklist's own thresholds

This is the most consequential thing in this pass, and it is a correction to a claim the
report has been making since Jul 24, 2026.

The `sthmvrv` row said prior cycle bottoms printed "well below 0.80". That was asserted
without the series, because the series was not available. With it in hand:

| Date | STH-MVRV | What it was |
|---|---|---|
| 2022-11-14 | **0.833** | trough of the window around the bottom |
| **2022-11-21** | **0.84** | the confirmed cycle-3 bottom |
| 2022-08-25 | **0.831** | the *bear-rally high*, $21,559 — **lower than the bottom** |
| 2026-02-05 | **0.70** | mid-decline, five months before the Jul 1 low |
| 2026-08-19 | 1.03 | today |

Three things follow. **First, the stated premise is false:** 0.80 was never reached at
the one confirmed bottom inside the free window, so the rule reads PARTIAL there and the
8-rule calibration publishes **95%**, not 100%. **Second, the threshold has already
misfired this cycle** — the series sat at or below 0.80 for **32 consecutive days** in
Feb–Mar 2026 (low 0.70 on Feb 5), plus shorter dips in Nov 2025 and Mar 2026, none of
which marked anything; the real low came in July. **Third, and most damning for a
level-based reading:** the summer-2022 bear-rally high printed *lower* than the bottom
itself. Sub-0.80 evidently marks "recent buyers are deeply underwater", which is a
mid-decline condition, not a bottom.

**The threshold is left at ≤0.80 anyway.** Re-specifying it in the same pass that found
it inconvenient is exactly what the no-retro-edit rule exists to prevent, and the
direction of the convenience is not the point — loosening it to ≤0.85 would restore the
100% headline, which is precisely why it is not being done now. A revision goes in
prospectively, with its derivation, in a later pass. What is fixed immediately is the
false *justification*, in the row's tooltip and in `cal_sum`.

Note this is *not* the same situation as the Aug 6 MVRV-Z fix. There, a threshold had
never once been evaluated against the series it was written for, so specifying it was
the only way to make the row mean anything. Here the threshold has been evaluated
against the right series all along — it was only the historical *precedent cited for it*
that was unverified. That is a claim to correct, not a threshold to re-derive.

The wider reading is that this strengthens falsifier #5 rather than weakening the
report: a checklist whose thresholds were calibrated on −78%-and-deeper capitulations now
has one measured instance of a threshold that the last confirmed bottom did not satisfy.

### Two measurement findings

**The Coinbase Premium streak is mostly a stablecoin artifact.** Measured directly from
public APIs rather than taken from news: the raw gap (Coinbase BTC-USD minus Binance
BTC-USDT, the standard convention) has run −0.08% to −0.11% for weeks and is now
**−0.016%** (Aug 20), from −0.108% on Aug 12. But USDT itself trades at 0.9990–0.9994,
and **normalising for that discount puts the premium at ~0.00%**, printing slightly
positive on Aug 19–20. So the "record 93-day negative streak" is largely the USDT basis,
not an absent US bid. The row's status is left at NOT YET on the standard convention —
the threshold is not retro-edited because a better measurement flatters it — but the
caveat is now in the row text, and it materially weakens how much the streak should be
read as evidence about US demand.

**The thesis paragraph's calibration figures were stale within a week.** The Aug 12 text
hardcoded "read 100% at the 2022 bottom … 43% today" while the live section rendered
**24%** by Aug 19 — the drawdown and 200W-MA rules flipped off as price rallied. That is
a bug class, not a typo: any figure typed into prose that is also computed on the same
page will drift. Both figures are now interpolated into `th_p` via `calibNums()`, as is
the premium over Realized Price (which read a hardcoded "21%" against a live 33%).

### A dated failure found while checking the interpolation fix

Fixing the stale-figure bug surfaced a worse one it would have masked. The free
bitcoin-data.com window is a **rolling** 1,461 days: every daily run returns a series
whose first date is one day later than yesterday's, and `build_data.py` replaced each
stored series wholesale. So `history.json` was losing its left edge every day, silently.

That has a date on it. The Nov 21, 2022 bottom — the calibration's only anchor, and the
source of the "95% at the confirmed bottom" figure now quoted in the thesis paragraph,
`cal_sum`, the README and the share card — **leaves the free window on Nov 20, 2026**,
92 days from this pass and *inside* the projected Sep–Nov bottom window. On that day
`coreOnDate('2022-11-21')` would have returned null, `calibNums()` with it, and the
thesis paragraph would have rendered em-dashes where its centrepiece numbers go, while
the cycle-3 trace eroded from the left. Interpolating those figures had converted them
from stale-but-present into computed-but-vanishing.

Fixed at the source rather than noted: `extend_series()` unions the stored series with
the fresh one and keeps the older head permanently. Fresh values win on overlap (the
provider does restate), the output is forced contiguous because `coreAt()` indexes by
day offset, and genuinely disjoint ranges keep the fresh series alone rather than
emitting a plausible-looking but misaligned array. Six merge cases were tested directly,
including idempotency and the disjoint refusal.

The consequence worth writing down: **`history.json` is now a data asset, not a
derivable artefact.** Its pre-Aug-2022 head cannot be re-fetched at any price once the
window slides past it, so it must never be regenerated from scratch or "cleaned".

### Also on the record

- **The Fed trigger does not test what actually moved.** "Fed pivot + dollar rolling
  over" was written for monetary policy; the Aug 19 liquidity impulse came from the
  Treasury. The trigger is **left exactly as specified** and the gap is recorded here
  rather than patched mid-move. If a future pass wants to broaden it, that is a
  prospective spec change with an entry in the changelog.
- **Strategy paused.** The Aug 17 8-K reports *no* BTC bought or sold Aug 10–16 — the
  first such week since the selling began — holdings flat at 840,447 BTC (avg $75,385),
  USD reserve up to $4.80B, and $333.7M of Class A stock sold in the week of which
  **$132.2M went to buying STRC back**. Flow pressure eased; the equity signal worsened
  (basic mNAV ~0.66× from ~0.68×). One paused week is not a policy change — the dividend
  run-rate does not pause — but it is the first evidence the sales are discretionary
  rather than forced, which weakens the leading second-catalyst candidate.
- **Fed pricing kept deflating:** Sep hike odds ~38% → ~32%, hold ~68%. Still
  hold-not-cut with no easing priced. Recession odds 9% → 8% (Polymarket, Aug 19).
- **Follow-up 2 (Aug 20, midday) — the confirmation trigger began converging for
  real.** Price extended to $72,490 intraday (first $72K since early June, −43% from
  ATH, the bounce now +24% off $57.8K) and the three pre-registered legs moved from
  "not close" to "converging": **(1)** the in-progress weekly candle sits at ~$71.8K —
  it would take a −2.5% drop by Sunday for the weekly close *not* to print above $70K;
  **(2)** the Coinbase premium oscillates at −0.02%…−0.07% raw, positive USDT-adjusted —
  the laggard leg; **(3)** spot ETFs took in **+$517M on Aug 19, the largest daily
  inflow in ~3.5 months**, with Aug 20 running stronger (~$700M reported intraday) — the
  4-week net goes from $0.49B toward ~$1.0–1.7B, so the $1.5B bar can be met within
  days. Polymarket followed: P(tags $75K) 70% → 83.5%, P($80K) → 60.5%, P(<$55K)
  37.5% → 35.5% (no-new-low ~64.5%). The market narrative for the move is "stealth QE".
  **One calendar observation recorded before Sunday resolves it:** this is week ~7 off
  the Jul 1 flush low at +24%; the 2018 bear rally topped at +48% in week ~4½ and the
  2022 one at +43% in week ~8 — so the current move sits, by both price and calendar,
  *inside* the envelope where both precedent rallies peaked and reversed. That is
  precisely why nothing is deployed on price action alone: the three-leg trigger exists
  to separate this from 2018/2022, where institutional premium and flows did **not**
  confirm the rally tops. Decision: no threshold, weight or probability touched today —
  the Sunday 00:15 UTC check (scheduled, with e-mail) adjudicates; only the two ETF
  narrative tails in the UI were refreshed, since the "$0.49B, barely a third of the
  bar" framing was overtaken by the $517M print.
- **Follow-up (Aug 20), on what else the rally day held.** Three more same-day items
  were checked for whether they change the read. The **Jul 28–29 FOMC minutes** (2pm ET
  Aug 19) were *hawkish* — participants beyond the three dissenters said tightening
  "would likely be necessary" if inflation does not decline — and the market rallied
  through them, which supports the positioning/Treasury reading of the day over any
  monetary one. **Trump hosted crypto leaders at the White House** and pushed the
  Clarity Act — same regulatory-clarity cluster as the SEC proposal, added to that row.
  **Whale accumulation (~$2.9B / ~43K BTC over 60 days)** made headlines but is not
  new — it is the same 1K+ BTC cohort the report has tracked at ~3.06M BTC since July.
  Nothing in the three constitutes bottom *confirmation* under the pre-registered
  criteria; the F&G flip 46 → 62 in a day and an 82 hourly RSI are bear-rally
  signatures, not capitulation ones. Also added to the events row: **Jackson Hole
  Aug 27–29, Warsh's first keynote as chair Aug 28**, same day as the BLS revision.
- **Hash ribbons are converging fast:** the 30d/60d gap closed from −2.0% (Aug 6) to
  −1.5% (Aug 11) to −0.7% (Aug 16). Still no cross. The ~Aug 22 retarget projects +0.45%,
  a second consecutive positive print after +0.99% on Aug 8. Row stays PARTIAL, now on a
  measured basis rather than an asserted one.
- **Puell drifted the wrong way**, 0.67 → 0.80, as the hashrate stabilised. Still
  PARTIAL.

---

## 2026-08-12 — Research refresh: the supply-floor story takes its first hit; Polymarket finally sourced clean

Scheduled-ahead-of-schedule pass (the cadence said late Aug; the Aug 12 CPI, the
Aug 7 payrolls and the Aug 11–13 refunding all landed this week, so the snapshot was
taken while they were fresh). Live state at the time of the pass, read from the
rendered page: BTC $63.4K, −50%, week 44, stage **Too early — 1 of 4 families lit**.

**Two checklist downgrades, both in Supply & flows (`lth`, `resv`: ACTIVE → PARTIAL).**
The Coldcard hardware-wallet firmware exploit (from Jul 30, ~$120–140M / ~1,816 BTC
stolen) triggered a mass wallet migration: ~210K BTC left old wallets in early August
(Coindesk, Aug 7 — the largest LTH outflow since Dec 2024) and ~20K BTC landed on
exchanges in a week, lifting aggregate reserves to a one-month high and Binance
reserves to a six-month high (multiple sources, Aug 11–12). Neither is economic
distribution — moving coins to a new wallet mechanically resets their age, and moving
them to an exchange for custody is not selling — but the rows are scored on what the
series *say*, and both thresholds ("LTH supply rising", "multi-month reserve decline")
read broken this week. Applied the hash-row convention: **event-contaminated +
provider-divergent ⇒ PARTIAL, not read either way.** Effect: 3/15 → 1/15 active,
expert 45% → 41%, equal 47% → 40% (still within the ~3-point agreement band). Stage
unchanged. To be reversed (either way) once the migration washes out of the series.

**Polymarket re-sourced — the stale label comes off.** The Aug 6 failure mode
(figures spread across months) was solved by hitting the Gamma API directly for the
"What price will Bitcoin hit in 2026?" event ($52M volume): one same-day snapshot,
Aug 12. P(<$55K) 57% · P(<$50K) 35.5% · P(<$45K) 22.5% · P(<$40K) 14.5% ·
P(tags $70K) 67.5%. Against the July figures the market moved hard toward the shallow
scenario (P(<$50K) was 45–59%, P(<$40K) was ~38%). Two readings worth writing down:
the market puts ~1-in-3 on price ever reaching the $44–50K core zone, and ~43% on
no new low below $55K — vs this report's ~25% counter-scenario. **The 25% was kept**:
it was set on the Jul 24 evidence and nothing in this pass's on-chain data (STH-MVRV
still rising, no catalyst, CBP streak intact) argues the flush is off the table — but
the gap to the market's 43% is now stated in the UI instead of hidden. The sourcing
procedure went into MAINTENANCE so the next pass doesn't rediscover it.

**Macro: the hike scare deflated without turning into easing.** Sep hike odds
~62% (Aug 4) → ~42% (after payrolls −23K, unemployment 4.1%, −103K revisions) →
~38% (after in-line CPI: 3.4% headline / 2.5% core). That un-fires the "Fed moved
backwards" texture from Aug 6 but is hold-not-cut; the real 10y (2.43% vs 1.99% 200d
MA) keeps the liquidity composite at 2 of 3. Refunding cleared its 3y/10y legs with
above-average bid-to-cover (2.57/2.53) — the drained-RRP stress scenario did not
materialise this week. Note logged for the tariff row: the earlier "re-imposed via
Section 301" wording was corrected to the fuller legal picture (Section 122 struck by
CIT in May, stayed by the Federal Circuit Jun 11 pending appeal; Section 338 Canada
tariffs land Aug 19) per law-firm client alerts — better sources than the news pieces
the July pass had.

**Strategy: reclassified from "Escalating" to "Escalating on flow, cushioned on
solvency."** Fifth 2026 sale tranche (1,690 BTC / ~$109M, Aug 3–9; YTD ~6,948 BTC /
~$432M), no purchases since late June — but the USD reserve nearly doubled to $4.65B
(a $653M equity raise routed straight to it), STRC was held at 12% rather than cut,
and Q2's $8.6B loss was ~96% non-cash. The dilution machine is currently refilling
the cash buffer faster than the BTC sales drain the treasury, so the second-catalyst
gate stays **partially armed** — the stress signal to watch is the ~0.68× basic mNAV,
not the sale pace.

**Indicator add/remove review — no change, three candidates rejected on record:**
- *Binance-reserve row*: provider- and venue-specific; duplicates `resv` with a noisier series.
- *Recession-odds row*: the macro composite already carries the regime read; a
  prediction-market level needs a regime baseline (the exact objection that kept
  levels out of the `fed` row), and N=3 bottoms give nothing to calibrate it on.
- *BTC/S&P ratio row*: the equities divergence is context (it lives in `mac`), not a
  bottom signal — it has no threshold that ever fired at a prior bottom.

**One code fix found by the render check:** `applyI18n()` set every `[data-t]`
element via `textContent`, so the `s2n` chart note — the only `data-t` string with
markup — rendered its `<b>` tags literally. Pre-existing (visible in the morning
render, before this pass touched anything); now routed through `innerHTML` only when
the string contains `<b>`/`<i>`. Exactly the bug class MAINTENANCE §2 warns about,
caught exactly the way §5 says to catch it.

**Number drift fixed while passing through:** the head meta descriptions said the
checklist "reads 34% today" (frozen Aug 6 figure); the same seven rules read **43%**
at this pass's price/week and the metas plus `th_p` now say so. The `rp` tooltip's
strip-the-institutions arithmetic was re-based to the current $52.3K Realized Price
(spot +21%, ex-premium +27%).

---

## 2026-08-06 (external review triage) — Two adoptions from a reader review, six rejections with reasons

A reader sent a written review of the dashboard. The source file lived outside the
repo and is not durable, so its substance is preserved here rather than referenced.
Most of it was already built or had already been considered and rejected on record;
two items were genuinely new and are now in the page. Logging the **rejections**
matters more than the adoptions — a suggestion that keeps arriving from different
readers and keeps getting declined needs its reason written once, in a place that can
be pointed at.

| # | The reviewer's suggestion | Disposition |
|---|---|---|
| 1 | Classify indicators by speed (fast / medium / slow) | **Adopted** — `BS_SPEED`, display only |
| 2 | Split into categories with explicit weights (Macro 30% …) | **Half adopted** — family weight *shares* now shown; top-down re-weighting rejected |
| 3 | Add Global M2 / macro liquidity | **Already built, more honestly** — a computed composite over **US** series; "global" is deliberately not claimed |
| 4 | Add ETF flows | **Already built** — `etf` row, live from SoSoValue since Aug 6 |
| 5 | Add more independent signals | **Already built** — four families exist precisely because the signals are *not* independent |
| 6 | Display "Bottom Probability: 15%" instead of a score | **Rejected** — reverses this month's deliberate demotion of the percentage headline |
| 7 | Rename to "Probability Dashboard" / "Probability Model" | **Rejected** — same calibration claim, in the title |
| 8 | Reduce the weight on weeks-since-ATH | **Already true** — time is not in `BS_W` at all |
| 9 | Frame it as Bayesian / "estimate probability of attractive returns" | **Already embodied, rejected in letter** — no priors exist to update |
| 10 | Add government accumulation, dormant supply / CDD | **Blocked on sourcing** — no free daily series; also a thesis-level change |
| 11 | Rating table (macro awareness 3 → 8.5, etc.) | **Not a finding** — unsourced scores, no methodology stated |

**Adopted 1 — response-latency tags on every checklist row.** The reviewer's framing
was "classify indicators by speed; this helps explain why indicators can disagree
without necessarily conflicting." That is a real gap: nothing on the page told a reader
that the rows operate on different clocks. Added `BS_SPEED` (display-only, touches no
score) tagging each of the 15 rows FAST (days) / MEDIUM (weeks) / SLOW (months):

| Speed | Rows | Why |
|---|---|---|
| fast (5) | funding, ETF flows, Coinbase premium, drawdown, 200W-MA cross | price- and flow-derived; can flip in days |
| medium (3) | SOPR, STH-MVRV, macro composite | weeks — the 155-day cohort, monthly M2, 200d averages |
| slow (7) | Realized Price, NUPL, MVRV-Z, Puell, Hash Ribbons, LTH supply, exchange reserves | realized cap, a 365-day miner-revenue average and holder/reserve stocks cannot move quickly |

The count is the finding, not the labels: **7 of 15 rows are slow by construction and
only 5 are fast.** That is the mechanical reason the checklist confirms a bottom rather
than calls one, and it means the current split — funding/flows/premium moving while
every valuation row stays dark — is the expected behaviour of a mostly-slow instrument
mid-turn, not a contradiction between signals. Written into the `bs_n` note in all
three languages. It also sharpens the existing "structurally cannot exceed ~70% at the
real low" caveat: the rows that cap out are disproportionately the slow ones.

**Adopted 2 — each family card now states its share of the expert-weighted score**
(Valuation 31% · Capitulation 39% · Supply & flows 23% · Macro liquidity 7%). This is
the honest half of the reviewer's "assign category weights" proposal. The shares were
always implied by `BS_W` but never shown, so a reader could not see that macro carries
7% until they summed the weights by hand. Computed from `BS_W` at render time rather
than written into the text, so it cannot drift if a weight changes.

**Rejected 1 — top-down category weights (the reviewer proposed Macro 30% / on-chain 30%
/ market structure 20% / sentiment 10% / time cycle 10%).** Three separate problems.
(a) The taxonomy does not map: there is **no sentiment row** in the checklist (Fear &
Greed lives in the scorecard, deliberately out of the score) and **time is not scored at
all**, so two of the five categories have nothing to weight. (b) Macro at 30% would
undo the collinearity fix on purpose. M2, the dollar, real rates and the Fed balance
sheet correlate 0.7–0.9 pairwise, which is why they were collapsed into **one**
composite row in the first place; a category budget re-inflates a single factor to
nearly a third of the checklist by fiat. (c) N=3 bear markets cannot fit 15 parameters,
let alone a second layer of category weights on top — the page already publishes the
equal-weighted score beside the expert-weighted one precisely to show how little the
weighting choice moves the answer (they agreed within 1pt at the Nov 2022 bottom).
Re-weighting to taste, without new evidence, is the retro-edit this project's
conventions exist to prevent.

**Rejected 2 — display "Bottom Probability: 15%" instead of a score.** This reverses a
documented decision taken **this month** and for the opposite reason. In Aug 2026 the
single readiness percentage was demoted from the headline in favour of the ordinal
family stage, because with three completed bear markets a number like "33%" implies a
calibration nobody has. A percentage labelled *probability* is strictly worse than one
labelled *readiness*: it asserts a frequency claim over N=3. The percentages are still
shown, one level down, and the retro-calibration is the only honest probability-adjacent
statement available — and it says N=1, marks a zone not a date, and says so.

**Rejected 2b — rename the page to "Bitcoin Market Probability Dashboard" or "Bitcoin
Cycle Probability Model".** Same objection as above, moved into the title where it is
harder to qualify. The premise — "don't call it a prediction tool" — is already
satisfied: the page is titled *Bitcoin Halving Cycles Dashboard*, describes itself as a
report, and pre-registers six falsifiers. Putting *Probability* in the name would assert
in three words the calibration the body of the page spends several tooltips declining to
claim.

**Rejected 3 — reduce the weight on "weeks since ATH".** Already true, and the
reviewer assumed otherwise: **there is no time signal in `BS_W`.** Time appears only in
the banner's cycle clock and in the timing-convergence section, both outside the score.
No change.

**Rejected 4 — add Global M2 / global liquidity.** Also assumed rather than checked: the
reviewer credited the dashboard with a Global M2 metric and called it the single most
important addition. The page deliberately does **not** claim one — Japan and China have
no free, current, programmatic series, so it publishes **US** net liquidity and labels
it as such. Adding a "global" label to a US-only series to satisfy the suggestion would
be the exact dishonesty the current wording avoids.

**Rejected 5 — new rows for government accumulation and dormant supply / CDD.** Wanted,
but blocked on sourcing: no free programmatic daily series (the same constraint already
caveated on the SSR row). And a new checklist row is not a cosmetic addition — it
perturbs `BS_W`'s sum to 100, shifts a family's majority threshold, and changes which
signals the retro-calibration can replay in both eras. That is a thesis-level change and
needs its own pass with data in hand, not a reviewer's wish list. Corporate-treasury
accumulation, the third item in that group, is already covered as a narrative macro row
and as the Strategy leg of the capitulation-tranche trigger.

**Already embodied, rejected in letter — the "biggest recommendation": treat this as a
Bayesian model and shift from "predict the bottom" to "estimate the probability that
expected long-term returns are unusually attractive."** The philosophy is what the page
already does: the headline is an ordinal that updates as families light, the falsifiers
pre-register what would make the thesis wrong, both weighting schemes are published
rather than one being chosen, and the retro-calibration replays today's rules over 2022
to test whether the score means anything. What cannot be adopted is the *literal* form —
the reviewer's worked example (50% → 65% → 72% → 61% → 55%) requires a prior and a
likelihood ratio per signal, and neither exists: N=3 bear markets, with signals that are
correlated by construction, cannot produce calibrated update factors. Writing them down
anyway would dress up judgement as arithmetic. The retro-calibration is the closest
honest statement available, and it already carries its own N=1 and zone-not-date
caveats.

**Not treated as a finding — the reviewer's rating table** (macro awareness 3 → 8.5,
etc.). Unsourced scores from a reader with no stated methodology are not evidence about
the page and did not drive any decision here.

Verified by headless render: all 15 rows carry a latency tag, the four family cards
report 31/39/23/7 (sums to 100), and EN/PT-BR/ES are at full key parity with the three
new keys present in each.

---

## 2026-08-06 (coherence pass) — Falsifier #6 was nearly vacuous, and two smaller drifts

A same-day review of the whole analysis for internal consistency. Three findings.

**1. Falsifier #6's deploy trigger was almost satisfied on the day it was written.**
As registered, it deployed the remaining probe + core tranches (65% of the plan) when
"price reclaims both Realized Price and the 200-week MA and holds 30 days on positive
4-week ETF flows". But price **never traded below Realized Price this cycle** — the
"reclaim" is vacuous — it sits ~1% above the 200-week MA, and 4-week flows are positive.
Only the 30-day hold was missing (price closed below the 200W MA Aug 1–3). A quiet
month would have fired it at ~$64K, against a page reading 0 of 7 core signals and
calling the current move a bear-market rally — while the thesis paragraph's own
confirmation for the same counter-scenario demands a weekly close above ~$70K with the
Coinbase Premium positive and 4-week flows above $1.5B. Two confirmations for the same
event, one weak and one strong, is incoherent; the weak one governs 65% of the capital.

**Fixed by unifying them:** #6 now uses exactly the thesis paragraph's confirmation.
This is a change to a pre-registered condition, which is why it is logged loudly: it
was **tightened before ever firing**, the old wording is preserved inside the falsifier
itself, and the direction of the change is against the report's own convenience (it
makes the "deploy anyway" escape harder, not easier).

**2. The cycle clock said "~368 days" from an average that computes to 369.5.**
`(363 + 376) / 2 = 369.5 ≈ 370`, not 368. Plain arithmetic slip, present since the
stat was added; fixed to ~370 in the code and all three languages (banner now reads
day *n* of ~370). Sub-1% effect on the progress bar, but a stated derivation should
compute to its own number.

**3. The ETF trigger card froze research figures that a live row contradicts.**
The card quoted "+$0.34B" (Aug 6 research pass) while the checklist's LIVE row showed
+$0.67B on the same page — the feed updated within a day of the snapshot. The card now
carries `{ETF4W}`/`{ETF3M}` placeholders filled from the live feed, with the snapshot
as offline fallback. Checked the other trigger cards for the same disease: Coinbase
Premium quotes a dated streak ("78 days as of Aug 4"), which is honest because dated;
the drift problem was specific to undated figures duplicating a live computation.

**Verified consistent, no change needed:** window weeks 50–60 ⇔ Sep 21–Nov 30 ⇔ the
capitulation-phase arithmetic (Jun 22 + 140–150d = Nov 9–19, inside); banner counts
(2/15, 9 partial) ⇔ family cards (0+0+2+0 active, 2+5+1+1 partial); drawdown steps
−85/−84/−78 consistent across cvp, tables and log; on-chain floor card 0.75–0.85×
against the measured 0.78×/0.76× precedent, with the band's lower edge correctly
flagged as the realistic end; ladder bands ⇔ chart lines ⇔ dd55/probe thresholds; all
directional cross-references between sections. The C3 low appears as both $15,476
(intraday-derived) and $15,479 (close-derived) in different tables — pre-existing,
sub-rounding, left alone.

**Found while testing whether `bitcoin-data.com` could be reached without the API
token.** It can, and its `/v1/mvrv-zscore` endpoint returned **0.3918** for the same
day `data.json` recorded `mvrv_zscore: 1.2254`. Those are different series:

    price / realized price = 64,524 / 52,328 = 1.233   ← the plain MVRV RATIO
    MVRV Z-Score                              = 0.392   ← standard deviations

The daily Action was calling BGeometrics' `/v1/mvrv` — the ratio — and writing it under
the key `mvrv_zscore`. The page then applied Z-score logic to it: the scorecard card
scaled the bar as `(v+1)/9` and coloured on `v<0` / `v>7`, and the checklist row scored
`< 0.5 = ACTIVE`. **The row has been fed the wrong series since it was created**, which
means it has never once been evaluated against the number its threshold was written for.

**Verified against the last confirmed bottom** (free 4-year window, 2022-08-06 onward):

| 2022-11-21 (C3 bottom) | value |
|---|---|
| MVRV Z-Score | **−0.316** (troughed −0.360 on Nov 9) |
| MVRV ratio | 0.780 |

So the tooltip's claim that bottoms print at "Z ≈ 0 or below" is right, and its quoted
2022 figure (−0.2) was slightly off — it is −0.32 at the low close.

**Threshold: specified, not retro-edited.** The standing rule is never to move a
threshold because of the reading it just produced. That rule does not apply here,
because `< 0.5` had never been evaluated against a Z-score at all — there was no reading
to dislike. It was specified from the measured precedent instead: **ACTIVE at Z < 0**
(where 2018 ≈ −0.3 and 2022 = −0.32 printed), **PARTIAL below 0.5**. Note the direction
this cuts: the loose reading of the old text (`< 0.5` on a Z-score) would have scored
today's 0.39 as ACTIVE. The specified threshold scores it PARTIAL. The correction still
*raised* the row, from a false OFF, but by less than the sloppy reading would have.

**Both series are now published** (`mvrv_zscore` and `mvrv`) and the row displays both,
so this class of confusion cannot recur silently.

## 2026-08-06 — What the checklist actually read at the last confirmed bottom

The largest addition of this pass, and the answer to the fair objection that a
"33% weighted readiness" reads like a calibrated probability when nothing calibrated it.

**Method.** Seven of the fifteen signals have clean daily history in both eras —
Realized Price, NUPL, MVRV Z-Score, SOPR, Puell, 200-week MA, drawdown depth. The other
eight (miner, supply, flow, macro) have no comparable free daily series back to 2022, so
they are excluded from **both** sides rather than estimated on one. The rules are not
re-implemented for the historical run: `RULE` is a single object in `index.html` that
both the live checklist and the retro trace call, so the two cannot drift apart.

**Result** (expert weights, renormalised over the seven; equal weights in brackets):

| | reading |
|---|---|
| 2022-08-11 · bear-rally high $23,934 | **53%** [50%] |
| 2022-09-18 | 96% |
| **2022-11-21 · confirmed C3 bottom** | **100%** [100%] — 7 of 7 active |
| 2023-01-01 | 90% |
| 2023-04-16 · +92% off the low | 25% [21%] |
| **2026-08-05 · cycle 4 today** | **34%** [36%] — 0 of 7 active |

The discrimination is real: 80–100% through the bottom zone, ~50% at the bear-market
rally high that preceded it, under 30% once the recovery was underway.

**Two caveats stated in the UI rather than buried here.** First, cycle 3 held above 80%
for roughly four months around its low — this identifies a **zone, not a date**, which
is the strongest argument yet for the price ladder over the calendar. Second, **N=1**:
only one confirmed bottom falls inside the free on-chain window. The keyless
`bitcoin-data.com` history is exactly 1,461 days, so December 2018 cannot be scored from
the report's own data and is not claimed.

**Consequence for the thesis.** This is now the single strongest piece of evidence for
the base case, and it is measured rather than argued: the same rules that printed 100%
at a confirmed bottom print 34% today.

## 2026-08-06 — Testing the "don't use fixed weights" objection, and largely dismissing it

**Objection raised externally:** avoid fixed weights unless validated out of sample,
because hand-weighting overfits.

**The prescription is unimplementable and the diagnosis is half right.** Out-of-sample
validation of 15 weights against 2 historical bottoms is arithmetically vacuous — you
cannot validate 15 parameters on 2 observations. The relevant small-sample result is the
opposite one (Dawes 1979, improper linear models): with few observations and correlated
predictors, **equal weights tend to beat estimated weights**, because estimation adds
variance without removing bias.

**So the honest test is whether the weighting choice changes the answer. It does not:**

| | expert | equal |
|---|---|---|
| C3 bottom, 2022-11-21 | 100% | 100% |
| C3 bear-rally high | 53% | 50% |
| C4 today | 34% | 36% |
| full 15-signal live checklist today | 40% | 43% |

Maximum divergence across the whole trace is about 7 points. **Both numbers are now
published side by side**, permanently, and the standing instruction is that a material
divergence between them is itself the finding.

**What was changed instead, because the diagnosis was half right.** The single
percentage was demoted from headline to footnote and replaced by an ordinal. The 15
signals group into four families — Valuation, Capitulation, Supply & flows, Macro — and
the headline is how many are lit. The grouping exists because the signals are not
independent: four are functions of realized cap, five read the same capitulation event.

**A bug this immediately exposed.** The first implementation lit a family on
`value >= n/2` with PARTIAL counting a half. A family whose signals are *all* PARTIAL
sums to exactly `n/2`, so it lit with nothing active — and the banner rendered
**"BOTTOM ZONE, 3 of 4 families lit" on 2 of 15 active signals**. Caught by rendering
the page, not by reading the code. Fixed to a strict majority (`> n/2`), which reads
"Too early, 0 of 4 lit" today. *Lesson repeated: read the rendered value.*

## 2026-08-06 — Macro: one composite row, not seven

**Objection raised externally:** add Global M2, Fed balance sheet, real rates, credit
spreads, DXY, a liquidity index, and ETF flows.

**Accepted in substance, rejected in form.** DXY, real rates, the Fed balance sheet and
global M2 are one collinear liquidity factor. Adding seven rows would have taken macro
from 7/100 to roughly 40/100 of the checklist without anyone deciding to — the same
overfitting the objection was warning against, arriving through the front door.

**What was built.** One computable `fed` row, three *directions* rather than levels
(levels need a regime-specific baseline; directions do not): M2 y/y accelerating vs three
months ago, dollar below its 200-day average, real 10-year yield below its 200-day
average. 3 of 3 = ACTIVE, 2 = PARTIAL. Plus one `etf` row, weighted below its narrative
prominence because it overlaps the Coinbase Premium row (both read US institutional
demand) and because flows chase price. Checklist grew 14 → **15**; `BS_W` rebalanced to
keep the sum at 100 by taking 5 points from the rows the new ones partly duplicate
(`sopr` 6→5, `hash` 7→6, `lth` 6→5, `cbp` 5→3).

**Credit spreads were deliberately kept OUT of the score** and put in the macro table as
a **depth** modifier. They are the one variable on the list that is not collinear with
liquidity, but they do not time bottoms — they discriminate an idiosyncratic drawdown
from a systemic one. At HY OAS **273bp** (below its 200-day average of 289bp, against a
long-run median near 450bp and a 600bp+ stress threshold) this drawdown is
crypto-idiosyncratic, which historically bottoms **shallower and faster**. That is
independent support for the damped −65% target over the historical −78%.

**Data-sourcing results** (all tested with live requests, 2026-08-06):

| Series | Source | Verdict |
|---|---|---|
| M2, Fed assets, TGA, RRP, DGS10, DFII10, DGS2, HY/IG OAS, broad USD | `fred.stlouisfed.org/graph/fredgraph.csv?id=` | keyless, works — **but sends no CORS header**, so it must go through the Action, not the browser |
| US spot ETF net flows | SoSoValue `api.sosovalue.xyz/openapi/v2/etf/historicalInflowChart` (POST) | keyless, daily, works; **undocumented** internal endpoint — routed through the Action so a breakage degrades gracefully |
| ICE DXY | licensed | substituted `DTWEXBGS`, the broad trade-weighted index, and labelled as such |
| **Global M2** | — | **not obtainable free.** US (FRED) and euro area (ECB SDMX, CORS-open) are live; Japan's FRED series are stale since 2017–2023 and no free current China series exists. The report therefore does **not** claim a global M2 or a "global liquidity index"; it publishes USD net liquidity and says so. |
| Farside / CoinGlass ETF flows | Cloudflare 403 / API key required | ruled out |

**Rejected outright:** bootstraps, confidence intervals or p-values on three
observations, and any additional on-chain indicators. Each would lower honesty while
appearing to raise rigour.

## 2026-08-06 — The contradiction the report was hiding from itself

Surfaced by an outside methodological review and **not resolved, only stated**, because
resolving it would mean guessing.

The headline thesis is that institutionalisation damps amplitude, so cycle 4 bottoms
near **−65%** rather than the historical −78% and deeper. But the checklist thresholds
are the *undamped* ones: MVRV-Z < 0, NUPL < 0, price below Realized Price were all
features of −77%-and-deeper capitulations. **If the damping thesis is right, MVRV-Z may
trough near 0.3, price may never close below Realized Price, and the checklist
structurally cannot exceed roughly 70% at the actual low — it would read "not yet" at
the bottom it predicted.**

Both cannot be right. Rather than retro-fit a "cycle-4 adjusted" threshold column —
which would be inventing damped thresholds with no observation to calibrate them
against — this was written into `bs_n` in the UI and registered as **falsifier #5**:
a confirmed bottom forming with fewer than 8 of 15 signals ever firing means the
thresholds belong to a regime that ended, and the response is to rebuild them, not to
trust them.

**Related and also now stated in the UI:** the −65% target is an *assumption*, not an
extrapolation. From −85% → −84% → −78%, repeating cycle 3 gives −78% (~$28K) and the
linear trend gives −75% (~$31K). **Both land below the report's own $35K black-swan
tranche** — the buy ladder is priced entirely for the damping thesis being right. Said
plainly in `cvp_sum` rather than left for a reader to derive.

**Falsifiers.** A new section lists six pre-registered kill conditions, because every
signal here moves toward ACTIVE as price falls: the framework can say "not yet" or
"buy", but had no way to say "I am broken". The sixth is not a falsifier but the
symmetric-error remedy — if price reclaims Realized Price and the 200-week MA and holds
30 days on positive 4-week ETF flows, the probe and core tranches deploy regardless of
the readiness reading, because unfilled lower rungs are otherwise a way of never buying.

**Also relabelled:** the four timing methods are described as *internal consistency*,
not corroboration. They are re-parameterisations of the same three observed cycle
lengths, so they cannot fail independently.

## 2026-08-06 — Research pass: the Fed moved away, Strategy escalated, valuation moved backwards

Twelve days since the last snapshot. Price is unchanged in substance — $64.5K, −48.9%,
ranging $62.8–66.6K since Jul 21 — but three inputs moved materially, and two of the
three run **against** the thesis timing.

**1. The Fed moved further from easing, not closer.** The Jul 28–29 FOMC held at
3.50–3.75% for a fifth time, but **9–3 with all three dissents wanting a hike**
(Hammack, Kashkari, Logan). Kevin Warsh has chaired since May 22, 2026 — the report
still described a Powell-era Fed. Core PCE 3.3% y/y, headline 3.7%. QT ended Dec 2025.
The real 10-year yield is **2.40%**, near a two-year high of 2.47% and far above its
200-day average of 1.98%; the 10-year nominal is at fresh 2026 highs. The committee
debate is now hold-versus-hike, not cut-versus-hold. **This pushes the liquidity turn
later**, and it is why the macro composite reads 2 of 3 rather than 3.

**2. Strategy's selling hardened from an event into a programme.** Holdings
843,775 → **842,138 BTC**, another ~1,638 BTC sold for ~$105M, and **five consecutive
weeks with zero purchases**. USD reserve built to $4B. Separately, and worth recording:
Strategy **redefined its own mNAV methodology on Jul 23**; its metric reads ~1.04× while
third-party basic mNAV computes ~0.68×. Those numbers are not comparable and the report
should never quote them as if they were. The `mac` row moves from "began selling" to
**escalating**; the capitulation gate stays *partially armed* — this is still a drip
against the treasury, not a cascade.

**3. Valuation moved the wrong way.** STH-MVRV **0.82 (Jun) → 0.92 (mid-Jul) → 0.95
(Aug 4)**. The cohort that actually capitulates is being *relieved*, not forced out.
This is the clearest single confirmation of the Jul 25 "bear-market rally, not a
completed bottom" reading — a flush in progress does not walk STH-MVRV up three
consecutive readings.

**4. Coinbase Premium set a record and kept it.** 78 consecutive negative days as of
Aug 4 (from May 19), against a prior record of 40. It survived both the July ETF-inflow
run and the August stabilisation. US spot demand has not returned.

**5. ETF flows stabilised without returning.** 4-week net **+$0.34B** against a 3-month
net of **−$7.78B** and 2026 year-to-date **−$4.91B** (cumulative since launch $51.7B,
AUM $78.3B). Under the v2 trigger spec adopted on Jul 24 — which requires ≥$1.5–2B —
this is **not fired**, where the old three-consecutive-weeks wording had it *fired,
low conviction*. The v2 spec is now doing the work it was written for.

**6. Geopolitics flipped sign.** The July pass recorded Hormuz blockaded and Brent above
$76. Brent is now **~$70.8**, about 38% off its post-invasion peak on ceasefire
expectations, and that energy unwind is most of why headline PCE fell 4.1% → 3.7%. The
oil shock is currently a tailwind to disinflation, not a threat to it — the reverse of
what the `fed` trigger tooltip assumed twelve days ago.

**Funding: measured, not assumed.** Research sources described long negative funding
streaks earlier in 2026. Binance Futures gives the 7-day average as **+0.0058%/8h with
zero negative periods in the last 21** — the row is OFF. The live computation governs;
the narrative did not.

**Not changed, deliberately:** the window (Sep–Nov 2026, weeks 50–60) and the ladder.
Nothing this pass touched the four timing methods or the price bands. Two forces act on
the window and they point opposite ways — the hawkish Fed argues later, tight credit
spreads argue shallower and faster — so moving it on either alone would be noise.

**Could not source, and said so in the UI:** a consistent same-day Polymarket snapshot.
Quoted figures ranged across months and disagreed by more than 10 points on P(<$50K),
so the card now shows a range, is labelled stale, and no reading is taken from it. Also
not found: a numeric Stablecoin Supply Ratio, current Deribit skew/max-pain, and an
exchange-reserve figure in BTC — the `resv` row rests on the trend alone, which is
recorded in its tooltip.

## 2026-07-25 — "Recovery" ≠ "bottom is in": the flush → rally → bottom precedent

**Question raised:** if July is already a recovery, haven't we passed the bottom?

Fair confusion, caused by loose wording in the phase note written earlier the same day
("that is a recovery, not a flush in progress"). There are **three** states, not two:

| | |
|---|---|
| **A** capitulation underway | the bottom is being carved now |
| **B** bear-market rally | the flush is still ahead ← base case |
| **C** bottom already in | new cycle has begun ← counter-scenario (~25%) |

July's data (STH-MVRV 0.82 → 0.92, price $58.6K → ~$64K, 200W MA reclaimed, three
positive ETF weeks, whales accumulating) **rules out A. It does not distinguish B from C.**
The original wording ruled out A but read as C.

**What separates B from C is valuation, and it is unambiguous:** price 22% *above*
Realized Price where every prior bottom printed below; NUPL 0.195 (bottoms < 0); MVRV-Z
1.24 (bottoms ≈ 0 or negative); STH-MVRV 0.92 (bottom zone ≤ 0.80); 2/14 signals active
at 33% weighted against 8+ and ≳75% at prior bottoms. A bottom formed with none of these
would be unprecedented.

**The shape has an exact precedent in both modern cycles** — verified from Binance daily
candles, not from memory:

| Cycle | Flush low | Relief rally | Real bottom |
|---|---|---|---|
| C2 | 2018-06-24 · $5,750 | 2018-07-25 · $8,492 (**+48%**) | **2018-12-15 · $3,156** — 45% below the flush, 174d later |
| C3 | 2022-06-18 · $17,622 | 2022-08-15 · $25,211 (**+43%**) | **2022-11-21 · $15,476** — 12% below the flush, 156d later |
| C4 | 2026-07-01 · $57,800 | 2026-07-21 · $66,956 (**+16%**) | ? |

In both cases the June flush was bought, rallied 43–48%, and the real bottom arrived 5–6
months later *below* the flush low — in C3 after a second catalyst (FTX in November). The
current bounce is +16%, smaller than either. So this recovery is not evidence against the
base case; in both precedents it is what **preceded** the bottom.

**Changed:** the phase note now states explicitly that this reads as a bear-market rally
and not a completed bottom, carries the C2/C3 precedent inline, and points at the
valuation rows as the thing that settles it.

**Secondary finding — the window's right edge is the tight constraint.** Measured from the
Jun 22 breakdown with the *raw* historical capitulation durations: C3's 161 days lands on
**2026-11-30, exactly week 60** — the closing edge of the window — and C2's 176 days lands
**2026-12-15, two weeks past it**. The window only has margin because C4 is assumed to run
~15% faster (140–150 days → Nov 9–19). If that assumption is wrong the window closes too
early, not too late. Added to `th_win_tip`, and `th_win_tip`'s "center of mass" aligned to
"late October" to match `cvt_sum`.

## 2026-07-25 — Audit: why the bottom window did *not* move

**Question raised:** after the STH-MVRV addition, the Strategy reversal and the Pi Cycle
finding, does the shaded window on the post-ATH drawdown chart still hold?

**Answer: yes — weeks 50–60 × $57K–$38K stands.** Recorded here because "we looked and
decided not to change it" is a decision, and without a record the next pass cannot tell
it apart from "we never looked".

First, an implementation fact that settles half the question: the box is **not an
independent constant**. It is drawn from the ladder's own price levels —
`y0=yd(57000), y1=yd(38000)` — so −54.9% and −69.9% are the probe top and capitulation
floor, and the box cannot drift from the ladder. "Did the window move?" reduces to "did
the ladder move?"

**Depth — the two new findings cancel:**

| Finding | Direction |
|---|---|
| Pi Cycle Top never fired (0.74× peak) | compressed amplitude → argues **shallower** |
| Strategy turned structural seller | supply pressure → argues the deep end is **more reachable** |

And the Pi Cycle result is *corroborating* evidence for a thesis already adopted — it is
why the target is −65% rather than −80%. It carries no new quantitative estimate of
depth, so moving the band on it would double-count one insight.

**Timing — nothing touched the four methods, but one needed recomputing.** See the entry
below: correcting the capitulation phase anchor moved that method from Sep–Oct to
Oct–Nov, which *tightened* the convergence rather than shifting the window. Three of four
methods now read Oct–Nov, midpoints clustering near Oct 27, all inside weeks 50–60
(Sep 21 – Nov 30). `cvt_sum` updated from "centered on October" to "centered on late
October"; the window itself is unchanged.

**The one live risk to the window, and it points later:** the capitulation-phase method
assumes the phase has begun. July's data argues it has not — see below.

## 2026-07-25 — Capitulation phase was anchored on the wrong date

**Found while checking the above.** `PHASES.c4` had the capitulation phase starting
**2026-07-12**, while the thesis text said it "began around the Jul 1 low". Two problems,
and the second is the real one:

1. Under the file's own C2/C3 convention the phase starts at the **flush** and *ends* at
   the low — C2: 2018-06-22 → 2018-12-15; C3: 2022-06-13 → 2022-11-21. So dating C4's
   start "at the low" inverts the convention.
2. Jul 12 is not a breakdown at all. It closed at **$63,780** — *above* the Jun 30 low
   close of $58,625 and after the Jul 1 intraday low of $57,800. It was a recovery date.

**Corrected to 2026-06-22**, the start of the week that broke down to $58,115 and closed
at **$59,577** — the first weekly close below the 200W MA since 2022. That is the true
analogue of the C2/C3 anchors. `ed` becomes 2026-01-06 → 2026-06-22 = **167 days** (was
187). Phase list stays contiguous; verified every coded `d` against its date span.

**This fixed an inconsistency the old anchor was hiding.** The tooltip claims ~140–150
days of capitulation at C4's ~15%-faster pace. From the old Jul 12 anchor that lands
**Nov 29 – Dec 9 — outside** the stated Oct–Nov window. From Jun 22 it lands **Nov 9–19**,
inside it. The projected phase end moved 2026-10-15 → **2026-11-09** to match; Oct 15
implied only 115 days, contradicting the same tooltip.

**Also corrected — my own earlier figures:**
- The 200W MA latch was recorded as "week of Jun 29 closed $59,486 vs $62,443". Per
  Binance, the page's own source, it is the week of **Jun 22–28 closing $59,577** against
  a **$62,414** 200W MA (−4.5%). The earlier numbers came from a news article on a
  different index; the report should quote what it can compute. Fixed in the tooltip and
  in `MAINTENANCE.md`.
- "The Jul 1 low ($58.6K)" conflated two things: **$58,625 was the lowest daily close, on
  Jun 30**; **$57,800 was the intraday low, on Jul 1**. `ph_foot` now states both.

**Left alone deliberately:** `ed`'s return stays `r:-31` — the anchor shift moves it from
−32.0% to −31.7%, inside the existing rounding, and the sibling rows use a price source I
cannot fully reconcile (`dist` codes −25 where closes give −25.8). Not worth churn.
Separately, `acc` codes 405 days where its span is 406; pre-existing, cosmetic, and the
"717 → 656 → 405 days" note depends on it, so left as-is.

## 2026-07-25 — July argues the capitulation phase has not begun

The phase timeline asserts "Capitulation (projected)" from Jun 22. The evidence gathered
during this pass runs against it:

| | late Jun | Jul 25 |
|---|---|---|
| STH-MVRV | 0.82 | **0.92** (less underwater) |
| Price | $58.6K close | **~$64K** |
| 200W MA | first weekly close below since 2022 | **reclaimed** |
| ETF flows | record 8-week outflow streak | **3 positive weeks** |
| Whales | — | **accumulating (+66.7K BTC / 60d)** |

That is a recovery, not a flush in progress. The phase label was already hedged
generically ("only confirmable in hindsight"); it now states the contradicting evidence
explicitly and tells the reader to read the label sceptically.

**Consequence for the window:** if the start date slips forward, the projected bottom
slips with it. This is the only vector currently acting on the window, and it pushes
**later**, not earlier — worth remembering when the temptation is to pull the window
forward because price is holding up.

## 2026-07-24 — Pi Cycle Top never fired in cycle 4

**Question raised:** does a *top* detector belong on a bottom-focused report?

**Finding:** the objection was right, but the real problem was larger. Computed the
ratio `MA(111d) / (2 × MA(350d))` — 1.00× is the firing threshold — across the full
Binance daily series (3,265 closes, 2017-08-17 → 2026-07-25):

| Cycle | Peak ratio | Result |
|---|---|---|
| 2021 top | **1.003** on 2021-04-17 (fired 2021-04-12 → 04-22, 11 days) | fired |
| Cycle 4 | **0.736** on 2024-06-01 | never reached the trigger — 74% of it |
| today | 0.407 | — |

Cycle 4's peak came in **June 2024, sixteen months before the Oct 2025 ATH**, and the
ATH itself did not come close: the top was built slowly enough that the 111D MA never
ran far ahead of the 350D. So the indicator did not merely fail to be *relevant* to the
bottom — **it failed at its own job this cycle.**

That miss is evidence, not noise. A fixed 2× multiple is calibrated to 2013/2017
volatility; an institutional market no longer produces that amplitude. It is the same
mechanism that makes the drawdown target −65% instead of the historical −80%, observed
on the way *up*.

**Two defects found alongside it:**
- The card computed `piCrossed` as a *state* (`ma111 >= ma350*2` today), so it read a
  permanent "not fired" for the whole bear market, and the alternate branch printed
  `"111D MA crossed 2×350D MA near ATH"` — unreachable **and false**, since it never
  crossed. Same state-vs-latch confusion as the 200W MA row.
- The tooltip directed readers to "the Pi Cycle Bottom status in the convergence
  section". No such indicator existed anywhere in the file. Dangling promise.

**Changed:** card now shows the live ratio with a computed description
("Never fired in cycle 4 · peaked at 0.74× the trigger (Jun 2024)"), derived live from
`allDailyCloses` via `calcPiCycle()` rather than hardcoded. Dead branch deleted,
dangling reference removed, and the non-firing added to `cvp_sum` as independent
corroboration for rejecting the naive −78/−84% projection. `renderScorecard` is now
re-invoked after `fetchAllHistory()` resolves, because the card needs 350+ days of
history that are not loaded on first paint.

**Data limitation to keep stating:** Binance BTCUSDT closes start 2017-08-17, so the
first valid 350-day MA is ~mid-2018. The report **cannot** verify the 2013 and 2017
Pi Cycle calls from its own data — those rest on the indicator's published record.

## 2026-07-24 — Does institutional buying invalidate the Realized Price comparison?

**Question raised:** Strategy and the ETFs bought at high prices. Does that make
"the average holder is still in profit" not comparable to prior cycles?

**Finding: no — and the arithmetic runs opposite to the intuition.** A coin's cost
basis is re-marked when it moves on-chain, so high-price accumulation pushes Realized
Price *up*, which *narrows* the gap to spot.

    realized cap ≈ 20.0M × $52,457            ≈ $1,049B
    Strategy      843,775 × ($75,476−$52,457) ≈ $19.4B  (1.9%)
    US spot ETFs  ~1.25M × ($78,000−$52,457)  ≈ $31.9B  (3.0%, ETF basis estimated)
    combined                                  ≈ $51.3B  (~4.9% of realized cap)

Strip that premium and Realized Price would be ~$49.9K rather than $52.5K — spot would
sit **29% above it instead of 22%**. Robust across the conflicting source figures for
Strategy (712K BTC @ $66K → 0.95%; 843K @ $75K → 1.9%): the conclusion does not move.

**Where the objection *is* right:** the mechanism is behavioural, not arithmetic. These
signals work because underwater holders eventually capitulate, and that forced selling
*is* the bottom. With ~10% of supply in hands that structurally don't capitulate, the
signals can fire later or weaker. That effect was already priced in — it is why the
target is −65%, not the naive −80%.

**Changed:** the arithmetic went into the `rp` tooltip so the objection is answered in
place, and `sthmvrv` was added as the 14th signal — short-term-holder MVRV excludes
permanently-held supply, so it reads the cohort that actually capitulates (0.92 now,
0.82 in June; ≤0.80 is the bottom zone).

## 2026-07-24 — Strategy has flipped from buyer to seller

Not a change we reasoned our way to — a development the Jul 21 research pass missed
entirely, surfaced while checking the question above.

mNAV hit 0.99 in late June; the treasury is ~$8.7B underwater (843,775 BTC at $75,476).
Preferred dividends annualise **$1.76B** with STRC raised to 12% from Jul 1. Strategy
sold **3,588 BTC for ~$216M** (1,363 @ $59,256 on Jun 29–30; 2,225 @ $60,773 on
Jul 1–5) to fund those distributions, is authorised to monetise up to **20,800 BTC**,
and has run two straight weeks of equity raises with **zero BTC bought**.

**Assessment:** genuine non-discretionary selling, so the 2nd-catalyst row moved from
*mixed / not fired* to *headwind / emerging, not fired*. But $216M against a $1.25B
programme is a drip, not a cascade — the capitulation tranche is marked **partially
armed** and still requires funding z < −2. Not a solvency event either: the USD reserve
is $2.55B.

**Explicitly rejected as catalysts:** the July depegs. Balance Coin's oracle exploit
lost ~$0.9M and StablR's May depeg $13.5M — orders of magnitude below anything that
moves a cycle. They stay out of the catalyst ledger.

**Consequence:** counter-scenario ("the low is already in at $58.6K") revised 30% → 25%.
One of the hands holding up the supply floor has turned into a seller.

## 2026-07-24 — Corrections to figures stated during this pass

- **Weighted readiness is 33%, not 26%.** The first estimate scored the 200W MA row as
  OFF; price is only ~1% above the line, which the live logic scores PARTIAL. Caught by
  rendering the page in headless Chrome instead of trusting a hand simulation. Active
  count (2) was unaffected. *Lesson: read the rendered value, don't recompute the
  scoring rules by hand.*
- **Pi Cycle C4 peak is 0.736, not 0.650.** The first figure was the maximum inside a
  Jan 2025–Mar 2026 window; measured from the start of the cycle-4 advance
  (`PHASES.c4[0].s`, the 2022-11-21 C3 bottom) the true peak is 0.736 on 2024-06-01.
- **Peak month renders as Jun 2024 only in UTC.** `toLocaleDateString` used the
  viewer's local timezone, turning the 2024-06-01 UTC candle into "May 2024" west of
  Greenwich. Pinned to `timeZone:'UTC'`, since the underlying candles are UTC daily.
