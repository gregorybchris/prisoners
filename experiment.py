import numpy as np


class Experiment:
    def __init__(self, n_boxes, n_checks,
                 random_state=None, cache=None):
        if random_state is not None:
            np.random.seed(random_state)

        self._cache = cache
        self._n_boxes = n_boxes
        self._n_checks = n_checks

    def run(self, n_iterations=1):
        all_n_finds = [self._run_iteration() for _ in range(n_iterations)]
        all_n_finds = np.array(all_n_finds, dtype=int)
        if self._cache is not None:
            self._cache.cache_results(self._n_boxes, self._n_checks,
                                      all_n_finds)
        return all_n_finds

    def _run_iteration(self):
        boxes = self._create_boxes()
        cycles = self._preprocess(boxes)
        n_finds = np.sum([len(c) for c in cycles if len(c) <= self._n_checks])
        return n_finds

    def _create_boxes(self):
        return np.random.permutation(self._n_boxes)

    def _preprocess(self, boxes):
        visited = set()
        cycles = []

        # Try to start a cycle at every box
        for starting_box in range(len(boxes)):
            if starting_box not in visited:
                # Create new cycle
                cycle = []
                box = starting_box
                while True:
                    cycle.append(box)
                    visited.add(box)
                    box = boxes[box]
                    if box == starting_box:
                        break

                # Add cycle to the list of cycles
                cycles.append(cycle)
        return cycles

    def get_n_boxes(self):
        return self._n_boxes

    def get_n_checks(self):
        return self._n_checks


if __name__ == '__main__':
    exp = Experiment(100, 50)
    all_n_finds = exp.run(n_iterations=10).tolist()
    print(all_n_finds)
