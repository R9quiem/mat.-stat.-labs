import numpy as np
from scipy import stats


def get_generators(rng):
    return {
        "Нормальное": lambda n: rng.normal(0, 1, n),
        "Коши": lambda n: rng.standard_cauchy(n),
        "Лапласа": lambda n: rng.laplace(0, 1 / np.sqrt(2), n),
        "Пуассона": lambda n: rng.poisson(5, n),
        "Равномерное": lambda n: rng.uniform(-np.sqrt(3), np.sqrt(3), n)
    }


def calculate_theoretical_density(name, x):
    if name == "Нормальное":
        return stats.norm.pdf(x, loc=0, scale=1)
    if name == "Коши":
        return stats.cauchy.pdf(x, loc=0, scale=1)
    if name == "Лапласа":
        return stats.laplace.pdf(x, loc=0, scale=1 / np.sqrt(2))
    if name == "Равномерное":
        return stats.uniform.pdf(x, loc=-np.sqrt(3), scale=2 * np.sqrt(3))
    return None


def poisson_pmf(x):
    return stats.poisson.pmf(x, mu=5)