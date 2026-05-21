import math

import numpy as np


POISSON_LAMBDA = 10


def get_generators(rng):
    return {
        "Нормальное": lambda n: rng.normal(0, 1, n),
        "Коши": lambda n: rng.standard_cauchy(n),
        "Лапласа": lambda n: rng.laplace(0, 1 / np.sqrt(2), n),
        "Пуассона": lambda n: rng.poisson(POISSON_LAMBDA, n),
        "Равномерное": lambda n: rng.uniform(-np.sqrt(3), np.sqrt(3), n),
    }


def get_distribution_titles():
    return {
        "Нормальное": "Нормальное распределение",
        "Коши": "Распределение Коши",
        "Лапласа": "Распределение Лапласа",
        "Пуассона": "Распределение Пуассона",
        "Равномерное": "Равномерное распределение",
    }


def get_plot_interval(dist_name):
    if dist_name == "Пуассона":
        return 6.0, 14.0
    return -4.0, 4.0


def normal_pdf(x):
    return np.exp(-0.5 * x * x) / np.sqrt(2 * np.pi)


def normal_cdf(x):
    return 0.5 * (1 + np.vectorize(math.erf)(x / np.sqrt(2)))


def cauchy_pdf(x):
    return 1 / (np.pi * (1 + x * x))


def cauchy_cdf(x):
    return 0.5 + np.arctan(x) / np.pi


def laplace_pdf(x):
    return np.exp(-np.sqrt(2) * np.abs(x)) / np.sqrt(2)


def laplace_cdf(x):
    x = np.asarray(x)
    result = np.empty_like(x, dtype=float)
    left = x < 0
    result[left] = 0.5 * np.exp(np.sqrt(2) * x[left])
    result[~left] = 1 - 0.5 * np.exp(-np.sqrt(2) * x[~left])
    return result


def uniform_pdf(x):
    x = np.asarray(x)
    left, right = -np.sqrt(3), np.sqrt(3)
    return np.where((x >= left) & (x <= right), 1 / (2 * np.sqrt(3)), 0.0)


def uniform_cdf(x):
    x = np.asarray(x)
    left, right = -np.sqrt(3), np.sqrt(3)
    return np.where(x < left, 0.0, np.where(x > right, 1.0, (x - left) / (right - left)))


def poisson_pmf(k, lam=POISSON_LAMBDA):
    k = np.asarray(k)
    values = np.zeros_like(k, dtype=float)
    valid = k >= 0
    valid_k = k[valid].astype(int)
    values[valid] = np.exp(valid_k * np.log(lam) - lam - np.vectorize(math.lgamma)(valid_k + 1))
    return values


def poisson_cdf(x, lam=POISSON_LAMBDA):
    result = []
    for value in np.asarray(x):
        upper = int(math.floor(value))
        if upper < 0:
            result.append(0.0)
            continue
        ks = np.arange(0, upper + 1)
        result.append(float(np.sum(poisson_pmf(ks, lam))))
    return np.asarray(result)


def theoretical_pdf(dist_name, x):
    if dist_name == "Нормальное":
        return normal_pdf(x)
    if dist_name == "Коши":
        return cauchy_pdf(x)
    if dist_name == "Лапласа":
        return laplace_pdf(x)
    if dist_name == "Равномерное":
        return uniform_pdf(x)
    if dist_name == "Пуассона":
        return poisson_pmf(np.rint(x).astype(int))
    raise ValueError(f"Неизвестное распределение: {dist_name}")


def theoretical_cdf(dist_name, x):
    if dist_name == "Нормальное":
        return normal_cdf(x)
    if dist_name == "Коши":
        return cauchy_cdf(x)
    if dist_name == "Лапласа":
        return laplace_cdf(x)
    if dist_name == "Равномерное":
        return uniform_cdf(x)
    if dist_name == "Пуассона":
        return poisson_cdf(x)
    raise ValueError(f"Неизвестное распределение: {dist_name}")
