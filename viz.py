import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from experiment import Experiment
from cache import ExperimentCache


def run_getter(n_boxes, n_checks, cache=None, n_iterations=1):
    exp = Experiment(n_boxes, n_checks, cache=cache)
    dist = exp.run(n_iterations=n_iterations)
    win_rate = dist[n_boxes] / n_iterations if n_boxes in dist else 0
    return dist, win_rate


def cache_getter(n_boxes, n_checks, cache=None):
    dist = cache.fetch(n_boxes, n_checks)
    win_rate = dist[n_boxes] / sum(dist.values()) if n_boxes in dist else 0
    return dist, win_rate


def grid_search(getter_func, boxes_opts, checks_opts, **kwargs):
    dist_grid = [[getter_func(n_boxes, n_checks, **kwargs)[0]
                 for n_checks in checks_opts] for n_boxes in boxes_opts]
    probas_grid = [[getter_func(n_boxes, n_checks, **kwargs)[1]
                   for n_checks in checks_opts] for n_boxes in boxes_opts]
    return dist_grid, probas_grid


def plot_dist(dist):
    all_n_finds = [n_finds for n_finds, count in dist.items()
                   for _ in range(count)]
    sns.distplot(all_n_finds, kde=False, bins=20)
    plt.show()


def plot_dist_grid(boxes_opts, checks_opts, dist_grid):
    samples = []
    for b, n_boxes in enumerate(boxes_opts):
        for c, n_checks in enumerate(checks_opts):
            dist = dist_grid[b][c]
            for n_finds, count in dist.items():
                for _ in range(count):
                    sample = {
                        'n_boxes': n_boxes,
                        'n_checks': n_checks,
                        'n_finds': n_finds
                    }
                    samples.append(sample)
    df = pd.DataFrame(samples)
    facet_grid = sns.FacetGrid(df, row='n_boxes', col='n_checks',
                               margin_titles=True)
    facet_grid.map(plt.hist, "n_finds", bins=20, color="#4CB391")
    plt.gcf().canvas.set_window_title('100 Prisoners Problem')
    plt.show()


def plot_contour(boxes_opts, checks_opts, probas_grid):
    plt.contourf(checks_opts, boxes_opts, probas_grid, 15,
                 cmap='Purples')
    plt.colorbar()
    plt.title('Probability space for finding your number')
    plt.xlabel('Number of checks allowed')
    plt.ylabel('Number of boxes/people')
    plt.gcf().canvas.set_window_title('100 Prisoners Problem')
    plt.show()


if __name__ == '__main__':
    sns.set()

    boxes_opts = np.linspace(80, 200, 10, dtype=int)
    checks_opts = np.linspace(10, 70, 6, dtype=int)

    cache = ExperimentCache('./cache.db')

    # Grid search by running many experiments
    # for every combination of parameters
    n_iterations = 100
    dist_grid, probas_grid = grid_search(run_getter, boxes_opts,
                                         checks_opts, cache=cache,
                                         n_iterations=n_iterations)

    # Grid search by pulling results from the cache
    # dist_grid, probas_grid = grid_search(cache_getter, boxes_opts,
    #                                      checks_opts, cache=cache)

    # dist = cache.fetch(100, 50)
    # p_win = dist[100] / sum(dist.values())
    # print(f"Probability of winning: {p_win}")
    # plot_dist(dist)

    plot_dist_grid(boxes_opts, checks_opts, dist_grid)
    plot_contour(boxes_opts, checks_opts, probas_grid)
