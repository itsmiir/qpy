"""Code for the representation of quantities and units.

The representations implemented here are derived from the BIPM's rules
and style conventions as published in Section 5 of the SI Brochure.
"""

from enum import Enum, auto

from qntpy.core.unit import Unit 

class Op(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

_superscripts = {
    "0":"⁰",
    "1":"¹",
    "2":"²",
    "3":"³",
    "4":"⁴",
    "5":"⁵",
    "6":"⁶",
    "7":"⁷",
    "8":"⁸",
    "9":"⁹",
    ".":"·",
    "-":"⁻"
}

def to_superscript(num: int):
    """Convert an integer to a superscript string."""
    n = str(num)
    new_n = ""
    for i in n:
        new_n += _superscripts[i]
    return new_n    

def unit_str(unit: Unit) -> str:
    strin = ""
    for k in sorted(unit.vec):
        if unit.vec[k] == 0:
            pass
        elif unit.vec[k] != 1:
            strin +=(k + to_superscript(unit.vec[k]))
        else:
            strin +=(k)
    if unit.factor != 1:
        return str(unit.factor) + " "+ strin
    else:
        return strin

def enumerated_repr():
    pass

