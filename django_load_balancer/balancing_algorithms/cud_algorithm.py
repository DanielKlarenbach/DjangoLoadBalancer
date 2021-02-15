import abc


class CUDAlgorithm(abc.ABC):
    def __init__(self, databases):
        self._databases = databases

    @abc.abstractmethod
    def execute_cud(self, query):
        pass
