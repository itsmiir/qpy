from __future__ import annotations

from enum import Enum, auto
from typing import Dict

from qntpy.core import defs
from qntpy.rep import rep

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
    
    def __repr__(self):
        match self:
            case Dim.L:
                return 'L'
            case Dim.T:
                return 'T'
            case Dim.M:
                return 'M'
            case Dim.I:
                return 'I'
            case Dim.THETA:
                return 'Θ'
            case Dim.N:
                return 'N'
            case Dim.J:
                return 'J'
  
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
        self._mag2 = None

    @property
    def mag2(self):
        """Magnitude squared of this vector."""
        if self._mag2 is None:
            total = 0
            for i in self:
                total += self[i]**2
            self._mag2 = total
        return self._mag2
            
    # def __dict__(self) -> dict:
    #     new_dict = {}
    #     for i in self:
    #         new_dict[i] = self[i]
    #     return new_dict
    
    def __add__(self, other: DimVec) -> DimVec:
        new_dict = dict(self)
        if not isinstance(other, DimVec):
            return NotImplemented
        for key in other:
            if key in new_dict:
                new_dict[key] += other[key]
            else:
                new_dict[key] = other[key]
        return DimVec(new_dict)
        
    def __sub__(self, other: DimVec) -> DimVec:
        if not isinstance(other, DimVec):
            return NotImplemented
        return self + (-other)
    
    def __neg__(self) -> DimVec:
        new_vec = self.copy()
        for key in new_vec.keys():
            new_vec[key] *= -1
        return new_vec
    
    def __pos__(self) -> DimVec:
        return self
    
    def copy(self) -> DimVec:
        return DimVec(super().copy())
    
    def is_empty(self) -> bool:
        return self.mag2 == 0
    
    def __repr__(self):
        s = self.__class__.__name__+'('
        return s + str(self) + ')'
        
    def __str__(self):
        s = ''
        for i in self:
            s += f'{repr(i)}{self[i]} '
        return rep.str_to_superscript(s.strip())
            
defs.DimVec = DimVec
