#!/usr/bin/env python3
"""Probe a public REST endpoint: print HTTP status, latency, rate-limit headers and a trimmed sample of the body.

Usage:
  probe.py URL                       # GET
  probe.py URL --post '{"type":"meta"}'   # POST JSON body
  probe.py URL -H "X-API-KEY: xxx"   # extra headers (repeatable)
  probe.py URL --proxy http://127.0.0.1:7890
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request

RATE_HEADERS = ("x-mbx-used-weight", "x-mbx-used-weight-1m", "x-ratelimit-limit", "x-ratelimit-remaining",
                "x-ratelimit-reset", "ratelimit-limit", "ratelimit-remaining", "retry-after", "x-bapi-limit",
                "x-bapi-limit-status", "x-bapi-limit-reset-timestamp", "ok-limit", "cf-ray")


def trim(obj, depth=0, max_items=3):
    if isinstance(obj, dict):
        return {k: trim(v, depth + 1) for k, v in list(obj.items())[:12]}
    if isinstance(obj, list):
        return [trim(v, depth + 1) for v in obj[:max_items]] + (["… +%d more" % (len(obj) - max_items)] if len(obj) > max_items else [])
    if isinstance(obj, str) and len(obj) > 120:
        return obj[:120] + "…"
    return obj


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--post", help="JSON body; switches to POST")
    p.add_argument("-H", "--header", action="append", default=[], help='"Name: value"')
    p.add_argument("--proxy")
    p.add_argument("--timeout", type=float, default=15)
    p.add_argument("--raw", action="store_true", help="print full body instead of trimmed sample")
    a = p.parse_args()

    headers = {"User-Agent": "crypto-data-map-probe/1.0", "Accept": "application/json"}
    for h in a.header:
        k, _, v = h.partition(":")
        headers[k.strip()] = v.strip()
    data = None
    if a.post is not None:
        data = a.post.encode()
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(a.url, data=data, headers=headers, method="POST" if data else "GET")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": a.proxy, "https": a.proxy})) if a.proxy else urllib.request.build_opener()

    t0 = time.time()
    try:
        resp = opener.open(req, timeout=a.timeout)
        status, body, hdrs = resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        status, body, hdrs = e.code, e.read(), e.headers
    except Exception as e:  # network / timeout
        print(f"ERROR {type(e).__name__}: {e}")
        sys.exit(2)
    ms = int((time.time() - t0) * 1000)

    print(f"HTTP {status}  {ms} ms  {len(body)} bytes")
    for k in RATE_HEADERS:
        if k in hdrs:
            print(f"  {k}: {hdrs[k]}")
    text = body.decode("utf-8", "replace")
    if a.raw:
        print(text)
        return
    try:
        obj = json.loads(text)
    except ValueError:
        print(text[:800])
        return
    if isinstance(obj, list):
        print(f"top-level: list[{len(obj)}]")
    elif isinstance(obj, dict):
        print(f"top-level keys: {list(obj.keys())[:20]}")
    print(json.dumps(trim(obj), ensure_ascii=False, indent=1)[:3000])


if __name__ == "__main__":
    main()
