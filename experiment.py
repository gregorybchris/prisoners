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
        n_finds_dict = dict()
        for _ in range(n_iterations):
            n_finds = self._run_iteration()
            if n_finds not in n_finds_dict:
                n_finds_dict[n_finds] = 0
            n_finds_dict[n_finds] += 1

        if self._cache is not None:
            self._cache.cache(self._n_boxes, self._n_checks,
                              n_finds_dict)

        return n_finds_dict

    def _run_iteration(self):
        boxes = np.random.permutation(self._n_boxes)
        cycles = self._preprocess(boxes)
        n_finds = np.sum([len(c) for c in cycles if len(c) <= self._n_checks])
        return n_finds

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
    all_n_finds = exp.run(n_iterations=10)
    print(all_n_finds)
