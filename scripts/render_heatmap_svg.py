"""data/contributions.json -> contrib-heatmap.svg (diagonal reveal, plays once)"""
import json, datetime as dt

D = json.load(open("data/contributions.json"))
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, LEFT, TOP = 12, 3, 38, 44
P = CELL + GAP
days = D["days"]
first = dt.date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7            # Sunday-first rows
ncols = (offset + len(days) + 6) // 7
W, H = LEFT + ncols * P + 20, TOP + 7 * P + 52
F = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     f'<style>text{{font-family:{F};font-size:10.5px;fill:#8b949e}}'
     '.b{opacity:0;animation:d .5s ease-out forwards}'
     '@keyframes d{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:none}}</style>',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>']
last_m = None
for i, d in enumerate(days):
    col, row = divmod(i + offset, 7)
    date = dt.date.fromisoformat(d["date"])
    if row == 0 and date.month != last_m and col < ncols - 2:
        o.append(f'<text x="{LEFT + col * P}" y="{TOP - 10}">{date.strftime("%b")}</text>')
        last_m = date.month
    lvl = min(d["level"], 4)
    if d["level"] >= 4 and d["count"] >= 10:
        lvl = 5
    delay = (col + row) * 0.018
    o.append(f'<rect class="b" x="{LEFT + col * P}" y="{TOP + row * P}" width="{CELL}" height="{CELL}" rx="3" '
             f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s"><title>{d["count"]} on {d["date"]}</title></rect>')
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="8" y="{TOP + r * P + 10}">{name}</text>')
yb = TOP + 7 * P + 24
o.append(f'<text x="{LEFT}" y="{yb}" style="fill:#c9d1d9">{D["total"]:,} contributions in the last year</text>')
o.append(f'<text x="{LEFT}" y="{yb + 16}">streak {D["current_streak"]}d  |  longest {D["longest_streak"]}d  |  best day {D["best_day"]["count"]}</text>')
lx = W - 20 - 6 * P - 70
o.append(f'<text x="{lx}" y="{yb + 10}">Less</text>')
for j, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx + 32 + j * P}" y="{yb}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx + 38 + 6 * P}" y="{yb + 10}">More</text></svg>')
open("contrib-heatmap.svg", "w").write("\n".join(o))
print("wrote contrib-heatmap.svg")
