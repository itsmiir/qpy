"""Forward definitions of classes."""

from __future__ import annotations

from numpy.typing import ArrayLike

class Dim():
    pass


class DimVec(dict):
    pass


class Unit(object):
    def __init__(self, 
                 vec: DimVec[Dim, int], 
                 symbol: str, 
                 factor: float=1, 
                 offset: float=0,
                 prefix: int=0,
                 ) -> Unit:
        pass
    symbol: str
    factor: float
    offset: float
    prefix: int
    def derived(orig: Unit, symbol: str, factor: float):
        pass
    

class Quantity(object):
    def __init__(
        self,
        value: ArrayLike,
        unit: Unit | Quantity,
        digits: int=0) -> Quantity:
        pass
    def __pow__(self, other):
        pass