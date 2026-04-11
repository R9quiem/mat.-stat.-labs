import numpy as np

from distributions import get_generators
from plotting import draw_distribution
from statistics_utils import calculate_location_statistics, summarize_statistics


SIZES = [10, 100, 1000]
REPEATS = 1000
SEED = 5


def build_report_table():
    return {
        "Выборочное среднее": [],
        "Медиана": [],
        "ZR": [],
        "ZQ": [],
        "Ztr": []
    }


def collect_estimates(generator, n, repeats):
    collected = {
        "mean": [],
        "median": [],
        "zR": [],
        "zQ": [],
        "ztr": []
    }

    for _ in range(repeats):
        sample = generator(n)
        stats = calculate_location_statistics(sample)
        for key in collected:
            collected[key].append(stats[key])

    return collected


def append_to_report(report_table, collected):
    report_table["Выборочное среднее"].append(summarize_statistics(collected["mean"]))
    report_table["Медиана"].append(summarize_statistics(collected["median"]))
    report_table["ZR"].append(summarize_statistics(collected["zR"]))
    report_table["ZQ"].append(summarize_statistics(collected["zQ"]))
    report_table["Ztr"].append(summarize_statistics(collected["ztr"]))


def print_report_table(dist_name, report_table):
    print(f"\nХарактеристики для {dist_name} распределения")
    print("-" * 75)
    print(f"{'Характеристика':<20} {'n=10':>15} {'n=100':>15} {'n=1000':>15}")
    print("-" * 75)

    for stat_name, triples in report_table.items():
        line = f"{stat_name:<20}"
        for mean_value, variance_value in triples:
            line += f"{f'{round(mean_value, 1)}±{round(np.sqrt(variance_value), 1)}':>15}"
        print(line)

    print("-" * 75)


def main():
    rng = np.random.default_rng(SEED)
    generators = get_generators(rng)

    for dist_name, generator in generators.items():
        report_table = build_report_table()

        for n in SIZES:
            collected = collect_estimates(generator, n, REPEATS)
            append_to_report(report_table, collected)

        print_report_table(dist_name, report_table)

        samples = [generator(n) for n in SIZES]
        draw_distribution(dist_name, samples, SIZES)


if __name__ == "__main__":
    main()