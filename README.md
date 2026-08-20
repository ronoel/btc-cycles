# Bitcoin Cycle-Bottom Report

A self-updating, single-file report that combines all 4 Bitcoin halving cycles with a full **cycle-bottom analysis**: a cycle-phase timeline, timing & price convergence, a **15-signal bottom checklist grouped into four families**, a **retro-calibration that replays the same scoring rules over the confirmed November 2022 bottom**, a staged buy ladder, pre-registered falsifiers, and computed macro/flow context. Live BTC data via Binance, on-chain + macro + ETF-flow data via a daily GitHub Action.

> The headline finding of the current build: the eight scoring rules with clean history in both eras read **95% at the confirmed Nov 21, 2022 bottom** and **21% today**. That is what makes the readiness number mean something rather than assert something — and the 95% is itself the point: when short-term-holder MVRV joined the subset in Aug 2026 it turned out to read PARTIAL at that bottom, so the calibration's first job after being extended was to fail one of the checklist's own thresholds rather than confirm it.

## Live demo

👉 **https://ronoel.github.io/btc-cycles/**

## What's inside

| Section | Data | Description |
|---|---|---|
| **Conclusion banner** | live + research | Projected bottom window (Sep–Nov 2026), core buy zone ($44–50K), live active-signal count + weighted readiness score, and two live "where are we" progress stats (**cycle clock** = days since ATH vs the ~370-day C2/C3 average, **drawdown progress** = deepest low vs the −65% target) with mini progress bars |
| **Cycle position scorecard** | live | Mayer Multiple, 200D MA, Pi Cycle, weekly RSI, Fear & Greed, Realized Price, MVRV-Z, NUPL, SOPR |
| **Overlaid cycles chart** | live | All 4 cycles aligned by ATH, halving-to-halving, click any week to compare indicators across cycles |
| **Post-ATH drawdown chart** | live | Bear-market comparison with the **projected bottom window** (weeks 50–60 × −55…−70%) and buy-ladder bands drawn on the chart |
| **Cycle phase timeline** | research | Per-cycle phase bars (Accumulation → Early Bull → Markup → Distribution → Early Decline → Capitulation) with hover tooltips, a live NOW marker and a projected C4 capitulation segment; comparison table + trend notes (accumulation shrinking, distribution lengthening) |
| **Timing convergence** | research | 4 independent methods (post-ATH duration, weeks-to-low, pre-halving distance, capitulation phase) → all point to Oct 2026 |
| **Price convergence** | live + research | Diminishing-drawdown consensus, on-chain floor (0.75–0.85× Realized Price, live), 200-week MA (live), Polymarket implied distribution |
| **15-signal bottom checklist** | live + research | Grouped into four families (Valuation · Capitulation · Supply & flows · Macro liquidity) because the signals are not independent. ACTIVE / PARTIAL / NOT YET per row, a family-lit count driving an ordinal stage (TOO EARLY → APPROACHING → BOTTOM ZONE → CONFIRMED), and **both** the expert-weighted and equal-weighted readiness scores, published side by side so the reader can see how little the weighting choice matters. Each family card states its share of the weighted score (computed from the per-signal weights, not allocated top-down), and every row carries a **response-latency tag** — fast (days) / medium (weeks) / slow (months) — because 7 of the 15 signals are slow by construction, which is why fast rows can improve while valuation rows stay dark without the two contradicting each other. Live rows include funding rate, **short-term-holder MVRV**, a **computed macro-liquidity composite** (M2 y/y · dollar vs 200d · real 10y vs 200d) and **ETF net flows** |
| **Retro-calibration** | live | Replays *today's exact scoring rules* over cycle 3 using the same code path, on the eight signals with clean daily history in both eras (short-term-holder MVRV joined the subset on Aug 19, 2026). Shows the readiness trace by weeks-since-ATH for cycle 3 vs cycle 4, the reading at the confirmed 2022 bottom, the peak, and the bear-rally high — with its own caveats stated (it marks a **zone**, not a date, and N=1) |
| **Falsifiers** | research | Six pre-registered conditions that would prove the thesis wrong, plus the symmetric-error trigger that deploys the ladder early if the bottom turns out to be shallower. Exists because every signal here moves toward ACTIVE as price falls — without this the framework can only say "not yet" or "buy", never "I am broken" |
| **Buy ladder** | live | Staged accumulation plan (probe / core / capitulation tranches) — highlights the band the live price is in |
| **Aggressive-buy triggers** | research | The 4 signals that override the ladder when they fire together |
| **Macro & flow context** | live + research | Rows tagged `LIVE` compute from FRED and SoSoValue: rates & real yields, USD net liquidity (Fed assets − TGA − RRP), the dollar index, credit spreads and ETF flows. Narrative rows cover Fed policy, tariffs/legal risk, geopolitics, Strategy/corporate-treasury flow, 2nd-catalyst risk and the **dated events scheduled inside the bottom window**. Credit spreads are deliberately kept *out* of the score and used as a drawdown-**depth** modifier |
| **Historical tables** | fixed + live | Halving data, post-ATH bear markets, same-week drawdown comparison |

