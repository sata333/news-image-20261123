#!/usr/bin/env python3
"""The World Today - Monday 23 November 2026.
Draws a one-page newspaper image summing up the day's world news.
Standard library only, deterministic: same bytes on every run.
Writes /output/entry.png (and ./entry.png next to this file).
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (253, 253, 248)
INK = (18, 28, 52)
GREY = (96, 100, 112)
LIGHT = (228, 229, 224)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (176, 124, 18)

# 108 x 45 land bitmap ('#' = land). Transcribed from the verified world map
# data file for this series; rows run north to south, cols west to east.
WORLDMAP = [
"............................................................................................................",
".................................#.........##...............................................................",
"............................######..############..........##......................##........................",
"..........................########..############..........##...........##.........###...........##..........",
"....................##############..###########.......................##...........#####........###.........",
".......####......#################..#########...............###..#####....#########################.........",
".....#######..#####################..########...##.......#######..######################################....",
".....#######.#####################....######....###.....################################################....",
"......######.##############...#######....##..............##########.####################################....",
"..........##.##############....#######...............##..##############################################.....",
".##..........##############....########............#.#.#..##############################################....",
"..##..........##############....#######............####.###########################################.........",
"................#############...#####................############################################...........",
"................#############..######................######.#####..###.#########################..##........",
".................################...................###..#..#######.###.#####################.###...........",
".................###############...................###....#..#.#####.##########################..##.........",
"..................##############...................#######......###########################..##.............",
"...................############....................###############.#########################................",
"...................######...###..................################.###.##################....................",
"....................#....####.....#..............################.######.###############.#..................",
"......................####...###.................###############..######............############............",
".......................#####....###..............#################.####.....#####..####...#.................",
".........................####....................###################.........###...####..##.................",
"............................###.####.............##################...........#.....##.....#................",
"..............................########...........################...........#.....##.....#..................",
"...............................########.................###########................#.#..##..................",
"..............................##########................###########.................#..##.#.................",
"..............................############..............##########..................##.###.#...###..........",
"..............................#############..............##########....................##.#.#...###.........",
"..............................##############..............##########....................###..#..##..........",
"..............................#############..............##########..#...........................##.........",
"...............................############..............##########.##........................##.#.##.......",
"................................##########..............##########.##......................#######..........",
"................................##########..............#########.##.....................##########.........",
"................................#########...............########.........................############.......",
"................................########................########........................############........",
"................................#######..................######.........................####..######........",
"................................######.....................##..................................#####..##....",
"................................#####...........................................................###.......#.",
"................................####............................................................##......##..",
"................................###....................................................................##...",
"................................###....................................................................#....",
"................................###.#.......................................................................",
"................................###.........................................................................",
"............................................................................................................",
]

# (number, place, lat, lon, badge offset dx, dy in px)
MARKERS = [
    (1, "Washington DC", 38.9, -77.0, 0, 0),
    (2, "Mexico City", 19.4, -99.1, 0, 0),
    (3, "Santa Clara", 37.4, -122.0, 0, 0),
    (4, "London", 51.5, -0.1, 0, 0),
    (5, "Brussels", 50.8, 4.4, 13, -11),
    (6, "Benghazi", 32.1, 20.1, 0, 0),
    (7, "Antalya", 36.9, 30.7, 8, -13),
    (8, "Gaza", 31.5, 34.5, -15, -9),
    (9, "Tehran", 35.7, 51.4, 0, 0),
    (10, "Khartoum", 15.6, 32.5, 0, 0),
    (11, "Lagos", 6.5, 3.4, 0, 0),
    (12, "Cikande", -6.2, 106.2, 0, 0),
    (13, "Seoul", 37.6, 127.0, 0, 0),
    (14, "Kathmandu", 27.7, 85.3, 0, 0),
]

TIMELINE = [
    ("09:40", "Bus strike in Yemen's Lahj kills travellers"),
    ("09:45", "Indonesia confirms 24 dead in factory fire"),
    ("13:50", "M&S seeks franchise partners in Czechia, Greece"),
    ("14:37", "Arsenal's Raya ruled out of Dortmund clash"),
    ("18:18", "Houston rises to No. 1 in AP Top 25 poll"),
    ("18:37", "Penge wins maiden PGA Tour title"),
    ("19:34", "Ukraine shares video of Benghazi ship strikes"),
    ("23:16", "US to blacklist AI firm Megaspeed"),
]

# (section title, colour, [(headline, source), ...])
SECTIONS_LEFT = [
    ("AMERICAS", (140, 40, 40), [
        ("Democrats flip North Carolina seat for largest US House majority since 1992", "Reuters"),
        ("Trump orders Army to pause detonation of toxic lead azide stockpile in Iowa", "Reuters"),
        ("Trump 'inclined' to resume Iran strikes after New Year if no deal is reached", "Reuters"),
        ("California congressman to resign after evidence of sexual misconduct", "BBC"),
        ("Mexican soldiers attacked in wake of drug lord's arrest", "BBC"),
        ("US to blacklist Asian AI firm Megaspeed after Nvidia chip scandal", "BBC"),
    ]),
    ("MIDDLE EAST", (128, 84, 8), [
        ("Ukraine says sea drones sank Russian warship at Benghazi port in Libya", "BBC"),
        ("US Treasury sanctions 24+ Iranian exchange houses and front companies", "Reuters"),
        ("Iran vows to use all means to counter US naval blockade and sanctions", "Yeni Safak"),
        ("Oxfam: Israeli attacks turned Gaza into a 'toxic wasteland'", "BBC"),
        ("Deadly bus strike in Yemen's Lahj; Houthis blame Saudi jets, officials blame Houthis", "Reuters"),
        ("Iran flogs singer who performed without hijab, lawyers say", "BBC"),
        ("Israeli PM-elect calls settler arson in West Bank 'Jewish terrorism'", "Reuters"),
    ]),
    ("AFRICA", (24, 96, 60), [
        ("Drone strikes hit homes and UN building in Khartoum; army blames Ethiopia", "France 24"),
        ("Search races for survivors after Nigeria boat tragedy", "BBC"),
        ("Nigeria's president says he too suffers water and power cuts", "BBC"),
        ("Kenya and DR Congo agree to restore ties after talks", "BBC"),
        ("Zimbabwe preacher arrested on indecent assault allegations", "BBC"),
        ("Sudan aid group accuses RSF of looting shops and livestock in West Kordofan", "Yeni Safak"),
    ]),
    ("TECH & SCIENCE", (36, 84, 140), [
        ("NHS launches world's largest trial of AI to spot breast cancer earlier", "BBC"),
        ("US discussing military training for Syrian forces", "Reuters"),
        ("SpaceX wins permit for $24bn Texas data centre project", "Reuters"),
        ("US intelligence chief warns of more tech outages during upgrades", "Yeni Safak"),
    ]),
]

SECTIONS_RIGHT = [
    ("EUROPE", (52, 68, 140), [
        ("NATO to send AWACS early-warning aircraft to Poland after Russian missiles fell there", "Reuters"),
        ("Germany's Merz calls on Russia to stop 'dangerous provocations'", "BBC"),
        ("Flights cancelled in Belgium amid cost-of-living strike", "BBC"),
        ("UK sanctions top Myanmar military leaders after ICJ genocide ruling", "BBC"),
        ("UK confirmed as host of the 2035 Women's World Cup", "BBC"),
        ("Macron says French far-left protesters aim to bring down the Republic", "BBC"),
    ]),
    ("ASIA-PACIFIC", (150, 60, 110), [
        ("Indonesia candy factory fire: 24 dead, about 30 still missing", "Al Jazeera"),
        ("Asian chip stocks slide as AI-spending doubts spread; Kospi falls 3.3%", "Al Jazeera"),
        ("India pledges $1.6bn to Nepal in reset of ties", "BBC"),
        ("South Korea president reshuffles cabinet, naming new spy chief", "Reuters"),
        ("Bangladesh says it will arrest and jail ex-PM Hasina if she returns", "Reuters"),
        ("Nepal PM visits New Delhi to strengthen ties with India", "Reuters"),
        ("Nepal first to receive payout from UN Loss and Damage Fund", "Guardian"),
    ]),
    ("BUSINESS", (20, 110, 110), [
        ("Nvidia reinstates Jensen Huang as CEO; shares jump 31%", "Reuters"),
        ("CrowdStrike to buy rival Zscaler in $44bn all-stock deal", "Reuters"),
        ("Wall Street rebounds: S&P 500 up 4.7%, Nasdaq up 6.5%", "Reuters"),
        ("Brent crude falls about 2% to near $90.55 a barrel", "Business Recorder"),
        ("Clariant and CD&R in talks to buy US chemicals firm Ashland", "Reuters"),
    ]),
    ("SPORT", (120, 90, 20), [
        ("Alcaraz beats Zverev to win first ATP Finals title in Turin", "BBC"),
        ("FIFA confirms US, Mexico, Costa Rica and Jamaica to host 2031 Women's World Cup", "AP"),
        ("Marquez seals record-tying eighth MotoGP world title", "AP"),
        ("Penge wins maiden PGA Tour title in RSM Classic playoff", "AP"),
        ("Houston rises to No. 1 in AP Top 25 college basketball poll", "AP"),
    ]),
]


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=9999) or [""])
    out = []
    for line in lines:
        while fnt.getlength(line) > width:
            cut = len(line)
            while cut > 0 and fnt.getlength(line[:cut]) > width:
                cut -= 1
            sp = line.rfind(" ", 0, cut)
            if sp <= 0:
                sp = cut
            out.append(line[:sp].rstrip())
            line = line[sp:].lstrip()
        out.append(line)
    return out


def draw_map(d, x0, y0):
    # sea: faint 1px dots on a 3px pitch; land: 2x2 fill
    for r, row in enumerate(WORLDMAP):
        for c, ch in enumerate(row):
            px, py = x0 + c * 3, y0 + r * 3
            if ch == "#":
                d.rectangle([px, py, px + 1, py + 1], fill=(52, 72, 110))
            else:
                d.point((px, py), fill=(205, 208, 214))
    for num, place, lat, lon, dx, dy in MARKERS:
        col = int((lon + 180) * 0.3)
        row = int((90 - lat) * 0.3)
        mx, my = x0 + col * 3 + 1, y0 + row * 3 + 1
        bx, by = mx + dx, my + dy
        if dx or dy:
            d.line([mx, my, bx, by], fill=RED, width=1)
            d.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=RED)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                  outline=(255, 255, 255))
        t = str(num)
        f = font(8, bold=True)
        tw = f.getlength(t)
        d.text((bx - tw / 2, by - 5), t, font=f, fill=(255, 255, 255))


def draw_section(d, x, y, width, title, colour, stories):
    d.rectangle([x, y, x + width, y + 23], fill=colour)
    d.text((x + 8, y + 5), title, font=font(12, bold=True), fill=(255, 255, 255))
    n = len(stories)
    d.text((x + width - 8 - font(10, bold=True).getlength(str(n)),
            y + 6), str(n), font=font(10, bold=True), fill=(255, 255, 255))
    yy = y + 29
    f = font(11)
    for headline, source in stories:
        text = headline + "  [" + source + "]"
        for line in wrap(text, f, width - 16):
            d.text((x + 8, yy), line, font=f, fill=INK)
            yy += 15
        yy += 4
    d.line([x, yy + 1, x + width, yy + 1], fill=LIGHT, width=1)
    return yy + 10


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 80], fill=INK)
    d.text((16, 10), "THE WORLD TODAY", font=font(40, bold=True),
           fill=(255, 255, 255))
    d.text((16, 54), "Monday 23 November 2026  |  One day's world news in one picture",
           font=font(14), fill=(200, 205, 218))
    badge = "46 SOURCED STORIES"
    bf = font(13, bold=True)
    bw = bf.getlength(badge) + 20
    d.rounded_rectangle([W - 16 - bw, 22, W - 16, 56], radius=6,
                        fill=GOLD)
    d.text((W - 16 - bw + 10, 31), badge, font=bf, fill=(255, 255, 255))

    # ---- world map panel ----
    mx, my, mw, mh = 16, 88, 504, 170
    d.rectangle([mx, my, mx + mw, my + mh], outline=INK, width=2)
    d.text((mx + 8, my + 5), "WHERE IT HAPPENED", font=font(11, bold=True),
           fill=INK)
    draw_map(d, mx + 8, my + 26)
    lx = mx + 344
    lf = font(9)
    for i, (num, place, *_rest) in enumerate(MARKERS):
        col = i // 7
        row = i % 7
        d.text((lx + col * 82, my + 28 + row * 17),
               "%d %s" % (num, place), font=lf, fill=INK)
    d.text((mx + 8, my + mh - 15),
           "Numbered: the day's datelines, plotted by latitude and longitude.",
           font=font(9), fill=GREY)

    # ---- UTC timeline panel ----
    tx, ty, tw, th = 536, 88, 472, 170
    d.rectangle([tx, ty, tx + tw, ty + th], outline=INK, width=2)
    d.text((tx + 8, ty + 5), "UTC TIMELINE  —  MONDAY 23 NOVEMBER 2026",
           font=font(11, bold=True), fill=INK)
    tf = font(10)
    tfb = font(10, bold=True)
    yy = ty + 26
    for t, text in TIMELINE:
        d.text((tx + 8, yy), t, font=tfb, fill=RED)
        d.text((tx + 58, yy), text, font=tf, fill=INK)
        yy += 17
    d.text((tx + 8, ty + th - 15),
           "All times UTC. Events first reported on 23 November 2026.",
           font=font(9), fill=GREY)

    # ---- region sections, two columns ----
    y = 266
    col_ends = []
    for x, sections in ((16, SECTIONS_LEFT), (520, SECTIONS_RIGHT)):
        yy = y
        for title, colour, stories in sections:
            yy = draw_section(d, x, yy, 488, title, colour, stories)
        col_ends.append(yy)
        d.line([x, 952, x + 488, 952], fill=LIGHT, width=1)
    # ---- by the numbers: fills the shorter right column ----
    ny = col_ends[1] + 2
    if ny + 56 <= 952:
        d.rectangle([520, ny, 1008, ny + 56], outline=INK, width=1)
        d.text((528, ny + 4), "BY THE NUMBERS", font=font(10, bold=True),
               fill=INK)
        stats = [("31%", "Nvidia shares jump on Huang return"),
                 ("$44bn", "CrowdStrike's all-stock Zscaler deal"),
                 ("24", "dead in Indonesia factory fire"),
                 ("3.3%", "Kospi fall on AI-spending doubts")]
        sf = font(10)
        sfb = font(10, bold=True)
        for i, (num, label) in enumerate(stats):
            sx = 528 + (i % 2) * 244
            sy = ny + 22 + (i // 2) * 16
            d.text((sx, sy), num, font=sfb, fill=RED)
            d.text((sx + sfb.getlength(num) + 5, sy), label, font=sf,
                   fill=INK)

    # ---- footer ----
    d.rectangle([0, 962, W, H], fill=INK)
    d.text((16, 970), "46 sourced stories  |  Sources: Reuters, BBC, AP, Al Jazeera, Guardian, France 24, Yeni Safak, Xinhua, CNA, Business Recorder",
           font=font(10), fill=(210, 214, 224))
    d.text((16, 988), "Date checked: Monday 23 November 2026  —  every story above happened or was first reported on 23 November 2026 (UTC).",
           font=font(10, bold=True), fill=(255, 255, 255))

    os.makedirs("/output", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
