from sqlitedict import SqliteDict


class ExperimentCache:
    def __init__(self, filename):
        self._db = SqliteDict(filename, autocommit=True)

    def cache(self, n_boxes, n_checks, dist):
        if n_boxes not in self._db:
            self._db[n_boxes] = dict()
        box_dict = self._db[n_boxes]
        if n_checks not in box_dict:
            box_dict[n_checks] = {}
        check_dict = box_dict[n_checks]
        for n_finds, count in dist.items():
            if n_finds not in check_dict:
                check_dict[n_finds] = 0
            check_dict[n_finds] += count
        self._db[n_boxes] = box_dict

    def fetch(self, n_boxes, n_checks):
        if n_boxes not in self._db:
            raise ValueError(f"No cached results for n_boxes={n_boxes}")
        elif n_checks not in self._db[n_boxes]:
            raise ValueError(f"No cached results for n_checks={n_checks}")

        return self._db[n_boxes][n_checks]
