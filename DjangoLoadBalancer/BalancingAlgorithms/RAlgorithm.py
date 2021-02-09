import abc


class RAlgorithm(abc.ABC):

    @abc.abstractmethod
    def execute_r(self, query):
        pass
