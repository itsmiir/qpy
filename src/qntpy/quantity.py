from math import pi as _pi
import sys as _sys
import json as _json
import os as _os

_NATURAL_UNITS_MODE = "natural mode"
_CONFIG = {
    _NATURAL_UNITS_MODE: False
}

def naturalUnits() -> bool:
    return _CONFIG[_NATURAL_UNITS_MODE]

_sys.path.append(".")

_directory = _os.path.dirname(_os.path.abspath(__file__))
with open(_directory+"/config.json") as f:
    _CONFIG = _json.load(f)

def toggleNaturalMode():
    """this is an experimental setting that redefines every constant such that the speed of light is 1 (unitless).
    it's intentionally obtuse to use because i'm not quite sure that it works properly.
    """
    if (naturalUnits()):
        _CONFIG[_NATURAL_UNITS_MODE] = False
        print("natural units mode off! restart to apply!")
        with open(_directory+"/config.json", "w") as f:
            f.write(_json.dumps(_CONFIG))
    else:
        _CONFIG[_NATURAL_UNITS_MODE] = True
        print("natural units mode on! the speed of light is 1!")
        print("this feature is highly experimental and will likely break some functionality!")
        print("restart to apply!")
        with open(_directory+"/config.json", "w") as f:
            f.write(_json.dumps(_CONFIG))

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

def _toSuperscript(num):
    n = str(num)
    newN = ""
    for i in n:
        newN += _superscripts[i]
    return newN        

class Unit(object):
    """represents a base or derived unit"""
    def __init__(self, vec, name="", factor=1, offset=0):
        # super(Unit, self).__init__()
        self.vec = vec.copy()
        for i in vec:
            if vec[i] == 0:
                del self.vec[i]
        del vec
        self.name = name
        self.factor = factor
        self.offset = offset

    def copy(self):
        newUnit = Unit(self.vec.copy(), self.name, self.factor, self.offset)
        return newUnit

    def derived(unit, name, factor=1, offset=0):
        """creates a new derived unit."""
        if (type(unit) == float):
            return Unit({},name, factor, offset)
        newUnit = unit.copy()
        newUnit.factor = unit.factor*factor
        newUnit.offset = unit.offset+offset
        newUnit.name = name
        return newUnit

    def __mul__(self, other):
        if type(other) != Unit:
            try:
                return Quantity(other, self)
            except:
                raise ArithmeticError()
        selfs = self.vec.copy()
        others = other.vec.copy()
        for k in others:
            if k in selfs:
                selfs[k] = others[k] + selfs[k]
            else:
                selfs[k] = others[k]
        for k in selfs:
            if not selfs[k] == 0:
                return Unit(selfs, self.name+"•"+other.name, self.factor*other.factor)
        return self.factor * other.factor
    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        unit = self.copy()
        for i in unit.vec:
            unit.vec[i] *= other
        unit.factor = unit.factor**other
        return unit

    def pow(self, exp):
        """computes self**exp"""
        newUnit = _One
        if exp != round(exp):
            raise ArithmeticError("cannot take non-integer exponent "+str(exp)+" of physical dimensions!")
        for u in self.vec:
            newUnit.vec[u]=self.vec[u]*exp
            newUnit.factor = self.factor**exp
        return newUnit
                
    def root(self, root):
        """computes (self)**(1/root)"""
        newUnit = _One
        if root != round(root):
            raise ArithmeticError("cannot take non-integer root "+str(root)+" of physical dimensions!")
        for u in self.vec:
            if self.vec[u] % root != 0:
                raise ArithmeticError("cannot take root "+str(root)+" of unit "+str(self)+"!")
            newUnit.vec[u]=self.vec[u]/root
            newUnit.factor = self.factor**(1/root)
        return newUnit

    def __neg__(self):
        return -1*self
    def __pos__(self):
        return self
    def __truediv__(self, other):
        if type(other) == Quantity:
            return Quantity(self.factor, self)/other
        elif type(other) != Unit:
            return Quantity(1/other, self)
        selfs  = self.vec.copy()
        others = other.vec.copy()
        for k in others:
            if k in selfs:
                selfs[k] = -others[k] + selfs[k]
            else:
                selfs[k] = -others[k]
        for k in selfs:
            if not selfs[k] == 0:
                return Unit(selfs,self.name+"/"+other.name, self.factor/other.factor)
        return self.factor / other.factor
        # return Unit({}, "", self.factor/other.factor)
    def __rtruediv__(self, other):
        return _One/self * other

    def __eq__(self, other):
        if type(other) == Unit and other.factor == self.factor:
            return self / other == 1
        if self.factor != 1 or self.offset != 0:
            return 1*self == other
        else:
            return len(self.vec) == 0 and other == self.factor

    def _getVecStr(self):
        strin = ""
        for k in sorted(self.vec, key=lambda k: abs(self.vec[k]-1), reverse=True):
            if self.vec[k] == 0:
                pass
            elif self.vec[k] != 1:
                strin +=(k + _toSuperscript(self.vec[k]))
            else:
                strin +=(k)
        return strin
    def __str__(self):
        # if self._isBase():
        return self.name
        if self.factor != 1:
            return str(self.factor) + " "+ simplify(self)
        else:
            return simplify(self)
    
    def _isBase(self):
        v = 0
        for u in self.vec:
            v += self.vec[u]
        return v == 1 or v == 0

    def __repr__(self) -> str:
        return str(self)
    def __float__(self):
        return self.factor
    def __int__(self):
        return int(float(self))
    def _dotProduct(self, other):
        k=0
        for i in self.vec:
            try:
                k += self.vec[i]*other.vec[i]
            except KeyError as e:
                pass
        return k
    def _orthogonal(self, other):
        for i in self.vec:
            try:
                if not self.vec[i]*other.vec[i] == 0:
                    return False
            except KeyError as e:
                pass
        return True
    def termsOf(self, other, rnd=-1):
        return (1*self).termsOf(other, rnd)
    def getDisplayName(self):
        pass

