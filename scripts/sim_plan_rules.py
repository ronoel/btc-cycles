#!/usr/bin/env python3
"""Backtests behind the Nov 21, 2026 plan-rule review (ANALYSIS-LOG.md, "plan rules by the numbers").

    python3 scripts/sim_plan_rules.py --cache DIR     # fetch once into DIR (not the repo), then report

Three questions, each answered on data the free sources cover:
  core  - does the core tranche's confirmation (NUPL < 0, MVRV-Z < 0, Puell < 0.5, premium turning up) ever open
          inside its band? CoinMetrics community metrics, 2010-, cross-checked against the page's provider.
  leg2  - does any Coinbase-premium form separate bear rallies from real recoveries, and does staging help?
          Coinbase BTC-USD vs Binance BTCUSDT daily closes, USDT-USD from Coinbase (2021-) / CoinMetrics (2017-).
  cap   - what releasing the capitulation tranche costs or gains per scenario low (measured post-low recoveries).

Definitions were fixed before outcomes were computed and no threshold here was tuned: the gate thresholds are the
published ones, the leg-1 analog is the $70K / $57.8K ratio the trigger was set at (1.21) applied only once the
running low is at least 50% under the ATH, and every premium form is reported. N is 2-4 cycles: read ranges and
failure modes, not optima. Bitfinex USDT is not used (it carries its own premium: +0.06% mean, 0.61% max vs Coinbase).
"""
import argparse, datetime as dt, json, math, os, sys, time, urllib.request

UA = {'User-Agent': 'btc-cycles/1.0 (+https://github.com/ronoel/btc-cycles)'}
CYC = {'C0': ('2011-06-08', '2011-11-18'), 'C1': ('2013-12-04', '2015-01-14'),
       'C2': ('2017-12-17', '2018-12-15'), 'C3': ('2021-11-08', '2022-11-21'), 'C4': ('2025-10-06', None)}


def get(url):
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:  # noqa: BLE001 - retry any transport error
            err = e; time.sleep(2)
    raise err


def cm_series(asset, metrics, start):
    rows, url = [], (f'https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets={asset}'
                     f'&metrics={metrics}&frequency=1d&start_time={start}&page_size=10000')
    while url:
        r = get(url); rows += r['data']; url = r.get('next_page_url')
    return rows


def cb_candles(prod, start):
    out, t, end = {}, dt.datetime.fromisoformat(start).replace(tzinfo=dt.UTC), dt.datetime.now(dt.UTC)
    while t < end:
        t2 = min(t + dt.timedelta(days=299), end)
        for c in get(f'https://api.exchange.coinbase.com/products/{prod}/candles?granularity=86400'
                     f'&start={t.isoformat()}&end={t2.isoformat()}'):
            out[dt.datetime.fromtimestamp(c[0], dt.UTC).date().isoformat()] = c[4]
        t = t2 + dt.timedelta(days=1); time.sleep(0.25)
    return out


def fetch(D):
    os.makedirs(D, exist_ok=True)
    def once(name, fn):
        p = os.path.join(D, name)
        if not os.path.exists(p):
            json.dump(fn(), open(p, 'w'))
        return json.load(open(p))
    cm = once('cm.json', lambda: cm_series('btc', 'CapMVRVCur,CapMrktCurUSD,IssTotUSD,PriceUSD', '2010-07-18'))
    def binance():
        k, st = [], 1502928000000
        while True:
            r = get(f'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime={st}&limit=1000')
            k += r
            if len(r) < 1000: break
            st = r[-1][0] + 86400000
        return {dt.datetime.fromtimestamp(x[0] / 1000, dt.UTC).date().isoformat(): [float(x[3]), float(x[4])]
                for x in k if x[6] < time.time() * 1000}          # completed candles only
    bn = once('bn.json', binance)
    cb = once('cb.json', lambda: cb_candles('BTC-USD', '2017-08-17'))
    cbu = once('cbusdt.json', lambda: cb_candles('USDT-USD', '2021-04-01'))
    cmu = once('cmusdt.json', lambda: {x['time'][:10]: float(x['PriceUSD'])
                                       for x in cm_series('usdt', 'PriceUSD', '2017-06-01')})
    def farside():
        sys.path.insert(0, os.path.dirname(__file__)); import build_data as b
        p = b.get(b.FARSIDE); p = p.decode() if isinstance(p, bytes) else p
        return [list(x) for x in b.parse_farside(p)]
    etf = once('etf.json', farside)
    return cm, bn, cb, cbu, cmu, etf


