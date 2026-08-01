#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["google-auth>=2.0", "requests>=2.31"]
# ///
"""Google Search Console for eurodetailing.com.

Auth is a service account, so no Google password is ever involved. Create one in
Google Cloud, enable the Search Console API, download the JSON key, then add the
service account's email as a Full user in Search Console under
Settings -> Users and permissions. The key alone does nothing until you do that
last step.

Point GSC_KEY at the downloaded JSON:

    export GSC_KEY=~/.config/gsc-key.json

Then:

    ./_build/seo_report.py sites            # what the service account can see
    ./_build/seo_report.py submit-sitemap   # push sitemap.xml
    ./_build/seo_report.py report           # queries, pages, clicks, position
    ./_build/seo_report.py inspect          # is each page actually indexed?
    ./_build/seo_report.py all

Keep the key OUT of this repo — everything at the repo root is deployed and
publicly readable. ~/.config is a good home for it.
"""

import json
import os
import sys
from datetime import date, timedelta
from urllib.parse import quote

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# eurodetailing.com is registered as a DOMAIN property, so the site key is
# "sc-domain:eurodetailing.com" — not the "https://www.…/" URL-prefix form.
# Using the wrong one returns 403 even when the service account has access.
# Run `seo_report.py sites` to see the exact string Google expects.
SITE = os.environ.get("GSC_SITE", "sc-domain:eurodetailing.com")
SITEMAP = "https://www.eurodetailing.com/sitemap.xml"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
WM = "https://www.googleapis.com/webmasters/v3"
INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

PAGES = ["/", "/services/interior", "/services/exterior", "/services/bundle",
         "/membership", "/addons", "/gallery", "/reviews"]


def creds():
    key = os.environ.get("GSC_KEY")
    if not key:
        sys.exit("GSC_KEY is not set. Point it at the service account JSON:\n"
                 "    export GSC_KEY=~/.config/gsc-key.json")
    key = os.path.expanduser(key)
    if not os.path.exists(key):
        sys.exit("No such key file: %s" % key)
    c = service_account.Credentials.from_service_account_file(key, scopes=SCOPES)
    c.refresh(Request())
    return c


def call(method, url, token, **kw):
    r = requests.request(method, url, headers={"Authorization": "Bearer " + token}, **kw)
    if r.status_code == 403:
        sys.exit("403 from Google. The service account is authenticated but not "
                 "authorised for %s.\nAdd its email as a Full user in Search "
                 "Console -> Settings -> Users and permissions." % SITE)
    if not r.ok:
        sys.exit("%s %s\n%s" % (r.status_code, url, r.text[:400]))
    return r.json() if r.content else {}


def cmd_sites(token):
    d = call("GET", WM + "/sites", token)
    entries = d.get("siteEntry", [])
    if not entries:
        print("No properties visible. The service account has not been added as a "
              "user in Search Console yet.")
        return
    print("Properties this service account can see:")
    for s in entries:
        mark = "  <- GSC_SITE" if s["siteUrl"] == SITE else ""
        print("  %-45s %s%s" % (s["siteUrl"], s.get("permissionLevel", ""), mark))


def cmd_submit(token):
    url = "%s/sites/%s/sitemaps/%s" % (WM, quote(SITE, safe=""), quote(SITEMAP, safe=""))
    call("PUT", url, token)
    print("Submitted %s" % SITEMAP)
    d = call("GET", "%s/sites/%s/sitemaps" % (WM, quote(SITE, safe="")), token)
    for s in d.get("sitemap", []):
        print("  %s" % s.get("path"))
        print("    submitted: %s  last downloaded: %s" % (
            (s.get("lastSubmitted") or "-")[:10], (s.get("lastDownloaded") or "never")[:10]))
        print("    warnings: %s  errors: %s" % (s.get("warnings", 0), s.get("errors", 0)))
        for c in s.get("contents", []):
            print("    %s: %s submitted, %s indexed" % (
                c.get("type"), c.get("submitted"), c.get("indexed", "?")))


def query(token, dims, days=28, limit=25):
    end = date.today() - timedelta(days=2)      # GSC data lags ~2 days
    body = {"startDate": str(end - timedelta(days=days)), "endDate": str(end),
            "dimensions": dims, "rowLimit": limit}
    return call("POST", "%s/sites/%s/searchAnalytics/query" % (WM, quote(SITE, safe="")),
                token, json=body).get("rows", [])


def cmd_report(token):
    end = date.today() - timedelta(days=2)
    print("Search Console — 28 days to %s\n" % end)

    total = query(token, [], limit=1)
    if not total:
        print("No data yet. Search Console needs a few days after a site is")
        print("submitted before it reports anything.")
        return
    t = total[0]
    print("  clicks %-6d impressions %-8d CTR %.1f%%  avg position %.1f\n"
          % (t["clicks"], t["impressions"], t["ctr"] * 100, t["position"]))

    print("Top queries")
    print("  %-42s %6s %7s %6s" % ("query", "clicks", "impr", "pos"))
    for r in query(token, ["query"], limit=15):
        print("  %-42s %6d %7d %6.1f"
              % (r["keys"][0][:42], r["clicks"], r["impressions"], r["position"]))

    print("\nTop pages")
    print("  %-42s %6s %7s %6s" % ("page", "clicks", "impr", "pos"))
    for r in query(token, ["page"], limit=15):
        path = r["keys"][0].replace("https://www.eurodetailing.com", "") or "/"
        print("  %-42s %6d %7d %6.1f"
              % (path[:42], r["clicks"], r["impressions"], r["position"]))


def cmd_inspect(token):
    print("Index status\n")
    print("  %-24s %-26s %s" % ("page", "coverage", "last crawl"))
    for p in PAGES:
        d = call("POST", INSPECT, token,
                 json={"inspectionUrl": "https://www.eurodetailing.com" + p,
                       "siteUrl": SITE})
        r = d.get("inspectionResult", {}).get("indexStatusResult", {})
        print("  %-24s %-26s %s" % (p, (r.get("coverageState") or "?")[:26],
                                    (r.get("lastCrawlTime") or "never")[:10]))
        if r.get("robotsTxtState") not in (None, "ALLOWED"):
            print("      robots.txt: %s" % r["robotsTxtState"])
        if r.get("indexingState") not in (None, "INDEXING_ALLOWED"):
            print("      indexing:   %s" % r["indexingState"])


CMDS = {"sites": cmd_sites, "submit-sitemap": cmd_submit,
        "report": cmd_report, "inspect": cmd_inspect}

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "report"
    token = creds().token
    if what == "all":
        for name in ("sites", "submit-sitemap", "report", "inspect"):
            print("\n" + "=" * 62 + "\n%s\n" % name + "=" * 62)
            CMDS[name](token)
    elif what in CMDS:
        CMDS[what](token)
    else:
        sys.exit("Unknown command %r. One of: %s, all" % (what, ", ".join(CMDS)))
