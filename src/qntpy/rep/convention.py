from __future__ import annotations
from dataclasses import dataclass

from qntpy.core.defs import Unit

@dataclass
class UnitSystem(object):
    length: Unit
    mass: Unit
    time: Unit
    electric_current: Unit
    thermodynamic_temperature: Unit
    amount_of_substance: Unit
    luminous_intensity: Unit

@dataclass
class NumRep(object):
    decimal_prefix: str
    decimal_marker: str
    thousands_seperator: str
    imag_marker: str
    milli_seperator: str
    mul_sign: str
    
