import logging

import django
import django.db.utils

from .database import DatabaseStatus


class Waiter:
    def __init__(self, database=None, executor=None):
        self._database = database
        self.executor = executor

    def run_query(self, query):
        pass


class WaitWaiter(Waiter):
    def __init__(self, database=None, executor=None):
        super(WaitWaiter, self).__init__(database, executor)

    def run_query(self, query):
        if self._database.check_status() == DatabaseStatus.RUNNING.value:
            try:
                logging.info(f'WaitWaiter: Running {query.method} {query.model} in {self._database.name}')
                self.executor.run_query(query)
                self._database.query_ended.set()
            except (django.db.utils.OperationalError, self._database.operational_error, django.db.utils.InterfaceError):
                logging.warning(f'WaitWaiter: {query.method} {query.model} in {self._database.name} failed')
                self._database.change_status(DatabaseStatus.DOWN.value)
                self.wait_for_connection(query)
        else:
            self.wait_for_connection(query)

    def wait_for_connection(self, query):
        logging.info(f'WaitWaiter: Waiting for connection with {self._database.name}')
        self._database.is_up.wait()
        self._database.is_up.clear()
        self.run_query(query)


class DontWaitWaiter(Waiter):
    def __init__(self, database=None, executor=None):
        super(DontWaitWaiter, self).__init__(database, executor)

    def run_query(self, query):
        if self._database.check_status() == DatabaseStatus.RUNNING.value:
            try:
                logging.info(f'DontWaitWaiter: Running {query.method} {query.model} in {self._database.name}')
                self.executor.run_query(query)
                self._database.query_ended.set()
                self._database.r_query_succeeded = True
                self._database.r_query_ended.set()
            except (django.db.utils.OperationalError, self._database.operational_error, django.db.utils.InterfaceError):
                logging.warning(f'DontWaitWaiter: {query.method} {query.model} in {self._database.name} failed')
                self._database.change_status(DatabaseStatus.DOWN.value)
                self._database.query_ended.set()
                self._database.r_query_succeeded = False
                self._database.r_query_ended.set()
        else:
            logging.warning(f'DontWaitWaiter: {query.method} {query.model} in {self._database.name} failed')
            self._database.query_ended.set()
            self._database.r_query_succeeded = False
            self._database.r_query_ended.set()
