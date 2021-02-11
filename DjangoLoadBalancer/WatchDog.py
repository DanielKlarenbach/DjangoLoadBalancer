from time import sleep

from django.db import connections

from .Database import DatabaseStatus


class WatchDog():
    def __init__(self, databases,wait_time):
        self._databases=databases
        self._wait_time=wait_time

    def check_databases_statuses(self):
        while True:
            sleep(self._wait_time)
            for database in self._databases:
                try:
                    connections[database.name].connect()
                    database.change_status(DatabaseStatus.RUNNING.value)
                    database.is_up.set()
                except database.operational_error:
                    database.change_status(DatabaseStatus.DOWN.value)
                    database.is_up.clear()

