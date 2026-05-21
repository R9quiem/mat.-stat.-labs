import numpy as np


def empirical_cdf(sample, grid):
    sample = np.sort(np.asarray(sample))
    return np.searchsorted(sample, grid, side="right") / sample.size


def silverman_bandwidth(sample):
    sample = np.asarray(sample)
    n = sample.size
    std = np.std(sample, ddof=1)
    q1, q3 = np.percentile(sample, [25, 75])
    robust_sigma = min(std, (q3 - q1) / 1.34) if q3 > q1 else std

    if robust_sigma <= 0 or not np.isfinite(robust_sigma):
        robust_sigma = 1.0

    return 0.9 * robust_sigma * n ** (-1 / 5)


def gaussian_kernel_density(sample, grid, bandwidth=None):
    sample = np.asarray(sample)
    grid = np.asarray(grid)

    if bandwidth is None:
        bandwidth = silverman_bandwidth(sample)

    scaled = (grid[:, None] - sample[None, :]) / bandwidth
    kernels = np.exp(-0.5 * scaled * scaled) / np.sqrt(2 * np.pi)
    return kernels.mean(axis=1) / bandwidth
