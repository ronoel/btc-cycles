#!/usr/bin/env python3
"""Regression tests for build_data.py. Run: python3 scripts/test_build_data.py"""
import datetime, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_data as bd  # noqa: E402

TODAY = datetime.datetime.now(datetime.timezone.utc).date()


def iso(days_ago):
    return (TODAY - datetime.timedelta(days=days_ago)).isoformat()


class ProviderRegression(unittest.TestCase):
    """Sep 11, 2026: bitcoin-data.com served sopr/nupl/mvrv/realized-price ending Sep 4
    after having served them to Sep 9. The build published the Sep 4 values as current
    and cut Sep 5-9 out of history.json."""

    def test_extend_series_keeps_both_ends(self):
        # Fresh starts earlier (a token-widened window) AND ends earlier (Sep 11).
        stored = {"d0": "2026-09-01", "v": [1, 2, 3, 4, 5, 6, 7, 8, 9]}  # to Sep 9
        fresh = {"d0": "2026-08-30", "v": [0, 0, 1, 2, 3, 40]}           # to Sep 4
        out = bd.extend_series(stored, fresh, "sopr")
        self.assertEqual(out["d0"], "2026-08-30")
        self.assertEqual(out["v"], [0, 0, 1, 2, 3, 40, 5, 6, 7, 8, 9])

    def test_extend_series_disjoint_keeps_fresh(self):
        stored = {"d0": "2026-09-01", "v": [1, 2, 3]}
        for fresh in ({"d0": "2026-09-10", "v": [7]}, {"d0": "2026-08-20", "v": [7]}):
            self.assertEqual(bd.extend_series(stored, fresh, "x"), fresh)

    def test_main_does_not_move_readings_backwards(self):
        # Stored series end yesterday; the provider now serves `sopr` ending 2 days ago
        # -- inside the 3-day freshness tolerance, so only the regression check sees it.
        names = [n for _, _, n in bd.ONCHAIN]
        prev = {"updated": "x", "onchain": {n: {"d": iso(1), "v": 1.0} for n in names},
                "macro": {}, "etf": None, "stale": []}
        hist = {n: {"d0": iso(10), "v": [1.0] * 10} for n in names}
        latest = {n: {"d": iso(1), "v": 1.0} for n in names}
        fresh_hist = {n: {"d0": iso(10), "v": [1.0] * 10} for n in names}
        latest["sopr"] = {"d": iso(2), "v": 0.5}
        fresh_hist["sopr"] = {"d0": iso(10), "v": [1.0] * 8 + [0.5]}

        with tempfile.TemporaryDirectory() as root:
            for f, obj in (("data.json", prev),
                           ("history.json", {"updated": "x", "series": hist})):
                with open(os.path.join(root, f), "w") as fh:
                    json.dump(obj, fh)
            saved = (bd.ROOT, bd.fetch_onchain, bd.fetch_fred, bd.build_macro, bd.fetch_etf)
            bd.ROOT = root
            bd.fetch_onchain = lambda: (latest, fresh_hist)
            bd.fetch_fred = lambda: {}
            bd.build_macro = lambda _: {}
            bd.fetch_etf = lambda: None
            try:
                bd.main()
            finally:
                (bd.ROOT, bd.fetch_onchain, bd.fetch_fred,
                 bd.build_macro, bd.fetch_etf) = saved
            data = json.load(open(os.path.join(root, "data.json")))
            series = json.load(open(os.path.join(root, "history.json")))["series"]

        self.assertEqual(data["onchain"]["sopr"], {"d": iso(1), "v": 1.0})
        self.assertIn("onchain", data["stale"])
        self.assertEqual(len(series["sopr"]["v"]), 10)
        self.assertEqual(series["sopr"]["v"][-2], 0.5)  # fresh still wins on overlap


# Head of the page FRED served, with HTTP 200, during its Oct 21, 2026 maintenance.
FRED_MAINTENANCE = b"""<!doctype html>
<html lang="en">
<head>
    <title>Site Maintenance | St. Louis Fed<</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,700" rel="stylesheet">
</head>
"""


