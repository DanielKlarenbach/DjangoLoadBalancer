import enum
import threading
from queue import Queue


class Database():
    def __init__(self, name, waiters, executors, engine=None, operational_error=None):
        self.name = name
        self.status = DatabaseStatus.RUNNING.value
        self.queries = Queue()
        self.has_queries = threading.Semaphore(value=0)
        self.status_lock = threading.Lock()
        self.is_up=threading.Event()
        self.waiters = waiters
        self.executors = executors
        self.engine = engine
        self.operational_error = operational_error
        self.info = Queue(1)

    def run_queries(self):
        while self.has_queries.acquire():
            query = self.queries.get()
            self.waiters[query.wait]._executor = self.executors[query.type]
            self.waiters[query.wait].run_query(query, self)

    def change_status(self, new_status):
        with self.status_lock:
            self.status = new_status

    def check_status(self):
        with self.status_lock:
            return self.status


class DatabaseStatus(enum.Enum):
    RUNNING = "RUNNING"
    DOWN = "DOWN"


class DatabaseEngine(enum.Enum):
    POSTGRESQL = "django.db.backends.postgresql"
    MYSQL = "django.db.backends.mysql"
    SQLITE = "django.db.backends.sqlite3"
