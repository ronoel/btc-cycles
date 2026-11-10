# Bitcoin Cycle-Bottom Report

A self-updating, single-file report on where Bitcoin stands in its four-year halving cycle: a verdict, a price map of the buy plan against today's price and cost bases, the three-leg buy-now trigger, a **15-signal bottom checklist grouped into four families**, the upcoming events that can move price, the macro backdrop, timing and price estimates, and pre-registered falsifiers — with live on-chain, macro and ETF-flow data. Redesigned Nov 10, 2026 to show only the current reading; the dated history of every reading lives in [`ANALYSIS-LOG.md`](ANALYSIS-LOG.md).


## Live demo

👉 **https://ronoel.github.io/btc-cycles/**

## What's inside

| Section | Data | Description |
|---|---|---|
| **Verdict** | live + research | Ordinal stage from the checklist (TOO EARLY → APPROACHING → BOTTOM ZONE → CONFIRMED), the plan's action at today's price, buy-now trigger count, cycle clock, the report's and the market's probability that the low is in, and the next events |
| **Price map** | live | Log price scale with today's price, the rally peak, the short-term-holder cost basis, the 200-week MA, the cycle low and Realized Price, drawn against the three buy-plan bands |
| **Buy-now trigger** | live + research | Falsifier #6's three legs, checked every Monday: weekly close above ~$70K (live), Coinbase Premium on the Sunday close (manual), four-week ETF flows ≥ +$1.5B (live) |
| **Buy plan** | live | Probe / core / capitulation tranches; highlights the band the price is in |
| **15-signal bottom checklist** | live + research | Four families, ACTIVE / PARTIAL / NOT YET per row, both expert- and equal-weighted readiness, plus the four confirmation signals |
| **Upcoming events** | research | Dated calendar with date sources (primary / press / derived); the next 45 days by default |
| **Cycle charts** | live | All 4 cycles aligned at the ATH (click a week to compare), and the post-ATH drawdown with the projected bottom window and the buy bands |
| **Macro backdrop** | live + research | One line per factor; rows tagged `LIVE` compute from FRED and Farside |
| **Timing and price estimates** | live + research | Four timing methods, the price anchors and the Polymarket distribution |
| **Falsifiers** | research | Six pre-registered conditions that would prove the thesis wrong |
| **How to buy in Brazil** | fixed | Exchange comparison |

Rows carry a **`?` tooltip** with the definition of the signal. Fully translated into **EN / PT-BR / ES**.

## Data sources & freshness

- **Cycles 1–3**: historical data committed to `index.html` (fixed, won't change), but **generated rather than hand-written since Sep 3, 2026** — [`scripts/build_cycles.py`](scripts/build_cycles.py) rebuilds the `D1`/`D2`/`D3` weekly drawdown series from Binance and Bitstamp daily closes, one point per week from 82 weeks before each ATH to 140 after, and `--verify` fails if the committed arrays drift from the sources. The hand-drawn arrays they replaced were off by an average of 13.8–19.4 p.p. through the pre-ATH run-up and 5.9–7.1 p.p. after it
- **Cycle 4**: daily via [Binance public API](https://api.binance.com) (no key needed), auto-refresh every 60s
- **On-chain metrics** (Realized Price, MVRV ratio **and** MVRV Z-Score, NUPL, SOPR, Puell, **short-term-holder MVRV and its cost basis** — live since Aug 19, 2026): updated daily at 06:00 UTC by a GitHub Action running [`scripts/build_data.py`](scripts/build_data.py) → `data.json` (latest) + `history.json` (4y+ of daily series, no longer read by the page since the Nov 10, 2026 redesign removed the retro-calibration — it **accumulates**, because the provider's free window is a rolling 1,461 days and the 2022 bottom would otherwise slide out of it in Nov 2026). Source: bitcoin-data.com / BGeometrics
- **Macro** (US M2 + y/y, Fed assets, TGA, reverse repo, net liquidity, 10y & 2y nominal, 10y real, HY/IG OAS, broad trade-weighted USD): same daily Action, from FRED's keyless CSV endpoint. It has to go through the Action rather than the browser because **FRED sends no CORS header**. The dollar series is `DTWEXBGS`, not the licensed ICE DXY, and is labelled as such
- **US spot ETF net flows** (5d / 20d / 60d / YTD / cumulative): same daily Action, from Farside's all-data table (SoSoValue until Oct 8, 2026). Scraped HTML table — treated as best-effort, and a failure only marks the section stale
- **Not claimed:** a "global M2" or "global liquidity index". Japan and China have no free, current, programmatic series, so the report publishes **USD** net liquidity and says so rather than implying global coverage
- **Funding rate**: [Binance Futures public API](https://fapi.binance.com) (`fapi/v1/fundingRate`, CORS-enabled, no key) — 7-day average of the 8-hourly BTCUSDT perpetual funding, computed live on page load
- **Research snapshot**: rows tagged with a `research:` date come from a manual research pass (web + on-chain sources) and need periodic manual refresh — everything else recomputes live
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