class FredMaintenancePage(unittest.TestCase):
    """Oct 21, 2026: the maintenance page parsed as one observation of 400.0 per series,
    so every macro row published 400.0 dated with an HTML fragment, and `stale` was
    clean because no series was missing."""

    def test_parse_rejects_html_and_accepts_csv(self):
        self.assertEqual(bd.parse_fred_csv(FRED_MAINTENANCE, "DGS10"), [])
        csv_body = b"observation_date,DGS10\n2026-10-16,5.10\n2026-10-17,.\n2026-10-19,5.15\n"
        self.assertEqual(bd.parse_fred_csv(csv_body, "DGS10"),
                         [("2026-10-16", 5.10), ("2026-10-19", 5.15)])

    def test_main_keeps_stored_macro_and_flags_stale(self):
        stored = {"d": "2026-10-19", "v": 5.15, "ma": 4.51, "hi2y": 5.31, "lo2y": 3.97}
        prev = {"updated": "x", "onchain": {}, "etf": None, "stale": [],
                "macro": {"nom10y": stored}}
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "data.json"), "w") as fh:
                json.dump(prev, fh)
            saved = (bd.ROOT, bd.fetch_onchain, bd.fetch_etf, bd.get)
            bd.ROOT = root
            bd.fetch_onchain = lambda: ({}, {})
            bd.fetch_etf = lambda: None
            bd.get = lambda url, *a, **k: FRED_MAINTENANCE
            try:
                bd.main()
            finally:
                bd.ROOT, bd.fetch_onchain, bd.fetch_etf, bd.get = saved
            data = json.load(open(os.path.join(root, "data.json")))
        self.assertEqual(data["macro"]["nom10y"], stored)
        self.assertNotIn("m2", data["macro"])
        self.assertIn("macro", data["stale"])


class FarsideEtfFeed(unittest.TestCase):
    """Oct 9 - Nov 4, 2026: the SoSoValue endpoint answered "interface does not exist",
    `etf` stayed frozen at the Oct 8 session (d20 +1.92, ACTIVE) for four weeks while the
    trailing 20 sessions were about -1.35. Farside's table replaced it; these pin its
    parsing rules: parentheses are negative, holiday rows and the day's half-filled row
    are not sessions, and a small fund's one-day gap does not drop a real session."""

    @staticmethod
    def page():
        def tr(cells, tag="td"):
            return "<tr>" + "".join(f"<{tag}><span>{c}</span></{tag}>" for c in cells) + "</tr>"
        head = ["Date", "IBIT", "FBTC", "MSBT", "GBTC", "Total"]
        day = datetime.date(2026, 7, 1)
        body = []
        for i in range(70):  # 70 sessions of +100 except a -1,250.5 one
            day += datetime.timedelta(days=1)
            v = "(1,250.5)" if i == 60 else "100.0"
            gap = "-" if i == 65 else "0.0"   # FBTC blank inside a complete row
            body.append(tr([day.strftime("%d %b %Y"), v, gap, "0.0", "0.0", v]))
        body.insert(30, tr(["01 Jul 2026"] + ["-"] * 4 + ["0.0"]))       # holiday
        day += datetime.timedelta(days=1)
        body.append(tr([day.strftime("%d %b %Y"), "-", "-", "0.0", "-", "0.0"]))  # partial
        body.append(tr(["Total", "x", "x", "x", "x", "5,649.5"]))
        small = "<table><tr><td>Fee</td></tr></table>"
        return small + "<table>" + tr(head, "th") + "".join(body) + "</table>"

    def test_parse_rules(self):
        rows = bd.parse_farside(self.page())
        self.assertEqual(len(rows), 70)
        self.assertNotIn("2026-07-01", [d for d, _ in rows])
        self.assertEqual(rows[60][1], -1250.5)
        self.assertEqual(rows[-1][0], "2026-09-09")

    def test_fetch_etf_reads_farside(self):
        saved = bd.get
        bd.get = lambda url, *a, **k: self.page().encode()
        try:
            out = bd.fetch_etf()
        finally:
            bd.get = saved
        self.assertIsNotNone(out)
        self.assertEqual(out["d"], "2026-09-09")
        self.assertEqual(out["d5"], 0.5)
        self.assertEqual(out["d20"], round((19 * 100 - 1250.5) / 1e3, 2))
        self.assertEqual(out["cum"], round((69 * 100 - 1250.5) / 1e3, 1))
        self.assertEqual(set(out), {"d", "d5", "d20", "d60", "ytd", "cum"})

    def test_changed_layout_is_rejected(self):
        self.assertEqual(bd.parse_farside("<table><tr><th>Date</th><th>Total</th></tr></table>"), [])
        self.assertEqual(bd.parse_farside("<html>blocked</html>"), [])


if __name__ == "__main__":
    unittest.main()
