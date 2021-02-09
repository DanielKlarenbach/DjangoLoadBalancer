import abc


class CUDAlgorithm(abc.ABC):

    @abc.abstractmethod
    def execute_cud(self, query):
        pass
