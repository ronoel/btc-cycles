#!/usr/bin/env python3
"""Generate (or verify) the D1/D2/D3 weekly drawdown series in index.html.

Cycles 1-3 are finished history, so these arrays are committed rather than fetched
at page load. Until Sep 3, 2026 they were hand-drawn approximations: rounded to
whole percent, sampled every 2-6 weeks, and read by a step lookup (`da()`), which
put the same-week comparison table up to 2.7 p.p. off the real number, inverted the
C1/C2 ordering at week 47, and were off by as much as 58.6 p.p. through the run-up. This script replaces them with measured closes.

    python3 scripts/build_cycles.py            # rewrite the arrays in index.html
    python3 scripts/build_cycles.py --verify   # check them, exit 1 on drift
    python3 scripts/build_cycles.py --print    # dump the lines, touch nothing

Convention, matched to how cycle 4 is built at runtime (`processKlines`) and to how
the click-to-compare panel reads history (`calcAtWeek`):

  x  weeks from the cycle ATH date, floor()ed, from -82 (the ch1 axis minimum)
     to +140 (its maximum)
  y  close / ATH_const - 1, in percent, one decimal, where the close is the last
     one at or before ATH_date + 7x days and ATH_const is the published intraday
     high already in `CYCLE_ATHS`
  x=0 is pinned to y=0. No cycle closes at its own intraday high, so an unpinned
     week 0 would read -4% to -6% for cycles 1-3 against a hard 0 for cycle 4 --
     the four lines would miss each other at the very point the chart aligns them
     on. The pin costs one week of fidelity and is the same seed `processKlines`
     already writes for cycle 4.

Sources: Binance BTCUSDT wherever it exists, because that is what `calcAtWeek` and
the retro-calibration already read, and Bitstamp BTC/USD only to backfill what
predates it. Binance's BTCUSDT starts Aug 17, 2017 -- *after* cycle 2's window
opens (week -82 = May 22, 2016), which is why the old array had to be hand-drawn
back to week -75 in the first place. So C1 is entirely Bitstamp, C3 entirely
Binance, and C2 carries one seam at week -17.

The seam is deliberately put in the run-up rather than in the bear market. The two
feeds are not interchangeable to the decimal: through the Oct-Nov 2018 Tether
scare USDT traded at a discount, so BTCUSDT ran ~1.5% above BTC/USD and cycle 2's
week 47 reads -67.9% on Bitstamp against -67.4% on Binance. Half a point is small,
but it is basis, not noise, and it belongs on the side of the chart where nothing
is quantified.
"""
import calendar, json, os, re, sys, time, datetime, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
UA = {"User-Agent": "btc-cycles/1.0 (+https://github.com/ronoel/btc-cycles)"}

W_MIN, W_MAX = -82, 140
DAY = 86400

# name, ATH date, published intraday ATH (must equal CYCLE_ATHS in index.html)
CYCLES = [
    ("D1", datetime.date(2013, 11, 30), 1150.0),
    ("D2", datetime.date(2017, 12, 17), 19783.0),
    ("D3", datetime.date(2021, 11, 10), 69000.0),
]


def utcday(ts):
    """Candle open timestamps are 00:00 UTC; date.fromtimestamp() would read them
    in local time and shift every day back by one in any negative offset."""
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def bitstamp(start, end):
    """Daily closes from Bitstamp BTC/USD, inclusive, as {date: close}."""
    out, s = {}, start
    while s < end:
        url = ("https://www.bitstamp.net/api/v2/ohlc/btcusd/"
               f"?step={DAY}&limit=1000&start={s}")
        rows = get(url)["data"]["ohlc"]
        if not rows:
            break
        for k in rows:
            ts = int(k["timestamp"])
            if start <= ts <= end:
                out[utcday(ts)] = float(k["close"])
        last = int(rows[-1]["timestamp"])
        if last > end:
            break
        if last < s:            # defensive: never loop on a non-advancing cursor
            break
        s = last + DAY
    return out


