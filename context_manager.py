from abc import ABC,abstractmethod,abstractclassmethod

class context_manager(ABC):
    @abstractclassmethod
    def __enter__(self):
        pass
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



