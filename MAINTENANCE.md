# Maintenance & Update Schedule

What keeps this report accurate, who updates it (automatic vs manual), and how often.

## 1. Automatic — no action required

| Data | Source | Frequency | Where |
|---|---|---|---|
| BTC price, drawdown, cycle-4 chart lines, cycle low | Binance public API | On page load + every 60s | client-side JS |
| Price indicators (Mayer Multiple, 200D MA, Pi Cycle Top, weekly RSI, 200-week MA) | Computed from Binance daily closes | On page load | client-side JS |
| Fear & Greed | alternative.me API | On page load | client-side JS |
| Funding rate (7-day avg of 8-hourly BTCUSDT perpetual funding) | Binance Futures API (`fapi/v1/fundingRate`) | On page load | client-side JS (`fetchFunding()`) |
| On-chain metrics (Realized Price, MVRV-Z, NUPL, SOPR, Puell) | BGeometrics API → `data.json` | **Daily 06:00 UTC** | GitHub Action `update-data.yml` |
| Live checklist rows (tagged `LIVE`, incl. funding rate), on-chain floor card, 200W MA card, buy-ladder highlight, active-signal count, weighted readiness %, cycle-clock & drawdown-progress thesis stats | Derived from the above | On page load | client-side JS |

**Health check (monthly):** confirm the GitHub Action is green (repo → Actions → "Update on-chain data") and `data.json`'s `updated` field is recent. If BGeometrics changes its response shape, `extract_latest` in the workflow and `fetchOnChainData()` in `index.html` are the two places to fix.

## 2. Manual — research snapshot (tagged `research: Jul 24, 2026` in the UI)

**Frequency: every 2–4 weeks.** Tighten to **weekly** when either happens:
- we enter the projected bottom window (**Sep–Nov 2026**), or
- BTC closes below **$57K** (probe band reached), or
- a 2nd crypto-native catalyst fires (exchange failure, stablecoin depeg, >$500M exploit).

What to refresh (all live in the `L.en` / `L.pt` i18n objects in `index.html`):

| Item | i18n keys | What to look up |
|---|---|---|
| Static checklist rows | `bs` entries `puell`*, `hash`, `lth`, `resv`, `cbp`, `fed` (fields `r` + `st`) | Hash Ribbons cross status, LTH supply, exchange reserves + SSR, Coinbase Premium streak, Fed/DXY liquidity turn |
| Macro & flow table | `mac` (fields `r` + `e`) | Fed rate path, DXY, tariffs, recession odds, weekly ETF flows, Deribit OI/max pain, catalyst watch, BTC-vs-equities |
| Polymarket card | `cvp[3]` (fields `v` + `d`) | P(BTC < $55K / $50K / $40K) for 2026, plus P(BTC tags $70K) as the market's counter-read |
| Trigger cards' current readings | `trig` (field `d`) | Coinbase Premium, ETF streak, hash ribbons, Fed pricing. Lead each with its status in bold (`FIRED` / `PARTIAL` / `NOT FIRED`) and keep the tally in `trig_n` in sync |
| Cycle-phase timeline (C4) | `PHASES.c4` const (Distribution / Early Decline / projected Capitulation dates) + phase table totals row in `renderPhases()` | Refine the C4 phase boundaries as new price action confirms them; the Capitulation segment stays `proj:true` (striped bar, "(proj.)" label, NOW marker) until the bottom is confirmed |
| Snapshot date badge | `an_asof` (EN + PT) | set to the new research date |

\* `puell` auto-switches to LIVE if `data.json` provides it — only its static fallback text needs the date kept honest. The `fund` (funding rate) row is normally LIVE from Binance Futures; only its static fallback text (`bs` entry `fund`, field `r`) matters when the Futures API is unreachable — keep the date honest there too.

**Procedure:** run a research pass (web search: each item above), edit the i18n arrays in `index.html` (EN + PT-BR; ES falls back to EN), bump `an_asof`, verify locally (`python3 -m http.server` + open), commit & push.

## 2b. Signal & trigger conventions

Rules that keep the checklist honest over time. **Never retro-edit a threshold because you dislike the reading it just produced** — change the spec prospectively and record it here.

**Latched vs live signals.** Some checklist rows are state ("is it true right now"), others are events ("has it happened this cycle"). The 200W MA row is an *event*: once a weekly close prints below the line, the signal has fired for the cycle even if price reclaims it. The row keeps rendering LIVE state — the latch lives in its tooltip and must be kept there.
- Latched so far in cycle 4: **200W MA — week of Jun 29, 2026 closed $59,486 vs a $62,443 200W MA** (first since 2022; reclaimed after).

**Trigger changelog.**

| Date | Trigger | Change |
|---|---|---|
| Jul 24, 2026 | ETF inflows 3+ weeks | Fired on the letter of the spec (+$197M / +$76M / +$274M) but with ~7% of the outflow recovered. Marked *fired — low conviction*; magnitude stated inline rather than moving the goalposts. **v2 spec, applies from the next firing:** require cumulative net inflows ≥ $1.5–2B, or ≥ 25% of the preceding outflow streak, alongside the 3-week condition. |
| Jul 24, 2026 | Capitulation tranche gate | Stays strictly crypto-native, but gained a documented parallel **macro gate** (Fed hike odds repriced + DXY breaks 103 + 200W MA lost again) so an oil-shock → CPI-reacceleration path to $38–44K is not silently uncovered. |

## 3. Event-driven — rewrite, not refresh

| Event | Action |
|---|---|
| **2nd crypto-native catalyst fires** | Update `mac` catalyst row + checklist; capitulation tranche ($38–44K) becomes actionable — reflect in thesis if bands shift |
| **Bottom confirmed** (8+ checklist signals active, price reclaims Realized Price and holds) | Rewrite thesis banner (`th_*` keys) from "projected bottom" to "bottom in / accumulation"; fill Cycle 4 row in the "Post-ATH bear market" table (low, date, weeks, drawdown); retire or archive the buy ladder; in the **cycle-phase timeline** (`PHASES.c4` const) set the projected Capitulation segment's real end date and remove the `proj:true` flag (fill `d`/`r`), so the bar, NOW marker and phase table reflect the confirmed bottom |
| **Thesis invalidated** (e.g. sustained reclaim of ~$90K+ with bottom signals still inactive, or new ATH) | Re-derive the whole convergence analysis — bands and window are no longer valid |
| **Price bands/window revised by new research** | Update in ALL places at once: `LAD_BANDS` const, `lad` rows, ch2 band plugin price levels (`[57000,50000,44000,38000]` + window weeks 50–60), `th_core` value in thesis HTML, `cvp` cards, `th_p` text |
| **New halving date estimate** | `H5` const in `index.html` |
| **Window or thesis changed (any of the above)** | Also update the OG/Twitter meta descriptions in the `<head>` of `index.html` (they cite the Sep–Nov 2026 window and $44–50K zone) and regenerate the share image: edit `og-card.html`, open it in a 1200×630 window, screenshot → replace `og.png` |

## 4. Fixed — never touch

Cycles 1–3 historical data (`D1`/`D2`/`D3` arrays, halving & bear-market tables), ATH reference ($126,296 / Oct 6, 2025 — `ATH`/`ATHD` consts), phase history.

---
**Last research snapshot: Jul 24, 2026** · next manual refresh due: **early–mid Aug 2026** (switch to **weekly** from September — projected bottom window)

Bring the Jul 28–29 FOMC outcome into the next pass: it is the single scheduled event that can move the `fed` checklist row and the Fed-pivot trigger.
