#!/usr/bin/env python3
"""Draw entry.png: a dense front-page poster summing up the world news of
Tuesday 24 November 2026. 1024x1024 PNG, baked here, shipped as-is."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# Palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY_LT = (38, 62, 110)
RED = (179, 38, 30)
GOLD = (198, 148, 42)
GREY = (110, 110, 105)
LINE = (200, 192, 172)
WHITE = (255, 255, 255)
CREAM = (250, 247, 238)

REGION_COLOURS = {
    "EUROPE": (31, 90, 160),
    "N. AMERICA": (13, 122, 122),
    "MIDDLE EAST": (196, 94, 20),
    "ASIA": (46, 125, 50),
    "AFRICA": (106, 62, 150),
    "LATIN AMERICA": (140, 90, 30),
    "SPACE": (60, 60, 90),
    "TECH": (31, 90, 160),
    "BUSINESS": (110, 80, 20),
    "MARKETS": (110, 80, 20),
    "SCIENCE": (60, 60, 90),
    "SPORT": (106, 62, 150),
}


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, text, fg, bg=None, fnt=None, pad=4):
    """Draw a small tag chip; returns width used."""
    fnt = fnt or font(SANS_B, 8)
    w = int(draw.textlength(text, font=fnt)) + pad * 2
    h = 13
    if bg is not None:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad, y + 1), text, font=fnt, fill=fg)
    return w


def draw_icon(d, kind, x, y, s, col):
    """Simple flat vector icon of size s at (x, y)."""
    if kind == "blast":  # explosion starburst
        cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)
    elif kind == "building":  # apartment block hit
        d.rectangle([x + 6, y + 8, x + s - 6, y + s - 2], fill=col)
        for r in range(3):
            for c in range(3):
                d.rectangle([x + 10 + c * 10, y + 13 + r * 11,
                             x + 16 + c * 10, y + 19 + r * 11], fill=WHITE)
        d.polygon([(x + s - 6, y + 8), (x + s + 2, y + 2), (x + s - 2, y + 14)],
                  fill=RED)
    elif kind == "chip":  # processor
        d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8], fill=col)
        d.rectangle([x + 16, y + 16, x + s - 16, y + s - 16], fill=WHITE)
        for i in range(3):
            d.line([x + 12 + i * 9, y + 2, x + 12 + i * 9, y + 8], fill=col, width=2)
            d.line([x + 12 + i * 9, y + s - 8, x + 12 + i * 9, y + s - 2],
                   fill=col, width=2)
            d.line([x + 2, y + 12 + i * 9, x + 8, y + 12 + i * 9], fill=col, width=2)
            d.line([x + s - 8, y + 12 + i * 9, x + s - 2, y + 12 + i * 9],
                   fill=col, width=2)
    elif kind == "pill":  # capsule
        d.rounded_rectangle([x + 4, y + s // 2 - 8, x + s - 4, y + s // 2 + 8],
                            radius=8, fill=col)
        d.rectangle([x + s // 2 - 1, y + s // 2 - 8, x + s // 2 + 1,
                     y + s // 2 + 8], fill=WHITE)
        d.ellipse([x + 6, y + s // 2 - 6, x + 14, y + s // 2 + 6], fill=WHITE)
    elif kind == "quake":  # seismograph waves
        pts = [(x + 2, y + s // 2), (x + 10, y + s // 2), (x + 14, y + 6),
               (x + 18, y + s - 6), (x + 22, y + s // 2), (x + 28, y + 10),
               (x + 32, y + s - 10), (x + 36, y + s // 2), (x + s - 2, y + s // 2)]
        d.line(pts, fill=col, width=3, joint="curve")
    elif kind == "plane":  # airliner
        d.polygon([(x + 4, y + s // 2 + 2), (x + s - 8, y + s // 2 - 8),
                   (x + s - 2, y + s // 2 - 2), (x + s - 8, y + s // 2 + 6)],
                  fill=col)
        d.polygon([(x + s // 2 - 4, y + s // 2 - 2), (x + s // 2 + 8, y + 4),
                   (x + s // 2 + 12, y + 8), (x + s // 2, y + s // 2 + 2)],
                  fill=col)
        d.polygon([(x + s // 2 - 2, y + s // 2 + 4), (x + s // 2 + 6, y + s - 4),
                   (x + s // 2 + 10, y + s - 2), (x + s // 2 + 2, y + s // 2 + 6)],
                  fill=col)
    elif kind == "school":  # schoolhouse
        d.polygon([(x + 4, y + s // 2), (x + s // 2, y + 4), (x + s - 4, y + s // 2)],
                  fill=col)
        d.rectangle([x + 8, y + s // 2, x + s - 8, y + s - 2], fill=col)
        d.rectangle([x + s // 2 - 5, y + s - 14, x + s // 2 + 5, y + s - 2],
                    fill=WHITE)
    elif kind == "oil":  # derrick
        d.polygon([(x + 6, y + s - 2), (x + s // 2 - 4, y + 4), (x + s // 2 + 6, y + 4),
                   (x + s - 6, y + s - 2)], outline=col, width=3)
        d.line([x + s // 2, y + 4, x + s // 2, y + s - 2], fill=col, width=3)
        d.line([x + 8, y + s // 2, x + s - 8, y + s // 2], fill=col, width=2)
    elif kind == "flame":  # fire
        d.polygon([(x + s // 2, y + 2), (x + s - 6, y + s // 2 + 4),
                   (x + s // 2 + 6, y + s - 2), (x + 6, y + s // 2 + 6)],
                  fill=col)
        d.ellipse([x + s // 2 - 6, y + s // 2 - 2, x + s // 2 + 6, y + s // 2 + 10],
                  fill=(255, 200, 60))
    elif kind == "phone":  # smartphone
        d.rounded_rectangle([x + 10, y + 2, x + s - 10, y + s - 2], radius=4,
                            fill=col)
        d.rectangle([x + 14, y + 8, x + s - 14, y + s - 10], fill=WHITE)
        d.line([x + s // 2 - 4, y + s - 6, x + s // 2 + 4, y + s - 6],
               fill=WHITE, width=2)
    elif kind == "trophy":  # cup
        d.polygon([(x + 12, y + 4), (x + s - 12, y + 4), (x + s - 16, y + s // 2),
                   (x + 12 + 4, y + s // 2)], fill=col)
        d.arc([x + 2, y + 8, x + 16, y + 26], 90, 270, fill=col, width=3)
        d.arc([x + s - 16, y + 8, x + s - 2, y + 26], -90, 90, fill=col, width=3)
        d.rectangle([x + s // 2 - 2, y + s // 2, x + s // 2 + 2, y + s - 8], fill=col)
        d.rectangle([x + s // 2 - 10, y + s - 8, x + s // 2 + 10, y + s - 4], fill=col)
    elif kind == "satellite":
        d.rectangle([x + s // 2 - 6, y + s // 2 - 6, x + s // 2 + 6, y + s // 2 + 6],
                    fill=col)
        d.polygon([(x + 2, y + 6), (x + s // 2 - 8, y + s // 2 - 2),
                   (x + s // 2 - 8, y + s // 2 + 8), (x + 2, y + s - 6)], fill=col)
        d.polygon([(x + s - 2, y + 6), (x + s // 2 + 8, y + s // 2 - 2),
                   (x + s // 2 + 8, y + s // 2 + 8), (x + s - 2, y + s - 6)],
                  fill=col)
        d.line([x + s // 2 + 6, y + s // 2 - 6, x + s - 6, y + 2], fill=col, width=2)
    elif kind == "podium":  # lectern
        d.rectangle([x + s // 2 - 3, y + 4, x + s // 2 + 3, y + s - 10], fill=col)
        d.polygon([(x + 6, y + 16), (x + s - 6, y + 16), (x + s // 2 + 8, y + 26),
                   (x + s // 2 - 8, y + 26)], fill=col)
        d.ellipse([x + s // 2 - 8, y + 2, x + s // 2 + 8, y + 12], fill=col)
        d.rectangle([x + 6, y + s - 8, x + s - 6, y + s - 4], fill=col)
    elif kind == "moon":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=(232, 214, 150))
        d.ellipse([x + 10, y + 10, x + 20, y + 20], fill=(205, 182, 110))
        d.ellipse([x + 24, y + 22, x + 32, y + 30], fill=(205, 182, 110))
        d.ellipse([x + 26, y + 8, x + 33, y + 15], fill=(205, 182, 110))
    elif kind == "chart":  # rising bars
        for i, h in enumerate((12, 20, 16, 28)):
            d.rectangle([x + 6 + i * 10, y + s - 4 - h, x + 13 + i * 10, y + s - 4],
                        fill=col)
        d.line([x + 4, y + s - 4, x + s - 4, y + s - 4], fill=INK, width=2)
    else:  # tower: skyscraper
        d.rectangle([x + s // 2 - 9, y + 4, x + s // 2 + 9, y + s - 2], fill=col)
        for r in range(4):
            d.rectangle([x + s // 2 - 6, y + 9 + r * 9, x + s // 2 + 6,
                         y + 14 + r * 9], fill=WHITE)
        d.rectangle([x + 6, y + s - 12, x + s // 2 - 12, y + s - 2], fill=col)
        d.rectangle([x + s // 2 + 12, y + s - 8, x + s - 6, y + s - 2], fill=col)


# ---- data: (num, icon, region, status, source, headline) ----
LEADS = [
    (1, "blast", "MIDDLE EAST", "CONFIRMED", "medics / police",
     "Israeli strike kills Hamas security chief in Gaza City"),
    (2, "building", "EUROPE", "CONFIRMED", "regional governor",
     "Russian strike on Zaporizhzhia kills 2, wounds 40"),
    (3, "chip", "TECH", "CONFIRMED", "SCMP / FT",
     "Nvidia reinstates Jensen Huang as CEO after Trump steps in"),
    (4, "pill", "BUSINESS", "CONFIRMED", "Sanofi",
     "Sanofi to buy US drugmaker Insmed for $41bn in cash"),
    (5, "quake", "ASIA", "CONFIRMED", "EMSC",
     "Magnitude 5.3 quake hits Nepal; felt across Asia"),
    (6, "plane", "ASIA", "CONFIRMED", "Reuters",
     "Sheikh Hasina plans return to Bangladesh on 16 Dec"),
    (7, "school", "EUROPE", "CONFIRMED", "police",
     "Teen gunman opens fire at Serbian school; 2 staff hurt"),
    (8, "oil", "MIDDLE EAST", "CONFIRMED", "PM's office",
     "Iraq takes over Kurdistan borders and oil fields"),
    (9, "flame", "ASIA", "CONFIRMED", "state media",
     "Gas blast at Hanoi food shop kills at least 6"),
    (10, "phone", "N. AMERICA", "CONFIRMED", "SCMP",
     "US states sue Musk firms over sexualised Grok images"),
    (11, "trophy", "AFRICA", "CONFIRMED", "Economic Times",
     "Senegal win back AFCON title as court overturns verdict"),
    (12, "satellite", "EUROPE", "REPORTED", "SCMP",
     "NATO warns Russia over nuclear-armed satellite reports"),
    (13, "podium", "N. AMERICA", "CONFIRMED", "SCMP",
     "Trump targets Newsom in speech on violent crime"),
    (14, "moon", "SCIENCE", "CONFIRMED", "The Learning IQ",
     "Beaver supermoon - full at 14:53 UTC, first of three"),
    (15, "chart", "MARKETS", "CONFIRMED", "Conference Board",
     "US consumer confidence jumps to 103.3"),
    (16, "tower", "MIDDLE EAST", "CLAIM", "coalition",
     "Riyadh skyscraper hit in 'terrorist attack'; none hurt"),
]

ONE_LINERS = [
    (17, "Bus-truck crash in Ras Al Khaimah kills at least 11", "CONFIRMED", "The National"),
    (18, "Modi and Merz review India-Germany partnership by phone", "CONFIRMED", "PMO"),
    (19, "Europe's largest satellite plant opens in Belgium", "CONFIRMED", "Royal Palace"),
    (20, "UK sanctions Houthis and four officials", "CONFIRMED", "Foreign Office"),
    (21, "UK destitution stays at record levels: 3.8m people", "CONFIRMED", "Yeni Safak"),
    (22, "South Korea offers $375,000 rewards to catch AI exam cheating", "CONFIRMED", "Just Security"),
    (23, "US set to raise tariffs on India, China over subsidies", "REPORTED", "WSJ"),
    (24, "Saudi Arabia approves 2027 budget, 190bn-riyal deficit", "CONFIRMED", "Econ. Times"),
    (25, "China Southern unit to buy 50 Boeing 737-8 jets, $7.4bn", "CONFIRMED", "Econ. Times"),
    (26, "Two arrested after break-in at Prince William's home", "CONFIRMED", "SCMP"),
    (27, "Global landmine casualties hit five-year high of 7,000", "CONFIRMED", "SCMP"),
    (28, "North Korea threatens to shut Swiss office over sanctions", "CONFIRMED", "SCMP"),
    (29, "Late pope's diary tells of seeing the devil three times", "REPORTED", "SCMP"),
    (30, "Hacked Russian data suggests nearly 500,000 soldiers dead", "REPORTED", "SCMP"),
    (31, "EU proposes banning Russian flags at sports events", "CONFIRMED", "SCMP"),
    (32, "China investigates Shanghai party chief in graft drive", "CONFIRMED", "Econ. Times"),
    (33, "China's cobalt firms race to beat DR Congo export ban", "CONFIRMED", "SCMP"),
    (34, "US envoy doubts Trump vow to end $3.8bn Israel funding", "REPORTED", "SCMP"),
    (35, "BJP and Akali Dal reunite for 2027 Punjab polls", "CONFIRMED", "WIO"),
    (36, "Fitch holds 'neutral' sovereign outlook, warns on debt", "CONFIRMED", "Econ. Times"),
    (37, "BYD in talks to buy Ineos car plant in France", "REPORTED", "Econ. Times"),
    (38, "House Democrat widens probe into Trump Jr's firm", "CONFIRMED", "Econ. Times"),
    (39, "Five-alarm fire in Union, New Jersey wrecks seven stores", "CONFIRMED", "Econ. Times"),
    (40, "Trump pardons Thanksgiving turkeys Freedom and Feathers", "CONFIRMED", "Econ. Times"),
    (41, "Car bomb wrecks Meta governor's office in Colombia", "REPORTED", "WIO"),
    (42, "Pennsylvania records ninth measles death; 46 counties hit", "CONFIRMED", "Horizon"),
    (43, "China opens Tiangong to first foreign astronaut: Pakistan", "CONFIRMED", "Straits Times"),
    (44, "School enrolment in Borno, Nigeria nearly doubles", "CONFIRMED", "Al Jazeera"),
    (45, "Gisele Pelicot book row: publisher apologises over photos", "CONFIRMED", "BBC"),
    (46, "England's reservoirs fall to 58% full despite wet week", "CONFIRMED", "Env. Agency"),
    (47, "FDA approves first drug for limb-girdle dystrophy", "CONFIRMED", "Principia"),
    (48, "Astronomers find most distant glowing black hole", "CONFIRMED", "Principia"),
    (49, "UN: 47,000 women killed by partners or relatives in 2025", "CONFIRMED", "UN"),
    (50, "WHO: fighting in eastern Congo traps Ebola teams", "CONFIRMED", "Principia"),
]

LEFT_OUT = [
    "ICJ: Myanmar guilty of Rohingya genocide - 19 Nov",
    "Anthropic's $2tn Wall Street debut - 19 Nov",
    "Riemann proof claim - 20 Nov",
    "US loses measles elimination status - 17 Nov",
    "COP31 ends with no deal - 22 Nov",
    "BepiColombo enters Mercury orbit - 21 Nov",
    "Verstappen wins Las Vegas Grand Prix - 22 Nov",
    "14 countries back ICJ Rohingya ruling - 23 Nov",
    "Guterres calls for AI-safety talks - 23 Nov",
    "Pentagon accuses Canada on defence - 23 Nov",
    "US blacklists Singapore cloud firm Megaspeed - 23 Nov",
    "Iran defies US naval blockade - statement 23 Nov",
]

NOT_YET = "Spain election 29 Nov  -  Hasina return 16 Dec  -  US Thanksgiving 27 Nov  -  Greece AI bill review 25 Nov"

TIMELINE = [
    ("EARLY", "5.3 quake strikes Nepal's Koshi Province"),
    ("MORNING", "Sanofi agrees $41bn Insmed buyout; EU moves to ban Russian flags"),
    ("MIDDAY", "Israeli strike kills Hamas security chief; US states sue Musk firms"),
    ("AFTERNOON", "Serbian school shooting; Hanoi gas blast; Beaver Moon full 14:53 UTC"),
    ("EVENING", "US confidence jumps to 103.3; Senegal regain AFCON title"),
]

# Map pins: (num, lon, lat)
PINS = [
    (1, 34.5, 31.5), (2, 35.2, 47.8), (3, -122.0, 37.4), (4, 2.3, 48.9),
    (5, 85.3, 27.7), (6, 90.4, 23.8), (7, 20.9, 44.0), (8, 44.4, 33.3),
    (9, 105.8, 21.0), (10, -95.0, 37.0), (11, -17.4, 14.7), (12, 4.4, 50.8),
    (13, -77.0, 38.9), (15, -77.0, 38.9), (16, 46.7, 24.7),
]

# Rough continent outlines (lon, lat) for the map strip.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-70, 45), (-75, 35), (-80, 26), (-85, 20),
     (-90, 15), (-95, 18), (-105, 22), (-115, 28), (-125, 40), (-125, 48),
     (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-78, 8), (-70, 10), (-60, 5), (-50, 0), (-40, -8), (-35, -15),
     (-40, -25), (-50, -32), (-60, -38), (-68, -45), (-70, -52), (-72, -40),
     (-72, -28), (-78, -15), (-80, -5), (-80, 2)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 66), (40, 68), (45, 60),
     (40, 50), (35, 45), (30, 42), (28, 41), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 42), (0, 39), (-2, 37), (-6, 36)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (48, 11),
     (51, 10), (46, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
     (15, -30), (12, -18), (9, -2), (9, 4), (0, 6), (-8, 5), (-13, 8),
     (-17, 12), (-16, 20), (-15, 27)],
    # Asia
    [(45, 68), (60, 69), (75, 72), (90, 75), (110, 74), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40),
     (130, 35), (122, 30), (115, 22), (108, 12), (103, 8), (100, 6),
     (95, 12), (90, 22), (85, 20), (80, 8), (75, 10), (70, 20), (60, 25),
     (55, 26), (50, 28), (48, 30), (45, 35), (40, 40), (42, 45), (45, 55),
     (48, 62)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (135, -12), (130, -13), (125, -14), (120, -20)],
]


def project(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 180.0) / 360.0 * w, y0 + (90.0 - lat) / 180.0 * h)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- header ----------
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 86, W, 88], fill=GOLD)
    d.text((24, 8), "THE WORLD IN ONE DAY", font=font(SERIF_B, 30), fill=WHITE)
    d.text((24, 46), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 22), fill=(255, 214, 120))
    d.text((700, 14), "50 STORIES", font=font(SANS_B, 20), fill=WHITE)
    d.text((700, 40), "7 REGIONS  ·  15 FIELDS", font=font(SANS_B, 13),
           fill=(200, 210, 235))
    d.text((700, 60), "ALL FROM ONE DAY", font=font(SANS_B, 13),
           fill=(200, 210, 235))
    d.text((1024 - 24 - d.textlength("No. 24", font=font(SERIF_B, 16)), 8),
           "No. 24", font=font(SERIF_B, 16), fill=(255, 214, 120))

    # ---------- timeline strip ----------
    y0 = 92
    d.rectangle([0, 88, W, 134], fill=(232, 226, 208))
    d.text((24, y0), "THE DAY IN FIVE PARTS  (UTC)",
           font=font(SANS_B, 11), fill=NAVY)
    seg_w = 196
    for i, (part, text) in enumerate(TIMELINE):
        x = 24 + i * seg_w
        d.text((x, y0 + 16), part, font=font(SANS_B, 10), fill=RED)
        for j, ln in enumerate(wrap(d, text, font(SANS, 9), seg_w - 12)):
            d.text((x, y0 + 24 + j * 11), ln, font=font(SANS, 9), fill=INK)
        if i:
            d.line([x - 8, y0 + 14, x - 8, y0 + 42], fill=LINE, width=1)

    # ---------- lead stories: 4 x 4 grid ----------
    gy0, cell_w, cell_h = 140, 256, 100
    d.text((24, gy0), "THE DAY'S LEADS", font=font(SANS_B, 12), fill=NAVY)
    d.line([150, gy0 + 8, 1000, gy0 + 8], fill=LINE, width=1)
    for idx, (num, icon, region, status, source, headline) in enumerate(LEADS):
        col, row = idx % 4, idx // 4
        x = col * cell_w
        y = gy0 + 16 + row * cell_h
        if col:
            d.line([x, y + 4, x, y + cell_h - 8], fill=LINE, width=1)
        if row:
            d.line([x + 8, y - 2, x + cell_w - 8, y - 2], fill=LINE, width=1)
        # number badge
        d.ellipse([x + 10, y + 6, x + 30, y + 26], fill=NAVY)
        num_txt = str(num)
        d.text((x + 20 - d.textlength(num_txt, font=font(SANS_B, 11)) / 2, y + 8),
               num_txt, font=font(SANS_B, 11), fill=WHITE)
        # icon
        colr = REGION_COLOURS.get(region, NAVY)
        draw_icon(d, icon, x + 38, y + 2, 40, colr)
        # headline
        lines = wrap(d, headline, font(SANS_B, 11), cell_w - 88)
        for j, ln in enumerate(lines[:3]):
            d.text((x + 84, y + 4 + j * 13), ln, font=font(SANS_B, 11), fill=INK)
        # tags row
        ty = y + 46
        w1 = chip(d, x + 10, ty, region, WHITE, bg=colr)
        st_bg = (46, 125, 50) if status == "CONFIRMED" else (176, 120, 20)
        w2 = chip(d, x + 14 + w1, ty, status, WHITE, bg=st_bg)
        d.text((x + 18 + w1 + w2, ty + 1), "Src: " + source,
               font=font(SANS, 8), fill=GREY)
        # second line of context under tags
        d.text((x + 10, ty + 17), "24 Nov 2026", font=font(SANS, 8), fill=GREY)

    # ---------- world map ----------
    my0 = 560
    d.rectangle([0, my0, W, my0 + 108], fill=(228, 236, 242))
    d.text((24, my0 + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=NAVY)
    d.text((24, my0 + 22), "Numbered pins mark the 16 lead stories. 14: the Beaver",
           font=font(SANS, 9), fill=GREY)
    d.text((24, my0 + 34), "supermoon, seen worldwide.",
           font=font(SANS, 9), fill=GREY)
    mx0, myy0, mw, mh = 210, my0 + 6, 800, 96
    for cont in CONTINENTS:
        pts = [project(lon, lat, mx0, myy0, mw, mh) for lon, lat in cont]
        d.polygon(pts, fill=(176, 196, 214), outline=(120, 150, 185))
    for num, lon, lat in PINS:
        px, py = project(lon, lat, mx0, myy0, mw, mh)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=WHITE, width=2)
        t = str(num)
        d.text((px - d.textlength(t, font=font(SANS_B, 9)) / 2, py - 7),
               t, font=font(SANS_B, 9), fill=WHITE)

    # ---------- one-liners ----------
    oy0 = 674
    d.text((24, oy0), "AND THE REST OF THE DAY  —  34 MORE STORIES",
           font=font(SANS_B, 12), fill=NAVY)
    d.line([330, oy0 + 8, 1000, oy0 + 8], fill=LINE, width=1)
    col_w = 500
    for i, (num, headline, status, source) in enumerate(ONE_LINERS):
        col = i // 17
        row = i % 17
        x = 24 + col * col_w
        y = oy0 + 22 + row * 12
        tag = "R" if status == "REPORTED" else "C"
        d.text((x, y), f"{num}. {headline}",
               font=font(SANS, 10), fill=INK)
        tw = d.textlength(f"{num}. {headline}", font=font(SANS, 10))
        d.text((x + tw + 4, y), f"[{tag}] {source}",
               font=font(SANS, 8), fill=GREY)

    # ---------- date check box ----------
    dy0 = 904
    d.rectangle([12, dy0, W - 12, dy0 + 60], outline=RED, width=2)
    d.text((24, dy0 + 5), "DATE CHECK — LEFT OUT ON PURPOSE: these broke on EARLIER days, not 24 Nov",
           font=font(SANS_B, 10), fill=RED)
    for i, item in enumerate(LEFT_OUT):
        col = i // 3
        row = i % 3
        x = 24 + col * 248
        y = dy0 + 22 + row * 11
        d.text((x, y), "✕ " + item, font=font(SANS, 8), fill=INK)
    # footer
    fy0 = 968
    d.rectangle([0, fy0, W, H], fill=NAVY)
    d.text((24, fy0 + 6),
           "Every story here happened, or was first reported, on Tuesday 24 November 2026; claims are attributed.",
           font=font(SANS_B, 11), fill=WHITE)
    d.text((24, fy0 + 22),
           "Sources: Just Security / AP · SCMP · WIO · Economic Times · Yeni Safak · Horizon · Principia · The Learning IQ · Reuters · BBC · Al Jazeera · UN · WHO · Conference Board",
           font=font(SANS, 9), fill=(200, 210, 235))
    d.text((24, fy0 + 34),
           "50 stories · 7 regions · 15 fields · Tuesday 24 November 2026",
           font=font(SANS, 9), fill=(255, 214, 120))

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    draw()
