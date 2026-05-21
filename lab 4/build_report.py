from pathlib import Path

import numpy as np
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from distributions import get_distribution_titles, get_generators
from main import FIGURES_DIR, SEED, SIZES, build_figures


LAB_DIR = Path(__file__).resolve().parent
REPORT_PATH = LAB_DIR / "4_lab_matstat.pdf"
REPOSITORY_URL = "https://github.com/R9quiem/mat.-stat.-labs/tree/main/lab%204"

FONT_REGULAR = r"C:\Windows\Fonts\times.ttf"
FONT_BOLD = r"C:\Windows\Fonts\timesbd.ttf"


def register_fonts():
    pdfmetrics.registerFont(TTFont("TimesNewRoman", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", FONT_BOLD))


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "ReportTitle",
            fontName="TimesNewRoman-Bold",
            fontSize=18,
            leading=23,
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            "ReportNormal",
            fontName="TimesNewRoman",
            fontSize=12,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            "ReportHeading",
            fontName="TimesNewRoman-Bold",
            fontSize=16,
            leading=20,
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "ReportSubheading",
            fontName="TimesNewRoman-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "Caption",
            fontName="TimesNewRoman",
            fontSize=11,
            leading=13,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "Center",
            fontName="TimesNewRoman",
            fontSize=12,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=7,
        )
    )
    return styles


def p(text, styles, style="ReportNormal"):
    return Paragraph(text, styles[style])


def title_page(story, styles):
    story.append(Spacer(1, 1.2 * cm))
    story.append(p("Санкт-Петербургский", styles, "ReportTitle"))
    story.append(p("Политехнический университет Петра Великого", styles, "ReportTitle"))
    story.append(Spacer(1, 1.6 * cm))
    story.append(
        p(
            "Отчет по лабораторной работе №4. Эмпирическая функция распределения и ядерные оценки плотности",
            styles,
            "ReportTitle",
        )
    )
    story.append(Spacer(1, 4.0 * cm))
    story.append(p("Студент: Бурачевский Е.А.", styles, "Center"))
    story.append(p("Преподаватель: Баженов А.Н.", styles, "Center"))
    story.append(p("Группа: 5030102/30202", styles, "Center"))
    story.append(Spacer(1, 5.8 * cm))
    story.append(p("Санкт-Петербург", styles, "Center"))
    story.append(p("2025", styles, "Center"))
    story.append(PageBreak())


