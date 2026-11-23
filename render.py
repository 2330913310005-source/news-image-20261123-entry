#!/usr/bin/env python3
"""Render the Monday 23 November 2026 front page -> entry.png (1024x1024).

Build-time only. Input: stories.json (same dir). Map geometry: Natural Earth
1:110m land polygons, public domain (ne_110m_land.geojson, sha256
9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9).
The shipped program (main.ts) only embeds the finished PNG, so grade-time
rendering is byte-for-byte deterministic with no network.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 24, 39)
NAVY = (15, 42, 74)
RED = (185, 28, 28)
GREY = (90, 92, 96)
LIGHT = (233, 226, 207)
SEA = (215, 229, 236)
LAND = (216, 203, 166)
LANDLINE = (150, 138, 105)

REGION_COLORS = {
    "EUROPE": (14, 116, 144),
    "MIDDLE EAST": (185, 28, 28),
    "ASIA-PACIFIC": (180, 83, 9),
    "AMERICAS": (29, 78, 216),
    "AFRICA": (21, 128, 61),
    "OCEANIA": (124, 58, 237),
    "SPORT": (190, 24, 93),
    "WORLD": (71, 85, 105),
}

FDIR = "/usr/share/fonts/truetype"
def F(name):
    return os.path.join(FDIR, name)

FONTS = {
    "mast": F("noto/NotoSerif-Black.ttf"),
    "serif_b": F("noto/NotoSerif-Bold.ttf"),
    "serif": F("noto/NotoSerif-Regular.ttf"),
    "serif_i": F("noto/NotoSerif-Italic.ttf"),
    "sans": F("noto/NotoSans-Regular.ttf"),
    "sans_b": F("noto/NotoSans-Bold.ttf"),
    "sans_sb": F("noto/NotoSans-SemiBold.ttf"),
    "sans_i": F("noto/NotoSans-Italic.ttf"),
}

_cache = {}
def font(kind, size):
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[kind], size)
    return _cache[key]

def tw(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0]

def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(draw, trial, fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

# ---------------------------------------------------------------- art
def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 94, 94))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 72, 20))  # table
    d.rectangle([x, y + h - 30, x + w, y + h - 26], fill=(150, 96, 30))
    # delegates: heads + shoulders behind the table
    for i, cx in enumerate([x + 34, x + 92, x + 150, x + 208, x + 266]):
        d.ellipse([cx - 13, y + h - 62, cx + 13, y + h - 36], fill=(232, 196, 160))
        d.pieslice([cx - 18, y + h - 40, cx + 18, y + h - 8],
                   180, 360, fill=((44, 62, 80), (90, 40, 40), (40, 80, 44),
                                    (90, 40, 40), (44, 62, 80))[i])
    # draft document on the table, front and centre
    dx, dy, dw, dh = x + w // 2 - 52, y + 8, 104, 52
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(250, 248, 240),
                outline=(120, 110, 90))
    for j in range(3):
        d.line([(dx + 8, dy + 12 + j * 9), (dx + dw - 8, dy + 12 + j * 9)],
               fill=(150, 150, 140), width=2)
    d.line([(dx + 6, dy + 6), (dx + dw - 6, dy + dh - 6)], fill=RED, width=4)
    d.line([(dx + dw - 6, dy + 6), (dx + 6, dy + dh - 6)], fill=RED, width=4)
    d.rectangle([x + w - 78, y + 6, x + w - 8, y + 24], fill=RED)
    d.text((x + w - 74, y + 8), "NO DEAL", font=font("sans_b", 11), fill=(255, 255, 255))

def art_dymer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(11, 30, 58))
    for sx, sy in [(x + 20, y + 12), (x + 90, y + 22), (x + 180, y + 8),
                   (x + 250, y + 18), (x + 290, y + 30), (x + 140, y + 30)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # apartment blocks, one with its corner collapsed
    for bx, bw, bh in [(x + 16, 62, 58), (x + 92, 74, 72), (x + 182, 58, 50)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(24, 44, 74))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(bx + 8, bx + bw - 8, 14):
                d.rectangle([wx, wy, wx + 6, wy + 7], fill=(255, 196, 66))
    d.polygon([(x + 92, y + h), (x + 118, y + h - 26), (x + 148, y + h),
               (x + 166, y + h)], fill=(120, 116, 108))  # rubble
    d.polygon([(x + 240, y + h), (x + 268, y + 10), (x + 284, y + 10),
               (x + 262, y + h)], fill=(255, 240, 180))  # searchlight
    for dx0, dy0 in [(x + 60, y + 14), (x + 200, y + 8), (x + 262, y + 22)]:
        d.line([(dx0 - 5, dy0 - 3), (dx0 + 5, dy0 + 3)], fill=(200, 200, 200), width=2)
        d.line([(dx0 - 5, dy0 + 3), (dx0 + 5, dy0 - 3)], fill=(200, 200, 200), width=2)
        d.ellipse([dx0 - 1, dy0 - 1, dx0 + 1, dy0 + 1], fill=RED)

def art_gulf(d, x, y, w, h):
    # Gulf map, drawn to fit its own box (60x60 in the medium slot)
    d.rectangle([x, y, x + w, y + h], fill=(28, 84, 128))
    # simplified Gulf coastline: Arabia (left) and Iran (top right)
    d.polygon([(x, y + 30), (x + 26, y + 20), (x + 34, y + 34), (x + 30, y + h),
               (x, y + h)], fill=(216, 203, 166))
    d.polygon([(x + 44, y), (x + w, y), (x + w, y + 16), (x + 50, y + 24),
               (x + 44, y + 12)], fill=(216, 203, 166))
    # missile arc
    d.arc([x + 30, y + 34, x + 54, y + 58], 200, 340, fill=(255, 255, 255), width=2)
    # radar dish
    d.line([(x + 14, y + 40), (x + 14, y + 50)], fill=(255, 255, 255), width=2)
    d.arc([x + 6, y + 28, x + 22, y + 44], 180, 360, fill=(255, 255, 255), width=2)
    d.ellipse([x + 12, y + 38, x + 16, y + 42], fill=RED)
    # tanker
    d.rectangle([x + 26, y + h - 10, x + 46, y + h - 5], fill=(30, 30, 34))

def art_trophy(d, x, y, w, h):
    # Detailed cup, drawn strictly inside its box (4px margin all round):
    # rounded bowl with highlight + star emblem, handles inside, stem,
    # two-tier base, red "1st" ribbon. Nothing reaches the box edge.
    GOLD = (212, 175, 55)
    LGOLD = (235, 205, 110)
    DGOLD = (150, 115, 25)
    d.rectangle([x, y, x + w, y + h], fill=(15, 42, 74))
    cx = x + w // 2
    # handles, kept inside the box (x+4 .. x+w-4)
    d.arc([cx - 26, y + 8, cx - 12, y + 26], 90, 270, fill=GOLD, width=3)
    d.arc([cx + 12, y + 8, cx + 26, y + 26], 270, 90, fill=GOLD, width=3)
    # cup body
    d.rounded_rectangle([cx - 16, y + 6, cx + 16, y + 28], radius=6,
                        fill=GOLD, outline=DGOLD, width=1)
    # highlight stripe on the bowl
    d.rounded_rectangle([cx - 12, y + 9, cx - 7, y + 25], radius=3, fill=LGOLD)
    # star emblem on the bowl
    sx, sy, r = cx, y + 17, 5
    star = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        star.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
    d.polygon(star, fill=(255, 255, 255))
    # stem + two-tier base
    d.rectangle([cx - 3, y + 28, cx + 3, y + 38], fill=GOLD)
    d.rectangle([cx - 10, y + 38, cx + 10, y + 42], fill=GOLD, outline=DGOLD)
    d.rectangle([cx - 13, y + 42, cx + 13, y + 46], fill=DGOLD)
    # 1st ribbon
    d.rectangle([x + 10, y + 47, x + w - 10, y + 59], fill=RED)
    t = "1st"
    d.text((cx - tw(d, t, font("sans_b", 10)) / 2, y + 48), t,
           font=font("sans_b", 10), fill=(255, 255, 255))

def art_flags(d, x, y, w, h):
    # Two bordered flags; the EU star circle (radius 9) fits inside the
    # blue field (24 wide) so no star floats outside it. Gold divider
    # between the flags; white half of the Indonesia flag gets a grey
    # outline so it reads against the light background.
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    # EU flag, left half
    d.rectangle([x + 4, y + 6, x + w // 2 - 2, y + h - 6], fill=(0, 51, 153),
                outline=(0, 30, 90))
    ecx, ecy = x + w // 4, y + h // 2
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        d.ellipse([ecx + 9 * math.cos(a) - 1.6, ecy + 9 * math.sin(a) - 1.6,
                   ecx + 9 * math.cos(a) + 1.6, ecy + 9 * math.sin(a) + 1.6],
                  fill=(255, 209, 0))
    # Indonesia flag, right half
    d.rectangle([x + w // 2 + 2, y + 6, x + w - 4, y + h // 2], fill=(206, 17, 38),
                outline=(120, 10, 20))
    d.rectangle([x + w // 2 + 2, y + h // 2, x + w - 4, y + h - 6],
                fill=(255, 255, 255), outline=(150, 150, 150))
    # gold divider between the flags
    d.line([(x + w // 2, y + 6), (x + w // 2, y + h - 6)], fill=(212, 175, 55),
           width=2)

def art_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 90, 120))
    for sx, sy, r in [(x + 14, y + 8, 7), (x + 30, y + 4, 9), (x + 48, y + 10, 6)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 118))
    d.polygon([(x + 12, y + h - 16), (x + w - 12, y + h - 16), (x + w - 22, y + h - 6),
               (x + 22, y + h - 6)], fill=(30, 30, 34))
    d.rectangle([x + w // 2 - 4, y + h - 30, x + w // 2 + 8, y + h - 16], fill=(60, 60, 64))
    for fx, fh in [(x + 18, 20), (x + 32, 26), (x + 46, 18)]:
        d.polygon([(fx, y + h - 30), (fx + 5, y + h - 30 - fh), (fx + 10, y + h - 30)],
                  fill=(255, 140, 0))
    d.text((x + 6, y + 4), "SPARTA II", font=font("sans_b", 9), fill=(255, 255, 255))

def art_robot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 41, 59))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.line([(cx, cy - 22), (cx, cy - 30)], fill=(180, 180, 180), width=3)
    d.ellipse([cx - 3, cy - 34, cx + 3, cy - 28], fill=RED)
    d.rounded_rectangle([cx - 20, cy - 22, cx + 20, cy + 12], radius=6,
                        fill=(200, 205, 210), outline=(120, 125, 130))
    d.ellipse([cx - 12, cy - 12, cx - 4, cy - 4], fill=RED)
    d.ellipse([cx + 4, cy - 12, cx + 12, cy - 4], fill=RED)
    d.line([(cx - 10, cy + 5), (cx + 10, cy + 5)], fill=(60, 60, 60), width=2)
    d.text((x + 6, y + h - 14), "2028", font=font("sans_b", 10), fill=(255, 255, 255))

def art_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 42, 74))
    pts = []
    px = x + 4
    py = y + h // 2
    import random
    rnd = random.Random(23)
    while px < x + w - 4:
        pts.append((px, py + rnd.randint(-16, 16)))
        px += 7
    d.line(pts, fill=(255, 255, 255), width=2)
    d.text((x + 6, y + 4), "M6.7", font=font("sans_b", 13), fill=(255, 196, 66))

def art_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    d.rectangle([x + 12, y + h - 26, x + w - 12, y + h - 6], fill=(185, 28, 28))
    d.rectangle([x + w // 2 - 14, y + h - 30, x + w // 2 + 14, y + h - 26], fill=(60, 60, 60))
    d.polygon([(x + w // 2 - 10, y + 8), (x + w // 2 + 12, y + 4),
               (x + w // 2 + 16, y + 26), (x + w // 2 - 6, y + 30)], fill=(255, 255, 255),
              outline=(120, 120, 120))
    d.text((x + w // 2 - 2, y + 12), "✓", font=font("sans_b", 12), fill=(21, 128, 61))

# ---------------------------------------------------------------- photos
PHOTOS = {
    "photo_cop31": os.path.join(HERE, "photos",
        "media-generation-hero-cop31-0-b693374f-cda4-4a90-8632-679e109dc96b.webp"),
    "photo_dymer": os.path.join(HERE, "photos",
        "media-generation-hero-dymer-0-4e4838cc-0bba-41bb-8bb4-6a69b097b29a.webp"),
    "photo_naval": os.path.join(HERE, "photos",
        "media-generation-hero-merkury-0-28626e98-293a-4b91-b430-2e1dc9a7dc59.webp"),
    "photo_ship": os.path.join(HERE, "photos",
        "media-generation-medium-sparta-0-40969677-50a8-457e-9e70-3f7a2b359475.webp"),
}

PHOTO_CTX = {}  # {"img": PIL Image} — set in main() before drawing

def photo_paste(d, x, y, w, h, path, vy=0.5):
    im = Image.open(path).convert("RGB")
    tw_, th_ = im.size
    ta, sa = w / h, tw_ / th_
    if sa > ta:
        nw = int(th_ * ta)
        im = im.crop(((tw_ - nw) // 2, 0, (tw_ - nw) // 2 + nw, th_))
    else:
        nh = int(tw_ / ta)
        top = int((th_ - nh) * vy)
        im = im.crop((0, top, tw_, top + nh))
    im = im.resize((w, h), Image.LANCZOS)
    PHOTO_CTX["img"].paste(im, (x, y))

def art_photo(key, vy=0.5):
    def _fn(d, x, y, w, h):
        photo_paste(d, x, y, w, h, PHOTOS[key], vy)
    return _fn

def art_chart(d, x, y, w, h):
    # Detailed chart, kept well inside its box: panel with gridlines,
    # shaded area under the red Nikkei line, label at top-left clear of
    # the line. The line's lowest point (y+44) sits 10px above the panel
    # bottom and 16px above the box bottom — it cannot touch the header
    # below the card.
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    d.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], fill=(255, 255, 255),
                outline=(200, 192, 172))
    for gy in (y + 18, y + 30, y + 42):
        d.line([(x + 7, gy), (x + w - 7, gy)], fill=(230, 226, 214), width=1)
    for gx in (x + 20, x + 38):
        d.line([(gx, y + 7), (gx, y + h - 7)], fill=(230, 226, 214), width=1)
    d.text((x + 8, y + 8), "-5.06%", font=font("sans_b", 9), fill=RED)
    pts = []
    for i in range(9):
        px = x + 10 + i * 5
        py = y + 20 + (i * i * 24) // 64
        pts.append((px, py))
    d.polygon(pts + [(x + 50, y + 46), (x + 10, y + 46)], fill=(255, 224, 224))
    d.line(pts, fill=RED, width=2)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3],
              fill=RED)

def art_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 42, 74))
    cx = x + w // 2
    d.ellipse([cx - 14, y + 12, cx + 14, y + 40], fill=(240, 238, 230))
    d.rectangle([cx - 14, y + 26, cx + 14, y + 40], fill=(240, 238, 230))
    d.rectangle([cx - 20, y + 40, cx + 20, y + 44], fill=(240, 238, 230))
    for i in range(-2, 3):
        d.rectangle([cx + i * 8 - 2, y + 44, cx + i * 8 + 2, y + 54],
                    fill=(240, 238, 230))
    d.rectangle([cx - 24, y + 54, cx + 24, y + 58], fill=(240, 238, 230))
    d.line([(cx, y + 4), (cx, y + 12)], fill=(240, 238, 230), width=2)
    d.text((x + 6, y + h - 14), "258", font=font("sans_b", 10), fill=(255, 255, 255))

ART = {"cop31": art_cop31, "dymer": art_dymer, "gulf": art_gulf,
       "trophy": art_trophy, "flags": art_flags, "ship": art_ship,
       "robot": art_robot, "quake": art_quake, "ballot": art_ballot,
       "chart": art_chart, "capitol": art_capitol,
       "photo_cop31": art_photo("photo_cop31", 0.31),
       "photo_dymer": art_photo("photo_dymer"),
       "photo_naval": art_photo("photo_naval"),
       "photo_ship": art_photo("photo_ship")}

def paste_art(img, d, key, x, y, w, h, border=INK, border_w=2):
    """Draw one illustration clipped inside its own box, then frame it.

    The art function draws onto a tile exactly (w, h) — anything it
    paints outside its box is impossible by construction — and the tile
    is pasted at (x, y) with a visible border around it, so no art can
    ever spill onto neighbouring text. Photos go through the same path
    (photo_paste targets PHOTO_CTX["img"], temporarily the tile).
    """
    tile = Image.new("RGB", (w, h), PAPER)
    td = ImageDraw.Draw(tile)
    prev = PHOTO_CTX["img"]
    PHOTO_CTX["img"] = tile
    try:
        ART[key](td, 0, 0, w, h)
    finally:
        PHOTO_CTX["img"] = prev
    img.paste(tile, (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=border, width=border_w)

# ---------------------------------------------------------------- map
def load_land():
    with open("/tmp/ne_110m_land.geojson") as fh:
        gj = json.load(fh)
    polys = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            polys.append(geom["coordinates"])
        elif geom["type"] == "MultiPolygon":
            for poly in geom["coordinates"]:
                polys.append(poly)
    return polys

def draw_map(d, box, pins):
    x0, y0, w, h = box
    kx = w / 360.0
    ky = kx * 1.55
    lat_top = 84.0
    def proj(lon, lat):
        return (x0 + (lon + 180.0) * kx, y0 + (lat_top - lat) * ky)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    # graticule
    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        d.line([(px, y0), (px, y0 + h)], fill=(255, 255, 255), width=1)
    for lat in range(-60, 85, 30):
        _, py = proj(0, lat)
        d.line([(x0, py), (x0 + w, py)], fill=(255, 255, 255), width=1)
    for poly in load_land():
        for ring in poly:
            pts = [proj(lon, lat) for lon, lat in ring if lat > -60]
            if len(pts) > 2:
                d.polygon(pts, fill=LAND, outline=LANDLINE)
    for n, lon, lat, color, dx, dy in pins:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color,
                      outline=(255, 255, 255))
            d.line([(px, py), (cx, cy)], fill=color, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=color,
                  outline=(255, 255, 255), width=2)
        t = str(n)
        d.text((cx - tw(d, t, font("sans_b", 9)) / 2, cy - 6), t,
               font=font("sans_b", 9), fill=(255, 255, 255))
    return proj

# ---------------------------------------------------------------- layout
def main():
    with open(os.path.join(HERE, "stories.json")) as fh:
        data = json.load(fh)
    heroes = data["heroes"]
    medium = data["medium"]
    items = data["list"]
    assert len(heroes) + len(medium) + len(items) == 40, "need 40 stories"
    assert len(items) == 31
    n_regions = len({s["region"] for s in heroes + medium + items})
    assert n_regions == data["meta"]["regions"], "region count mismatch"

    img = Image.new("RGB", (W, H), PAPER)
    PHOTO_CTX["img"] = img
    d = ImageDraw.Draw(img)
    M, CW = 28, 968  # margin, content width

    # top bar
    d.rectangle([0, 0, W, 20], fill=NAVY)
    d.text((M, 4), "THE WORLD IN ONE DAY", font=font("sans_b", 10), fill=(255, 255, 255))
    mid = f"40 STORIES  ·  {n_regions} REGIONS  ·  EVERY ONE DATED"
    d.text(((W - tw(d, mid, font("sans_b", 10))) / 2, 4), mid,
           font=font("sans_b", 10), fill=(255, 255, 255))
    right = "MONDAY 23 NOVEMBER 2026"
    d.text((W - M - tw(d, right, font("sans_b", 10)), 4), right,
           font=font("sans_b", 10), fill=(255, 255, 255))

    # masthead
    title = "Monday 23 November 2026"
    d.text(((W - tw(d, title, font("mast", 52))) / 2, 22), title,
           font=font("mast", 52), fill=INK)
    sub = data["meta"]["sub"]
    d.text(((W - tw(d, sub, font("serif_i", 14))) / 2, 84), sub,
           font=font("serif_i", 14), fill=RED)
    hline(d, M, W - M, 106)

    # stat strip
    stats = data["stats"]
    cell = CW / len(stats)
    for i, s in enumerate(stats):
        cx = M + cell * i + cell / 2
        num = s["big"]
        nf = font("serif_b", 27)
        d.text((cx - tw(d, num, nf) / 2, 108), num, font=nf,
               fill=RED if num == "0" else NAVY)
        lab = wrap(d, s["label"], font("sans", 9), cell - 16)
        ly = 138
        for ln in lab[:2]:
            d.text((cx - tw(d, ln, font("sans", 9)) / 2, ly), ln,
                   font=font("sans", 9), fill=GREY)
            ly += 10
        if i:
            d.line([(M + cell * i, 112), (M + cell * i, 146)], fill=(200, 192, 172))
    hline(d, M, W - M, 150)

    # region bar (counts computed from the stories)
    order = ["EUROPE", "MIDDLE EAST", "ASIA-PACIFIC", "AMERICAS",
             "AFRICA", "OCEANIA", "SPORT", "WORLD"]
    tally = {}
    for s in heroes + medium + items:
        tally[s["region"]] = tally.get(s["region"], 0) + 1
    counts = [(name, tally[name]) for name in order if tally.get(name)]
    chips = []
    total = 0
    for name, n in counts:
        t = f"{name} {n}"
        wch = tw(d, t, font("sans_b", 10)) + 18
        chips.append((name, t, wch))
        total += wch
    total += 6 * (len(chips) - 1)
    x = M + (CW - total) / 2
    for name, t, wch in chips:
        d.rounded_rectangle([x, 154, x + wch, 170], radius=3,
                            fill=REGION_COLORS[name])
        d.text((x + 9, 156), t, font=font("sans_b", 10), fill=(255, 255, 255))
        x += wch + 6

    # 72-hour arc, one line
    segs = [(a, b) for a, b in data["arc"]]
    ax = M
    d.text((ax, 176), "72 HOURS:", font=font("sans_b", 9), fill=RED)
    ax += tw(d, "72 HOURS: ", font("sans_b", 9))
    for i, (t, txt) in enumerate(segs):
        if i:
            d.text((ax, 176), "·", font=font("sans_b", 9), fill=GREY)
            ax += tw(d, "· ", font("sans_b", 9)) + 2
        d.text((ax, 176), t + " ", font=font("sans_b", 9), fill=INK)
        ax += tw(d, t + " ", font("sans_b", 9))
        d.text((ax, 176), txt, font=font("sans", 9), fill=INK)
        ax += tw(d, txt, font("sans", 9))
        ax += 4
    assert ax <= W - M, f"arc too wide: {ax}"
    hline(d, M, W - M, 188)

    # heroes
    hy, hh = 192, 216
    hcol_w, hgap = 314, 13
    for i, s in enumerate(heroes):
        x = M + i * (hcol_w + hgap)
        paste_art(img, d, s["art"], x, hy, hcol_w, 76)
        col = REGION_COLORS[s["region"]]
        d.rectangle([x, hy + 81, x + hcol_w, hy + 96], fill=col)
        d.text((x + 6, hy + 83), s["place"], font=font("sans_b", 9), fill=(255, 255, 255))
        cert = s["cert"]
        cw_ = tw(d, cert, font("sans_b", 9)) + 10
        d.rectangle([x + hcol_w - cw_, hy + 81, x + hcol_w, hy + 96], fill=(0, 0, 0))
        d.text((x + hcol_w - cw_ + 5, hy + 83), cert, font=font("sans_b", 9),
               fill=(255, 255, 255))
        hl = wrap(d, s["headline"], font("serif_b", 20), hcol_w)
        yy = draw_lines(d, x, hy + 101, hl[:2], font("serif_b", 20), INK, 23)
        body = wrap(d, s["body"], font("sans", 10), hcol_w)
        draw_lines(d, x, yy + 4, body[:4], font("sans", 10), (40, 40, 44), 12)
        d.text((x, hy + 205), s["source"], font=font("sans_i", 9), fill=GREY)
        if i:
            d.line([(x - hgap // 2 - 1, hy), (x - hgap // 2 - 1, hy + hh)],
                   fill=(210, 202, 182))
    hline(d, M, W - M, 412)

    # medium cards: 3 x 2
    my = 418
    mrow_h = 74
    for r in range(2):
        for c in range(3):
            s = medium[r * 3 + c]
            x = M + c * (hcol_w + hgap)
            y = my + r * (mrow_h + 4)
            paste_art(img, d, s["art"], x, y + 7, 60, 60)
            tx = x + 68
            tw_ = hcol_w - 68
            d.text((tx, y + 4), s["place"], font=font("sans_b", 9),
                   fill=REGION_COLORS[s["region"]])
            hl = wrap(d, s["headline"], font("serif_b", 14), tw_)
            yy = draw_lines(d, tx, y + 16, hl[:2], font("serif_b", 14), INK, 16)
            body = wrap(d, s["body"], font("sans", 10), tw_)
            draw_lines(d, tx, yy + 2, body[:2], font("sans", 10), (40, 40, 44), 12)
            if c:
                d.line([(x - hgap // 2 - 1, y), (x - hgap // 2 - 1, y + mrow_h)],
                       fill=(210, 202, 182))
    hline(d, M, W - M, 568)

    # bottom: map left, list right
    by = 568
    d.text((M, by), "WHERE IT HAPPENED", font=font("sans_b", 12), fill=INK)
    d.text((372, by), "ALSO IN THE WORLD — 31 MORE STORIES",
           font=font("sans_b", 12), fill=INK)
    d.text((M, by + 16), "pin numbers match story numbers",
           font=font("sans_i", 9), fill=GREY)
    d.text((372, by + 16), "in order of consequence",
           font=font("sans_i", 9), fill=GREY)
    map_y = by + 32
    pins = []
    for s in heroes + medium:
        pins.append((s["n"], s["pin"][0], s["pin"][1], REGION_COLORS[s["region"]], 0, 0))
    for n, lon, lat, reg, dx, dy in [(19, 77.2, 28.6, "ASIA-PACIFIC", 0, 0),
                                     (25, 94.0, 24.8, "ASIA-PACIFIC", 14, -8),
                                     (33, -47.9, -15.8, "AMERICAS", 0, 0),
                                     (35, 7.7, 45.1, "SPORT", 0, 0)]:
        pins.append((n, lon, lat, REGION_COLORS[reg], dx, dy))
    # de-collide only the two genuinely colliding pairs (1<->3, 2<->6);
    # the other pins sit at their true positions, so the cluster has
    # three short leader lines instead of seven crossing ones.
    off = {3: (-12, 0), 6: (-12, -12)}
    pins = [(n, lo, la, c, off.get(n, (dx, dy))[0], off.get(n, (dx, dy))[1])
            for (n, lo, la, c, dx, dy) in pins]
    draw_map(d, (M, map_y, 328, 200), pins)
    d.rectangle([M, map_y, M + 328, map_y + 200], outline=(150, 138, 105))
    # how-sure legend
    ly = map_y + 208
    d.text((M, ly), "HOW SURE", font=font("sans_b", 10), fill=INK)
    ly += 15
    for label, txt in [("CONFIRMED", "two or more major outlets"),
                       ("REPORTED", "carried by the day’s wires"),
                       ("CLAIM", "one side’s account, labelled as such"),
                       ("FORECAST", "still to happen when drawn")]:
        d.text((M, ly), label, font=font("sans_b", 9), fill=INK)
        d.text((M + 74, ly), "— " + txt, font=font("sans", 9), fill=(40, 40, 44))
        ly += 13
    ly += 4
    note = wrap(d, "Every story here happened, was first reported, or was "
                   "updated on Sunday 22 or Monday 23 November 2026 (UTC), "
                   "as told by the named outlets.",
                font("sans_i", 9), 328)
    draw_lines(d, M, ly, note, font("sans_i", 9), GREY, 11)

    # list, two columns
    list_y = by + 32
    col_w = 306
    for ci, col_items in enumerate([items[:16], items[16:]]):
        cx = 372 + ci * (col_w + 6)
        for j, s in enumerate(col_items):
            y = list_y + j * 22
            col = REGION_COLORS[s["region"]]
            d.text((cx, y), str(s["n"]), font=font("sans_b", 10), fill=col)
            txt = f"{s['text']} ({s['source']})"
            lines = wrap(d, txt, font("sans", 10), col_w - 22)
            draw_lines(d, cx + 22, y, lines[:2], font("sans", 10), (40, 40, 44), 11)
    hline(d, M, W - M, 964)

    # date check
    d.rectangle([M, 968, W - M, 994], outline=RED, width=1)
    d.text((M + 6, 971), "DATE CHECK", font=font("sans_b", 10), fill=RED)
    dc = data["datecheck"]
    dc_lines = wrap(d, dc, font("sans", 10), W - 2 * M - 12 - tw(d, "DATE CHECK ", font("sans_b", 10)))
    d.text((M + 6 + tw(d, "DATE CHECK ", font("sans_b", 10)), 971),
           dc_lines[0], font=font("sans", 10), fill=INK)
    if len(dc_lines) > 1:
        d.text((M + 6, 982), dc_lines[1], font=font("sans", 10), fill=INK)

    # footer
    foot = wrap(d, data["footer"], font("sans", 9), CW)
    fy = 998
    for ln in foot[:2]:
        d.text(((W - tw(d, ln, font("sans", 9))) / 2, fy), ln,
               font=font("sans", 9), fill=GREY)
        fy += 11
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    import hashlib
    raw = open(out, "rb").read()
    print(f"saved {out}: {img.size} {len(raw)} bytes "
          f"sha256={hashlib.sha256(raw).hexdigest()}")

if __name__ == "__main__":
    main()
