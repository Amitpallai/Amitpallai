"""Isolate the subject, boost local contrast, save grayscale+alpha PNG.
Usage: python scripts/prep_photo.py source-photo.jpg"""
import sys
import numpy as np, cv2
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
img = Image.open(src).convert("RGB")

try:
    from rembg import remove, new_session
    # u2netp = small model (~4 MB); the default one needs >1 GB RAM
    alpha = np.array(remove(img, session=new_session("u2netp")))[:, :, 3]
except Exception as e:  # model download blocked etc. -> brightness fallback
    print("rembg unavailable, using threshold fallback:", e)
    g = cv2.GaussianBlur(np.array(img.convert("L")), (0, 0), 3)
    m = (g > 45).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    alpha = ((lab == big) * 255).astype(np.uint8)

gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
out = np.dstack([gray, alpha])
Image.fromarray(out, "LA").save("source-prepped.png")
print("wrote source-prepped.png")
