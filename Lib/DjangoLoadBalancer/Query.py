import enum


class Query:
    def __init__(self, wait, type, method=None, args=[], kwargs={}, model=None, query_id=None):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.type = type
        self.wait = wait
        self.model = model
        self.query_id = query_id


class QueryType(enum.Enum):
    QUERYSET = "QUERYSET"
    NO_QUERYSET = "NO_QUERYSET"
    INFO_NUMBER_OF_CONNECTIONS = "INFO_NUMBER_OF_CONNECTIONS"
    INFO_RESPONSE_TIME = "INFO_RESPONSE_TIME"


class Wait(enum.Enum):
    WAIT = "WAIT"
    DONT_WAIT = "DONT_WAIT"