class Quantity(object):
    """represents a numerical value with an attached unit"""
    def __init__(self, value, unit, digits:int=0):
        if type(unit) == Quantity:
            self.unit = unit.unit
            self.value = unit.value*value # lmao
        else:
            try:
                self.unit = unit.copy()
                self.value = (value*self.unit.factor)+self.unit.offset
            except AttributeError:
                self.unit = _One
                self.value = value
            self.unit.factor = 1
            self.unit.offset = 0
        self.digits = digits

    def __add__(self, other):
        if type(other) == Unit:
            return self + Quantity(1, other)
        elif type(other) == Quantity:
            if not other.unit == self.unit and other.value != 0 and self.value != 0:
                raise ArithmeticError("Incompatible units: "+ simplify(self.unit)+ " and "+ simplify(other.unit))
            return Quantity(self.value+other.value, self.unit)
        else:
            if self.unit == _One:
                return self.value + other
            elif other == 0:
                return self
            else:
                raise ArithmeticError("Incompatible units: "+str(self)+" and "+str(other))
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
            return self * Quantity(1, other)
        elif type(other) == Quantity:
            return Quantity(self.value*other.value, self.unit*other.unit)
        else:
            return Quantity(other*self.value, self.unit)
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if type(other) == Unit:
            return self / Quantity(1, other)
        elif type(other) == Quantity:
            if other.unit == self.unit:
                return self.value/other.value
            return Quantity(self.value/other.value, self.unit/other.unit)
        else:
            return Quantity(self.value/other, self.unit)
    def __rtruediv__(self, other):
        return (_One/self) * other

    def __round__(self, i):
        return Quantity(round(self.value, i), self.unit)

    def __cmp__(self, other):
        return (self - other).value

    def __str__(self):
        if self.digits > 0:
            val = round(self.value, self.digits)
        else:
            val = self.value
        return str(val)+" "+str(simplify(self.unit))
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
        elif self.unit == _One:
            return self.value == other
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
        if round(other) == other:
            return self.pow(other)
        else:
            if round(1/other) == 1/other:
                return self.root(1/other)
        raise ArithmeticError("cannot compute "+str(self.unit)+" to the nth power!")
    
    def pow(self, exp):
        """computes self**exp"""
        return Quantity(self.value**exp, self.unit.pow(exp))
                
    def root(self, root):
        """computes (self)**(1/root)"""
        return Quantity(self.value**(1/root), self.unit.root(root))

    def termsOf(self, other,rnd: int=-1)->str:
        if type(other) == Unit:
            if (other.offset != 0):
                val = (self.value-other.offset) / other.factor
                return (str(val)+" "+other.name)
            return self.termsOf(1*other, rnd)
        elif type(other) == Quantity:
            if self.unit != other.unit:
                raise ArithmeticError("Incompatible units: "+ simplify(self.unit)+ " and "+ simplify(other.unit))
            val = self.value/(other.value)+other.unit.offset
            if rnd > -1:
                val = round(val, rnd)
            return (str(val)+" "+other.unit.name)
    def round(self, digits):
        return Quantity(self.value, self.unit, digits)


