import numpy as np
from pathlib import Path

from distributions import get_distribution_titles, get_generators
from plotting import draw_boxplots
from statistics_utils import estimate_average_outlier_share


SIZES = [20, 100]
REPEATS = 1000
SEED = 5
LAB_DIR = Path(__file__).resolve().parent
FIGURES_DIR = LAB_DIR / "figures"


def collect_outlier_table(generators, sizes, repeats):
    table = {}

    for dist_name, generator in generators.items():
        table[dist_name] = []
        for n in sizes:
            table[dist_name].append(estimate_average_outlier_share(generator, n, repeats))

    return table


def print_outlier_table(table, sizes):
    print("\nСредняя доля выбросов по правилу Тьюки")
    print("-" * 58)
    print(f"{'Распределение':<18} {f'n={sizes[0]}':>15} {f'n={sizes[1]}':>15}")
    print("-" * 58)

    for dist_name, values in table.items():
        print(f"{dist_name:<18} {values[0]:>14.4f} {values[1]:>15.4f}")

    print("-" * 58)


def build_figures(generators, sizes, seed):
    titles = get_distribution_titles()

    for index, (dist_name, generator) in enumerate(generators.items(), start=1):
        samples = [generator(n) for n in sizes]
        output_path = FIGURES_DIR / f"{index}_{dist_name.lower()}.png"
        draw_boxplots(titles[dist_name], samples, sizes, output_path)


def main():
    rng = np.random.default_rng(SEED)
    generators = get_generators(rng)

    outlier_table = collect_outlier_table(generators, SIZES, REPEATS)
    print_outlier_table(outlier_table, SIZES)
    build_figures(generators, SIZES, SEED)


if __name__ == "__main__":
    main()
