from pathlib import Path

import numpy as np

from distributions import get_distribution_titles, get_generators
from plotting import draw_distribution_estimates


SIZES = [20, 60, 100]
SEED = 5
LAB_DIR = Path(__file__).resolve().parent
FIGURES_DIR = LAB_DIR / "figures"


def build_figures(generators, sizes):
    titles = get_distribution_titles()

    for index, (dist_name, generator) in enumerate(generators.items(), start=1):
        samples = [generator(n) for n in sizes]
        output_path = FIGURES_DIR / f"{index}_{dist_name.lower()}.png"
        draw_distribution_estimates(dist_name, titles[dist_name], samples, sizes, output_path)
        print(f"Сохранён график: {output_path}")


def main():
    rng = np.random.default_rng(SEED)
    generators = get_generators(rng)
    build_figures(generators, SIZES)


if __name__ == "__main__":
    main()
