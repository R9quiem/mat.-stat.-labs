import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from statistics_utils import calculate_tukey_boxplot


FONT_REGULAR = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def nice_ticks(left, right, count=5):
    if left == right:
        return [left]

    raw_step = (right - left) / max(1, count - 1)
    magnitude = 10 ** math.floor(math.log10(abs(raw_step)))
    candidates = [1, 2, 2.5, 5, 10]
    step = min(candidates, key=lambda value: abs(value * magnitude - raw_step)) * magnitude
    start = math.floor(left / step) * step
    ticks = []
    value = start

    while value <= right + step:
        if value >= left - step * 0.1:
            ticks.append(value)
        value += step

    return ticks[:7]


def draw_single_boxplot(draw, area, sample, label, fonts):
    x0, y0, x1, y1 = area
    box = calculate_tukey_boxplot(sample)
    sample = np.asarray(sample)

    if len(box["outliers"]) > 0:
        left = min(np.min(sample), box["lower_fence"])
        right = max(np.max(sample), box["upper_fence"])
    else:
        left = min(np.min(sample), box["lower_fence"])
        right = max(np.max(sample), box["upper_fence"])

    margin = 0.08 * (right - left if right != left else 1)
    left -= margin
    right += margin

    def sx(value):
        return x0 + (value - left) / (right - left) * (x1 - x0)

    center_y = (y0 + y1) // 2
    box_h = 82
    axis_y = y1 - 46
    text_color = (30, 30, 30)
    stroke = (30, 68, 110)
    fill = (196, 218, 239)
    accent = (165, 55, 65)
    grid = (215, 220, 226)

    draw.text((x0, y0 - 4), label, fill=text_color, font=fonts["subtitle"])
    draw.line((x0, axis_y, x1, axis_y), fill=(120, 120, 120), width=2)

    for tick in nice_ticks(left, right):
        tx = sx(tick)
        draw.line((tx, axis_y - 5, tx, axis_y + 5), fill=(80, 80, 80), width=1)
        draw.line((tx, y0 + 32, tx, axis_y), fill=grid, width=1)
        tick_text = f"{tick:.1f}" if abs(tick) < 10 else f"{tick:.0f}"
        tw = draw.textlength(tick_text, font=fonts["small"])
        draw.text((tx - tw / 2, axis_y + 8), tick_text, fill=text_color, font=fonts["small"])

    lw = sx(box["lower_whisker"])
    uw = sx(box["upper_whisker"])
    q1 = sx(box["q1"])
    med = sx(box["median"])
    q3 = sx(box["q3"])

    draw.line((lw, center_y, q1, center_y), fill=stroke, width=4)
    draw.line((q3, center_y, uw, center_y), fill=stroke, width=4)
    draw.line((lw, center_y - 32, lw, center_y + 32), fill=stroke, width=4)
    draw.line((uw, center_y - 32, uw, center_y + 32), fill=stroke, width=4)
    draw.rectangle((q1, center_y - box_h // 2, q3, center_y + box_h // 2), fill=fill, outline=stroke, width=4)
    draw.line((med, center_y - box_h // 2, med, center_y + box_h // 2), fill=accent, width=4)

    for value in box["outliers"]:
        ox = sx(value)
        draw.ellipse((ox - 4, center_y - 4, ox + 4, center_y + 4), fill=accent)


def draw_boxplots(dist_name, samples, sizes, output_path):
    width, height = 1500, 720
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    fonts = {
        "title": load_font(FONT_BOLD, 44),
        "subtitle": load_font(FONT_BOLD, 31),
        "small": load_font(FONT_REGULAR, 24),
    }

    draw.text((50, 32), dist_name, fill=(20, 20, 20), font=fonts["title"])

    top = 130
    panel_height = 250
    for index, (sample, n) in enumerate(zip(samples, sizes)):
        panel_top = top + index * panel_height
        draw_single_boxplot(
            draw,
            (95, panel_top + 35, width - 95, panel_top + 205),
            sample,
            f"n = {n}",
            fonts,
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
