#!/usr/bin/env python3
"""
Fetch the numbers behind the arc-reactor core panel.

Primary source: GraphQL. One request returns

  * contributionCalendar — the same rolling 12-month window the streak card and
    the radar already report, but at day resolution. That is what lets the
    reactor's outer ring colour 53 weeks individually instead of showing one
    aggregate, and it is why this panel replaced the third-party 3D graph: the
    data was always available, only the rendering was outsourced.
  * languages across public owned repos — GitHub's own byte counts, aggregated
    by language, so the panel's language bar is measured rather than hand-listed.

Fallback: without a GITHUB_TOKEN (local preview) a previous reactor.json is kept
and only its language mix is refreshed from merged.json when that exists.
"""
import json, os, ssl, sys, urllib.request

USER = os.environ.get("GH_USER", "Shivala-08")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("REACTOR_OUT", "reactor.json")
MERGED = os.environ.get("MERGED_IN", "merged.json")
CTX = ssl._create_unverified_context()

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { contributionCount date }
        }
      }
    }
    repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def post_graphql():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        method="POST",
        data=json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": USER}}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "profile-reactor",
        },
    )
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    user = payload["data"]["user"]
    return user["contributionsCollection"]["contributionCalendar"], user["repositories"]


def aggregate_languages(repos):
    """Sum GitHub's per-repo byte counts by language name."""
    totals = {}
    for node in repos.get("nodes") or []:
        for edge in (node.get("languages") or {}).get("edges") or []:
            name = edge["node"]["name"]
            totals[name] = totals.get(name, 0) + int(edge.get("size") or 0)
    return dict(sorted(totals.items(), key=lambda kv: -kv[1]))


def shape(calendar, languages):
    weeks = []
    for week in calendar["weeks"]:
        days = week["contributionDays"]
        counts = [int(d["contributionCount"]) for d in days]
        weeks.append({
            "start": days[0]["date"] if days else None,
            "end": days[-1]["date"] if days else None,
            "days": counts,
            "total": sum(counts),
        })
    flat = [c for w in weeks for c in w["days"]]
    return {
        "user": USER,
        "window": "last 12 months",
        "total": int(calendar.get("totalContributions") or sum(flat)),
        "weeks": weeks,
        "days": flat,
        "longest_run": longest_run(flat),
        "languages": languages,
    }


def longest_run(flat):
    best = run = 0
    for count in flat:
        run = run + 1 if count > 0 else 0
        best = max(best, run)
    return best


def from_merged():
    """Token-less preview: keep the last calendar, refresh the language mix."""
    with open(MERGED) as f:
        projects = json.load(f)
    totals = {}
    for p in projects:
        for name, size in (p.get("languages") or {}).items():
            totals[name] = totals.get(name, 0) + int(size)
    return dict(sorted(totals.items(), key=lambda kv: -kv[1]))


def main():
    stats = None
    if TOKEN:
        try:
            calendar, repos = post_graphql()
            stats = shape(calendar, aggregate_languages(repos))
            print(f"graphql: {stats['total']} contributions over {len(stats['weeks'])} weeks, "
                  f"{len(stats['languages'])} languages")
        except Exception as e:  # noqa: BLE001 - fall back to the previous snapshot
            print(f"warn: graphql fetch failed ({e}); falling back", file=sys.stderr)
    else:
        print("warn: no GITHUB_TOKEN; using the previous snapshot", file=sys.stderr)

    if stats is None:
        if not os.path.exists(OUT):
            print(f"error: no reactor data available and no {OUT} to reuse", file=sys.stderr)
            sys.exit(1)
        with open(OUT) as f:
            stats = json.load(f)
        try:
            stats["languages"] = from_merged()
        except Exception as e:  # noqa: BLE001
            print(f"warn: could not refresh languages either ({e})", file=sys.stderr)

    with open(OUT, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
