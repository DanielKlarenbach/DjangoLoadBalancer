import logging
import queue
import sys
import threading

from .query import Wait


class LoadBalancer:
    def __init__(self, databases, cud_algorithm, r_algorithm):
        self._current_query_id = 0
        self._result = queue.Queue(1)
        self._query_ended = threading.Event()
        self._query_ended_lock = threading.Lock()
        self._databases = databases
        self._cud_algorithm = cud_algorithm
        self._r_algorithm = r_algorithm

    def run_query(self, query):
        logging.info(f'LoadBalancer: Running {query.method} {query.model}')
        query.id = self._current_query_id
        if query.wait == Wait.DONT_WAIT.value:
            self._r_algorithm.execute_r(query)
        else:
            self._cud_algorithm.execute_cud(query)
        self._query_ended.wait()
        self._query_ended.clear()
        logging.info(f'LoadBalancer: {query.method} {query.model} successful')
        return self._result.get()

    def end_query(self, query, result):
        with self._query_ended_lock:
            if self._current_query_id == query.id:
                self._generate_query_id()
                self._result.put(result)
                self._query_ended.set()

    def _generate_query_id(self):
        if self._current_query_id == sys.maxsize:
            self._current_query_id = 0
        else:
            self._current_query_id += 1
