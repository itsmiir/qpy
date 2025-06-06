from abc import abstractmethod, ABC

from qntpy.core.quantity import Quantity

class QuantityConvertible(ABC):
    
    @abstractmethod
    def as_quantity(self) -> Quantity:
        pass