from enum import Enum, auto
from __future__ import annotations

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

class DimVec(dict):
    """A dimension vector."""
    
    def copy(self) -> DimVec:
        return super().copy()


