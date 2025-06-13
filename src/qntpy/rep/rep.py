"""Code for the representation of quantities and units.

The representations implemented here are derived from the BIPM's rules
and style conventions as published in Section 5 of the SI Brochure.
"""

from enum import Enum, auto
from numbers import Number as num

from numpy import number as np_num, ndarray
import numpy as np
from uncertainties.core import AffineScalarFunc as u_num, ufloat_fromstr

from qntpy.rep.convention import NumRep

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
    '':         ('',  0),
    'deca':    ('da', 1),     
    'hecto':    ('h', 2),
    'kilo':     ('k', 3),   '4': 0,   '5': 0,
    'mega':     ('M', 6),   '7': 0,   '8': 0,
    'giga':     ('G', 9),  '10': 0,  '11': 0,
    'tera':    ('T', 12),  '13': 0,  '14': 0,
    'peta':    ('P', 15),  '16': 0,  '17': 0,
    'exa':     ('E', 18),  '19': 0,  '20': 0,
    'zetta':   ('Z', 21),  '22': 0,  '23': 0,
    'yotta':   ('Y', 24),  '25': 0,  '26': 0,
    'ronna':   ('R', 27),  '28': 0,  '29': 0,
    'quetta':  ('Q', 30),
}

def str_to_superscript(s: str) -> str:
    """Convert a string to a superscript string. If a character is not in the superscript dictionary, it's passed through to the output."""
    new_str = ''
    for c in s:
        if c in _superscripts:
            new_str += _superscripts[c]
        else:
            new_str += c
    return new_str

def to_superscript(num: int) -> str:
    """Convert an integer to a superscript string."""
    n = str(num)
    new_n = ""
    for i in n:
        try:
            new_n += _superscripts[i]
        except KeyError:
            raise ValueError(f"Value {str(num)} cannot be superscripted")
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
            return f'{symbol_1} {symbol_2}'
        case Op.DIV:
            return f'{symbol_1}/{symbol_2}'

def print_ndarray(value: ndarray, **kwargs) -> str:
    raise NotImplementedError()
    
def array_dispatch(value: ndarray, num_rep: NumRep, **kwargs) -> str:
    """Format a numpy array according to the recommendations of the SI Brochure 9th Edition, sections 5.4.3 through 5.4.5."""

def get_exp(value: num) -> tuple[int, float]:
    raw_exp = np.log10(value)
    if raw_exp <= -1:
        exp = int(np.ceil(raw_exp))
    elif raw_exp >= 1:
        exp = int(np.floor(raw_exp))
    else:
        exp = 0
    mantissa = value / 10**exp
    return exp, mantissa

def ufloat_SI_repr(value: u_num) -> str:
    exp, mantissa = get_exp(value.nominal_value)
    u_mantissa = value.std_dev / 10**exp
    u_exp, u_mantissa = get_exp(u_mantissa)
    u_prec = (1 - u_exp) if u_exp < -1 else 1
    return(str(mantissa) + ' ' + str(u_mantissa) + ' ' + f'{u_mantissa:.{u_prec}f}')
 
def value_to_SI_rep(value: object, num_rep: NumRep, **kwargs) -> str:
    """Format a value to a numerical string according to the recommendations of the SI Brochure 9th Edition, sections 5.4.3 through 5.4.5.
    
    By default, this function includes handling for python's `Number`, numpy's `number`, and `uncertainties`' ``AffineScalarFunc` (superclass of `Variable`).
    Your custom number class can implement functionality for this function by implementing the following static method:
    ```
    class MyClass:
        @staticmethod
        def __SI_rep__(value: MyClass, num_rep: NumRep, **kwargs) -> str
    ```
    You can choose what, if any, `kwargs` to handle. 
    """
    # Check input to make sure we can format it, and try to fall back to a custom implementation if we can't.
    imag_val: float = 0
    imag_unc: float = 0
    real_val: float = 0
    real_unc: float = 0
    
    
    if isinstance(value, ndarray):
        return array_dispatch(value, num_rep, **kwargs)
    
    if isinstance(value, (num, np_num)):
        if hasattr(value, 'imag'):
            pass
    try:
        return value.__class__.__SI_rep__(value, num_rep, **kwargs)
    except AttributeError:
        raise TypeError(f"Cannot format value of type {type(value)}")
        

def enumerated_repr():
    raise NotImplementedError()

u_num.__repr__ = ufloat_SI_repr

