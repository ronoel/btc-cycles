#!/usr/bin/env python3
"""Build data.json (latest readings) and history.json (series for the retro-calibration).

Runs in the daily GitHub Action and locally (`python3 scripts/build_data.py`).
Every source below is keyless; BGEOMETRICS_TOKEN, when present, only lifts the
bitcoin-data.com rate limit (10 req/h anonymous) and may extend the history window.

Sources
  on-chain  bitcoin-data.com/v1/*          (BGeometrics)
  macro     fred.stlouisfed.org/graph/fredgraph.csv?id=*   (keyless CSV; no CORS,
            which is why it has to come through this Action rather than the page)
  ETF flow  api.sosovalue.xyz/openapi/v2/etf/historicalInflowChart  (undocumented;
            see MAINTENANCE.md — treated as best-effort, never fatal)

Nothing here is allowed to fail the build. A source that errors keeps its previous
value in data.json and is marked stale, because a report that silently drops a row
is worse than one that says "as of three days ago".
"""
import json, os, sys, time, csv, io, urllib.request, urllib.error, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ.get("BGEOMETRICS_TOKEN", "").strip()
UA = {"User-Agent": "btc-cycles/1.0 (+https://github.com/ronoel/btc-cycles)"}


def get(url, data=None, headers=None, tries=3):
    h = dict(UA)
    if headers:
        h.update(headers)
    body = json.dumps(data).encode() if data is not None else None
    if body:
        h["Content-Type"] = "application/json"
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers=h)
            return urllib.request.urlopen(req, timeout=45).read()
        except Exception as e:  # noqa: BLE001 - any failure is non-fatal by design
            last = e
            time.sleep(2 + 3 * i)
    print(f"  ! {url} failed: {last}", file=sys.stderr)
    return None


# ---------------------------------------------------------------- on-chain
# Endpoint -> (key in the JSON rows, name we publish under).
# NOTE: `mvrv` and `mvrv-zscore` are DIFFERENT series. The ratio is market cap /
# realized cap (~1.24 today); the Z-score is that gap in standard deviations
# (~0.39 today). Until Aug 2026 this file fetched the ratio and published it as
# `mvrv_zscore`, so the report scored a Z-score threshold against a ratio. Both
# are published now, under honest names.
#
# Request budget: bitcoin-data.com allows 10 requests/hour anonymously and this list
# is now EIGHT of them, so retries are the thing that trips the limit, not the list.
# `fetch_onchain` therefore passes tries=2. If more series are ever added here, set
# BGEOMETRICS_TOKEN (the limit is the only thing it buys) rather than hoping.
#
# Added Aug 19, 2026: `sth-mvrv` plus `realized-price-sth`. The ratio carries 1,461
# days of daily history — the whole
# free window, which reaches back past the Nov 2022 bottom — so the short-term-holder
# row stopped being a hand-quoted research figure and joined the retro-calibration. The
# cost basis is fetched alongside it so the live row can be built as spot / cost basis,
# the same construction as the Realized Price row, instead of lagging on yesterday's
# published ratio. Note `sth-realized-price` and `/{last}` suffixes return empty bodies
# for several series on this API — `realized-price-sth` with no suffix is the one that
# works.
# Still deliberately NOT fetched, and why:
#   exchange-reserve-btc  HTTP 403, subscription only as of Aug 19, 2026.
#   hashribbons           free and returns {sma_30, sma_60, hashribbons:"Down"|...},
#                         but the classic signal is stateful ("cross AFTER capitulation")
#                         and a naive sma30>sma60 rule reads ACTIVE through any bull
#                         market. Validate the state field against Jan 2026 (the known
#                         misfire) and Nov 2022 before scoring on it.
ONCHAIN = [
    ("realized-price", "realizedPrice", "realized_price"),
    ("mvrv-zscore",    "mvrvZscore",    "mvrv_zscore"),
    ("mvrv",           "mvrv",          "mvrv"),
    ("nupl",           "nupl",          "nupl"),
    ("sopr",           "sopr",          "sopr"),
    ("puell-multiple", "puellMultiple", "puell"),
    ("sth-mvrv",       "sthMvrv",       "sth_mvrv"),
    ("realized-price-sth", "realizedPriceSth", "sth_realized_price"),
]


def fetch_onchain():
    latest, hist = {}, {}
    for path, field, name in ONCHAIN:
        url = f"https://bitcoin-data.com/v1/{path}"
        if TOKEN:
            url += f"?token={TOKEN}"
        raw = get(url, tries=2)
        if not raw:
            continue
        try:
            rows = json.loads(raw)
        except Exception:
            print(f"  ! {path}: unparseable response", file=sys.stderr)
            continue
        if not isinstance(rows, list) or not rows:
            print(f"  ! {path}: unexpected shape", file=sys.stderr)
            continue
        rows = [r for r in rows if r.get(field) is not None]
        rows.sort(key=lambda r: r["d"])
        latest[name] = {"d": rows[-1]["d"], "v": round(float(rows[-1][field]), 4)}
        hist[name] = {"d0": rows[0]["d"],
                      "v": [round(float(r[field]), 4) for r in rows]}
        print(f"  {name:15} {latest[name]['v']:>12}  ({latest[name]['d']}, {len(rows)}d)")
        time.sleep(1)  # be polite to the anonymous rate limit
    return latest, hist


