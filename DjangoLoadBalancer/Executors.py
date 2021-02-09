import inspect

from django.db import connections
from django.db import models


class Executor():
    def __init__(self, result=None):
        self.result = result

    def run_query(self, query, database):
        pass


class NoQuerySetExecutor(Executor):
    def run_query(self, query, database):
        instance = query.model.loadbalancer_base_manager if query.method == 'get_queryset' else query.model
        new_result = instance.__getattribute__(query.method) \
            (*query.args, **query.kwargs).using(database.name) \
            if query.method == 'get_queryset' else dict(inspect.getmembers(models.Model))[query.method](instance,
                                                                                                        using=database.name)
        self.result.put({query.query_id: new_result})
        print(database.name + ' ' + str(query.method))


class QuerySetExecutor(Executor):
    def run_query(self, query, database):
        objects = query.model.models_manager.using(database.name)
        new_result = objects.__getattribute__(query.method)(*query.args, **query.kwargs)
        self.result.put({query.query_id: new_result})
        print(database.name + ' ' + str(query.method))


class InfoQueryExecutor(Executor):
    def run_query(self, query, database):
        with connections[database.name].cursor() as cursor:
            new_info = self.get_statistic(query, cursor, database)
            database.info.put(new_info)

    def get_statistic(self, query, cursor, database):
        pass