def onchain(cm):
    """NUPL, MVRV-Z (expanding std of market cap), Puell (issuance / 365d mean), Realized Price."""
    m, s, s2, n = {}, 0.0, 0.0, 0
    for r in cm:
        try:
            mv, mc, px = float(r['CapMVRVCur']), float(r['CapMrktCurUSD']), float(r['PriceUSD'])
        except (KeyError, TypeError, ValueError):
            continue
        n += 1; s += mc; s2 += mc * mc
        sd = math.sqrt(max(s2 / n - (s / n) ** 2, 1e-9))
        iss = float(r.get('IssTotUSD') or 'nan')
        m[r['time'][:10]] = {'px': px, 'nupl': 1 - 1 / mv, 'mvrvz': (mc - mc / mv) / sd, 'rp': px / mv, 'iss': iss}
    ds = sorted(m)
    for i, d in enumerate(ds):
        w = [m[x]['iss'] for x in ds[max(0, i - 364):i + 1] if not math.isnan(m[x]['iss'])]
        m[d]['puell'] = m[d]['iss'] / (sum(w) / len(w)) if len(w) >= 300 and not math.isnan(m[d]['iss']) else None
    return m


def days_between(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def report_core(m):
    ds = sorted(m)
    print('== CORE GATE: first date each condition held after the ATH (CoinMetrics daily close)')
    for c, (ath, low) in CYC.items():
        end = low or ds[-1]; athp = m[ath]['px']
        w = [d for d in ds if ath <= d <= end]; lowd = min(w, key=lambda d: m[d]['px']); lowp = m[lowd]['px']
        print(f'{c} ATH {ath} {athp:,.0f}  low {lowd} {lowp:,.0f} ({(lowp / athp - 1) * 100:.1f}%)')
        conds = [('dd<=-60% (core top)', lambda o: o['px'] <= athp * 0.40),
                 ('NUPL<0 (=MVRV-Z<0)', lambda o: o['nupl'] < 0),
                 ('Puell<0.5', lambda o: o['puell'] is not None and o['puell'] < 0.5),
                 ('NUPL<0 & Puell<0.5', lambda o: o['nupl'] < 0 and o['puell'] is not None and o['puell'] < 0.5)]
        for lab, f in conds:
            d = next((x for x in w if f(m[x])), None)
            print(f'   {lab:22s} ' + (f'{d} {m[d]["px"]:>9,.0f} {(m[d]["px"] / lowp - 1) * 100:+6.1f}% vs low, '
                                      f'{days_between(d, lowd):4d}d before, dd {(m[d]["px"] / athp - 1) * 100:.0f}%'
                                      if d else 'never'))
    last = ds[-1]; mp = sum(m[x]['px'] for x in ds[-365:]) / 365
    r = [m[d]['puell'] / (m[d]['px'] / (sum(m[x]['px'] for x in ds[i - 364:i + 1]) / 365))
         for i, d in enumerate(ds) if d >= '2025-05-01' and m[d]['puell']]
    r.sort(); q = lambda f: r[int(f * (len(r) - 1))]
    print(f'Puell / (price/365d mean) since 2025-05 (block-count noise): p5 {q(.05):.2f} p50 {q(.5):.2f} p95 {q(.95):.2f}'
          f' min {r[0]:.2f} max {r[-1]:.2f} -> a single daily Puell < 0.5 needs price < 0.5/ratio x mean')
    for P in (56000, 48000):
        px = [m[x]['px'] for x in ds[-365:]]; out = []
        for w in range(27):
            if w: px = px[7:] + [P] * 7
            if w in (0, 4, 8, 13, 26): out.append(f'+{w}w ${0.5 * sum(px) / 365:,.0f}')
        print(f'   Puell-0.5 price (median ratio) if price holds at ${P:,}: ' + ' '.join(out))
    print(f'Today ({last}): Puell {m[last]["puell"]:.3f} ~ price/365d mean {m[last]["px"] / mp:.3f}; '
          f'Puell 0.5 at ~${0.5 * mp:,.0f} (0.47-0.53: ${0.47 * mp:,.0f}-{0.53 * mp:,.0f}); '
          f'Realized Price ${m[last]["rp"]:,.0f}')


def premium(bn, cb, cbu, cmu):
    u = lambda d: cbu.get(d) or cmu.get(d)
    ds = sorted(d for d in bn if d in cb and u(d))
    return ds, {d: (cb[d] / bn[d][1] - 1) * 100 for d in ds}, {d: (cb[d] / (bn[d][1] * u(d)) - 1) * 100 for d in ds}


def report_leg2(bn, cb, cbu, cmu, etf):
    ds, raw, adj = premium(bn, cb, cbu, cmu)
    forms = {'F0 no leg 2': lambda s, r, a: True, 'F1 raw Sunday': lambda s, r, a: raw[s] > 0,
             'F2 adj Sunday': lambda s, r, a: adj[s] > 0, 'F3 raw week mean': lambda s, r, a: sum(r) / len(r) > 0,
             'F4 adj week mean': lambda s, r, a: sum(a) / len(a) > 0, 'F5 any raw +': lambda s, r, a: max(r) > 0,
             'F6 any adj +': lambda s, r, a: max(a) > 0}
    suns = [d for d in ds if dt.date.fromisoformat(d).weekday() == 6]
    print('\n== LEG 2: weekly close >= 1.21 x running low (low <= 50% under ATH) AND form; C4 also needs ETF d20 >= +1.5B.'
          '\n   FALSE = a lower low printed later in the cycle.')
    fires = {}
    for c, ath, end in [('C2', '2017-12-17', '2019-12-15'), ('C3', '2021-11-08', '2023-11-21'), ('C4', '2025-10-06', ds[-1])]:
        lo = athp = 0; lo = 1e18
        for s in [d for d in suns if ath <= d <= end]:
            lo = min(lo, min(v[0] for d, v in bn.items() if ath <= d <= s)); athp = max(bn[d][1] for d in bn if ath <= d <= s)
            if lo > 0.5 * athp or bn[s][1] < 1.21 * lo: continue
            wk = [x for x in ((dt.date.fromisoformat(s) - dt.timedelta(days=i)).isoformat() for i in range(6, -1, -1)) if x in raw]
            r, a = [raw[x] for x in wk], [adj[x] for x in wk]
            ok = {k: f(s, r, a) for k, f in forms.items()}
            if c == 'C4':
                e = sum(v for d, v in [x for x in etf if x[0] <= s][-20:])      # the arbiter: 20 sessions
                ok = {k: v and e >= 1500 for k, v in ok.items()}
            false = min(v[0] for d, v in bn.items() if s < d <= end) < lo if any(s < d <= end for d in bn) else False
            fires.setdefault(c, []).append((s, bn[s][1], false, ok))
        for k in forms:
            f_ = [(s, round(p)) for s, p, fa, ok in fires.get(c, []) if ok[k] and fa]
            t_ = [(s, round(p)) for s, p, fa, ok in fires.get(c, []) if ok[k] and not fa]
            print(f'   {c} {k:17s} false {len(f_):3d} (first {f_[0] if f_ else "-"}) | true {len(t_):3d} (first {t_[0] if t_ else "-"})')
    print('   staging on F1, first fire of each episode (gaps <= 4 weeks): lump vs 4 weekly quarters')
    for c, rows in fires.items():
        eps, prev = [], None
        for s, p, fa, ok in rows:
            if not ok['F1 raw Sunday']: continue
            if prev and days_between(prev, s) <= 28: eps[-1].append((s, p, fa))
            else: eps.append([(s, p, fa)])
            prev = s
        for e in eps:
            i = suns.index(e[0][0]); nxt = [suns[i + k] for k in range(4) if i + k < len(suns)]
            stg = sum(bn[d][1] for d in nxt) / len(nxt)
            print(f'   {c} {e[0][0]} {"FALSE" if e[0][2] else "true "} lump {e[0][1]:>9,.0f}  staged {stg:>9,.0f} ({(stg / e[0][1] - 1) * 100:+.1f}%)')


def report_extras(m, bn, cb, cbu, cmu):
    ds, raw, adj = premium(bn, cb, cbu, cmu)
    k = [d for d in cbu if d in cmu]; dd = sorted((cmu[d] - cbu[d]) * 100 for d in k)
    print(f'\n== USDT source check: CoinMetrics - Coinbase USDT-USD, n {len(k)}, mean {sum(dd) / len(dd):+.3f}% '
          f'max|d| {max(map(abs, dd)):.3f}%')
    sun = [d for d in ds if dt.date.fromisoformat(d).weekday() == 6 and d in cbu]
    for lab, f in [('USDT < 0.999', lambda d: cbu[d] < 0.999), ('USDT >= 0.999', lambda d: cbu[d] >= 0.999)]:
        x = [d for d in sun if f(d)]
        print(f'   Sundays {lab}: n {len(x)}, raw > 0 {sum(raw[d] > 0 for d in x) / max(1, len(x)):.0%}, '
              f'adjusted > 0 {sum(adj[d] > 0 for d in x) / max(1, len(x)):.0%}')
    ma = lambda sr, i, n: sum(sr[x] for x in ds[max(0, i - n + 1):i + 1]) / min(n, i + 1)
    fam = {'P1 7d adj > 0': lambda i: ma(adj, i, 7) > 0,
           'P2 7d adj > 28d & rising': lambda i: ma(adj, i, 7) > ma(adj, i, 28) and ma(adj, i, 7) > ma(adj, i - 7, 7),
           'P3 7d raw > 0': lambda i: ma(raw, i, 7) > 0}
    print('== "Premium turning up" family (fixed before looking), with NUPL < 0:')
    for c in ('C2', 'C3'):
        ath, low = CYC[c]; idx = [i for i, d in enumerate(ds) if ath <= d <= low and i > 35 and m[d]['nupl'] < 0]
        for kk, f in fam.items():
            on = [i for i in idx if f(i)]
            first = ds[on[0]] if on else None
            print(f'   {c} {kk:26s} first {first} {bn[first][1] if first else 0:>9,.0f} '
                  f'({(bn[first][1] / bn[low][0] - 1) * 100 if first else 0:+.0f}% vs low) | on {len(on) / max(1, len(idx)):.0%} of NUPL<0 days')
    print('   C4 last 30 days on: ' + ' '.join(f'{kk[:2]} {sum(f(i) for i in range(len(ds) - 30, len(ds))) / 30:.0%}' for kk, f in fam.items()))
    print('== Weekly close vs first daily close under each band top (closes, not intraday touches; all deep cycles):')
    for c in ('C1', 'C2', 'C3'):
        ath, low = CYC[c]; athp = m[ath]['px']; dsm = sorted(m)
        for lv in (0.45, 0.40, 0.35):
            d1 = next(d for d in dsm if d >= ath and m[d]['px'] <= athp * lv)
            w1 = next(d for d in dsm if d >= ath and dt.date.fromisoformat(d).weekday() == 6 and m[d]['px'] <= athp * lv)
            print(f'   {c} -{int((1 - lv) * 100)}%: daily {d1} | weekly {w1} {(m[w1]["px"] / (athp * lv) - 1) * 100:+.1f}% vs level')
    print('== Interim lows that later broke: weeks each running low stood (daily lows, Binance; CoinMetrics before 2017)')
    for c in ('C1', 'C2', 'C3', 'C4'):
        ath, low = CYC[c]; end = low or max(bn)
        src = {d: v[0] for d, v in bn.items()} if ath >= '2017-08-17' else {d: m[d]['px'] for d in m}
        seq = sorted(d for d in src if ath <= d <= end); recs, lo = [], 1e18
        for d in seq:
            if src[d] < lo * 0.97 or not recs:      # a new low at least 3% under the standing one
                if recs: recs[-1].append(d)
                recs.append([d, src[d]]); lo = src[d]
            elif src[d] < lo: lo = src[d]; recs[-1][1] = lo
        stood = [(r[0], round(r[1]), days_between(r[0], r[2]) / 7) for r in recs if len(r) == 3]
        top = sorted(stood, key=lambda x: -x[2])[:3]
        print(f'   {c}: longest-standing lows that broke: ' + '; '.join(f'{d} ${p:,} stood {w:.0f}w' for d, p, w in top))


def report_cap(m):
    ds = sorted(m)
    add = lambda d, n: (dt.date.fromisoformat(d) + dt.timedelta(days=n)).isoformat()
    print('\n== CAPITULATION RELEASE: price / cycle low after the low (cost of waiting)')
    mult = {}
    for c in ('C1', 'C2', 'C3'):
        ath, low = CYC[c]; lp = m[low]['px']
        mult[c] = {w: m[add(low, 7 * w)]['px'] / lp for w in (4, 8, 13, 26, 52)}
        print(f'   {c} low week {days_between(ath, low) / 7:.0f}: ' + ' '.join(f'+{w}w x{v:.2f}' for w, v in mult[c].items()))
    m52 = sorted(v[52] for v in mult.values())[1]; m13 = [v[13] for v in mult.values()]
    scen = [(56.0, .235), (52.5, .271), (47.5, .284), (42.5, .090), (37.5, .041), (32.0, .079)]
    print(f'   regret table: value of the 35% tranche 52w after the low (x{m52:.2f} median), cash x1.04;'
          f' scenario weights = Polymarket touch-by-Dec-31 buckets, Nov 21 ($K, weight): {scen}')
    fill = lambda L, lo, hi: max(L, (lo + hi) / 2) if L < hi else None
    rules = {'R0 cap band only (status quo)': lambda L: fill(L, 38, 44),
             'R1 merged into core band': lambda L: fill(L, 44, 50),
             f'R2 cap band, else week 70 (x{min(m13):.2f})': lambda L: fill(L, 38, 44) or L * min(m13),
             f'R2 cap band, else week 70 (x{max(m13):.2f})': lambda L: fill(L, 38, 44) or L * max(m13)}
    for k, f in rules.items():
        cells = [(L, w, f(L)) for L, w in scen]
        ev = sum(w * (L * m52 / c if c else 1.04) for L, w, c in cells)
        print(f'   {k:34s} EV x{ev:.2f} | ' + ' '.join(f'{L}:{"$%.1fK" % c if c else "cash"}' for L, w, c in cells))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--cache', required=True); a = ap.parse_args()
    cm, bn, cb, cbu, cmu, etf = fetch(a.cache)
    m = onchain(cm)
    report_core(m); report_leg2(bn, cb, cbu, cmu, etf); report_extras(m, bn, cb, cbu, cmu); report_cap(m)
