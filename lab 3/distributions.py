import numpy as np


def get_generators(rng):
    return {
        "Нормальное": lambda n: rng.normal(0, 1, n),
        "Коши": lambda n: rng.standard_cauchy(n),
        "Лапласа": lambda n: rng.laplace(0, 1 / np.sqrt(2), n),
        "Пуассона": lambda n: rng.poisson(10, n),
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
