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

Cycles 1-3 are redrawn too, from `D1`/`D2`/`D3` in index.html rather than from the
network -- the page is the single source of truth, so the card cannot disagree with
it. Until Sep 4, 2026 this script deliberately had no code to reach them, on the
grounds that they were finished history; that was right about the history and wrong
about the drawing. Those arrays were hand-drawn and wrong by 5.9-7.1 p.p. on average
across the post-ATH span this card shows (see ANALYSIS-LOG.md, Sep 3), so og.png was
still publishing the fabricated curve after index.html had been corrected.

The low markers and their labels are NOT regenerated: they are the true low day
(weeks 59/52/54 at -85/-84/-78) and sit slightly below their own weekly-sampled
lines on purpose. Same rule as PRIOR_LOWS in index.html.
"""
import io, json, os, re, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD = os.path.join(ROOT, "og-card.html")
PAGE = os.path.join(ROOT, "index.html")

# stroke colour -> the const in index.html that draws the same cycle on the page
HIST = [("#378ADD", "D1"), ("#1D9E75", "D2"), ("#7F77DD", "D3")]

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


def hist_paths():
    """{colour: svg path} for cycles 1-3, read off index.html's committed arrays."""
    page = io.open(PAGE, encoding="utf-8").read()
    out = {}
    for colour, name in HIST:
        m = re.search(r"^const %s=\[(.*?)\];$" % name, page, re.M)
        assert m, "%s not found in index.html" % name
        pts = {int(a): float(b)
               for a, b in re.findall(r"\{x:(-?\d+),y:(-?[\d.]+)\}", m.group(1))}
        # the card's x axis is weeks 0..65 after the ATH; the run-up is not shown
        xy = [(X0 + w * PX_WEEK, Y0 - pts[w] * PX_PCT)
              for w in range(0, 66) if w in pts]
        assert len(xy) == 66, "%s is missing weeks in 0..65" % name
        out[colour] = "M" + " L".join("%.1f,%.1f" % p for p in xy)
    return out


# ---------------------------------------------------------------- `now` label placement
# Until Sep 27, 2026 the label sat at a fixed (+14, +34) from the dot. From week ~49 that
# put it on the projected-window captions and their leader line, and any fixed offset
# fails again within a few weeks as the dot walks across the window. So the captions moved
# to the top of the plot (the leader line went: it blocked the whole x=933 column from
# -15% to -54%, leaving no clear spot at weeks 52-58), and the label tries candidate
# positions and takes the first that clears the captions and the C4 line.
# Widths are estimates (0.55 em per glyph for the proportional fonts, 0.6 for mono) --
# generous enough for a collision check, not for typesetting.
CANDIDATES = [("middle", 0, -16), ("end", -12, -10), ("start", 12, -10),
              ("middle", 0, 32), ("start", 14, 6), ("end", -14, 6)]


def text_box(x, y, anchor, text, size, em=0.55):
    w = len(text) * size * em
    x0 = {"middle": x - w / 2, "end": x - w, "start": x}[anchor]
    return (x0, y - size * 0.8, x0 + w, y + size * 0.25)


def overlaps(a, b, pad=2.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or
                a[3] + pad <= b[1] or b[3] + pad <= a[1])


def card_obstacles(svg):
    """Boxes the label must not touch: the window captions (and a leader line, if any)."""
    out = []
    for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)" text-anchor="middle" class="(win2?)">([^<]*)</text>', svg):
        x, y, cls, txt = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
        out.append(text_box(x, y, "middle", txt, 17 if cls == "win" else 14,
                            0.55 if cls == "win" else 0.6))
    m = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="\1" y2="([\d.]+)" stroke="#5f5e58"', svg)
    if m:
        x, y1, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3))
        out.append((x - 1, min(y1, y2), x + 1, max(y1, y2)))
    return out


def hits_line(box, pts, pad=3.0):
    """True if the polyline `pts` passes through `box` (segments sampled every ~2px)."""
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(1, int(max(abs(bx - ax), abs(by - ay)) / 2))
        for i in range(n + 1):
            px, py = ax + (bx - ax) * i / n, ay + (by - ay) * i / n
            if x0 <= px <= x1 and y0 <= py <= y1:
                return True
    return False


def place_now_label(ex, ey, text, obstacles, pts):
    """(x, y, anchor) of the first candidate clear of `obstacles` and the C4 line."""
    for anchor, dx, dy in CANDIDATES:
        box = text_box(ex + dx, ey + dy, anchor, text, 18)
        if not any(overlaps(box, o) for o in obstacles) and not hits_line(box, pts):
            return ex + dx, ey + dy, anchor
    anchor, dx, dy = CANDIDATES[0]
    print("  ! no clear spot for the now label; using the default", file=sys.stderr)
    return ex + dx, ey + dy, anchor


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

    # 0. Cycles 1-3, from index.html. Each is identified by its stroke colour.
    for colour, path_d in hist_paths().items():
        s, n = re.subn(r'(<path d=")M[^"]+("[^>]*stroke="%s")' % colour,
                       lambda m: m.group(1) + path_d + m.group(2), s, count=1)
        assert n == 1, "historical path %s not found" % colour

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

    # 3. Its label, at the first candidate position clear of captions, leader line and
    # the C4 line itself (see place_now_label).
    label = "now · −%d%%" % round(-end_dd)
    lx, ly, anchor = place_now_label(ex, ey, label, card_obstacles(s), pts)
    s, n = re.subn(r'<text x="[\d.]+" y="[\d.]+"( text-anchor="\w+")? class="lbl now" fill="#D85A30">now[^<]*</text>',
                   '<text x="%.1f" y="%.1f" text-anchor="%s" class="lbl now" fill="#D85A30">%s</text>'
                   % (lx, ly, anchor, label), s, count=1)
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
    print("og-card.html: cycles 1-3 redrawn from index.html (66 weekly pts each); "
          "C4 %d pts, %s -> %s, ends week %.1f at %.1f%% ($%.0f)"
          % (len(pts), series[0][0], end_d, (end_d - ATH_DATE).days / 7, end_dd, end_px))
    print("now re-screenshot per MAINTENANCE.md (firefox headless, 1200x630)")


if __name__ == "__main__":
    main()
