from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from distributions import get_plot_interval, poisson_pmf, theoretical_cdf, theoretical_pdf
from statistics_utils import empirical_cdf, gaussian_kernel_density


FONT_REGULAR = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def draw_polyline(draw, points, fill, width=3):
    if len(points) > 1:
        draw.line(points, fill=fill, width=width, joint="curve")


def draw_panel(draw, area, title, x_grid, y_values, reference, y_label, fonts, bars=None):
    x0, y0, x1, y1 = area
    pad_left, pad_right, pad_top, pad_bottom = 58, 16, 42, 42
    px0, py0 = x0 + pad_left, y0 + pad_top
    px1, py1 = x1 - pad_right, y1 - pad_bottom
    axis = (70, 70, 70)
    grid_color = (224, 228, 232)
    empirical_color = (31, 73, 125)
    theory_color = (175, 55, 65)
    text_color = (28, 28, 28)

    x_min, x_max = float(x_grid[0]), float(x_grid[-1])
    y_max = max(float(np.nanmax(y_values)), float(np.nanmax(reference)), 1e-6)
    if bars is not None:
        y_max = max(y_max, max(value for _, value in bars))
    y_max *= 1.12
    y_min = 0.0

    def sx(value):
        return px0 + (value - x_min) / (x_max - x_min) * (px1 - px0)

    def sy(value):
        return py1 - (value - y_min) / (y_max - y_min) * (py1 - py0)

    draw.rectangle((x0, y0, x1, y1), outline=(218, 218, 218), width=1)
    draw.text((x0 + 12, y0 + 9), title, fill=text_color, font=fonts["subtitle"])
    draw.text((x0 + 10, py0 - 2), y_label, fill=text_color, font=fonts["small"])

    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        yy = py1 - frac * (py1 - py0)
        draw.line((px0, yy, px1, yy), fill=grid_color, width=1)
        label = f"{y_min + frac * (y_max - y_min):.2f}"
        draw.text((x0 + 7, yy - 10), label, fill=text_color, font=fonts["tiny"])

    for tick in np.linspace(x_min, x_max, 5):
        xx = sx(tick)
        draw.line((xx, py0, xx, py1), fill=grid_color, width=1)
        label = f"{tick:.0f}" if abs(tick) >= 6 else f"{tick:.1f}"
        tw = draw.textlength(label, font=fonts["tiny"])
        draw.text((xx - tw / 2, py1 + 7), label, fill=text_color, font=fonts["tiny"])

    draw.line((px0, py1, px1, py1), fill=axis, width=2)
    draw.line((px0, py0, px0, py1), fill=axis, width=2)

    if bars is not None:
        step = (px1 - px0) / max(1, (x_max - x_min))
        for x_value, y_value in bars:
            xx = sx(x_value)
            draw.rectangle(
                (xx - step * 0.22, sy(y_value), xx + step * 0.22, py1),
                fill=(224, 166, 166),
                outline=theory_color,
            )
    else:
        reference_points = [(sx(x), sy(y)) for x, y in zip(x_grid, reference)]
        draw_polyline(draw, reference_points, theory_color, width=3)

    empirical_points = [(sx(x), sy(y)) for x, y in zip(x_grid, y_values)]
    draw_polyline(draw, empirical_points, empirical_color, width=3)

    draw.line((x1 - 145, y0 + 20, x1 - 115, y0 + 20), fill=empirical_color, width=4)
    draw.text((x1 - 108, y0 + 10), "оценка", fill=text_color, font=fonts["tiny"])
    draw.line((x1 - 145, y0 + 42, x1 - 115, y0 + 42), fill=theory_color, width=4)
    draw.text((x1 - 108, y0 + 32), "теория", fill=text_color, font=fonts["tiny"])


def draw_distribution_estimates(dist_name, title, samples, sizes, output_path):
    width, height = 1700, 1040
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    fonts = {
        "title": load_font(FONT_BOLD, 44),
        "subtitle": load_font(FONT_BOLD, 24),
        "small": load_font(FONT_REGULAR, 19),
        "tiny": load_font(FONT_REGULAR, 17),
    }

    draw.text((45, 28), title, fill=(20, 20, 20), font=fonts["title"])

    left, right = get_plot_interval(dist_name)
    x_grid = np.linspace(left, right, 360)
    theory_cdf = theoretical_cdf(dist_name, x_grid)
    theory_pdf = theoretical_pdf(dist_name, x_grid)
    poisson_bars = None
    if dist_name == "Пуассона":
        xs = np.arange(int(left), int(right) + 1)
        poisson_bars = list(zip(xs, poisson_pmf(xs)))

    panel_w, panel_h = 520, 385
    x_start, gap = 45, 25
    y_top, y_bottom = 120, 565

    for index, (sample, n) in enumerate(zip(samples, sizes)):
        x0 = x_start + index * (panel_w + gap)
        cdf = empirical_cdf(sample, x_grid)
        kde = gaussian_kernel_density(sample, x_grid)

        draw_panel(
            draw,
            (x0, y_top, x0 + panel_w, y_top + panel_h),
            f"ЭФР, n = {n}",
            x_grid,
            cdf,
            theory_cdf,
            "F(x)",
            fonts,
        )
        draw_panel(
            draw,
            (x0, y_bottom, x0 + panel_w, y_bottom + panel_h),
            f"KDE, n = {n}",
            x_grid,
            kde,
            theory_pdf,
            "f(x)",
            fonts,
            bars=poisson_bars,
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