# prefix definitions
def quecto(unit):
    return Unit.derived(unit, "q"+unit.name, 1e-15)
def ronto(unit):
    return Unit.derived(unit, "r"+unit.name, 1e-15)
def yocto(unit):
    return Unit.derived(unit, "y"+unit.name, 1e-15)
def zepto(unit):
    return Unit.derived(unit, "z"+unit.name, 1e-15)
def atto(unit):
    return Unit.derived(unit, "a"+unit.name, 1e-18)
def femto(unit):
    return Unit.derived(unit, "f"+unit.name, 1e-15)
def pico(unit):
    return Unit.derived(unit, "p"+unit.name, 1e-12)
def nano(unit):
    return Unit.derived(unit, "n"+unit.name, 1e-9)
def micro(unit):
    return Unit.derived(unit, "μ"+unit.name, 1e-6)
def milli(unit):
    return Unit.derived(unit, "m"+unit.name, 1e-3)
def centi(unit):
    return Unit.derived(unit, "c"+unit.name, 1e-2)
def deci(unit):
    return Unit.derived(unit, "d"+unit.name, 1e-1)
# --- #
def deka(unit):
    return Unit.derived(unit, "da"+unit.name, 1e1)
def hecto(unit):
    return Unit.derived(unit, "h"+unit.name, 1e2)
def kilo(unit):
    return Unit.derived(unit, "k"+unit.name, 1e3)
def mega(unit):
    return Unit.derived(unit, "M"+unit.name, 1e6)
def giga(unit):
    return Unit.derived(unit, "G"+unit.name, 1e9)
def tera(unit):
    return Unit.derived(unit, "T"+unit.name, 1e12)
def peta(unit):
    return Unit.derived(unit, "P"+unit.name, 1e15)
def exa(unit):
    return Unit.derived(unit, "P"+unit.name, 1e18)
def zetta(unit):
    return Unit.derived(unit, "Z"+unit.name, 1e21)
def yotta(unit):
    return Unit.derived(unit, "Y"+unit.name, 1e24)
def ronna(unit):
    return Unit.derived(unit, "R"+unit.name, 1e27)
def quetta(unit):
    return Unit.derived(unit, "Q"+unit.name, 1e30)

# unit definitions: base
s = Unit({"s": 1}, "s")
m = Unit({"m": 1}, "m")
if naturalUnits():
    print("warning: using experimental natural units mode. c = 1!")
    m = Unit.derived(s, "m", 1/299792458)
kg = Unit({"kg": 1}, "kg")
A = Unit({"A": 1}, "A")
K = Unit({"K": 1}, "K")
cd = Unit({"cd": 1}, "cd")
mol = 6.02214076e23

# unit definitions: derived
_One = Unit({},"") # unitless unit; for 1/<unit>
rad = _One # just for readability
pct = Unit.derived(_One, "%", .01)

Hz = Unit.derived(_One/s, "Hz")
N = Unit.derived(kg*m/s/s, "N")
Pa = Unit.derived(N/m/m, "Pa")
J = Unit.derived(N*m, "J")

