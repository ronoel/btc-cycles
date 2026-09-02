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
