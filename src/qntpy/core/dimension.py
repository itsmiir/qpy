from __future__ import annotations

from enum import Enum, auto
from typing import Dict

from qntpy.core import defs

class Dim(Enum):
    """Base physical dimensions."""
    L = auto()
    """Length."""
    T = auto()
    """Time."""
    M = auto()
    """Mass."""
    I = auto()
    """Electric current."""
    THETA = auto()
    """Thermodynamic temperature."""
    N = auto()
    """Amount of substance."""
    J = auto()
    """Luminous intensity."""
    
    def __str__(self):
        match self:
            case Dim.L:
                return 'm'
            case Dim.T:
                return 's'
            case Dim.M:
                return 'g'
            case Dim.I:
                return 'A'
            case Dim.THETA:
                return 'K'
            case Dim.N:
                return 'mol'
            case Dim.J:
                return 'cd'

defs.Dim = Dim

class DimVec(Dict):
    """A dimension vector."""
    def __init__(self, map):
        super().__init__(map)
        to_del = []
        for key in self.keys():
            if type(key) is not Dim:
                raise ValueError(f"Key {key} in DimVec is not of type Dim!")
            if int(self[key]) != self[key]:
                raise ValueError(f"Value {self[key]} at key {key} in DimVec is not an int!")
            if self[key] == 0:
                to_del.append(key)
        for key in to_del:
            del self[key]
    
    def copy(self) -> DimVec:
        return DimVec(super().copy())
    
    def invert(self) -> DimVec:
        for key in self.keys():
            self[key] *= -1
        return self
    
    def is_empty(self) -> bool:
        if len(self.keys()) == 0: return True
        else:
            for i in self:
                if self[i] != 0:
                    return False
            return True
        
            
defs.DimVec = DimVec
