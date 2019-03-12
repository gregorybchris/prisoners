from sqlitedict import SqliteDict

class ExperimentCache:
    def __init__(self, filename):
        self._db = SqliteDict(filename, autocommit=True)
        
    def cache_results(self, n_boxes, n_checks, results):
        if n_boxes not in self._db:
            self._db[n_boxes] = dict()
        box_dict = self._db[n_boxes]
        if n_checks not in box_dict:
            box_dict[n_checks] = {}
        check_dict = box_dict[n_checks]
        for result in results:
            if result not in check_dict:
                check_dict[result] = 0
            check_dict[result] += 1
        self._db[n_boxes] = box_dict

    def fetch_results(self, n_boxes, n_checks):
        return self._db[n_boxes][n_checks]