import numpy as np


def calculate_bin_count(sample):
    sample = np.asarray(sample)
    n = sample.size

    if n < 2:
        return 1

    q1, q3 = np.percentile(sample, [25, 75])
    iqr = q3 - q1

    if iqr == 0:
        k = np.ceil(1 + np.log2(n))
    else:
        width = 2 * iqr / (n ** (1 / 3))
        if width <= 0:
            k = np.ceil(1 + np.log2(n))
        else:
            k = np.ceil((sample.max() - sample.min()) / width)

    k = int(k)
    k = max(2, k)
    k = min(k, 100)
    k = min(k, max(2, len(np.unique(sample))))
    return k


def trimmed_mean(sample, proportion=0.1):
    ordered = np.sort(sample)
    n = len(ordered)
    cut = int(proportion * n)
    trimmed = ordered[cut:n - cut]
    return np.mean(trimmed)


def calculate_location_statistics(sample):
    q1, q3 = np.percentile(sample, [25, 75])

    return {
        "mean": np.mean(sample),
        "median": np.median(sample),
        "zR": 0.5 * (np.min(sample) + np.max(sample)),
        "zQ": 0.5 * (q1 + q3),
        "ztr": trimmed_mean(sample)
    }


def summarize_statistics(values):
    arr = np.asarray(values)
    return np.mean(arr), np.var(arr, ddof=1)