import requests
import os
import json

GITHUB_TOKEN = os.environ.get("GH_TOKEN")
USERNAME = "Shivala-08"

def fetch_contributions():
    if not GITHUB_TOKEN:
        raise ValueError("GH_TOKEN environment variable not set")
    
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """

    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"login": USERNAME}},
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
    )
    
    if resp.status_code != 200:
        raise Exception(f"Query failed with status code {resp.status_code}: {resp.text}")
        
    data = resp.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
        
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

    # grid[week][day] = contribution count
    grid = []
    for i, week in enumerate(weeks):
        days = [day["contributionCount"] for day in week["contributionDays"]]
        if len(days) < 7:
            if i == 0:
                # First week: pad at the start (pre-fill days with 0)
                days = [0] * (7 - len(days)) + days
            else:
                # Last week: pad at the end (post-fill days with 0)
                days = days + [0] * (7 - len(days))
        grid.append(days)

    with open("contributions.json", "w") as f:
        json.dump(grid, f)

if __name__ == "__main__":
    fetch_contributions()
