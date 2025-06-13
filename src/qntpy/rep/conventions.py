"""Conventions for representation of values.

"""
from abc import ABC

from qntpy.rep.convention import UnitSystem, NumRep

class NumberSystems(ABC):
    NIST: NumRep = NumRep(
        decimal_prefix='0',
        decimal_marker='.',
        thousands_seperator=' ',
        milli_seperator=' ',
        imag_marker='i',
        mul_sign='⨯'
    )