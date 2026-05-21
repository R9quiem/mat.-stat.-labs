import numpy as np


def calculate_tukey_boxplot(sample):
    sample = np.asarray(sample)
    q1, median, q3 = np.percentile(sample, [25, 50, 75])
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    lower_whisker = np.min(sample[sample >= lower_fence])
    upper_whisker = np.max(sample[sample <= upper_fence])
    outliers = sample[(sample < lower_fence) | (sample > upper_fence)]

    return {
        "q1": q1,
        "median": median,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
        "lower_whisker": lower_whisker,
        "upper_whisker": upper_whisker,
        "outliers": outliers,
    }


def calculate_outlier_share(sample):
    boxplot = calculate_tukey_boxplot(sample)
    return len(boxplot["outliers"]) / len(sample)


def estimate_average_outlier_share(generator, n, repeats):
    shares = []

    for _ in range(repeats):
        sample = generator(n)
        shares.append(calculate_outlier_share(sample))

    return float(np.mean(shares))
