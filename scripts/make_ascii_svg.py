"""source-prepped.png -> ascii-portrait.svg (monochrome, types itself in once)."""
import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

COLS, CW, LH, FS = 100, 3.7, 7.4, 6.2
RAMP = " .`:-=+*cs#%@"          # background/dark (space) -> bright (dense)
CROP_W, CROP_H = 0.78, 1.0     # crop width as fraction of subject width; height ratio
GAMMA = 0.8                    # <1 lifts dark areas (hair), >1 darkens mids
FILL, BG = "#c9d1d9", "#0d1117"

im = Image.open("source-prepped.png").convert("LA")
a = np.array(im)[:, :, 1]
ys, xs = np.where(a > 128)
pad = 12
box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
       min(xs.max() + pad, im.width), min(ys.max() + pad, im.height))
# head-and-upper-shoulders crop, centred on the head (centroid of the top 30% of the subject)
top, bot, bw = ys.min(), ys.max(), xs.max() - xs.min()
head = a[top:top + int((bot - top) * 0.3)]
hx = int(np.average(np.arange(a.shape[1]), weights=(head > 128).sum(axis=0) + 1e-9))
half = int(bw * CROP_W / 2)
box = (max(hx - half, 0), max(top - pad, 0), min(hx + half, im.width), min(top - pad + 2 * half * CROP_H, im.height))
box = tuple(int(v) for v in box)
im = im.crop(box)
rows = round(COLS * im.height / im.width * (CW / LH))
im = im.resize((COLS, rows), Image.LANCZOS)
lum, alpha = (np.array(im)[:, :, i].astype(float) for i in (0, 1))
fg = lum[alpha > 128]
lo, hi = np.percentile(fg, 3), np.percentile(fg, 99)
lum = np.clip((lum - lo) / (hi - lo), 0, 1) * 255   # stretch subject tones

lines = []
for r in range(rows):
    s = ""
    for c in range(COLS):
        if alpha[r, c] < 128:
            s += " "
        else:
            v = (lum[r, c] / 255) ** GAMMA
            s += RAMP[min(int(v * (len(RAMP) - 1) + 0.5), len(RAMP) - 1)]
    lines.append(s.rstrip())

W, H = COLS * CW + 20, rows * LH + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">',
     f'<rect width="100%" height="100%" rx="10" fill="{BG}"/>']
for i, line in enumerate(lines):
    y = 10 + (i + 1) * LH - 1.5
    t = i * 0.045
    o.append(f'<clipPath id="c{i}"><rect x="10" y="{y - LH:.1f}" width="0" height="{LH:.1f}">'
             f'<animate attributeName="width" from="0" to="{COLS * CW:.1f}" begin="{t:.3f}s" dur="0.7s" fill="freeze"/>'
             f'</rect></clipPath>')
    if line.strip():
        o.append(f'<g clip-path="url(#c{i})"><text x="10" y="{y:.1f}" xml:space="preserve" fill="{FILL}" '
                 f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{FS}" '
                 f'textLength="{len(line) * CW:.1f}" lengthAdjust="spacing">{escape(line)}</text></g>')
    o.append(f'<rect x="10" y="{y - LH + 1:.1f}" width="{CW:.1f}" height="{LH - 1:.1f}" fill="{FILL}" opacity="0">'
             f'<animate attributeName="x" from="10" to="{10 + COLS * CW:.1f}" begin="{t:.3f}s" dur="0.7s" fill="freeze"/>'
             f'<set attributeName="opacity" to="0.9" begin="{t:.3f}s"/>'
             f'<set attributeName="opacity" to="0" begin="{t + 0.7:.3f}s"/></rect>')
o.append("</svg>")
open("ascii-portrait.svg", "w").write("\n".join(o))
print(f"wrote ascii-portrait.svg ({COLS}x{rows})")
