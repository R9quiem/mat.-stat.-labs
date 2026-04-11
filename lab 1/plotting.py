import numpy as np
import matplotlib.pyplot as plt

from distributions import calculate_theoretical_density, poisson_pmf
from statistics_utils import calculate_bin_count


def calculate_visible_range(sample, dist_name):
    if dist_name == "Коши":
        left, right = np.percentile(sample, [1, 99])
        return left, right
    return sample.min(), sample.max()


def draw_distribution(name, samples, sizes):
    fig, axes = plt.subplots(1, len(sizes), figsize=(16, 5))

    for ax, sample, n in zip(axes, samples, sizes):
        if name == "Пуассона":
            values, counts = np.unique(sample, return_counts=True)
            probs = counts / counts.sum()

            ax.bar(values, probs, width=0.75, alpha=0.8)

            x = np.arange(0, max(15, sample.max() + 3))
            y = poisson_pmf(x)
            ax.vlines(x, 0, y, linewidth=2)
            ax.scatter(x, y, zorder=3)
        else:
            left, right = calculate_visible_range(sample, name)
            bins = calculate_bin_count(sample)

            ax.hist(sample, bins=bins, range=(left, right), density=True, alpha=0.8)

            x = np.linspace(left, right, 800)
            y = calculate_theoretical_density(name, x)
            ax.plot(x, y, linewidth=2)

        ax.set_title(f"n = {n}")
        ax.set_xlabel("Значение")
        ax.set_ylabel("Плотность")
        ax.grid(alpha=0.3)

    fig.suptitle(f"{name} распределение")
    plt.tight_layout()
    plt.show()