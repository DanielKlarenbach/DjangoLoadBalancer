import time

import django
import django.db
from django.db import connections

from .Database import DatabaseStatus


class Waiter:
    def __init__(self, executor=None):
        self._executor = executor

    def run_query(self, query, database):
        pass


class WaitWaiter(Waiter):
    def __init__(self, wait_time, executor=None):
        super(WaitWaiter, self).__init__(executor)
        self._wait_time = wait_time

    def run_query(self, query, database):
        try:
            self._executor.run_query(query, database)
        except django.db.utils.OperationalError:
            database.status = DatabaseStatus.DOWN
            self.wait_for_connection(query, database)

    def wait_for_connection(self, query, database):
        while True:
            time.sleep(self._wait_time)
            try:
                connections[database.name].connect()
            except database.operational_error:
                pass
            else:
                self._executor.run_query(query, database)
                database.status = DatabaseStatus.RUNNING
                break


class DontWaitWaiter(Waiter):
    def run_query(self, query, database):
        try:
            self._executor.run_query(query, database)
        except django.db.utils.OperationalError:
            database.status = DatabaseStatus.DOWN
            raise django.db.utils.OperationalError
