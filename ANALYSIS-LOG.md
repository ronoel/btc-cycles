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
