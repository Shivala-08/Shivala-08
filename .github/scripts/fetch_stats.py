#!/usr/bin/env python3
"""
Fetch the numbers behind the activity radar (Phase 4 of the profile revamp).

Primary source: GraphQL contributionsCollection — the same rolling 12-month
window the streak/3D-graph panels already use, so every activity panel on the
profile measures the same period.

Fallback: the public REST search API, used when no GITHUB_TOKEN is present
(local preview runs). It can only report all-time totals, so stats.json records
which window it actually measured and the radar labels itself accordingly.

Writes stats.json next to the repo root.
"""
import json, os, ssl, sys, urllib.request

USER = os.environ.get("GH_USER", "Shivala-08")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("STATS_OUT", "stats.json")
CTX = ssl._create_unverified_context()

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
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
            "User-Agent": "profile-radar",
        },
    )
    with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    user = payload["data"]["user"]
    c = user["contributionsCollection"]
    return {
        "user": USER,
        "commits": c["totalCommitContributions"],
        "issues": c["totalIssueContributions"],
        "pulls": c["totalPullRequestContributions"],
        "reviews": c["totalPullRequestReviewContributions"],
        "repos": user["repositories"]["totalCount"],
        "window": "last 12 months",
        "source": "graphql",
    }


def get_rest(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-radar",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
        return json.load(r)


def from_rest():
    def count(q):
        return get_rest(
            f"https://api.github.com/search/issues?q={q}&per_page=1"
        )["total_count"]

    commits = get_rest(
        f"https://api.github.com/search/commits?q=author:{USER}&per_page=1"
    )["total_count"]
    user = get_rest(f"https://api.github.com/users/{USER}")
    return {
        "user": USER,
        "commits": commits,
        "issues": count(f"author:{USER}+type:issue"),
        "pulls": count(f"author:{USER}+type:pr"),
        "reviews": count(f"reviewed-by:{USER}+type:pr"),
        "repos": user.get("public_repos", 0),
        "window": "all-time",
        "source": "rest",
    }


def main():
    stats = None
    if TOKEN:
        try:
            stats = post_graphql()
            print(f"graphql: {stats}")
        except Exception as e:  # noqa: BLE001 - fall through to REST
            print(f"warn: graphql fetch failed ({e}); trying REST", file=sys.stderr)
    try:
        stats = stats or from_rest()
        if stats["source"] == "rest":
            print(f"rest fallback: {stats}")
    except Exception as e:  # noqa: BLE001
        if os.path.exists(OUT):
            print(f"warn: could not refresh {OUT} ({e}); reusing previous file", file=sys.stderr)
            return
        print(f"error: no stats available ({e})", file=sys.stderr)
        sys.exit(1)

    with open(OUT, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
