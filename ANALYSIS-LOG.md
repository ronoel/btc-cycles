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
