import logging
from time import sleep

import django.db
import django.db.utils

from .database import DatabaseStatus
from .info_query_executor import Generator


class WatchDog():
    def __init__(self, databases, wait_time):
        self._databases = databases
        self._wait_time = wait_time

    def check_databases_statuses(self):
        while True:
            sleep(self._wait_time)
            for database in self._databases:
                if database.check_status() == DatabaseStatus.RUNNING.value:
                    try:
                        cursor = django.db.connections[database.name].cursor()
                        cursor.execute(Generator.generate(database))
                        cursor.close()
                    except (database.operational_error, django.db.utils.OperationalError):
                        database.change_status(DatabaseStatus.DOWN.value)
                        logging.warning(f'WatchDog: {database.name} went down')
                else:
                    try:
                        django.db.connections[database.name].close()
                        django.db.connections[database.name].connect()
                        database.change_status(DatabaseStatus.RUNNING.value)
                        database.is_up.set()
                        logging.info(f'WatchDog: {database.name} went up')
                    except (database.operational_error, django.db.utils.OperationalError):
                        pass
