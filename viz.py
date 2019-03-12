import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from experiment import Experiment
from cache import ExperimentCache


def grid_search(boxes_opts, checks_opts, n_iterations, cache=None):
    probas_grid = np.zeros((len(boxes_opts), len(checks_opts)))
    finds_grid = np.zeros((len(boxes_opts), len(checks_opts), n_iterations), dtype=int)
    for b, n_boxes in enumerate(boxes_opts):
        for c, n_checks in enumerate(checks_opts):
            exp = Experiment(n_boxes, n_checks, cache=cache)
            all_n_finds = exp.run(n_iterations=n_iterations)
            win_rate = np.sum(all_n_finds == n_boxes) / n_iterations
            probas_grid[b, c] = win_rate
            finds_grid[b, c, :] = all_n_finds
    return probas_grid, finds_grid


def visualize_simple():
    exp = Experiment(100, 50)
    all_n_finds = exp.run(n_iterations=10000)
    sns.distplot(all_n_finds, kde=False, bins=20)
    plt.show()


def plot_from_cache(cache, n_boxes, n_checks):
    res = cache.fetch_results(n_boxes, n_checks)
    dist = [n_finds for n_finds, count in res.items() for _ in range(count)]
    sns.distplot(dist, kde=False, bins=20)
    plt.show()


def facet(boxes_opts, checks_opts, finds_grid):
    samples = []
    for b, n_boxes in enumerate(boxes_opts):
        for c, n_checks in enumerate(checks_opts):
            all_n_finds = finds_grid[b, c]
            for n_finds in all_n_finds:
                sample = {
                    'n_boxes': n_boxes,
                    'n_checks': n_checks,
                    'n_finds': n_finds
                }
                samples.append(sample)
    df = pd.DataFrame(samples)
    facets = sns.FacetGrid(df, row='n_boxes', col='n_checks', palette='Set1')
    facets.map(plt.hist, "n_finds", bins=20, color="b")
    plt.show()

def contour(boxes_opts, checks_opts, probas_grid):
    plt.contourf(checks_opts, boxes_opts, probas_grid, 15)
    plt.colorbar()
    plt.title('Probability space for finding your number')
    plt.xlabel('Number of checks allowed')
    plt.ylabel('Number of boxes/people')
    plt.gcf().canvas.set_window_title('100 Prisoners Problem')
    plt.show()

if __name__ == '__main__':
    n_iterations = 100
    boxes_opts = [90, 100, 110, 120, 130]
    checks_opts = [20, 30, 40, 50, 60, 70]
    cache = ExperimentCache('./cache.db')
    plot_from_cache(cache, 90, 20)

    probas_grid, finds_grid = grid_search(boxes_opts, checks_opts,
                                          n_iterations, cache=cache)

    facet(boxes_opts, checks_opts, finds_grid)
    contour(boxes_opts, checks_opts, probas_grid)
