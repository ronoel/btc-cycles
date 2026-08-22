#!/usr/bin/env python3
"""Refresh the Cycle-4 line and the `now` marker in og-card.html from live data.

Why this exists: the card's C4 polyline was a hand-pasted snapshot. By Aug 21, 2026 it
ended at week ~40 / -51% while the live reading was week ~46 / -39% -- a ten-point drift
on the image that gets embedded in every social preview of the report. MAINTENANCE.md
called that drift "by design", which was true only because regenerating it was manual.
It isn't any more.

Usage:
    python3 scripts/build_og_card.py          # rewrites og-card.html in place
then re-screenshot per MAINTENANCE.md:
    python3 -m http.server 8931 &
    firefox --headless --profile ~/ffprof --no-remote \\
            --screenshot ~/og.png --window-size 1200,630 \\
            http://localhost:8931/og-card.html
(Chromium/Opera tile the card; Firefox is the one that renders it faithfully. Snap
browsers cannot write into the repo, hence the $HOME hop.)

Only the C4 line, the `now` marker and the snapshot date are touched. Cycles 1-3 are
finished history and are never regenerated -- they are as fixed as the tables in
index.html, and this script deliberately has no code that could rewrite them.
"""
import io, json, os, re, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD = os.path.join(ROOT, "og-card.html")

# Must match index.html's ATH/ATHD consts. MAINTENANCE.md §4 lists these as never-touch.
ATH, ATH_DATE = 126296.0, datetime.date(2025, 10, 6)

# The SVG's own scale, read off its axis ticks rather than assumed: week 0 sits at
# x=70 and week 65 at x=1090; 0% sits at y=14 and -80% at y=309.1.
X0, PX_WEEK = 70.0, (1090.0 - 70.0) / 65
Y0, PX_PCT = 14.0, (309.1 - 14.0) / 80
STEP_DAYS = 3  # sampling density of the original path, kept so the line reads the same


def daily_closes(start):
    """(date, close) from `start` to today, oldest first, from Binance klines."""
    out, cursor = {}, int(datetime.datetime.combine(
        start, datetime.time(), datetime.timezone.utc).timestamp() * 1000)
    while True:
        url = ("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d"
               "&limit=1000&startTime=%d" % cursor)
        req = urllib.request.Request(url, headers={"User-Agent": "btc-cycles/1.0"})
        rows = json.load(urllib.request.urlopen(req, timeout=45))
        if not rows:
            break
        for r in rows:
            d = datetime.datetime.fromtimestamp(r[0] / 1000, datetime.timezone.utc).date()
            out[d] = float(r[4])
        if len(rows) < 1000:
            break
        cursor = rows[-1][0] + 86_400_000
    return sorted(out.items())


def main():
    series = daily_closes(ATH_DATE)
    if not series:
        sys.exit("no candles returned")

    # Sample every STEP_DAYS, and always keep the newest point so the marker is current.
    picked = [series[i] for i in range(0, len(series), STEP_DAYS)]
    if picked[-1][0] != series[-1][0]:
        picked.append(series[-1])

    pts = []
    for d, px in picked:
        wk = (d - ATH_DATE).days / 7
        dd = (px / ATH - 1) * 100
        pts.append((X0 + wk * PX_WEEK, Y0 - dd * PX_PCT))
    # Anchor week 0 at exactly 0%, like the other three lines. The chart is "aligned at
    # the ATH", and ATH is an intraday high: the close that day was 1.3% below it, which
    # would start C4 a hair under the 0% gridline and under the other three cycles for no
    # reason the reader could interpret.
    pts[0] = (X0, Y0)
    path = " L".join("%.1f,%.1f" % p for p in pts)
    path = "M" + path[1:] if path.startswith("L") else "M" + path

    end_d, end_px = series[-1]
    ex, ey = pts[-1]
    end_dd = (end_px / ATH - 1) * 100

    s = io.open(CARD, encoding="utf-8").read()
    before = s

    # 1. The C4 line: the ONLY path drawn at stroke-width 3.5. Cycles 1-3 use 2.
    s, n = re.subn(r'(<path d=")M[^"]+("[^>]*stroke-width="3\.5")',
                   lambda m: m.group(1) + path + m.group(2), s, count=1)
    assert n == 1, "C4 path (stroke-width 3.5) not found"

    # 2. The `now` marker: the halo and the dot, both at the old endpoint.
    old_xy = re.search(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="10"', s)
    assert old_xy, "now halo not found"
    ox, oy = old_xy.group(1), old_xy.group(2)
    s = s.replace('<circle cx="%s" cy="%s" r="10"' % (ox, oy),
                  '<circle cx="%.1f" cy="%.1f" r="10"' % (ex, ey))
    s = s.replace('<circle cx="%s" cy="%s" r="5"' % (ox, oy),
                  '<circle cx="%.1f" cy="%.1f" r="5"' % (ex, ey))

    # 3. Its label, keeping the original's offset from the dot (+14, +34).
    s, n = re.subn(r'<text x="[\d.]+" y="[\d.]+" class="lbl now" fill="#D85A30">now[^<]*</text>',
                   '<text x="%.1f" y="%.1f" class="lbl now" fill="#D85A30">'
                   'now · −%d%%</text>' % (ex + 14, ey + 34, round(-end_dd)),
                   s, count=1)
    assert n == 1, "now label not found"

    # 4. The provenance comment at the top of the file.
    s, n = re.subn(r'C4 line is a static snapshot \([^)]*\)',
                   'C4 line regenerated by scripts/build_og_card.py (data through %s)'
                   % end_d.isoformat(), s, count=1)
    if not n:
        s, n = re.subn(r'C4 line regenerated by scripts/build_og_card\.py \(data through [^)]*\)',
                       'C4 line regenerated by scripts/build_og_card.py (data through %s)'
                       % end_d.isoformat(), s, count=1)
    assert n == 1, "provenance comment not found"

    if s == before:
        print("no change")
        return
    io.open(CARD, "w", encoding="utf-8").write(s)
    print("og-card.html: C4 %d pts, %s -> %s, ends week %.1f at %.1f%% ($%.0f)"
          % (len(pts), series[0][0], end_d, (end_d - ATH_DATE).days / 7, end_dd, end_px))
    print("now re-screenshot per MAINTENANCE.md (firefox headless, 1200x630)")


if __name__ == "__main__":
    main()
