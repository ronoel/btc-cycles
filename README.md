# Bitcoin Halving Cycles Dashboard

A self-updating, single-file dashboard that overlays all 4 Bitcoin halving cycles aligned by their ATH (all-time high). Auto-fetches live BTC price from the CoinGecko API and persists weekly data in localStorage.

## Live demo

👉 **https://ronoel.github.io/btc-cycles/**

## Features

- **Auto-updating**: fetches current BTC price on every page load via CoinGecko API (free, no key needed)
- **Persistent data**: weekly drawdown data saved in localStorage — only fetches the delta since last visit
- **Offline-capable**: works with cached data when there's no internet connection
- **4 overlaid cycles**: halving-to-halving view aligned by ATH for direct comparison
- **Post-ATH drawdown chart**: isolated bear market comparison
- **Interactive legends**: click to toggle individual cycles on/off
- **Full data tables**: halving stats, bear market data, same-week comparison
- **Mobile responsive**: works on desktop and mobile

## Setup (GitHub Pages)

1. Create a new repository on GitHub (e.g., `btc-cycles`)
2. Upload `index.html` to the repository root
3. Go to **Settings → Pages → Source** → select `main` branch, `/ (root)` folder
4. Click **Save** — your dashboard will be live at `https://YOUR_USERNAME.github.io/btc-cycles/`

## Data sources

- **Cycles 1-3**: historical data hardcoded (fixed, won't change)
- **Cycle 4**: seed data up to week 23 + auto-extended via [CoinGecko API](https://www.coingecko.com/en/api)
- **ATH reference**: $126,296 on October 6, 2025

## How the auto-update works

```
Page load
  ↓
Check localStorage for saved cycle 4 data
  ↓
Fetch current BTC price from CoinGecko
  ↓
Calculate current week number from ATH
  ↓
If weeks are missing → fetch historical range from CoinGecko
  ↓
Merge new data with saved data → save to localStorage
  ↓
Render all charts and tables
```

## License

MIT
