import time

from .Database import DatabaseEngine
from .Executors import InfoQueryExecutor


class ResponseTimeExecutor(InfoQueryExecutor):
    def get_statistic(self, query, cursor, database):
        start = time.perf_counter()
        cursor.execute("select * from loadbalancer_destination limit 1")
        result = cursor.fetchall()
        end = time.perf_counter()
        return end - start


class NumberOfConnectionsExecutor(InfoQueryExecutor):
    def get_statistic(self, query, cursor, database):
        cursor.execute(self.Generator.generate(database))
        return self.Parser.parse(cursor.fetchall(), database)

    class Parser:
        @staticmethod
        def parse(result, database):
            if database.engine == DatabaseEngine.POSTGRESQL.value:
                return result[0][0]

    class Generator:
        @staticmethod
        def generate(database):
            if database.engine == DatabaseEngine.POSTGRESQL.value:
                return "select count(*) from pg_stat_activity where pid <> pg_backend_pid() and usename = current_user;"