if naturalUnits():
    W = N
else:
    W = Unit.derived(J/s, "W")
C = Unit.derived(s*A, "C")
V = Unit.derived(W/A, "V")
F = Unit.derived(C/V, "F")
ohm = Unit.derived(V/A, "Ω")
S = Unit.derived(_One/ohm, "S")
Wb = Unit.derived(V*s, "Wb")
T = Unit.derived(Wb/m/m, "T")
H = Unit.derived(Wb/A, "H")
if naturalUnits():
    Sv = _One
else:
    Sv = Unit.derived(J/kg, "Sv")
# non-standard derived units: baseUnit = derivedUnit*factor + offset
deg = Unit.derived(rad, "⁰", 0.01745329)

degC = Unit.derived(K, "⁰C", 1, 273.15)

L = Unit.derived(m*m*m, "L", 0.001)
mL = Unit.derived(L, "mL", 0.001)

ms = milli(s)
us = micro(s)
ns = nano(s)
ps = pico(s)
minute = Unit.derived(s, "min", 60)
hr = Unit.derived(minute, "hr", 60)
day = Unit.derived(hr, "d", 24)
wk = Unit.derived(day, "wk", 7)
# not even gonna try to do months
yr = Unit.derived(day, "yr", 365.25)
My = Unit.derived(yr, "My", 1e6)
aeon = Unit.derived(yr, "AE", 1e9)

cal = Unit.derived(J, "cal", 4.184)
kcal = kilo(cal)

eV = Unit.derived(J, "eV", 1.602176634e-19)
keV = kilo(eV)
MeV = mega(eV)
GeV = giga(eV)
TeV = tera(eV)

kN = kilo(N)
MN = mega(N)
GN = giga(N)

eVc2 = Unit.derived(kg, "(eV/c²)", 1.78266192e-36)
keVc2= kilo(eVc2)
MeVc2= mega(eVc2)
GeVc2= giga(eVc2)
TeVc2= tera(eVc2)

kPa = kilo(Pa)
MPa = mega(Pa)
GPa = giga(Pa)
mmHg = Unit.derived(Pa, "mmHg", 133.3224)
atm = Unit.derived(Pa, "atm", 101325)

kJ = kilo(J)
MJ = mega(J)
GJ = giga(J)

Wh = Unit.derived(W*hr, "Wh")
kWh = kilo(Wh)
MWh = mega(Wh)
GWh = giga(Wh)
TWh = tera(Wh)

mW = milli(W)
kW = kilo(W)
MW = mega(W)
GW = giga(W)
TW = tera(W)

nm = nano(m)
um = micro(m)
mm = milli(m)
cm = Unit.derived(m, "cm", 0.01)
km = kilo(m)
Gm = giga(m)
Mm = mega(m)
AU = Unit.derived(m, "AU", 149597870700)
pc = Unit.derived(AU, "pc", 648000/_pi)
ly = Unit.derived(m, "ly", 9460730472580800)

m2 = Unit.derived(m*m, "(m²)")
m3 = Unit.derived(m*m*m, "(m³)")
ha = Unit.derived(m2, "ha", 10000)

kA = kilo(A)
mA = milli(A)

kV = kilo(V)
mV = milli(V)

mF = milli(F)
uF = micro(F)
nF = nano(F)
pF = pico(F)

mH = milli(H)
uH = micro(H)
nH = nano(H)

kohm = kilo(ohm)
Mohm = mega(ohm)
Gohm = giga(ohm)

kHz = kilo(Hz)
MHz = mega(Hz)
GHz = giga(Hz)
THz = tera(Hz)

g = Unit.derived(kg, "g", 0.001)
mg = milli(g)
ug = micro(g)
ng = nano(g)
Da = Unit.derived(kg, "Da", 1.66053906660e-27)


# units that printed answers can be expressed in
# includes most named, derived units except Sv because i find that J/kg is often more useful by itself
# ordering: a unit must always go before its inverse (i.e., s must go before Hz) so that the unit simplifier
# does not use units of 1/Hz for time!
# updating this list (via addBaseUnit, please) will change what values get simplified
units = [
    C, kg, A, K, cd, s, Hz
]
def addBaseUnit(unit):
    units.append(unit)

