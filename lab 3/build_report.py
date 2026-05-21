from pathlib import Path

import numpy as np
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from distributions import get_distribution_titles, get_generators
from main import REPEATS, SEED, SIZES, build_figures, collect_outlier_table


LAB_DIR = Path(__file__).resolve().parent
REPORT_PATH = LAB_DIR / "3_lab_matstat.pdf"
FIGURES_DIR = LAB_DIR / "figures"
REPOSITORY_URL = "https://github.com/R9quiem/mat.-stat.-labs/tree/main/lab%203"

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
            "Отчет по лабораторной работе №3. Боксплот Тьюки и анализ выбросов",
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
        ("2.2 Боксплот Тьюки", "3"),
        ("3 Реализация", "3"),
        ("4 Результаты", "4"),
        ("5 Обсуждение", "6"),
        ("6 Вывод", "7"),
        ("7 Список литературы", "7"),
        ("8 Приложение", "7"),
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
            "Сгенерировать выборки объёмом n = 20 и n = 100 для каждого из пяти распределений. "
            "Для каждой выборки построить боксплот Тьюки. Экспериментально определить долю выбросов: "
            "для каждого распределения сгенерировать 1000 выборок заданного объёма, вычислить долю "
            "выбросов в каждой выборке и найти среднее значение.",
            styles,
        )
    )
    story.append(p("Цели и задачи:", styles, "ReportNormal"))
    story.append(
        p(
            "• научиться применять боксплот Тьюки для обработки и анализа одномерных распределений;<br/>"
            "• проанализировать, как размер выборки влияет на долю отсеиваемых аномальных значений.",
            styles,
        )
    )


def theory_section(story, styles):
    story.append(p("2 Теоретическая часть", styles, "ReportHeading"))
    story.append(p("2.1 Используемые распределения", styles, "ReportSubheading"))
    story.append(
        p(
            "В работе исследуются нормальное распределение N(0, 1), распределение Коши C(0, 1), "
            "распределение Лапласа L(0, 1/sqrt(2)), распределение Пуассона P(10) и равномерное "
            "распределение U(-sqrt(3), sqrt(3)).",
            styles,
        )
    )
    story.append(p("2.2 Боксплот Тьюки", styles, "ReportSubheading"))
    story.append(
        p(
            "Боксплот Тьюки строится по квартилям выборки. Пусть Q1 — первый квартиль, Q2 — медиана, "
            "Q3 — третий квартиль. Межквартильный размах определяется как IQR = Q3 - Q1. Границы "
            "допустимых значений задаются выражениями Q1 - 1.5 IQR и Q3 + 1.5 IQR. Значения, выходящие "
            "за эти границы, считаются выбросами.",
            styles,
        )
    )
    story.append(
        p(
            "Практическая доля выбросов в выборке объёма n вычисляется как отношение количества "
            "элементов, отмеченных правилом Тьюки как выбросы, к общему числу элементов выборки. "
            "В эксперименте эта доля усредняется по 1000 повторным генерациям.",
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
            "• calculate_tukey_boxplot(sample) — вычисляет квартили, межквартильный размах, границы "
            "Тьюки, усы и список выбросов;<br/>"
            "• calculate_outlier_share(sample) — вычисляет долю выбросов в одной выборке;<br/>"
            "• estimate_average_outlier_share(generator, n, repeats) — находит среднюю долю выбросов "
            "по 1000 повторным выборкам;<br/>"
            "• draw_boxplots(dist_name, samples, sizes, output_path) — строит и сохраняет боксплоты "
            "для выборок объёма n = 20 и n = 100;<br/>"
            "• main() — запускает эксперимент, печатает итоговую таблицу и сохраняет графики.",
            styles,
        )
    )


