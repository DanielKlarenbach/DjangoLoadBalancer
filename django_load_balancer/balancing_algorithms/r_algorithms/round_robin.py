from ..r_algorithm import RAlgorithm
from ...database import DatabaseStatus


class RoundRobin(RAlgorithm):
    def __init__(self, databases):
        super(RoundRobin, self).__init__(databases)
        self._next_db = 0

    def _change_db(self, query):
        while self._databases[self._next_db].check_status() == DatabaseStatus.DOWN.value \
                or not self._databases[self._next_db].queries.empty \
                or not self._databases[self._next_db].query_ended.isSet():
            self._next_db += 1
            if self._next_db == len(self._databases): self._next_db = 0
        db_for_read = self._databases[self._next_db]
        db_for_read.queries.put(query)
        db_for_read.has_queries.release()
        self._next_db += 1
        if self._next_db == len(self._databases): self._next_db = 0
        return db_for_read
