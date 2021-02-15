import enum
import queue
import threading


class Database():
    def __init__(self, name, waiters=None, engine=None, operational_error=None, load_balancer=None):
        self.name = name
        self.status = DatabaseStatus.RUNNING.value
        self.status_lock = threading.Lock()
        self.queries = queue.Queue()
        self.has_queries = threading.Semaphore(value=0)
        self.query_ended = threading.Event()
        self.is_up = threading.Event()
        self.waiters = waiters
        self.engine = engine
        self.operational_error = operational_error
        self.info = queue.Queue(1)
        self.load_balancer = load_balancer
        self.r_query_succeeded = False
        self.r_query_ended = threading.Event()

    def run_queries(self):
        while self.has_queries.acquire():
            self.query_ended.clear()
            query = self.queries.get()
            self.waiters[query.wait].run_query(query)

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