def binance(start, end):
    """Daily closes from Binance BTCUSDT, inclusive, as {date: close}."""
    out, s = {}, start * 1000
    while s < end * 1000:
        url = ("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d"
               f"&startTime={s}&limit=1000")
        rows = get(url)
        if not rows:
            break
        for k in rows:
            ts = k[0] // 1000
            if start <= ts <= end:      # a startTime before the pair listed returns
                out[utcday(ts)] = float(k[4])   # 2017 candles, which are not ours
        last = rows[-1][0]
        if last > end * 1000:
            break
        if last < s:
            break
        s = last + DAY * 1000
    return out


def series(ath_date, ath):
    """[(week, drawdown_pct)] over W_MIN..W_MAX, skipping weeks with no data yet."""
    first = ath_date + datetime.timedelta(days=W_MIN * 7)
    last = ath_date + datetime.timedelta(days=W_MAX * 7)
    # a month of lead-in so week W_MIN can still resolve a close at or before it
    lo = calendar.timegm((first - datetime.timedelta(days=30)).timetuple())
    hi = calendar.timegm((last + datetime.timedelta(days=1)).timetuple())
    closes = bitstamp(lo, hi)
    closes.update(binance(lo, hi))      # Binance wins wherever it reaches back
    if not closes:
        raise SystemExit("no data returned from either source")
    days = sorted(closes)
    pts = []
    for w in range(W_MIN, W_MAX + 1):
        if w == 0:
            pts.append((0, 0.0))        # pinned; see the module docstring
            continue
        target = ath_date + datetime.timedelta(days=w * 7)
        if target > days[-1] or target < days[0]:
            continue
        # last close at or before the target day, matching calcAtWeek()
        d = max(x for x in days if x <= target)
        if (target - d).days > 7:       # a gap that wide is not a close, it's a guess
            continue
        pts.append((w, round((closes[d] / ath - 1) * 100, 1)))
    return pts


def js(name, pts):
    body = ",".join("{x:%d,y:%s}" % (w, ("%g" % y)) for w, y in pts)
    return "const %s=[%s];" % (name, body)


def parse(line):
    return [(int(m.group(1)), float(m.group(2)))
            for m in re.finditer(r"\{x:(-?\d+),y:(-?[\d.]+)\}", line)]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--write"
    html = open(HTML, encoding="utf-8").read()
    lines, worst, missing = {}, 0.0, []

    for name, ath_date, ath in CYCLES:
        pts = series(ath_date, ath)
        lines[name] = js(name, pts)
        print(f"{name}: {len(pts)} weeks, {pts[0][0]}..{pts[-1][0]}, "
              f"deepest {min(y for _, y in pts)}%", file=sys.stderr)

        if mode == "--verify":
            cur = re.search(r"^const %s=\[.*?\];$" % name, html, re.M)
            if not cur:
                missing.append(name)
                continue
            have = dict(parse(cur.group(0)))
            for w, y in pts:
                if w in have:
                    worst = max(worst, abs(have[w] - y))
                else:
                    missing.append(f"{name} week {w}")

    if mode == "--verify":
        if missing:
            print(f"MISSING {len(missing)} point(s): {missing[:8]}"
                  f"{' ...' if len(missing) > 8 else ''}", file=sys.stderr)
        print(f"max deviation vs committed: {worst:.1f} p.p.", file=sys.stderr)
        if missing or worst > 0.15:
            print("FAIL — run `python3 scripts/build_cycles.py` to regenerate.",
                  file=sys.stderr)
            return 1
        print("OK", file=sys.stderr)
        return 0

    if mode == "--print":
        for name in lines:
            print(lines[name])
        return 0

    out, n = html, 0
    for name, line in lines.items():
        out, k = re.subn(r"^const %s=\[.*?\];$" % name, lambda _: line, out,
                         count=1, flags=re.M)
        if not k:
            raise SystemExit(f"could not find `const {name}=[...]` in index.html")
        n += k
    open(HTML, "w", encoding="utf-8").write(out)
    print(f"rewrote {n} series in index.html", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