if (not naturalUnits()):
    # energy == mass,
    # distance == time,
    # power == force

    units.append(m)
    units.append(N)
    units.append(J)
    units.append(Pa)
    units.append(F)
    units.append(V)
    units.append(ohm)
    units.append(W)
    units.append(H)
    units.append(T)
    units.append(Wb)
    units.append(S)


def setUnits(us):
    units = us
def getUnits():
    return units

# units that will not be simplified; e.g., m/s² will not be simplified to N/kg
explicitUnits = [
    m*m, m*m*m,
    m/s, m/s**2,

]
def addExplicit(unit):
    explicitUnits.append(unit)
def setExplicits(units):
    explicitUnits = units
def getExplicits():
    return explicitUnits

def getDistance(unit1, unit2):
    d = unit2/unit1
    sum = 0
    if type(d) != Unit:
        return 0
        # try:
        #     return unit1.factor - unit2.factor
        # except AttributeError:
        #     pass
    for i in d.vec:
        sum+=(d.vec[i]**2)
    return (sum)
def __simplify(unit, expU, units=units):
    """if you're curious, this function sequentially factors out the "closest" unit to the unit being tested;
    "closest" being defined via euclidean (ish) distance in 6D base-SI-unit space
    """
    if type(unit) != Unit:
        return ""
    if unit == Hz:
        return Hz.name
    for i in expU:
        if unit == i:
            return unit._getVecStr()
    d = getDistance(unit, units[0])
    closest = [units[0], False, 1]
    for i in units:
        order = 1
        goAgain = False
        if not unit._orthogonal(i):
            if unit._dotProduct(i) > 0:
                d1 = getDistance(unit, i)
                d2 = d1 - 1
                while d2 < d1 or goAgain:
                    goAgain = False
                    d2 = getDistance(unit, (i**(order+1)))
                    if d2 < d1:
                        order+=1
                        d1 = d2
                        goAgain = True
                if d1 < d:
                    d = d1
                    closest[0] = i
                    closest[1]=False
                    closest[2]=order
            else:
                d1 = getDistance(unit, _One/i)
                d2 = d1 -1
                while d2 < d1 or goAgain:
                    goAgain = False
                    d2 = getDistance(unit, _One/(i**(order+1)))
                    if d2 < d1:
                        order+=1
                        d1 = d2
                        goAgain = True
                if d1 < d:
                    d = d1
                    closest[0] = i
                    closest[1]=True
                    closest[2]=order

    closestUnit = closest[0]
    expIsNegative = closest[1]
    exponent = closest[2]
    exponentStr = ""

    if exponent != 1 or expIsNegative:
        if expIsNegative:
            exponentStr += "⁻";
        exponentStr += _toSuperscript(exponent)
    simplifiedStr = closestUnit.name + exponentStr
    if expIsNegative:
        newUnit = unit*(closestUnit**exponent)
    else:
        newUnit = unit/(closestUnit**exponent)
    if newUnit == _One:
        return simplifiedStr
    else:
        return simplifiedStr+ __simplify(newUnit, expU)

def simplify(unit,expU=explicitUnits):
    if type(unit) == Quantity:
        return str(unit.value)+" "+ simplify(unit.unit, expU)
    if len(unit.vec) == 0:
        return ""
    units = {}
    strn = __simplify(unit, expU)
    for i in strn.split():
        u = i
        if i.startswith("⁻"):
            u = u[1:]
            if u in units:
                units[u] -= 1
            else:
                units[u] = -1
        else:
            if u in units:
                units[u] += 1
            else:
                units[u] = 1
    strn = ""
    unitsSrt = sorted(units, key=lambda k: abs(units[k]-1), reverse=False)
    for i in unitsSrt:
        if units[i] == 0:
            pass
        if units[i] == 1:
            strn+=i
        else:
            strn+=(i+_toSuperscript(units[i]))
    return strn


# todo: readme
if __name__ == '__main__':
    pass
