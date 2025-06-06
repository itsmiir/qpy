from __future__ import annotations
from copy import deepcopy
from typing import Any

# from uncertainties import ufloat
# from uncertainties.unumpy import uarray, umatrix
import numpy as np
from numpy.typing import ArrayLike
from typing import TYPE_CHECKING

from qntpy.core.defs import Unit
from qntpy.core import defs
from qntpy.util.exceptions import IncommensurableError

if TYPE_CHECKING:
    from qntpy.core.unit import Unit
class Quantity:   
    """Represents a physical quantity; i.e., a `Unit` with an associated numerical value.
    
    "The value of a quantity is generally expressed as the product of a number and a unit. The unit
    is a particular example of the quantity concerned which is used as a reference, and the number
    is the ratio of the value of the quantity to the unit." -*The International System of Units*
    """
    def __new__(cls, value: ArrayLike, unit: 'Unit' | Quantity, digits: int=0, bypass_checks=False) -> Quantity | Any:
        if bypass_checks:
            return super().__new__(cls)
            
        if isinstance(value, Quantity):
            unit *= value.unit
            value = value.value
        if isinstance(unit, Quantity):
            value *= unit.value
            unit = unit.unit
        if value == 1:
            if hasattr(unit, 'offset') and unit.offset != 0:
                return super().__new__(cls)
            else:
                return unit
        if isinstance(unit, float):
            return value * unit
        if isinstance(unit, Quantity) or hasattr(unit, 'vec'):
            return super().__new__(cls)
        else:   
            return value * unit       
    
    def __init__(self, value: ArrayLike | Quantity, unit: 'Unit' | Quantity, digits: int=0) -> Quantity:
        """Create a new `Quantity` object, and return it.
        
        A quantity is a `Unit` with an associated value. This value can be a numpy array,
        
        """
        self.value = 1
        self.unit: 'Unit'=None
        if type(unit) == Quantity:
            value *= unit.value
            unit = unit.unit
        else:
            try:
                self.unit = unit.copy()
                self.value = (value*self.unit.factor)+self.unit.offset
                self.unit.factor = 1
                self.unit.offset = 0
            except AttributeError:
                self.unit = None
        self.digits = digits
        if type(value) == Quantity:
            self.value = value.value
            self.unit = value.unit * unit

    def as_quantity(self):
        return self

    def __add__(self, other):
        if type(other) == Unit:
            return self + Quantity(1, other)
        elif type(other) == Quantity:
            if not other.unit == self.unit and other.value != 0 and self.value != 0:
                raise IncommensurableError("Incompatible units: "+ simplify(self.unit)+ " and "+ simplify(other.unit))
            return Quantity(self.value+other.value, self.unit)
        else:
            if other == 0:
                return self
            else:
                raise IncommensurableError("Incompatible units: "+str(self)+" and "+str(other))
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -1 * other
    def __rsub__(self, other):
        return other + -1*self

    def __mul__(self, other):
        if other == 0:
            return 0
        if type(other) == Unit:
            return Quantity(self.value, self.unit * other, self.digits)
        elif type(other) == Quantity:
            return Quantity(self.value*other.value, self.unit*other.unit)
        else:
            return Quantity(other*self.value, self.unit)
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        if type(other) == Quantity:
            return Quantity(self.value/other.value, self.unit/other.unit)
        else:
            try:
                return self * other.invert()
            except AttributeError:
                return Quantity(self.value / other, self.unit)
    def __rtruediv__(self, other):
        return other / self.value / self.unit

    def __round__(self, i):
        return Quantity(round(self.value, i), self.unit)
    
    def __cmp__(self, other):
        return (self - other).value

    def __str__(self):
        from qntpy.rep.simplify import simplify
        if self.digits > 0:
            val = round(self.value, self.digits)
        else:
            val = self.value
            val /= 10**self.unit.prefix
        return str(val)+" "+self.unit.symbol
    def __float__(self):
        return self.value
    def __int__(self):
        return int(float(self))
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        if type(other) == Unit:
            return self == Quantity(1, other)
        elif type(other) == Quantity:
            return other.value == self.value and other.unit == self.unit
        else:
            return False
    def __gt__(self, other):
        return (self - other).value > 0
    def __lt__(self, other):
        return (self - other).value < 0
    def __ge__(self, other):
        return (self - other).value >= 0
    def __le__(self, other):
        return (self - other).value <= 0
    
    def __neg__(self):
        return -1*self
    def __pos__(self):
        return self
    def __pow__(self, other):
        return Quantity(self.value**other, self.unit**other)
    
    def __array__(self, dtype=None) -> np.ndarray:
        return np.array(self.value)
    
    
    def __array_ufunc__(ufunc, method, *inputs, **kwargs):
        pass
    

    def round(self, digits):
        return Quantity(self.value, self.unit, digits)
    def copy(self) -> Quantity:
        return Quantity(deepcopy(self.value), self.unit.copy(), self.digits)