def make_result_table(outlier_table):
    rows = [["Распределение", "n = 20", "n = 100"]]
    for name, values in outlier_table.items():
        rows.append([name, f"{values[0]:.4f}", f"{values[1]:.4f}"])

    table = Table(rows, colWidths=[6.2 * cm, 4 * cm, 4 * cm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "TimesNewRoman"),
                ("FONTNAME", (0, 0), (-1, 0), "TimesNewRoman-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def results_section(story, styles, outlier_table):
    titles = get_distribution_titles()
    captions = {
        "Нормальное": "нормального распределения",
        "Коши": "распределения Коши",
        "Лапласа": "распределения Лапласа",
        "Пуассона": "распределения Пуассона",
        "Равномерное": "равномерного распределения",
    }
    story.append(p("4 Результаты", styles, "ReportHeading"))
    story.append(p("Таблица 1: Средняя доля выбросов по правилу Тьюки", styles, "Caption"))
    story.append(make_result_table(outlier_table))
    story.append(Spacer(1, 0.4 * cm))

    for index, (dist_name, title) in enumerate(titles.items(), start=1):
        story.append(p(f"4.{index} {title}", styles, "ReportSubheading"))
        image_path = FIGURES_DIR / f"{index}_{dist_name.lower()}.png"
        story.append(Image(str(image_path), width=15.6 * cm, height=7.5 * cm))
        story.append(p(f"Рис. {index}: Боксплоты для {captions[dist_name]}", styles, "Caption"))
        if index in (2, 4):
            story.append(PageBreak())


def discussion_section(story, styles):
    story.append(p("5 Обсуждение", styles, "ReportHeading"))
    story.append(
        p(
            "Наибольшая средняя доля выбросов наблюдается у распределения Коши: около 0.15 для обоих "
            "объёмов выборки. Это связано с тяжёлыми хвостами распределения: крайние значения появляются "
            "часто и регулярно попадают за границы Q1 - 1.5 IQR и Q3 + 1.5 IQR.",
            styles,
        )
    )
    story.append(
        p(
            "У распределения Лапласа доля выбросов меньше, чем у распределения Коши, но заметно выше, "
            "чем у нормального распределения. Это соответствует более резкому пику и более тяжёлым "
            "хвостам распределения Лапласа по сравнению с нормальным.",
            styles,
        )
    )
    story.append(
        p(
            "Для нормального и пуассоновского распределений при увеличении объёма выборки с 20 до 100 "
            "средняя доля выбросов уменьшается. Для равномерного распределения выбросы практически "
            "отсутствуют, поскольку распределение ограничено на конечном отрезке.",
            styles,
        )
    )
    story.append(
        p(
            "Полученные результаты показывают, что боксплот Тьюки хорошо выявляет распределения с "
            "тяжёлыми хвостами и позволяет наглядно сравнивать устойчивость выборок разных типов.",
            styles,
        )
    )


def conclusion_section(story, styles):
    story.append(p("6 Вывод", styles, "ReportHeading"))
    story.append(
        p(
            "В результате выполнения лабораторной работы были построены боксплоты Тьюки для выборок "
            "объёма n = 20 и n = 100, а также экспериментально оценена средняя доля выбросов для пяти "
            "распределений. Было установлено, что наибольшая доля выбросов характерна для распределения "
            "Коши, а наименьшая — для равномерного распределения.",
            styles,
        )
    )
    story.append(
        p(
            "Размер выборки влияет на устойчивость оценки доли выбросов, однако основное различие "
            "определяется видом распределения и поведением его хвостов. Поставленная цель работы "
            "достигнута.",
            styles,
        )
    )


def references_section(story, styles):
    story.append(p("7 Список литературы", styles, "ReportHeading"))
    story.append(
        p(
            "1. Тьюки Дж. Анализ результатов наблюдений. Разведочный анализ. — М.: Мир, 1981.<br/>"
            "2. Крамер Г. Математические методы статистики. — М.: Мир, 1975.<br/>"
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
    generators = get_generators(rng)
    outlier_table = collect_outlier_table(generators, SIZES, REPEATS)
    build_figures(generators, SIZES, SEED)

    doc = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="Отчет по лабораторной работе №3",
    )

    story = []
    title_page(story, styles)
    contents_page(story, styles)
    task_section(story, styles)
    theory_section(story, styles)
    implementation_section(story, styles)
    results_section(story, styles, outlier_table)
    discussion_section(story, styles)
    conclusion_section(story, styles)
    references_section(story, styles)
    appendix_section(story, styles)

    doc.build(story)
    return REPORT_PATH


if __name__ == "__main__":
    print(build_report())
