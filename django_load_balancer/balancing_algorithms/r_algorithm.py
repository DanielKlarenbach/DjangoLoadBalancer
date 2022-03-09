import abc
import logging


class RAlgorithm(abc.ABC):
    def __init__(self, databases):
        self._databases = databases

    def execute_r(self, query):
        while True:
            db_for_read = self._change_db(query)
            logging.info(f'RAlgorithm: {db_for_read.name} was chosen for {query.method} {query.model}')
            db_for_read.r_query_ended.wait()
            db_for_read.r_query_ended.clear()
            if db_for_read.r_query_succeeded:
                break
            logging.warning(f'RAlgorithm: {query.method} {query.model} in {db_for_read.name} did not succeed')

    @abc.abstractmethod
    def _change_db(self, query):
        pass