defs.Quantity = Quantity

# unit definitions: derived
# rad = One # just for readability

# Hz = Unit.derived(One/s, "Hz")
# N = Unit.derived(kg*m/s/s, "N")
# Pa = Unit.derived(N/m/m, "Pa")
# J = Unit.derived(N*m, "J")
# W = Unit.derived(J/s, "W")
# C = Unit.derived(s*A, "C")
# V = Unit.derived(W/A, "V")
# F = Unit.derived(C/V, "F")
# Ohm = Unit.derived(V/A, "Ω")
# S = Unit.derived(One/Ohm, "S")
# Wb = Unit.derived(V*s, "Wb")
# T = Unit.derived(Wb/m/m, "T")
# H = Unit.derived(Wb/A, "H")
# Sv = Unit.derived(J/kg, "Sv")

# # non-standard derived units: baseUnit = derivedUnit*factor + offset
# deg = Unit.derived(rad, "⁰", 0.01745329)

# degC = Unit.derived(K, "⁰C", 1, 273.15)

# L = Unit.derived(m*m*m, "L", 0.001)
# mL = Unit.derived(L, "mL", 0.001)

# ms = milli(s)
# us = micro(s)
# ns = nano(s)
# ps = pico(s)
# minute = Unit.derived(s, "min", 60)
# hr = Unit.derived(minute, "hr", 60)
# day = Unit.derived(hr, "d", 24)
# wk = Unit.derived(day, "wk", 7)
# # not even gonna try to do months
# yr = Unit.derived(day, "yr", 365.25)
# My = Unit.derived(yr, "My", 1e6)
# aeon = Unit.derived(yr, "AE", 1e9)

# eV = Unit.derived(J, "eV", 1.602176634e-19)
# keV = kilo(eV)
# MeV = mega(eV)
# GeV = giga(eV)
# TeV = tera(eV)

# kN = kilo(N)
# MN = mega(N)
# GN = giga(N)

# eVc2 = Unit.derived(kg, "(eV/c²)", 1.78266192e-36)
# keVc2= kilo(eVc2)
# MeVc2= mega(eVc2)
# GeVc2= giga(eVc2)
# TeVc2= tera(eVc2)

# kPa = kilo(Pa)
# MPa = mega(Pa)
# GPa = giga(Pa)

# kJ = kilo(J)
# MJ = mega(J)
# GJ = giga(J)

# Wh = Unit.derived(W*hr, "Wh")
# kWh = kilo(Wh)
# MWh = mega(Wh)
# GWh = giga(Wh)
# TWh = tera(Wh)

# mW = milli(W)
# kW = kilo(W)
# MW = mega(W)
# GW = giga(W)
# TW = tera(W)

# nm = nano(m)
# um = micro(m)
# mm = milli(m)
# cm = Unit.derived(m, "cm", 0.01)
# km = kilo(m)
# Gm = giga(m)
# Mm = mega(m)
# au = Unit.derived(m, "au", 149597870700)
# pc = Unit.derived(au, "pc", 648000/_pi)
# ly = Unit.derived(m, "ly", 9460730472580800)

# m2 = Unit.derived(m*m, "(m²)")
# m3 = Unit.derived(m*m*m, "(m³)")
# ha = Unit.derived(m2, "ha", 10000)

# kA = kilo(A)
# mA = milli(A)

# kV = kilo(V)
# mV = milli(V)

# mF = milli(F)
# uF = micro(F)
# nF = nano(F)
# pF = pico(F)

# mH = milli(H)
# uH = micro(H)
# nH = nano(H)

# kOhm = kilo(Ohm)
# MOhm = mega(Ohm)
# GOhm = giga(Ohm)

# kHz = kilo(Hz)
# MHz = mega(Hz)
# GHz = giga(Hz)
# THz = tera(Hz)

# g = Unit.derived(kg, "g", 0.001)
# mg = milli(g)
# ug = micro(g)
# ng = nano(g)


# # units that printed answers can be expressed in
# # includes most named, derived units except Sv because i find that J/kg is often more useful by itself
# # ordering: a unit must always go before its inverse (i.e., s must go before Hz) so that the unit simplifier
# # does not use units of 1/Hz for time!
# # updating this list (via addBaseUnit, please) will change what values get simplified
# repr_units = [
#     J, W, N, Pa, C, F, V, Ohm, S, Wb, T, H, units.kg, m, A, K, cd, s, Hz
# ]
# def add_base_unit(unit):
#     repr_units.append(unit)
# def setUnits(us):
#     repr_units = us
# def getUnits():
#     return repr_units

