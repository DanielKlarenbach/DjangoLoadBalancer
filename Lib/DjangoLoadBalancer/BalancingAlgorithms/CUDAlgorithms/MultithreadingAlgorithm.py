from ...BalancingAlgorithms.CUDAlgorithm import CUDAlgorithm


class MultithreadingAlgorithm(CUDAlgorithm):
    def __init__(self, threads, databases):
        self._databases = databases
        self._threads = threads

    def execute_cud(self, query):
        for db in self._databases:
            db.queries.put(query)
            db.has_queries.release()
