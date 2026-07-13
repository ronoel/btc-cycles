# Bitcoin Cycle-Bottom Report

A self-updating, single-file report that combines all 4 Bitcoin halving cycles with a full **cycle-bottom analysis**: a cycle-phase timeline, timing & price convergence across independent methods, a 13-signal bottom checklist with a weighted readiness score, a staged buy ladder, and macro/flow context. Live BTC data via Binance API, on-chain metrics via daily GitHub Actions.

## Live demo

👉 **https://ronoel.github.io/btc-cycles/**

## What's inside

| Section | Data | Description |
|---|---|---|
| **Conclusion banner** | live + research | Projected bottom window (Sep–Nov 2026), core buy zone ($44–50K), live active-signal count + weighted readiness score, and two live "where are we" progress stats (**cycle clock** = days since ATH vs the ~368-day average, **drawdown progress** = deepest low vs the −65% target) with mini progress bars |
| **Cycle position scorecard** | live | Mayer Multiple, 200D MA, Pi Cycle, weekly RSI, Fear & Greed, Realized Price, MVRV-Z, NUPL, SOPR |
| **Overlaid cycles chart** | live | All 4 cycles aligned by ATH, halving-to-halving, click any week to compare indicators across cycles |
| **Post-ATH drawdown chart** | live | Bear-market comparison with the **projected bottom window** (weeks 50–60 × −55…−70%) and buy-ladder bands drawn on the chart |
| **Cycle phase timeline** | research | Per-cycle phase bars (Accumulation → Early Bull → Markup → Distribution → Early Decline → Capitulation) with hover tooltips, a live NOW marker and a projected C4 capitulation segment; comparison table + trend notes (accumulation shrinking, distribution lengthening) |
| **Timing convergence** | research | 4 independent methods (post-ATH duration, weeks-to-low, pre-halving distance, capitulation phase) → all point to Oct 2026 |
| **Price convergence** | live + research | Diminishing-drawdown consensus, on-chain floor (0.75–0.85× Realized Price, live), 200-week MA (live), Polymarket implied distribution |
| **13-signal bottom checklist** | live + research | On-chain (live), miner, accumulation, flow and macro signals — including a **live funding rate** row (Binance Futures 7-day average) — with ACTIVE / PARTIAL / NOT YET status and a weighted readiness % (structural/valuation signals weighted above sentiment/flow) |
| **Buy ladder** | live | Staged accumulation plan (probe / core / capitulation tranches) — highlights the band the live price is in |
| **Aggressive-buy triggers** | research | The 4 signals that override the ladder when they fire together |
| **Macro & flow context** | research | Fed, DXY, tariffs, ETF flows, options positioning, 2nd-catalyst risk |
| **Historical tables** | fixed + live | Halving data, post-ATH bear markets, same-week drawdown comparison |

Every analysis card and table row carries a **`?` tooltip** explaining the methodology, thresholds and historical precedents. Interface in **EN / PT-BR / ES**.

## Data sources & freshness

- **Cycles 1–3**: historical data hardcoded (fixed, won't change)
- **Cycle 4**: daily via [Binance public API](https://api.binance.com) (no key needed), auto-refresh every 60s
- **On-chain metrics** (Realized Price, MVRV-Z, NUPL, SOPR, Puell): updated daily at 06:00 UTC by GitHub Actions → `data.json` (BGeometrics API)
- **Funding rate**: [Binance Futures public API](https://fapi.binance.com) (`fapi/v1/fundingRate`, CORS-enabled, no key) — 7-day average of the 8-hourly BTCUSDT perpetual funding, computed live on page load
- **Sentiment**: [alternative.me](https://alternative.me/crypto/fear-and-greed-index/) Fear & Greed
- **Research snapshot**: rows/cards tagged `research: Jul 12, 2026` come from a manual research pass (web + on-chain sources) and need periodic manual refresh — everything else recomputes live
- **ATH reference**: $126,296 on October 6, 2025 · next halving ~Apr 2028

## Setup (GitHub Pages)

1. Fork/create the repo, upload `index.html` + `data.json` + `.github/workflows/update-data.yml`
2. Add the `BGEOMETRICS_TOKEN` secret (Settings → Secrets → Actions) for the daily on-chain update
3. **Settings → Pages → Source** → `main` branch, `/ (root)` → Save

## Maintenance

See [`MAINTENANCE.md`](MAINTENANCE.md) — what updates automatically (Binance live, daily on-chain Action), what needs a manual research refresh (**every 2–4 weeks**, weekly inside the Sep–Nov 2026 bottom window), and which events require rewriting the thesis.

## Disclaimer

Cycle analysis is historical pattern matching, not financial advice. Past cycles do not guarantee future outcomes.

## License

MIT
