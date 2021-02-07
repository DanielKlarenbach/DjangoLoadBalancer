
from django.db import connections


class Executor():
    def __init__(self,result=None):
        self.result=result

    def run_query(self,query,database):
        pass

class NoQuerySetExecutor(Executor):
    def run_query(self,query,database):
        new_result = query.method().using(database.name) if query.method.__name__=='get_queryset' else query.method(using=database.name)
        self.result.put({query.query_id : new_result})
        print(str(query.method)+database.name)

class QuerySetExecutor(Executor):
    def run_query(self,query,database):
        objects = query.model.helper.using(database.name)
        new_result = objects.__getattribute__(query.method)(*query.args, **query.kwargs)
        self.result.put({query.query_id : new_result})

class InfoQueryExecutor(Executor):
    def run_query(self,query,database):
        with connections[database.name].cursor() as cursor:
            new_info = self.get_statistic(query,cursor,database)
            database.info.put(new_info)

    def get_statistic(self,query,cursor,database):
        pass