"""Code for the representation of quantities and units.

The representations implemented here are derived from the BIPM's rules
and style conventions as published in Section 5 of the SI Brochure.
"""

from enum import Enum, auto

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

_prefices = {
    'quecto': ('q', -30), '-29': 0, '-28': 0,
    'ronto':  ('r', -27), '-26': 0, '-25': 0,
    'yocto':  ('y', -24), '-23': 0, '-22': 0,
    'zepto':  ('z', -21), '-20': 0, '-19': 0,
    'atto':   ('a', -18), '-17': 0, '-16': 0,
    'femto':  ('f', -15), '-14': 0, '-13': 0,
    'pico':   ('p', -12), '-11': 0, '-10': 0,
    'nano':    ('n', -9),  '-8': 0,  '-7': 0,
    'micro':   ('μ', -6),  '-5': 0,  '-4': 0,
    'milli':   ('m', -3),
    'centi':   ('c', -2),
    'deci':    ('d', -1),
    '':          ('', 0),
    'deca':     ('da', 1),     
    'hecto':    ('h', 2),
    'kilo':     ('k', 3),  '4': 0,  '5': 0,
    'mega':     ('M', 6),  '7': 0,  '8': 0,
    'giga':     ('G', 9), '10': 0, '11': 0,
    'tera':    ('T', 12), '13': 0, '14': 0,
    'peta':    ('P', 15), '16': 0, '17': 0,
    'exa':     ('E', 18), '19': 0, '20': 0,
    'zetta':   ('Z', 21), '22': 0, '23': 0,
    'yotta':   ('Y', 24), '25': 0, '26': 0,
    'ronna':   ('R', 27), '28': 0, '29': 0,
    'quetta':  ('Q', 30),
}

def to_superscript(num: int):
    """Convert an integer to a superscript string."""
    n = str(num)
    new_n = ""
    for i in n:
        new_n += _superscripts[i]
    return new_n    

def prefix_to_exponent(prefix: str, is_kg: bool) -> int:
    kg_mod = 3 if is_kg else 0
    return _prefices[prefix][1]
def prefix_to_abbrev(prefix: str, is_kg: bool) -> str:
    kg_mod = 3 if is_kg else 0
    return _prefices[prefix][0]
def exponent_to_prefix(expnt: int, is_kg: bool) -> str:
    kg_mod = 3 if is_kg else 0
    return list(_prefices.keys())[expnt+30+kg_mod][1]
def exponent_to_abbrev(expnt: int, is_kg: bool) -> str:
    kg_mod = 3 if is_kg else 0
    return _prefices[list(_prefices.keys())[expnt+30+kg_mod]][0]

def concat_symbols(symbol_1: str, symbol_2: str, op: Op) -> str:
    match op:
        case Op.ADD:
            return symbol_1
        case Op.SUB:
            return symbol_2
        case Op.MUL:
            return f'{symbol_1}•{symbol_2}'
        case Op.DIV:
            return f'{symbol_1}/{symbol_2}'
            



def enumerated_repr():
    pass