# # units that will not be simplified; e.g., m/s² will not be simplified to N/kg
# _explicit_units = [
#     # m*m, m*m*m,
#     # m/s, m/s**2,

# ]
# def add_explicit(unit):
#     _explicit_units.append(unit)
# def set_explicits(units):
#     _explicit_units = units
# def get_explicit_units():
#     return _explicit_units

# def get_distance(unit1, unit2):
#     d = unit2/unit1
#     sum = 0
#     if type(d) != Unit:
#         return 0
#         # try:
#         #     return unit1.factor - unit2.factor
#         # except AttributeError:
#         #     pass
#     for i in d.vec:
#         sum+=(d.vec[i]**2)
#     return (sum)**.5

# def __simplify(unit, expU, units=repr_units):
#     """if you're curious, this function sequentially factors out the "closest" unit to the unit being tested;
#     "closest" being defined via euclidean (ish) distance in 6D base-SI-unit space
#     """
#     if type(unit) != Unit:
#         return ""
#     for i in expU:
#         if unit == i:
#             return str(unit)
#     d = get_distance(unit, units[0])
#     closest = [units[0], False, 1]
#     for i in units:
#         order = 1
#         goAgain = False
#         if not unit._orthogonal(i):
#             if unit._dot_product(i) > 0:
#                 d1 = get_distance(unit, i)
#                 d2 = d1 - 1
#                 while d2 < d1 or goAgain:
#                     goAgain = False
#                     d2 = get_distance(unit, (i**(order+1)))
#                     if d2 < d1:
#                         order+=1
#                         d1 = d2
#                         goAgain = True
#                 if d1 < d:
#                     d = d1
#                     closest[0] = i
#                     closest[1]=False
#                     closest[2]=order
#             else:
#                 d1 = get_distance(unit, One/i)
#                 d2 = d1 -1
#                 while d2 < d1 or goAgain:
#                     goAgain = False
#                     d2 = get_distance(unit, One/(i**(order+1)))
#                     if d2 < d1:
#                         order+=1
#                         d1 = d2
#                         goAgain = True
#                 if d1 < d:
#                     d = d1
#                     closest[0] = i
#                     # print(i)
#                     closest[1]=True
#                     closest[2]=order
              
#     if (closest[2])==0:
#           return str(closest[0])
#     else:
#         name = closest[0].abbrev
#     if d == 0:
#         s=""
#         if closest[1]:
#             s = "⁻"
#         u = s+name
#         for i in range(closest[2]-1):
#             u+= " "
#             u+= (s+name)
#         return u
#     if closest[1]:
#         return ("⁻"+name+" ")*closest[2] +__simplify(unit*(closest[0]**closest[2]), expU)
#     # print("closest:", closest[0], closest[2])
#     return ((closest[0]**closest[2]).abbrev+" ")+ __simplify(unit/(closest[0]**closest[2]), expU)

# def simplify(unit,expU=_explicit_units):
#     # print(unit)
#     if type(unit) == Quantity:
#         return str(unit.value)+" "+ simplify(unit.unit, expU)
#     if len(unit.vec) == 0:
#         return ""
#     units = {}
#     strn = __simplify(unit, expU)
#     for i in strn.split():
#         u = i
#         if i.startswith("⁻"):
#             u = u[1:]
#             if u in units:
#                 units[u] -= 1
#             else:
#                 units[u] = -1
#         else:
#             if u in units:
#                 units[u] += 1
#             else:
#                 units[u] = 1
#     strn = ""
#     for i in units:
#         if units[i] == 0:
#             pass
#         if units[i] == 1:
#             strn+=i
#         else:
#             strn+=(i+_to_superscript(units[i]))
#     return strn


# # todo: m3 rendering as m in certain scenarios??
# # todo: readme
# if __name__ == '__main__':
#     print("checking units...")
#     assert (1.5*V) * (10*mA) == 15*mW
#     assert (373.15*K) == (100*degC)
#     assert C/m3 == Pa/V
#     assert 1*F*V + A*s == 2*C
#     assert 3*L-L == round((m/20)*(m/5)*(m/5), 15)
#     assert L / (m*m*m) == 1/1000
#     assert (T/Pa/V*N*Hz) == 1
#     assert (kg*Wb/T/J*Hz**2) == 1
#     assert (Pa/V/A/Wb/N*W*H*C*m**2*Hz) == 1
#     assert ((kPa/V*Sv**3/C*N/W**3*H**2/W*A/Hz**3*g)==s**3/A**3)
#     assert (J/(N*m)) == 1
#     assert (1 - 5*m/m) == -4
#     assert (1000 - km/m) == (m/(2*m) - 1/2) == 0
#     assert ((N*s**2/m**4) == kg/m3) 
#     print("all tests passed")
