import abc
import inspect
import logging
import pickle

import django.db
import django.db.models

from .query import QueryType


class Executor(abc.ABC):
    def __init__(self, database=None):
        self._database = database

    @abc.abstractmethod
    def run_query(self, query):
        pass


class QueryExecutor(Executor):
    def __init__(self, database=None):
        super(QueryExecutor, self).__init__(database)

    def run_query(self, query):
        if query.method == 'get_queryset':
            instance = query.model.loadbalancer_base_manager
            result = instance.__getattribute__(query.method)(*query.args, **query.kwargs).using(self._database.name)
        elif query.type == QueryType.NO_QUERYSET.value:
            instance = query.model
            result = dict(inspect.getmembers(django.db.models.Model))[query.method](instance, using=self._database.name)
        else:
            instance = query.model.models_manager.using(self._database.name)
            result = instance.__getattribute__(query.method)(*query.args, **query.kwargs)
        result = pickle.dumps(result)
        self._database.load_balancer.end_query(query, result)
        logging.info(f'QueryExecutor: {query.method} {query.model} in {self._database.name} succeed')


class InfoQueryExecutor(Executor):
    def __init__(self, database=None):
        super(InfoQueryExecutor, self).__init__(database)

    def run_query(self, query):
        with django.db.connections[self._database.name].cursor() as cursor:
            new_info = self.get_statistic(query, cursor, self._database)
            self._database.info.put(new_info)

    def get_statistic(self, query, cursor, database):
        pass