# ------------------------------------------------------------------- macro
FRED = ["M2SL", "WALCL", "WTREGEN", "RRPONTSYD", "DFII10", "DGS10", "DGS2",
        "BAMLH0A0HYM2", "DTWEXBGS"]


def fetch_fred():
    out = {}
    for sid in FRED:
        raw = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}")
        if not raw:
            continue
        rows = list(csv.reader(io.StringIO(raw.decode())))[1:]
        pts = [(r[0], float(r[1])) for r in rows if len(r) > 1 and r[1] not in (".", "")]
        if pts:
            out[sid] = pts
            print(f"  {sid:14} {pts[-1][1]:>12}  ({pts[-1][0]}, {len(pts)} obs)")
    return out


def ma(pts, n):
    v = [p[1] for p in pts[-n:]]
    return sum(v) / len(v) if v else None


def build_macro(f):
    """Reduce the FRED series to the handful of readings the page actually scores.

    Deliberately small: DXY, real rates, the Fed balance sheet and M2 are one
    collinear liquidity factor, so they feed ONE composite row rather than four
    checklist rows. Credit spreads stay separate — they measure systemic stress,
    not liquidity, and the report uses them for drawdown DEPTH, not timing.
    """
    m = {}
    if "M2SL" in f:
        p = f["M2SL"]
        m["m2"] = {"d": p[-1][0], "level": p[-1][1],
                   "yoy": round((p[-1][1] / p[-13][1] - 1) * 100, 2) if len(p) > 13 else None,
                   "yoy_3m": round((p[-4][1] / p[-16][1] - 1) * 100, 2) if len(p) > 16 else None,
                   "yoy_6m": round((p[-7][1] / p[-19][1] - 1) * 100, 2) if len(p) > 19 else None}
    if all(k in f for k in ("WALCL", "WTREGEN", "RRPONTSYD")):
        tga, rrp = dict(f["WTREGEN"]), dict(f["RRPONTSYD"])
        # RRP is daily, TGA/WALCL weekly (Wednesday) — align on the WALCL dates.
        nl = []
        for d, v in f["WALCL"]:
            if d in tga and d in rrp:
                nl.append((d, round(v / 1000 - tga[d] / 1000 - rrp[d], 1)))
        if nl:
            m["netliq"] = {"d": nl[-1][0], "v": nl[-1][1],
                           "w4": nl[-5][1] if len(nl) > 5 else None,
                           "w13": nl[-14][1] if len(nl) > 14 else None,
                           "w52": nl[-53][1] if len(nl) > 53 else None,
                           "assets": round(f["WALCL"][-1][1] / 1000, 1),
                           "tga": round(f["WTREGEN"][-1][1] / 1000, 1),
                           "rrp": round(f["RRPONTSYD"][-1][1], 1)}
    for sid, name, win in (("DFII10", "real10y", 200), ("DGS10", "nom10y", 200),
                           ("DGS2", "nom2y", 200), ("BAMLH0A0HYM2", "hy_oas", 200),
                           ("DTWEXBGS", "dxy", 200)):
        if sid not in f:
            continue
        p = f[sid]
        v = [x[1] for x in p]
        m[name] = {"d": p[-1][0], "v": p[-1][1],
                   "ma": round(ma(p, win), 2),
                   "hi2y": max(v[-500:]), "lo2y": min(v[-500:])}
    m["dxy_src"] = "FRED DTWEXBGS (broad trade-weighted USD) — the ICE DXY is licensed"
    return m


# --------------------------------------------------------------- ETF flows
def fetch_etf():
    raw = get("https://api.sosovalue.xyz/openapi/v2/etf/historicalInflowChart",
              data={"type": "us-btc-spot"})
    if not raw:
        return None
    try:
        rows = json.loads(raw)["data"]
    except Exception:
        print("  ! ETF: unexpected response shape", file=sys.stderr)
        return None
    if not isinstance(rows, list) or not rows:
        return None
    rows.sort(key=lambda r: r["date"])
    B = 1e9
    s = lambda n: round(sum(r["totalNetInflow"] for r in rows[-n:]) / B, 2)
    yr = datetime.date.today().year
    ytd = round(sum(r["totalNetInflow"] for r in rows
                    if r["date"] >= f"{yr}-01-01") / B, 2)
    out = {"d": rows[-1]["date"], "d5": s(5), "d20": s(20), "d60": s(60),
           "ytd": ytd, "ytd_partial": rows[0]["date"] > f"{yr}-01-01",
           "cum": round(rows[-1]["cumNetInflow"] / B, 1),
           "aum": round(rows[-1]["totalNetAssets"] / B, 1)}
    print(f"  etf 20d {out['d20']:+.2f}B  60d {out['d60']:+.2f}B  ytd {out['ytd']:+.2f}B  ({out['d']})")
    return out