Every analysis card and table row carries a **`?` tooltip** explaining the methodology, thresholds and historical precedents. Fully translated into **EN / PT-BR / ES** — including the analysis, which until Aug 2026 fell back to English in Spanish.

## Data sources & freshness

- **Cycles 1–3**: historical data hardcoded (fixed, won't change)
- **Cycle 4**: daily via [Binance public API](https://api.binance.com) (no key needed), auto-refresh every 60s
- **On-chain metrics** (Realized Price, MVRV ratio **and** MVRV Z-Score, NUPL, SOPR, Puell, **short-term-holder MVRV and its cost basis** — live since Aug 19, 2026): updated daily at 06:00 UTC by a GitHub Action running [`scripts/build_data.py`](scripts/build_data.py) → `data.json` (latest) + `history.json` (4y+ of daily series, used only by the retro-calibration — it **accumulates**, because the provider's free window is a rolling 1,461 days and the 2022 bottom would otherwise slide out of it in Nov 2026). Source: bitcoin-data.com / BGeometrics
- **Macro** (US M2 + y/y, Fed assets, TGA, reverse repo, net liquidity, 10y & 2y nominal, 10y real, HY/IG OAS, broad trade-weighted USD): same daily Action, from FRED's keyless CSV endpoint. It has to go through the Action rather than the browser because **FRED sends no CORS header**. The dollar series is `DTWEXBGS`, not the licensed ICE DXY, and is labelled as such
- **US spot ETF net flows** (5d / 20d / 60d / YTD / cumulative / AUM): same daily Action, from SoSoValue. Undocumented endpoint — treated as best-effort, and a failure only marks the section stale
- **Not claimed:** a "global M2" or "global liquidity index". Japan and China have no free, current, programmatic series, so the report publishes **USD** net liquidity and says so rather than implying global coverage
- **Funding rate**: [Binance Futures public API](https://fapi.binance.com) (`fapi/v1/fundingRate`, CORS-enabled, no key) — 7-day average of the 8-hourly BTCUSDT perpetual funding, computed live on page load
- **Sentiment**: [alternative.me](https://alternative.me/crypto/fear-and-greed-index/) Fear & Greed
- **Research snapshot**: rows/cards tagged `research: Jul 24, 2026` come from a manual research pass (web + on-chain sources) and need periodic manual refresh — everything else recomputes live
- **ATH reference**: $126,296 on October 6, 2025 · next halving ~Apr 2028

## Setup (GitHub Pages)

1. Fork/create the repo, upload `index.html` + `data.json` + `history.json` + `scripts/build_data.py` + `.github/workflows/update-data.yml`
2. *(Optional)* Add the `BGEOMETRICS_TOKEN` secret (Settings → Secrets → Actions). Every source is keyless; the token only lifts bitcoin-data.com's anonymous rate limit of 10 requests/hour and may widen the history window
3. **Settings → Pages → Source** → `main` branch, `/ (root)` → Save

## Maintenance

See [`MAINTENANCE.md`](MAINTENANCE.md) — what updates automatically (Binance live, daily on-chain Action), what needs a manual research refresh (**every 2–4 weeks**, weekly inside the Sep–Nov 2026 bottom window), and which events require rewriting the thesis.

See [`ANALYSIS-LOG.md`](ANALYSIS-LOG.md) for the reasoning behind the conclusions — the calculations, the counter-arguments tested, rejected hypotheses and data limitations, dated. A conclusion lives in `index.html`; a procedure in `MAINTENANCE.md`; a derivation in the analysis log.

## Support

If this report is useful, you can send a Lightning tip: `squashycolumn40@walletofsatoshi.com` ⚡

## Disclaimer

Cycle analysis is historical pattern matching, not financial advice. Past cycles do not guarantee future outcomes.

## License

MIT
