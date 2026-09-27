#!/usr/bin/env python3
"""Regression tests for build_og_card.py. Run: python3 scripts/test_build_og_card.py"""
import io, os, re, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_og_card as og  # noqa: E402

CARD = os.environ.get("OG_CARD", og.CARD)


def now_label(svg):
    m = re.search(r'<text x="([\d.]+)" y="([\d.]+)"(?: text-anchor="(\w+)")? class="lbl now" '
                  r'fill="#D85A30">(now[^<]*)</text>', svg)
    return float(m.group(1)), float(m.group(2)), m.group(3) or "start", m.group(4)


def c4_points(svg):
    m = re.search(r'<path d="(M[^"]+)"[^>]*stroke-width="3\.5"', svg)
    return [tuple(map(float, p.split(","))) for p in re.findall(r"[\d.]+,[\d.]+", m.group(1))]


class NowLabel(unittest.TestCase):
    """Sep 27, 2026: the `now` label sat at a fixed (+14, +34) from the dot and, from
    week ~49, printed over the projected-window captions and their leader line."""

    def test_committed_card_label_is_clear(self):
        svg = io.open(CARD, encoding="utf-8").read()
        x, y, anchor, text = now_label(svg)
        box = og.text_box(x, y, anchor, text, 18)
        for o in og.card_obstacles(svg):
            self.assertFalse(og.overlaps(box, o), "now label %r overlaps %r" % (box, o))
        self.assertFalse(og.hits_line(box, c4_points(svg)), "now label sits on the C4 line")

    def test_placement_clears_captions_across_the_window(self):
        # Walk the dot through weeks 49-60 at every drawdown above the window box, with
        # the line arriving from the lower left (a bounce) or the upper left (a decline).
        svg = io.open(CARD, encoding="utf-8").read()
        obstacles = og.card_obstacles(svg)
        for w10 in range(490, 601, 5):
            for dd in range(-25, -55, -1):
                ex, ey = og.X0 + w10 / 10 * og.PX_WEEK, og.Y0 - dd * og.PX_PCT
                for rise in (+8, -8):
                    pts = [(ex - 3 * og.PX_WEEK, ey + rise * og.PX_PCT), (ex, ey)]
                    lx, ly, anchor = og.place_now_label(ex, ey, "now · −%d%%" % -dd, obstacles, pts)
                    box = og.text_box(lx, ly, anchor, "now · −%d%%" % -dd, 18)
                    for o in obstacles:
                        self.assertFalse(og.overlaps(box, o),
                                         "week %.1f dd %d: label %r on %r" % (w10 / 10, dd, box, o))


if __name__ == "__main__":
    unittest.main()