# ------------------------------------------------------------------- write
# Every series each section is expected to deliver. A PARTIAL failure (e.g. the
# on-chain rate limit tripping mid-fetch) must not shrink the published dict —
# fresh values are merged OVER the previous ones, and the section is marked stale
# whenever anything expected is missing from the fresh batch. Replacing instead
# of merging once lost four of six on-chain series without any flag.
EXPECT = {"onchain": [name for _, _, name in ONCHAIN],
          "macro": ["m2", "netliq", "real10y", "nom10y", "nom2y", "hy_oas", "dxy"],
          "etf": ["d20"]}


def extend_series(stored, fresh, name):
    """Union a stored series with a freshly fetched one, keeping the older head.

    Why this exists: the free bitcoin-data.com window is a rolling 1,461 days, so every
    daily run returns a series whose FIRST date is one day later than yesterday's. The
    old behaviour replaced each series wholesale, which meant history.json silently lost
    its left edge every single day. That matters on a dated schedule: the Nov 21, 2022
    bottom -- the calibration's only anchor, and the source of the "95% at the confirmed
    bottom" figure in the thesis and the README -- drops out of the free window on
    **Nov 20, 2026**, in the middle of this report's own projected bottom window. When it
    did, `coreOnDate('2022-11-21')` would have started returning null, `calibNums()` with
    it, and the thesis paragraph would have rendered em-dashes where its centrepiece
    figures go. The 2022 slice is immutable history, so the fix is simply never to throw
    it away.

    Emits a contiguous daily array, because `coreAt()` in index.html indexes by
    (date - d0) in days and a gap would misalign every reading after it. Disjoint ranges
    therefore keep the fresh series alone rather than producing a plausible-looking but
    wrong array.
    """
    if not stored or not stored.get("v") or not stored.get("d0"):
        return fresh
    def spread(entry):
        d0 = datetime.date.fromisoformat(entry["d0"])
        return {d0 + datetime.timedelta(days=i): v for i, v in enumerate(entry["v"])}
    old, new = spread(stored), spread(fresh)
    lo, hi = min(old), max(new)
    if min(new) > max(old) + datetime.timedelta(days=1):
        print(f"  ! {name}: stored and fresh ranges are disjoint "
              f"({max(old)} -> {min(new)}); keeping fresh only", file=sys.stderr)
        return fresh
    old.update(new)  # fresh wins wherever the two overlap (restatements happen)
    out, cur, missing = [], lo, 0
    while cur <= hi:
        if cur in old:
            out.append(old[cur])
        else:  # carry forward rather than shift every later index by one
            out.append(out[-1] if out else None)
            missing += 1
        cur += datetime.timedelta(days=1)
    if missing:
        print(f"  ! {name}: {missing} day(s) carried forward to keep the series "
              f"contiguous", file=sys.stderr)
    if len(out) > len(fresh["v"]):
        print(f"  {name:15} history extended {len(fresh['v'])}d -> {len(out)}d "
              f"(from {lo})")
    return {"d0": lo.isoformat(), "v": out}


def main():
    prev = {}
    try:
        with open(os.path.join(ROOT, "data.json")) as fh:
            prev = json.load(fh)
    except Exception:
        pass

    print("on-chain:")
    onchain, hist = fetch_onchain()
    print("macro (FRED):")
    macro = build_macro(fetch_fred())
    print("etf:")
    etf = fetch_etf()

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {"updated": now,
            "onchain": {**prev.get("onchain", {}), **onchain},
            "macro": {**prev.get("macro", {}), **macro},
            "etf": etf or prev.get("etf")}
    # A section whose fresh batch is incomplete keeps the old values for the gaps
    # and is flagged, so the page says "stale" rather than presenting them as new.
    fresh = {"onchain": onchain, "macro": macro, "etf": etf or {}}
    data["stale"] = [k for k in EXPECT if any(n not in fresh[k] for n in EXPECT[k])]

    with open(os.path.join(ROOT, "data.json"), "w") as fh:
        json.dump(data, fh, indent=2)

    # history.json gets the same treatment: merge fresh series over the stored
    # ones so a partial on-chain fetch never truncates the calibration's inputs.
    if hist:
        stored = {}
        try:
            with open(os.path.join(ROOT, "history.json")) as fh:
                stored = json.load(fh).get("series", {})
        except Exception:
            pass
        merged = dict(stored)
        for name, fresh in hist.items():
            merged[name] = extend_series(stored.get(name), fresh, name)
        with open(os.path.join(ROOT, "history.json"), "w") as fh:
            json.dump({"updated": now, "series": merged},
                      fh, separators=(",", ":"))
    print(f"\nwrote data.json ({len(json.dumps(data))}B)"
          + (" + history.json" if hist else "")
          + (f"  STALE: {data['stale']}" if data["stale"] else ""))


if __name__ == "__main__":
    main()
