"""Neofetch-style info card -> info-card.svg. Edit ROWS to change content.
STATIC=1 emits a frozen frame."""
import os
from xml.sax.saxutils import escape

STATIC = os.environ.get("STATIC") == "1"
USER, HOST = "amit", "github"
ROWS = [  # (key, value, key_color)
    ("Name",       "Amit Kumar Pallai", "#58a6ff"),
    ("Now",        "Final-year CSE @ Bhadrak Institute of Engg & Tech", "#3fb950"),
    ("Prev",       "IT Consultant @ Lloyd (Havells) - 500+ requests", "#d29922"),
    ("Location",   "Gurgaon  (from Odisha)", "#f778ba"),
    ("", "", ""),
    ("Languages",  "Java, JavaScript, TypeScript", "#58a6ff"),
    ("Stack",      "React, Next.js, Node.js", "#3fb950"),
    ("Data",       "MongoDB, PostgreSQL, Power BI", "#d29922"),
    ("", "", ""),
    ("BlinkBasket","E-commerce: 1200+ txns, 92% retention", "#f778ba"),
    ("Meet.io",    "Video calls: 50+ concurrent users", "#58a6ff"),
    ("Status",     "Open to work - let's build something", "#3fb950"),
]
W, LH, TOP = 490, 21, 62
H = TOP + len(ROWS) * LH + 40
F = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     '<style>'
     f'text{{font-family:{F};font-size:12.5px}}'
     + ('' if STATIC else '.l{opacity:0;animation:in .45s ease-out forwards}'
        '@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}'
        '.cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}')
     + '</style>',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
     f'<path d="M0 10a10 10 0 0 1 10-10h{W-20}a10 10 0 0 1 10 10v22H0z" fill="#161b22"/>',
     '<circle cx="20" cy="16" r="5.5" fill="#ff5f56"/><circle cx="40" cy="16" r="5.5" fill="#ffbd2e"/><circle cx="60" cy="16" r="5.5" fill="#27c93f"/>',
     f'<text x="{W/2}" y="20" text-anchor="middle" fill="#8b949e" style="font-size:11.5px">{USER}@{HOST}: ~</text>',
     f'<text x="20" y="52" fill="#3fb950">{USER}@{HOST}</text><text x="{20+len(USER+HOST)*7.6+8:.0f}" y="52" fill="#8b949e">---------------</text>']
for i, (k, v, c) in enumerate(ROWS):
    if not k:
        continue
    y = TOP + 14 + i * LH
    st = '' if STATIC else f' style="animation-delay:{0.25 + i * 0.12:.2f}s"'
    cls = '' if STATIC else ' class="l"'
    o.append(f'<g{cls}{st}><text x="20" y="{y}" fill="{c}" font-weight="bold">{escape(k)}</text>'
             f'<text x="132" y="{y}" fill="#c9d1d9">{escape(v)}</text></g>')
yb = TOP + 14 + len(ROWS) * LH + 6
o.append(f'<g><text x="20" y="{yb}" fill="#3fb950">$</text><rect class="cur" x="32" y="{yb-11}" width="8" height="14" fill="#c9d1d9"/></g>')
for j, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39c5cf"]):
    o.append(f'<rect x="{W-20-6*22+j*22}" y="{yb-12}" width="18" height="14" rx="3" fill="{col}"/>')
o.append("</svg>")
open("info-card.svg", "w").write("\n".join(o))
print("wrote info-card.svg")
