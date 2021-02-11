from time import sleep

from ..RAlgorithm import RAlgorithm
from ...Database import DatabaseStatus
from ...Query import Query, Wait


class Interval(RAlgorithm):
    def __init__(self, databases):
        self._databases = databases
        self._next_db = 0
        self._info_per_database = {x: 0 for x in range(len(databases))}

    def execute_r(self, query):
        info_per_database = sorted(self._info_per_database, key=self._info_per_database.get)
        while self._databases[info_per_database[self._next_db]].check_status() == DatabaseStatus.DOWN.value or not self._databases[info_per_database[self._next_db]].queries.empty:
            self._next_db += 1
            if self._next_db == len(self._databases): self._next_db = 0
        db_for_read = self._databases[info_per_database[self._next_db]]
        db_for_read.queries.put(query)
        db_for_read.has_queries.release()
        self._next_db = 0

    def update_info(self, interval, query_type):
        while True:
            print(self._info_per_database)
            for i, db in enumerate(self._databases):
                if not db.info.empty():
                    self._info_per_database[i] = db.info.get()
                db.queries.put(Query(wait=Wait.WAIT.value, type=query_type))
                db.has_queries.release()
            sleep(interval)
