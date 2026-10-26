"""Scrape the public contribution calendar (no token) -> data/contributions.json"""
import json, os, re, sys, datetime as dt
from collections import defaultdict
import requests
from bs4 import BeautifulSoup

USER = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "Amitpallai"))
r = requests.get(f"https://github.com/users/{USER}/contributions",
                 headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day[data-date]"):
    tip = tips.get(td.get("id"), "")
    m = re.match(r"(\d[\d,]*)\s+contribution", tip)
    days.append({"date": td["data-date"], "level": int(td.get("data-level", 0)),
                 "count": int(m.group(1).replace(",", "")) if m else 0})
days.sort(key=lambda d: d["date"])
if not days:
    sys.exit("no contribution cells found - GitHub markup may have changed")

total = sum(d["count"] for d in days)
best = max(days, key=lambda d: d["count"])
longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
cur = 0
for d in reversed(days):
    if d["count"]:
        cur += 1
    elif d is not days[-1] or d["date"] != str(dt.date.today()):
        break
monthly = defaultdict(int)
for d in days:
    monthly[d["date"][:7]] += d["count"]

os.makedirs("data", exist_ok=True)
json.dump({"user": USER, "total": total, "current_streak": cur, "longest_streak": longest,
           "best_day": best, "monthly": monthly, "days": days},
          open("data/contributions.json", "w"), indent=1)
print(f"{USER}: {total} contributions, {len(days)} days, streak {cur}/{longest}")
