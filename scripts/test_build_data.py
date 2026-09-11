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


if __name__ == "__main__":
    unittest.main()
