#!/usr/bin/env python3
"""Render news-26-b173-numbers entry.png (1024x1024, <=1 MiB).
Fresh build for make.fun news-image-20261126, account b173.
Layout V22 (new): masthead / DATE CHECK strip / Macy's banner hero /
Hormuz + tariffs side by side / 10 cards 2x5 / world map + key /
ALSO 3 columns / sources footer. All facts from KANON-20261126.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette ----
PAPER = (246, 241, 229)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
NAVY2 = (36, 56, 96)
RED = (181, 52, 42)
TEAL = (14, 107, 107)
GOLD = (227, 181, 5)
GOLD_DK = (146, 108, 0)
CREAM = (250, 247, 238)
CARD_BG = (255, 255, 255)
CARD_LINE = (201, 196, 182)
SEA = (207, 224, 234)
LAND = (124, 154, 94)
LAND_DK = (104, 134, 76)
MUTED = (90, 88, 80)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


# ---- rect bookkeeping for asserts ----
TEXT_RECTS = []  # (label, x0, y0, x1, y1)
ART_RECTS = []   # (label, x0, y0, x1, y1)
BADGE_RECTS = []  # (card_no, x0, y0, x1, y1)


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines, each fits max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading, box, label):
    """Draw lines top-left at (x, y); assert every line fits its box
    with >=2px margin on all sides. Returns y just below last line."""
    bx0, by0, bx1, by1 = box
    for ln in lines:
        w = draw.textlength(ln, font=font)
        asc, desc = font.getmetrics()
        lh = asc + desc
        assert x >= bx0 and x + w <= bx1, \
            "%s line too wide: '%s' %.1fpx in box %s" % (label, ln, w, box)
        assert y >= by0 and y + lh <= by1, \
            "%s line outside box vertically: y=%d box %s" % (label, y, box)
        draw.text((x, y), ln, font=font, fill=fill)
        TEXT_RECTS.append((label, x, y, x + w, y + leading))
        y += leading
    return y


def fit_lines(draw, text, font, max_w, max_lines, label):
    lines = wrap(draw, text, font, max_w)
    assert len(lines) <= max_lines, \
        "%s needs %d lines (max %d): %r" % (label, len(lines), max_lines, text)
    return lines


# ---- content ----
HERO1 = {
    "key": "macys-parade",
    "kicker": "NEW YORK  ·  [C]",
    "head": "MACY'S 100TH PARADE POSTPONED",
    "deck": "Thanksgiving parade delayed by storm — first ever weather "
            "postponement; balloons grounded as gusts hit 60 mph.",
    "why": "WHY IT MATTERS: America's most iconic Thanksgiving parade "
           "moves to Saturday, and the storm that stopped it is hitting "
           "the whole East Coast.",
    "stat": "100TH EDITION  ·  RESCHEDULED SAT 28 NOV, 08:30 ET  ·  GUSTS 60 MPH",
}
HERO2 = {
    "key": "hormuz-mines",
    "kicker": "STRAIT OF HORMUZ  ·  [CL]",
    "head": "IRGC CLAIMS 2 TANKERS HIT BY MINES",
    "deck": "Tehran says two tankers exploded and burned; one carried "
            "2m barrels of crude.",
    "why": "WHY IT MATTERS: The unverified claim puts the top oil "
           "chokepoint at the centre of the Iran war.",
    "stat": "2M BARRELS ABOARD · BRENT $93.8 (+0.9%)",
}
HERO3 = {
    "key": "tariffs-rebound",
    "kicker": "GLOBAL MARKETS  ·  [C]",
    "head": "TRUMP TARIFFS: MARKETS REBOUND",
    "deck": "Stocks in Europe and Asia bounce back as the new duties look "
            "milder than feared.",
    "why": "WHY IT MATTERS: The salvo hit 14 partners, yet investors "
           "judged the hit modest and bought the dip.",
    "stat": "14 PARTNERS · CHINA 20% · STOXX +1.6% · MSCI +0.4%",
}

CARDS = [
    {"key": "gaza-strike", "place": "GAZA", "tag": "[C]",
     "head": "ISRAEL KILLS HAMAS EDUCATION OFFICIAL",
     "deck": "Khaled Abu Nada and wife killed in Deir al-Balah; 9 dead overnight.",
     "stat": "9 KILLED OVERNIGHT"},
    {"key": "kyiv-mall", "place": "KYIV", "tag": "[C]",
     "head": "RUSSIAN MISSILES HIT KYIV MALL",
     "deck": "Ballistic strike on Desnianskyi mall; 7 hurt as 113 drones hit.",
     "stat": "7 HURT  ·  113 DRONES"},
    {"key": "bogor-mine", "place": "BOGOR", "tag": "[C]",
     "head": "FLOODED GOLD MINE: 13 DEAD, 13 MISSING",
     "deck": "Illegal mine floods after heavy rain; teams dig 100 m down.",
     "stat": "13 DEAD  ·  13 MISSING"},
    {"key": "netanyahu-case", "place": "JERUSALEM", "tag": "[R]",
     "head": "JUDGE: DROP NETANYAHU BRIBERY CASE",
     "deck": "Judge urges dropping Case 4000, the PM's bribery charge.",
     "stat": "CASE 4000"},
    {"key": "kim-nuclear", "place": "PYONGYANG", "tag": "[C]",
     "head": "KIM AT NUCLEAR PLANT, PUSHES TACTICAL ARMS",
     "deck": "Kim visits a nuclear-material plant, urges wider tactical use.",
     "stat": "TACTICAL NUCLEAR PUSH"},
    {"key": "spacex-starmind", "place": "WASHINGTON", "tag": "[C]",
     "head": "SPACEX 'STARMIND': 1M SATELLITES OKAYED",
     "deck": "US approves 1m orbital compute modules; first space-data nod.",
     "stat": "1M MODULES  ·  NOV 25"},
    {"key": "uk-migration", "place": "LONDON", "tag": "[C]",
     "head": "UK NET MIGRATION FALLS TO 77,000",
     "deck": "Lowest since 1997 outside the pandemic; year to June 2026.",
     "stat": "77,000  ·  LOWEST SINCE 1997"},
    {"key": "russia-budget", "place": "MOSCOW", "tag": "[C]",
     "head": "RUSSIA OKAYS RECORD MILITARY BUDGET",
     "deck": "Biggest post-Soviet defence budget signed off.",
     "stat": "RECORD POST-SOVIET"},
    {"key": "bangkok-depot", "place": "BANGKOK", "tag": "[C]",
     "head": "OIL DEPOT BLAST HURTS 7 IN BANGKOK",
     "deck": "Blast at a Bangkok oil depot; fire out in about 30 minutes.",
     "stat": "7 HURT  ·  FIRE OUT ~30 MIN"},
    {"key": "germany-plot", "place": "COLOGNE", "tag": "[C]",
     "head": "2 HELD OVER GERMAN SYNAGOGUE PLOT",
     "deck": "Iraqi suspects held in Cologne and Heidelberg over a March plan.",
     "stat": "2 SUSPECTS HELD"},
]

# ALSO items: (text, tag, hero_subfact?) — each a distinct story, max 1x.
# 25-Nov items carry [CL] + "25 Nov" in the text.
ALSO = [
    ("Eisenkot wins first Israeli coalition deal", "[C]", False),
    ("Merz warns Russia's ambitions go beyond Ukraine", "[C]", False),
    ("UK on alert over drone threat to airbases", "[R]", False),
    ("Norse Atlantic suspends all flights, warns of bankruptcy", "[C]", False),
    ("Poundland enters administration, 11,000 jobs at risk", "[C]", False),
    ("Malaysia sues Google $146m over harmful content", "[C]", False),
    ("Kenya court halts US-backed Ebola facility", "[C]", False),
    ("Belarus offers to fly Zelensky to Moscow; he declines", "[R]", False),
    ("Kushner calls Putin \"grandmaster of politics\"", "[C]", False),
    ("Estonia decides to close border", "[C]", False),
    ("Copernicus confirms longest stretch above 2°C warming", "[C]", False),
    ("Nvidia reports halting AI server shipments to 4 countries", "[R]", False),
    ("Bitcoin funds hit record $4.94bn monthly outflows", "[C]", False),
    ("Philadelphia Thanksgiving parade cancelled over weather", "[C]", True),
    ("UKMTO: blast near tanker 50 nm west of Dubai, crew safe", "[C]", True),
    ("Couple aged 37 and 38 killed in Kharkiv apartment strike", "[C]", False),
    ("18 wounded in Kryvyi Rih strike", "[C]", False),
    ("Ukraine hits Savasleyka base, 5 jets damaged (3 MiG-31, 2 Su-34)", "[C]", False),
    ("Subkhankulovo pump station in Bashkortostan ablaze", "[C]", False),
    ("Cargo ship near Odesa reportedly hit", "[R]", False),
    ("UN rights chief Turk warns of atrocity crimes risk in Gaza", "[C]", False),
    ("OPEC+ meets 29 Nov on 2027 output", "[C]", False),
    ("Iraq closes two Kurdistan border crossings with Syria, Iran", "[C]", False),
    ("Guinea-Bissau military delays elections to 2028", "[C]", False),
    ("Russia claims it hit drone-linked sites in Kyiv strike", "[R]", False),
    ("Serbia calls presidential election for 27 December", "[C]", False),
    ("Two Italians killed in Iranian drone attack in Kuwait", "[C]", False),
    ("De Cos chosen as next European Central Bank chief", "[C]", False),
    ("Bank of Korea raises rates to 3.25%", "[C]", False),
    ("Diesel tanker capsizes off Ibiza, 1 crew killed", "[C]", False),
    ("German synagogue plot targeted late March attack", "[C]", False),
    ("Saudi defences downed 2 missiles bound for Riyadh [CL] · 25 Nov", "[CL]", False),
    ("UKMTO 223-26: tanker hit 18 nm east of Khasab [CL] · 25 Nov", "[CL]", False),
    ("UK signs £8bn Babcock deal for nuclear submarines", "[C]", False),
    ("Five European nations buy 430 CV90 combat vehicles", "[C]", False),
    ("Houthi claim strike on Ras Tanura refinery [CL] · 25 Nov", "[CL]", False),
    ("Myanmar rejects parts of ICJ genocide ruling", "[C]", False),
]

DATE_CHECK = [
    "DATE CHECK — NOT 26 NOV:  COP31 failed, no deal — 22 Nov  ·  "
    "Shenzhou-24 launched — 25 Nov  ·  Cairo tanker blast, 31 killed — 25 Nov",
    "Cartagena hostages freed — 25 Nov  ·  Australia–Solomon pact — 25 Nov  ·  "
    "UK energy +26% — 25 Nov  ·  Huawei convicted — 24 Nov",
]

# ---- world map: rough lon/lat outlines (equirectangular) ----
N_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
             (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
             (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
             (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-81, 13), (-84, 16),
             (-87, 21), (-90, 21), (-91, 19), (-96, 19), (-97, 26),
             (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
             (-76, 35), (-74, 40), (-70, 42), (-68, 44), (-65, 44),
             (-60, 47), (-55, 47), (-60, 50), (-65, 50), (-68, 52),
             (-60, 55), (-65, 58), (-68, 58), (-72, 62), (-78, 62),
             (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70),
             (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-25, 76), (-35, 78), (-50, 76),
             (-58, 74), (-60, 70)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
             (-72, -18), (-70, -23), (-70, -30), (-73, -37), (-73, -44),
             (-74, -50), (-70, -54), (-66, -55), (-68, -50), (-65, -45),
             (-62, -41), (-58, -38), (-52, -33), (-48, -28), (-41, -23),
             (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0),
             (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-75, 10)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
          (-2, 49), (0, 50), (2, 51), (4, 52), (7, 54), (8, 57), (10, 59),
          (5, 60), (5, 62), (10, 64), (13, 66), (18, 69), (25, 71),
          (30, 70), (32, 68), (36, 66), (38, 64), (36, 60), (34, 56),
          (32, 54), (30, 52), (28, 50), (30, 48), (32, 46), (30, 44),
          (28, 44), (27, 42), (25, 40), (23, 38), (22, 37), (24, 36),
          (26, 38), (28, 40), (30, 41), (32, 41), (30, 41), (28, 41),
          (27, 40), (26, 39), (23, 36), (21, 38), (19, 40), (16, 38),
          (15, 40), (12, 42), (10, 44), (8, 44), (6, 43), (3, 42),
          (0, 40), (-2, 37), (-6, 36), (-9, 37)]
# Eastern Europe / western Russia: extends Europe east to lon ~48.
E_EUROPE = [(28, 50), (34, 52), (38, 54), (43, 55), (48, 58), (48, 62),
            (45, 66), (40, 68), (34, 68), (30, 68), (28, 64), (28, 58),
            (29, 54)]
ASIA = [(28, 41), (30, 42), (33, 44), (36, 45), (39, 47), (42, 47),
        (46, 47), (49, 46), (51, 44), (54, 42), (58, 40), (60, 38),
        (63, 37), (66, 37), (68, 38), (70, 40), (73, 42), (76, 44),
        (80, 45), (84, 47), (88, 48), (92, 49), (96, 50), (100, 52),
        (104, 53), (108, 54), (112, 55), (116, 55), (120, 56), (124, 56),
        (128, 56), (132, 57), (136, 58), (140, 59), (144, 60), (148, 60),
        (152, 60), (156, 59), (160, 60), (162, 62), (162, 65), (160, 67),
        (158, 69), (162, 68), (170, 66), (178, 65), (179, 64), (176, 61),
        (170, 60), (162, 56), (158, 52), (156, 50), (150, 46), (142, 44),
        (140, 40), (138, 38), (135, 34), (132, 33), (129, 31), (127, 30),
        (126, 28), (124, 26), (122, 24), (120, 22), (118, 20), (116, 18),
        (114, 16), (112, 14), (110, 12), (108, 10), (106, 8), (105, 6),
        (104, 4), (103, 2), (101, 1), (100, 3), (99, 6), (98, 9), (97, 12),
        (96, 15), (94, 17), (92, 18), (91, 21), (89, 22), (88, 21),
        (86, 20), (84, 19), (82, 17), (80, 15), (79, 13), (78, 10),
        (77, 8), (76, 10), (74, 13), (72, 16), (70, 19), (68, 22),
        (66, 24), (64, 25), (62, 25), (60, 25), (58, 26), (56, 27),
        (54, 27), (52, 28), (50, 29), (49, 30), (48, 30), (48, 29),
        (50, 27), (52, 25), (54, 24), (56, 22), (58, 20), (57, 18),
        (55, 17), (52, 15), (50, 14), (48, 13), (45, 12), (43, 12),
        (42, 14), (41, 16), (40, 18), (39, 20), (38, 22), (37, 24),
        (36, 26), (35, 28), (34, 29), (35, 31), (36, 33), (35, 35),
        (34, 36), (33, 36), (32, 36), (30, 36), (28, 38), (27, 40)]
CHUKOTKA = [(-179, 65), (-170, 66), (-168, 64), (-170, 60), (-178, 62)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
          (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, 0),
          (12, -4), (13, -10), (12, -15), (13, -20), (12, -25), (14, -30),
          (18, -33), (20, -35), (25, -34), (28, -33), (32, -29), (35, -25),
          (36, -20), (40, -16), (40, -11), (41, -5), (42, -1), (44, 2),
          (46, 5), (48, 10), (51, 11), (48, 11), (44, 10), (42, 12),
          (40, 14), (39, 18), (38, 20), (37, 22), (36, 25), (35, 28),
          (33, 30), (31, 31), (29, 31), (26, 32), (22, 33), (18, 34),
          (15, 34), (11, 34), (10, 35), (8, 35), (5, 36), (0, 36), (-3, 35)]
AUSTRALIA = [(114, -22), (114, -30), (115, -34), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (151, -24),
             (149, -20), (146, -19), (143, -15), (142, -11), (141, -13),
             (139, -17), (136, -15), (135, -12), (132, -11), (130, -13),
             (126, -14), (122, -17), (118, -20)]
SUMATRA = [(95, 5), (97, 3), (99, 0), (101, -2), (103, -4), (105, -5),
           (106, -6), (104, -5), (102, -3), (100, 0), (98, 3)]
JAVA_POLY = [(105, -5.5), (108, -6.5), (111, -7), (114, -7.5), (114, -8.5),
             (111, -8), (108, -7.5), (105, -6.5)]
BORNEO = [(109, 1), (111, 3), (113, 4), (116, 6), (118, 2), (117, -1),
          (115, -3), (112, -3), (110, -1)]
SULAWESI = [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -5),
            (120, -3)]
NEW_GUINEA = [(131, -1), (134, -2), (137, -3), (140, -4), (143, -5),
              (146, -6), (148, -8), (150, -10), (147, -8), (144, -6),
              (141, -4), (138, -2), (135, -1), (132, 0)]
PHILIPPINES = [(120, 18), (121, 16), (122, 14), (121, 11), (122, 9),
               (123, 10), (124, 12), (122, 16)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37),
         (141, 39), (142, 41), (143, 43), (141, 45), (140, 42), (139, 38),
         (137, 36), (135, 34), (133, 33), (131, 32)]
UK_ISLE = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (1, 51), (-2, 50)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (44, -25), (43, -21)]
NEW_ZEALAND = [(167, -45), (170, -42), (174, -39), (176, -38), (178, -37),
               (175, -40), (172, -43), (168, -46)]
CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, EUROPE, E_EUROPE, ASIA,
              CHUKOTKA, AFRICA, AUSTRALIA, SUMATRA, JAVA_POLY, BORNEO,
              SULAWESI, NEW_GUINEA, PHILIPPINES, JAPAN, UK_ISLE,
              MADAGASCAR, NEW_ZEALAND]

# pins: (lon, lat, label, dx, dy) — dx/dy shift the drawn circle (leader
# line points back to the true spot). Drawn centres must sit on land.
PINS = [
    (-74.0, 40.7, "NEW YORK — MACY'S PARADE", 10, -9),
    (57.8, 27.2, "HORMUZ — TANKER CLAIM", 0, 0),
    (34.5, 31.5, "GAZA — GAZA STRIKE", -9, 9),
    (30.5, 50.5, "KYIV — MISSILE STRIKE", -8, 9),
    (106.8, -6.6, "BOGOR — MINE FLOOD", 0, 0),
    (35.2, 31.8, "JERUSALEM — NETANYAHU CASE", 9, 9),
    (125.8, 39.0, "PYONGYANG — KIM TOUR", 0, 0),
    (-0.1, 51.5, "LONDON — MIGRATION", -6, -8),
    (37.6, 55.8, "MOSCOW — MILITARY BUDGET", 8, -8),
    (100.5, 13.8, "BANGKOK — DEPOT BLAST", 0, 0),
    (7.0, 50.9, "COLOGNE — SYNAGOGUE PLOT", 9, 8),
    (-77.0, 38.9, "WASHINGTON — FCC NOD", -10, 9),
]
PIN_R = 6


def project(lon, lat, ox, oy, s):
    return (ox + (lon + 180.0) * s, oy + (80.0 - lat) * s)


# ---- hero art (drawn on separate layers, clipped to their boxes) ----
def art_macys(box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(h):  # sky gradient
        t = i / max(1, h - 1)
        d.line([(0, i), (w, i)],
               fill=(int(168 + 40 * t), int(198 + 30 * t), int(228 - 20 * t), 255))
    d.ellipse([w * 0.62, 8, w * 0.78, 30], fill=(255, 255, 255, 220))
    d.ellipse([w * 0.70, 14, w * 0.88, 34], fill=(255, 255, 255, 200))
    d.ellipse([w * 0.06, 18, w * 0.20, 36], fill=(255, 255, 255, 190))
    # buildings
    for bx, bw, bh in [(0, 52, 46), (56, 44, 62), (104, 56, 40),
                       (164, 48, 56), (216, 52, 44), (272, 46, 60),
                       (322, 58, 42)]:
        d.rectangle([bx, h - bh, bx + bw, h], fill=(52, 58, 74, 255))
        for wy in range(h - bh + 8, h - 6, 12):
            for wx in range(bx + 8, bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 5, wy + 6], fill=(240, 210, 110, 255))
    # balloon 1 (red/blue)
    cx, cy, rx, ry = int(w * 0.34), int(h * 0.48), 52, 54
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(181, 52, 42, 255))
    d.ellipse([cx - rx + 18, cy - ry, cx + rx - 18, cy + ry],
              fill=(250, 247, 238, 255))
    d.ellipse([cx - 12, cy - ry, cx + 12, cy + ry], fill=(27, 42, 74, 255))
    d.polygon([(cx - 16, cy + ry - 4), (cx + 16, cy + ry - 4),
               (cx + 8, cy + ry + 14), (cx - 8, cy + ry + 14)],
              fill=(120, 84, 40, 255))
    # balloon 2 (teal, smaller, right)
    cx2, cy2, rx2, ry2 = int(w * 0.80), int(h * 0.36), 34, 40
    d.ellipse([cx2 - rx2, cy2 - ry2, cx2 + rx2, cy2 + ry2],
              fill=(14, 107, 107, 255))
    d.ellipse([cx2 - 8, cy2 - ry2, cx2 + 8, cy2 + ry2],
              fill=(250, 247, 238, 255))
    d.polygon([(cx2 - 10, cy2 + ry2 - 2), (cx2 + 10, cy2 + ry2 - 2),
               (cx2 + 5, cy2 + ry2 + 11), (cx2 - 5, cy2 + ry2 + 11)],
              fill=(120, 84, 40, 255))
    # confetti
    for px, py, c in [(30, 70, RED), (120, 26, GOLD), (210, 60, TEAL),
                      (300, 90, RED), (90, 96, GOLD), (250, 30, (27, 42, 74))]:
        d.rectangle([px, py, px + 5, py + 5], fill=c + (255,))
    return lay


def art_tanker(box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(h):  # dusk sky -> sea
        t = i / max(1, h - 1)
        if t < 0.45:
            d.line([(0, i), (w, i)],
                   fill=(int(214 - 60 * t), int(148 - 40 * t), int(92 - 10 * t), 255))
        else:
            u = (t - 0.45) / 0.55
            d.line([(0, i), (w, i)],
                   fill=(int(52 - 20 * u), int(96 - 30 * u), int(128 - 30 * u), 255))
    horizon = int(h * 0.45)
    # smoke
    for sx, sy, sr in [(w * 0.30, 22, 16), (w * 0.36, 12, 20),
                       (w * 0.44, 20, 14)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 90, 200))
    # tanker hull + superstructure
    d.polygon([(8, horizon + 26), (w - 8, horizon + 26), (w - 22, horizon + 44),
               (22, horizon + 44)], fill=(30, 30, 34, 255))
    d.rectangle([w * 0.58, horizon + 2, w * 0.78, horizon + 26],
                fill=(240, 240, 235, 255))
    d.rectangle([w * 0.60, horizon + 8, w * 0.76, horizon + 13],
                fill=(27, 42, 74, 255))
    # containers
    for i, cc in enumerate([(181, 52, 42), (14, 107, 107), (227, 181, 5)]):
        d.rectangle([14 + i * 26, horizon + 10, 36 + i * 26, horizon + 26],
                    fill=cc + (255,))
    # flames
    fx = int(w * 0.30)
    d.polygon([(fx - 22, horizon + 26), (fx - 8, horizon - 6), (fx, horizon - 18),
               (fx + 10, horizon - 2), (fx + 22, horizon + 26)],
              fill=(235, 120, 20, 255))
    d.polygon([(fx - 12, horizon + 26), (fx - 3, horizon + 4), (fx + 4, horizon - 6),
               (fx + 12, horizon + 26)], fill=(250, 210, 60, 255))
    # mine in water
    mx, my = int(w * 0.86), int(h * 0.82)
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(20, 20, 20, 255))
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 13
        dy = math.sin(math.radians(ang)) * 13
        d.line([(mx, my), (mx + dx, my + dy)], fill=(20, 20, 20, 255), width=2)
    # waves
    for wy in (h - 18, h - 10):
        for wx in range(0, w, 26):
            d.arc([wx, wy, wx + 24, wy + 10], 180, 360,
                  fill=(255, 255, 255, 160), width=2)
    return lay


def art_chart(box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, w, h], fill=(232, 240, 235, 255))
    for gy in range(12, h, 22):
        d.line([(0, gy), (w, gy)], fill=(190, 200, 195, 255), width=1)
    # bars
    vals = [0.30, 0.24, 0.34, 0.28, 0.44, 0.40, 0.58, 0.52, 0.72, 0.86]
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = v * (h - 34)
        d.rectangle([i * bw + 3, h - 22 - bh, (i + 1) * bw - 3, h - 22],
                    fill=(27, 42, 74, 255) if i < 7 else (14, 107, 107, 255))
    # rising line
    pts = [(i * bw + bw / 2, h - 22 - v * (h - 34)) for i, v in enumerate(vals)]
    d.line(pts, fill=(181, 52, 42, 255), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(181, 52, 42, 255))
    # arrow head at last point
    ex, ey = pts[-1]
    d.polygon([(ex - 2, ey + 2), (ex + 10, ey - 8), (ex + 2, ey + 8)],
              fill=(181, 52, 42, 255))
    # containers bottom-left
    for i, cc in enumerate([(227, 181, 5), (181, 52, 42)]):
        d.rectangle([6 + i * 20, h - 20, 22 + i * 20, h - 6], fill=cc + (255,))
    return lay

# ---- layout ----
M = 16
CONTENT_R = 1008


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)

    # ===== masthead (0..48) =====
    d.rectangle([0, 0, W, 48], fill=NAVY)
    d.rectangle([0, 48, W, 51], fill=GOLD)
    draw_lines(d, M, 8, ["THE WORLD IN ONE DAY"], F(30, True), CREAM, 34,
               (0, 0, W, 48), "masthead-title")
    r1 = "THURSDAY · 26 NOVEMBER 2026"
    r2 = "50 STORIES · 10 REGIONS"
    w1 = d.textlength(r1, font=F(14, True))
    w2 = d.textlength(r2, font=F(11, True))
    draw_lines(d, CONTENT_R - w1, 7, [r1], F(14, True), CREAM, 17,
               (0, 0, W, 48), "masthead-date")
    draw_lines(d, CONTENT_R - w2, 26, [r2], F(11, True), GOLD, 14,
               (0, 0, W, 48), "masthead-count")

    # ===== DATE CHECK strip (52..90) =====
    d.rectangle([M, 52, CONTENT_R, 90], fill=GOLD)
    y = 55
    for ln in DATE_CHECK:
        draw_lines(d, M + 6, y, [ln], F(11, True), INK, 14,
                   (M, 52, CONTENT_R, 90), "datecheck")
        y += 15

    # ===== hero 1: Macy's banner (94..234) =====
    h1 = (M, 94, CONTENT_R, 234)
    d.rectangle(h1, fill=CARD_BG)
    d.rectangle([M, 94, CONTENT_R, 97], fill=RED)
    art1 = (M, 94, 396, 234)
    lay1 = art_macys(art1)
    img.paste(lay1, (art1[0], art1[1]), lay1)
    ART_RECTS.append(("hero1-art",) + art1)
    tx0, tx1 = 412, CONTENT_R
    draw_lines(d, tx0, 98, [HERO1["kicker"]], F(12, True), RED, 15,
               (tx0, 94, tx1, 234), "h1-kicker")
    draw_lines(d, tx0, 116, [HERO1["head"]], F(23, True), INK, 26,
               (tx0, 94, tx1, 234), "h1-head")
    deck1 = fit_lines(d, HERO1["deck"], F(13), tx1 - tx0 - 4, 2, "h1-deck")
    y = draw_lines(d, tx0, 145, deck1, F(13), INK, 16,
                   (tx0, 94, tx1, 234), "h1-deck")
    why1 = fit_lines(d, HERO1["why"], F(12), tx1 - tx0 - 4, 2, "h1-why")
    y = draw_lines(d, tx0, 180, why1, F(12), MUTED, 15,
                   (tx0, 94, tx1, 234), "h1-why")
    d.rectangle([tx0, 212, tx1, 230], fill=NAVY)
    sw = d.textlength(HERO1["stat"], font=F(11, True))
    draw_lines(d, tx0 + (tx1 - tx0 - sw) / 2, 214, [HERO1["stat"]],
               F(11, True), CREAM, 14, (tx0, 212, tx1, 230), "h1-stat")

    # ===== heroes 2 + 3 (238..374) =====
    for hero, box, artfn in ((HERO2, (M, 238, 496, 374), art_tanker),
                             (HERO3, (528, 238, CONTENT_R, 374), art_chart)):
        d.rectangle(box, fill=CARD_BG)
        d.rectangle([box[0], 238, box[2], 241], fill=RED)
        ax0, ax1 = box[0], box[0] + 150
        art = (ax0, 238, ax1, 374)
        lay = artfn(art)
        img.paste(lay, (art[0], art[1]), lay)
        ART_RECTS.append(("hero-art",) + art)
        tx0, tx1 = ax1 + 16, box[2] - 8
        draw_lines(d, tx0, 243, [hero["kicker"]], F(11, True), RED, 14,
                   (tx0, 238, tx1, 374), "hero-kicker")
        head_lines = fit_lines(d, hero["head"], F(18, True), tx1 - tx0 - 4,
                               2, "hero-head")
        y = draw_lines(d, tx0, 257, head_lines, F(18, True), INK, 21,
                       (tx0, 238, tx1, 374), "hero-head")
        deck = fit_lines(d, hero["deck"], F(12), tx1 - tx0 - 4, 2, "hero-deck")
        y = draw_lines(d, tx0, 301, deck, F(12), INK, 14,
                       (tx0, 238, tx1, 374), "hero-deck")
        why = fit_lines(d, hero["why"], F(11), tx1 - tx0 - 4, 2, "hero-why")
        y = draw_lines(d, tx0, 331, why, F(11), MUTED, 13,
                       (tx0, 238, tx1, 374), "hero-why")
        d.rectangle([tx0, 358, tx1, 374], fill=NAVY)
        draw_lines(d, tx0 + 2, 360, [hero["stat"]], F(9, True), CREAM, 12,
                   (tx0, 358, tx1, 374), "hero-stat")

    # ===== cards 2x5 (378..586) =====
    card_w, card_h, gap = 192, 100, 8
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 5)
        cx = M + col * (card_w + gap)
        cy = 378 + row * (card_h + gap)
        box = (cx, cy, cx + card_w, cy + card_h)
        d.rectangle(box, fill=CARD_BG)
        d.rectangle([cx, cy, cx + card_w, cy + 3], fill=TEAL)
        # number badge top-right
        bx0, by0, bx1, by1 = cx + 168, cy + 6, cx + 190, cy + 28
        d.ellipse([bx0, by0, bx1, by1], fill=NAVY)
        num = "%02d" % (i + 1)
        nw = d.textlength(num, font=F(10, True))
        draw_lines(d, bx0 + (22 - nw) / 2, by0 + 4, [num], F(10, True),
                   CREAM, 12, (bx0, by0, bx1, by1), "card-badge")
        BADGE_RECTS.append((i + 1, bx0, by0, bx1, by1))
        draw_lines(d, cx + 8, cy + 8, [c["place"] + "  ·  " + c["tag"]],
                   F(10, True), RED, 13, box, "card-kicker")
        head = fit_lines(d, c["head"], F(12, True), card_w - 16, 2, "card-head")
        y = draw_lines(d, cx + 8, cy + 26, head, F(12, True), INK, 15,
                       box, "card-head")
        deck = fit_lines(d, c["deck"], F(10), card_w - 16, 2, "card-deck")
        deck_top = draw_lines(d, cx + 8, cy + 58, deck, F(10), INK, 12,
                              box, "card-deck")
        assert deck_top <= cy + 84, "card %d deck overflows" % (i + 1)
        draw_lines(d, cx + 8, cy + 84, [c["stat"]], F(10, True), TEAL, 12,
                   box, "card-stat")

    # ===== map panel (590..796) =====
    map_box = (M, 590, CONTENT_R, 796)
    d.rectangle(map_box, fill=CARD_BG)
    d.rectangle([M, 590, CONTENT_R, 593], fill=NAVY)
    sea = (M, 598, 560, 788)
    d.rectangle(sea, fill=SEA)
    md.rectangle(sea, fill=0)
    ox, oy, s = 16.0, 591.0, 1.51
    for poly in CONTINENTS:
        pts = [project(lon, lat, ox, oy, s) for lon, lat in poly]
        d.polygon(pts, fill=LAND)
        md.polygon(pts, fill=255)
    # Java drawn thick so it stays visible at this scale
    jx0, jy0 = project(105, -6, ox, oy, s)
    jx1, jy1 = project(114, -8, ox, oy, s)
    d.line([(jx0, jy0), (jx1, jy1)], fill=LAND, width=5)
    md.line([(jx0, jy0), (jx1, jy1)], fill=255, width=5)
    # pins
    pin_centres = []
    for n, (lon, lat, label, dx, dy) in enumerate(PINS, 1):
        px, py = project(lon, lat, ox, oy, s)
        cxp, cyp = px + dx, py + dy
        pin_centres.append((n, cxp, cyp))
        if dx or dy:
            d.line([(cxp, cyp), (px, py)], fill=MUTED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([cxp - PIN_R, cyp - PIN_R, cxp + PIN_R, cyp + PIN_R],
                  fill=RED, outline=(255, 255, 255), width=1)
        num = "%02d" % n
        nw = d.textlength(num, font=F(7, True))
        draw_lines(d, cxp - nw / 2, cyp - 5, [num], F(7, True), CREAM, 9,
                   (cxp - PIN_R, cyp - PIN_R, cxp + PIN_R, cyp + PIN_R),
                   "pin-%02d" % n)
    # map legend (right of map, inside panel)
    lx = 576
    draw_lines(d, lx, 598, ["MAP KEY — 12 PINS · 10 REGIONS"], F(11, True),
               NAVY, 14, (lx, 590, CONTENT_R, 796), "map-legend-head")
    for i, (lon, lat, label, dx, dy) in enumerate(PINS):
        col = i // 6
        row = i % 6
        x = lx + col * 216
        y = 622 + row * 30
        num = "%02d" % (i + 1)
        draw_lines(d, x, y, [num + "  " + label], F(10, True), INK, 13,
                   (x, y, x + 210, y + 13), "map-legend-%02d" % (i + 1))

    # ===== ALSO (800..972) =====
    also_box = (M, 800, CONTENT_R, 972)
    d.rectangle(also_box, fill=CARD_BG)
    d.rectangle([M, 800, CONTENT_R, 803], fill=GOLD)
    draw_lines(d, M + 8, 810, ["ALSO TODAY — 37 MORE STORIES"], F(12, True),
               NAVY, 14, also_box, "also-head")
    leg = "[C] CONFIRMED  ·  [R] REPORTED  ·  [CL] CLAIM"
    lw = d.textlength(leg, font=F(10, True))
    draw_lines(d, CONTENT_R - 8 - lw, 811, [leg], F(10, True), MUTED, 13,
               also_box, "also-legend")
    col_w, col_x = 320, [M + 8, 344, 672]
    for i, (text, tag, _sub) in enumerate(ALSO):
        disp = text if tag in text else text + " " + tag
        col = i // 13
        row = i % 13
        x = col_x[col]
        y = 826 + row * 11
        assert d.textlength(disp, font=F(9)) <= col_w, \
            "ALSO item too wide (%dpx): %r" % (d.textlength(disp, font=F(9)), disp)
        draw_lines(d, x, y, [disp], F(9), INK, 11,
                   (x, y, x + col_w, y + 12), "also-%02d" % (i + 1))

    # ===== footer (976..1024) =====
    d.rectangle([0, 976, W, H], fill=NAVY)
    draw_lines(d, M, 982,
               ["SOURCES: REUTERS · AP · BBC · CNN · XINHUA · NPR · ONS · "
                "UKMTO · FCC · KCNA"], F(11, True), CREAM, 14,
               (0, 976, W, H), "footer-sources")
    draw_lines(d, M, 1002,
               ["REGIONS: NORTH AMERICA · SOUTH AMERICA · EUROPE · MIDDLE EAST · "
                "AFRICA · EAST ASIA · SOUTHEAST ASIA · SOUTH ASIA · OCEANIA · "
                "CENTRAL ASIA — ALL STORIES 26 NOV 2026 UNLESS NOTED"],
               F(10), GOLD, 13, (0, 976, W, H), "footer-regions")

    # ===== asserts =====
    _assert_all(d, mask, pin_centres, map_box)
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    assert img.size == (1024, 1024), img.size
    assert size < 1024 * 1024, "entry.png %d bytes > 1 MiB" % size
    print("OK entry.png %d bytes 1024x1024" % size)
    return OUT


def _assert_all(d, mask, pin_centres, map_box):
    # 1. art vs text: zero overlap (incl. title)
    for tl, tx0, ty0, tx1, ty1 in TEXT_RECTS:
        for al, ax0, ay0, ax1, ay1 in ART_RECTS:
            assert not overlap((tx0, ty0, tx1, ty1), (ax0, ay0, ax1, ay1)), \
                "text %s overlaps art %s" % (tl, al)
    # 2. all text inside canvas, and no two text blocks overlap
    for tl, tx0, ty0, tx1, ty1 in TEXT_RECTS:
        assert 0 <= tx0 and ty0 >= 0 and tx1 <= W and ty1 <= H, \
            "text %s outside canvas" % tl
    for i in range(len(TEXT_RECTS)):
        for j in range(i + 1, len(TEXT_RECTS)):
            a, b = TEXT_RECTS[i], TEXT_RECTS[j]
            assert not overlap(a[1:], b[1:]), \
                "text overlap: %s vs %s" % (a[0], b[0])
    # 3. card deck vs badge: zero overlap
    for tl, tx0, ty0, tx1, ty1 in TEXT_RECTS:
        if tl == "card-deck":
            for no, bx0, by0, bx1, by1 in BADGE_RECTS:
                assert not overlap((tx0, ty0, tx1, ty1), (bx0, by0, bx1, by1)), \
                    "card deck overlaps badge %d" % no
    # 4. map panel vs cards/text: map box starts below the card rows
    assert map_box[1] >= 590
    # 5. ALSO rules
    assert len(ALSO) == 37, "ALSO count %d" % len(ALSO)
    for text, tag, _sub in ALSO:
        assert tag in ("[C]", "[R]", "[CL]"), "bad tag %s" % tag
        last = text.rstrip().split(" ")[-1].lower()
        assert last not in ("in", "on", "at", "of", "to"), \
            "ALSO ends with preposition: %r" % text
    assert sum(1 for _t, _g, s in ALSO if s) <= 2, "too many hero sub-facts"
    # 6. DATE CHECK: exact seven items by content, nothing extra
    dc = " ".join(DATE_CHECK)
    for need in ("COP31", "Shenzhou-24", "Cairo", "Cartagena", "Australia",
                 "+26%", "Huawei", "22 Nov", "24 Nov", "25 Nov"):
        assert need in dc, "DATE CHECK missing %r" % need
    for banned in ("Trump tariffs announced", "Ras Tanura", "Riyadh"):
        assert banned not in dc, "DATE CHECK must not contain %r" % banned
    # 7. story uniqueness + bans across the whole image text
    keys = [HERO1["key"], HERO2["key"], HERO3["key"]] + \
           [c["key"] for c in CARDS]
    assert len(keys) == len(set(keys)) == 13
    corpus = " ".join([HERO1["head"], HERO1["deck"], HERO1["why"],
                       HERO2["head"], HERO2["deck"], HERO2["why"],
                       HERO3["head"], HERO3["deck"], HERO3["why"]] +
                      [c["head"] + " " + c["deck"] for c in CARDS] +
                      [t for t, _g, _s in ALSO] + DATE_CHECK)
    assert "Bangchak" not in corpus, "Bangchak banned"
    assert "third senior Hamas" not in corpus.lower()
    assert "Khasab" not in HERO2["deck"], "hero 2 deck must not say Khasab"
    assert corpus.count("Ras Tanura") <= 1, "Ras Tanura max 1x"
    assert "Kryvyi Rih" in corpus and "Kyiv's Rih" not in corpus
    assert "grandmaster of politics" in corpus, "Kushner quote exact"
    assert "outflows" in corpus, "Bitcoin must say outflows"
    assert "inflow" not in corpus.lower().replace("outflows", "")
    # 8. map pins: on land pixels, spaced, inside panel
    for n, cxp, cyp in pin_centres:
        assert mask.getpixel((int(round(cxp)), int(round(cyp)))) == 255, \
            "pin %02d centre not on drawn land" % n
        assert (map_box[0] + 2 + PIN_R <= cxp <= 560 - 2 - PIN_R and
                map_box[1] + 2 + PIN_R <= cyp <= map_box[3] - 2 - PIN_R), \
            "pin %02d circle outside map panel" % n
    for i in range(len(pin_centres)):
        for j in range(i + 1, len(pin_centres)):
            dx = pin_centres[i][1] - pin_centres[j][1]
            dy = pin_centres[i][2] - pin_centres[j][2]
            dist = (dx * dx + dy * dy) ** 0.5
            assert dist >= 2 * PIN_R + 2, \
                "pins %02d/%02d too close: %.1fpx" % (pin_centres[i][0],
                                                     pin_centres[j][0], dist)
    assert len(PINS) == 12, "legend must list all 12 pins"
    print("ASSERTS PASS: text=%d art=%d pins=%d stories=%d" %
          (len(TEXT_RECTS), len(ART_RECTS), len(PINS),
           3 + len(CARDS) + len(ALSO)))


if __name__ == "__main__":
    render()