def contents_page(story, styles):
    story.append(p("Содержание", styles, "ReportHeading"))
    rows = [
        ("1 Формулировка задачи", "3"),
        ("2 Теоретическая часть", "3"),
        ("2.1 Используемые распределения", "3"),
        ("2.2 Эмпирическая функция распределения", "3"),
        ("2.3 Ядерная оценка плотности", "3"),
        ("3 Реализация", "4"),
        ("4 Результаты", "4"),
        ("5 Обсуждение", "7"),
        ("6 Вывод", "8"),
        ("7 Список литературы", "8"),
        ("8 Приложение", "8"),
    ]
    table = Table(rows, colWidths=[14 * cm, 1.2 * cm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "TimesNewRoman"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())


def task_section(story, styles):
    story.append(p("1 Формулировка задачи", styles, "ReportHeading"))
    story.append(
        p(
            "Сгенерировать выборки объёмом n = 20, 60, 100 для каждого из пяти распределений. "
            "Построить эмпирическую функцию распределения и теоретическую функцию распределения. "
            "Построить ядерную оценку плотности с гауссовым ядром и теоретическую плотность. "
            "Для непрерывных распределений построения выполнить на отрезке [-4, 4], для распределения "
            "Пуассона — на отрезке [6, 14].",
            styles,
        )
    )
    story.append(
        p(
            "Цель работы — исследовать, как мощность выборки влияет на приближение эмпирической "
            "функции к истинной функции распределения, а также сравнить ядерную оценку плотности "
            "с теоретической плотностью.",
            styles,
        )
    )


def theory_section(story, styles):
    story.append(p("2 Теоретическая часть", styles, "ReportHeading"))
    story.append(p("2.1 Используемые распределения", styles, "ReportSubheading"))
    story.append(
        p(
            "В работе рассматриваются нормальное распределение N(0, 1), распределение Коши C(0, 1), "
            "распределение Лапласа L(0, 1/sqrt(2)), распределение Пуассона P(10) и равномерное "
            "распределение U(-sqrt(3), sqrt(3)).",
            styles,
        )
    )
    story.append(p("2.2 Эмпирическая функция распределения", styles, "ReportSubheading"))
    story.append(
        p(
            "Эмпирическая функция распределения F_n(x) определяется как доля элементов выборки, "
            "не превосходящих x. Эта функция является ступенчатой и при увеличении объёма выборки "
            "сходится к истинной функции распределения F(x).",
            styles,
        )
    )
    story.append(p("2.3 Ядерная оценка плотности", styles, "ReportSubheading"))
    story.append(
        p(
            "Ядерная оценка плотности строит гладкое приближение плотности по выборке. В работе "
            "используется гауссово ядро. Ширина окна сглаживания выбрана по устойчивому варианту "
            "правила Сильвермана: она зависит от объёма выборки и робастной оценки масштаба. "
            "При росте n оценка обычно становится менее случайной и лучше повторяет форму истинной плотности.",
            styles,
        )
    )


def implementation_section(story, styles):
    story.append(p("3 Реализация", styles, "ReportHeading"))
    story.append(p("Используемый язык программирования: Python 3.12.", styles))
    story.append(p("Используемые библиотеки: numpy, Pillow, reportlab.", styles))
    story.append(p("Описание реализованных функций:", styles))
    story.append(
        p(
            "• get_generators(rng) — создаёт генераторы пяти исследуемых распределений;<br/>"
            "• theoretical_cdf(dist_name, x) — вычисляет теоретическую функцию распределения;<br/>"
            "• theoretical_pdf(dist_name, x) — вычисляет теоретическую плотность или вероятности "
            "для распределения Пуассона;<br/>"
            "• empirical_cdf(sample, grid) — вычисляет эмпирическую функцию распределения на сетке;<br/>"
            "• gaussian_kernel_density(sample, grid, bandwidth) — строит ядерную оценку плотности "
            "с гауссовым ядром;<br/>"
            "• draw_distribution_estimates(...) — сохраняет графики ЭФР и KDE для n = 20, 60, 100;<br/>"
            "• main() — запускает построение всех графиков.",
            styles,
        )
    )


def results_section(story, styles):
    titles = get_distribution_titles()
    captions = {
        "Нормальное": "нормального распределения",
        "Коши": "распределения Коши",
        "Лапласа": "распределения Лапласа",
        "Пуассона": "распределения Пуассона",
        "Равномерное": "равномерного распределения",
    }
    story.append(p("4 Результаты", styles, "ReportHeading"))
    for index, (dist_name, title) in enumerate(titles.items(), start=1):
        story.append(p(f"4.{index} {title}", styles, "ReportSubheading"))
        image_path = FIGURES_DIR / f"{index}_{dist_name.lower()}.png"
        story.append(Image(str(image_path), width=16.2 * cm, height=9.9 * cm))
        story.append(
            p(
                f"Рис. {index}: Эмпирическая функция распределения и ядерная оценка для {captions[dist_name]}",
                styles,
                "Caption",
            )
        )
        if index in (1, 2, 3):
            story.append(PageBreak())


def discussion_section(story, styles):
    story.append(p("5 Обсуждение", styles, "ReportHeading"))
    story.append(
        p(
            "Для всех распределений при увеличении объёма выборки эмпирическая функция распределения "
            "становится ближе к теоретической. При n = 20 ступенчатая оценка заметно зависит от "
            "случайного состава выборки, при n = 60 отличие уменьшается, а при n = 100 основные "
            "особенности теоретической функции уже хорошо воспроизводятся.",
            styles,
        )
    )
    story.append(
        p(
            "Ядерная оценка плотности сглаживает выборочные данные. Для нормального распределения, "
            "распределения Лапласа и равномерного распределения с ростом n форма оценки становится "
            "более устойчивой. Для распределения Коши результат сильнее зависит от хвостовых значений, "
            "поэтому отдельные выборки могут давать заметные отклонения даже при большем объёме.",
            styles,
        )
    )
    story.append(
        p(
            "Для распределения Пуассона теоретическая плотность представлена вероятностями в целых "
            "точках, а ядерная оценка является сглаженной непрерывной кривой. Поэтому она не повторяет "
            "ступенчатую дискретную структуру буквально, но передаёт положение центра и общий вид "
            "распределения на отрезке [6, 14].",
            styles,
        )
    )


def conclusion_section(story, styles):
    story.append(p("6 Вывод", styles, "ReportHeading"))
    story.append(
        p(
            "В ходе лабораторной работы были построены эмпирические функции распределения и ядерные "
            "оценки плотности для пяти распределений и трёх объёмов выборки. Было показано, что рост "
            "объёма выборки улучшает согласование эмпирической функции с теоретической, а ядерная "
            "оценка позволяет получить более гладкое приближение плотности, чем гистограмма.",
            styles,
        )
    )
    story.append(
        p(
            "Наиболее стабильные результаты получаются для распределений без тяжёлых хвостов. "
            "Для распределения Коши влияние отдельных больших наблюдений остаётся заметным. "
            "Поставленная цель работы достигнута.",
            styles,
        )
    )


def references_section(story, styles):
    story.append(p("7 Список литературы", styles, "ReportHeading"))
    story.append(
        p(
            "1. Крамер Г. Математические методы статистики. — М.: Мир, 1975.<br/>"
            "2. Вентцель Е.С. Теория вероятностей. — М.: Высшая школа, 1999.<br/>"
            "3. Документация NumPy: https://numpy.org/doc/",
            styles,
        )
    )


def appendix_section(story, styles):
    story.append(p("8 Приложение", styles, "ReportHeading"))
    story.append(
        p(
            f"Ссылка на репозиторий GitHub с исходным кодом программы: {REPOSITORY_URL}",
            styles,
        )
    )


def build_report():
    register_fonts()
    styles = make_styles()

    rng = np.random.default_rng(SEED)
    build_figures(get_generators(rng), SIZES)

    doc = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="Отчет по лабораторной работе №4",
    )

    story = []
    title_page(story, styles)
    contents_page(story, styles)
    task_section(story, styles)
    theory_section(story, styles)
    implementation_section(story, styles)
    results_section(story, styles)
    discussion_section(story, styles)
    conclusion_section(story, styles)
    references_section(story, styles)
    appendix_section(story, styles)

    doc.build(story)
    return REPORT_PATH


if __name__ == "__main__":
    print(build_report())
