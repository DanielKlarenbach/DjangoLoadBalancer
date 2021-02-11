import sys

import django.db.utils

from .Query import Wait


class LoadBalancer():
    def __init__(self, result, databases, cud_algorithm, r_algorithm,watch_dog):
        self.current_query_id = 0
        self.result = result
        self.databases = databases
        self.cud_algorithm = cud_algorithm
        self.r_algorithm = r_algorithm
        self.watch_dog=watch_dog

    def run_query(self, query):
        self.generate_query_id()
        query.query_id = self.current_query_id
        if query.wait == Wait.DONT_WAIT.value:
            self.execute_r(query)
        else:
            self.execute_cud(query)
        res = self.result.get()
        while list(res.keys())[0] != self.current_query_id:
            res = self.result.get()
        return list(res.values())[0]

    def execute_cud(self, query):
        self.cud_algorithm.execute_cud(query)

    def execute_r(self, query):
        while True:
            try:
                self.r_algorithm.execute_r(query)
            except django.db.utils.OperationalError:
                pass
            else:
                break

    def generate_query_id(self):
        if self.current_query_id == sys.maxsize:
            self.current_query_id = 0
        else:
            self.current_query_id += 1
