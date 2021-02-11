from ..RAlgorithm import RAlgorithm
from ...Database import DatabaseStatus


class RoundRobin(RAlgorithm):
    def __init__(self, databases):
        self._databases = databases
        self._next_db = 0

    def execute_r(self, query):
        while self._databases[self._next_db].check_status() == DatabaseStatus.DOWN.value or not self._databases[self._next_db].queries.empty:
            self._next_db += 1
            if self._next_db == len(self._databases): self._next_db = 0
        db_for_read = self._databases[self._next_db]
        db_for_read.queries.put(query)
        db_for_read.has_queries.release()
        self._next_db += 1
        if self._next_db == len(self._databases): self._next_db = 0
