#!/usr/bin/env python3
"""Render the news-image-20261124 front page as a 1024x1024 PNG (PIL only).

What it draws, top to bottom: a "THE WORLD TODAY" masthead with a navy
date bar (Tuesday, 24 November 2026); a lead story on Ukraine sinking a
Russian warship off Libya; a 2x2 grid of secondary stories (Russia's
nuclear-armed satellite, Nvidia's CEO return and share surge, the US
states suing Musk's firms over Grok images, Russian strikes near Kyiv);
a full-width bottom story on the India-EU trade deal; and a footer
crediting Reuters, AP, Bloomberg, WSJ and CNN.

Output: entry.png, 1024x1024 RGB, saved next to this script. The layout
is drawn sequentially and each block returns its bottom y, so content
cannot overflow the canvas (the script prints the final content y).

Fonts: Noto Serif (Black/Bold) for headlines and the masthead, Noto Sans
(Bold/Regular) for kickers, decks and the footer, loaded from
/usr/share/fonts/truetype/noto/. Requires Pillow only; fully
deterministic — the same run always produces the same PNG bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 46
PAPER = (251, 248, 241)
INK = (26, 26, 26)
GRAY = (90, 86, 78)
RED = (155, 27, 30)
NAVY = (31, 58, 95)
TEAL = (15, 92, 92)
GOLD = (150, 105, 30)
LIGHT_RULE = (190, 184, 172)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

y = 44
# ---- masthead ----
d.text((W // 2, y), "THE WORLD TODAY", font=font("NotoSerif-Black.ttf", 60),
       fill=INK, anchor="ma")
y += 72
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 6
d.rectangle([(M, y), (W - M, y + 44)], fill=NAVY)
d.text((W // 2, y + 22), "TUESDAY,  24  NOVEMBER  2026",
       font=font("NotoSans-Bold.ttf", 25), fill=(255, 255, 255), anchor="mm")
y += 44 + 6
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 18

# ---- lead story ----
pill = font("NotoSans-Bold.ttf", 16)
pw = d.textlength("WAR AT SEA  ·  LIBYA", font=pill) + 26
d.rectangle([(M, y), (M + pw, y + 28)], fill=RED)
d.text((M + 13, y + 14), "WAR AT SEA  ·  LIBYA", font=pill,
       fill=(255, 255, 255), anchor="lm")
y += 40
y = draw_lines(d, wrap(d, "Ukraine sinks Russian warship off Libya in drone raid",
                       font("NotoSerif-Bold.ttf", 44), W - 2 * M),
               M, y, font("NotoSerif-Bold.ttf", 44), INK, 52)
y += 8
y = draw_lines(d, wrap(d, "Seven sea drones struck the corvette Merkury at Benghazi on "
                          "Sunday, Kyiv said, sinking one of Russia's newest warships and "
                          "hitting a cargo vessel it says carried weapons. President "
                          "Zelenskyy called the mission \u201cexemplary\u201d.",
                       font("NotoSans-Regular.ttf", 19), W - 2 * M),
               M, y, font("NotoSans-Regular.ttf", 19), (52, 50, 46), 27)
y += 14
d.line([(M, y), (W - M, y)], fill=LIGHT_RULE, width=2)
y += 16

# ---- secondary stories: 2x2 grid ----
def story_block(x, top, w, kicker, color, head, body):
    cy = top
    d.text((x, cy), kicker, font=font("NotoSans-Bold.ttf", 14), fill=color)
    cy += 22
    hf = font("NotoSerif-Bold.ttf", 26)
    cy = draw_lines(d, wrap(d, head, hf, w), x, cy, hf, INK, 31)
    cy += 6
    bf = font("NotoSans-Regular.ttf", 15)
    cy = draw_lines(d, wrap(d, body, bf, w), x, cy, bf, (52, 50, 46), 21)
    return cy

stories = [
    ("SPACE  ·  SECURITY", NAVY,
     "Russia may launch nuclear-armed satellite next month",
     "Western intelligence says Moscow has built a satellite, Sputnik-S, able to "
     "carry a nuclear warhead and could launch it as soon as December. The Kremlin "
     "denies the reports."),
    ("MARKETS  ·  TECH", TEAL,
     "Nvidia chief back; shares soar 31% in a day",
     "Jensen Huang was reinstated as Nvidia CEO 11 days after resigning, after "
     "President Trump pressed the board. Shares jumped 31%, adding about $950 "
     "billion; Asian markets rallied on Tuesday."),
    ("TECH  ·  LAW", RED,
     "Two US states sue Musk firms over Grok images",
     "Virginia and Oregon sued SpaceX and X, alleging Grok generated sexualised "
     "images of real people, including children \u2014 near 3 million in 11 days, "
     "a study cited in the suits says."),
    ("WAR  ·  UKRAINE", NAVY,
     "Russian strikes kill at least 14 near Kyiv",
     "Missiles and drones hit homes across the Kyiv region, killing at least 14 "
     "people and damaging 21 sites, Ukrainian officials said."),
]
col_w = (W - 2 * M - 28) // 2
for ri in range(2):
    top = y
    bottoms = []
    for ci in range(2):
        s = stories[ri * 2 + ci]
        bottoms.append(story_block(M + ci * (col_w + 28), top, col_w, *s))
    y = max(bottoms)
    if ri == 0:
        y += 18
        d.line([(M, y), (W - M, y)], fill=LIGHT_RULE, width=1)
        y += 18

y += 18
d.line([(M, y), (W - M, y)], fill=LIGHT_RULE, width=2)
y += 18

# ---- bottom full-width story ----
d.text((M, y), "TRADE  ·  DIPLOMACY", font=font("NotoSans-Bold.ttf", 14), fill=GOLD)
y += 22
hf = font("NotoSerif-Bold.ttf", 26)
y = draw_lines(d, wrap(d, "India and EU to sign landmark trade deal on 16 December",
                       hf, W - 2 * M), M, y, hf, INK, 31)
y += 6
bf = font("NotoSans-Regular.ttf", 15)
y = draw_lines(d, wrap(d, "New Delhi and the 27-nation bloc are expected to formally sign "
                          "their long-awaited free-trade agreement during Prime Minister "
                          "Modi's visit to Brussels, capping years of talks.",
                       bf, W - 2 * M), M, y, bf, (52, 50, 46), 21)
y += 14

# ---- footer ----
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 12
d.text((W // 2, y), "All stories reported on Tuesday, 24 November 2026  ·  Sources: Reuters, AP, Bloomberg, WSJ, CNN",
       font=font("NotoSans-Regular.ttf", 13), fill=GRAY, anchor="ma")
print("content bottom y:", y, "canvas:", H)

img.save("/home/hatch/workspace/makefun/news-image-20261124/repo/entry.png", "PNG", optimize=True)
print("saved")
