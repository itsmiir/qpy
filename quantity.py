

def lerp(a, b, delta):
    """quality is the percentage of sat. vapor in a mixture of sat vapor and sat liquid"""
    return a + (b - a) * delta

def getDelta(a, b, middle):
    return (middle - a)/(b - a) 

def flerp(x, x1, x2, y1, y2):
    return lerp(y1, y2, getDelta(x1, x2, x))

superscripts = {
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

def toSuperscript(num):
    # print(num)
    n = str(num)
    newN = ""
    for i in n:
        newN += superscripts[i]
    return newN        

class Unit(object):
    """docstring for Unit"""
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

    def base(symbol, ):
        pass
    def copy(self):
        newUnit = Unit(self.vec.copy(), self.name, self.factor, self.offset)
        return newUnit

    def derived(unit, name, factor=1, offset=0):
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
                raise ArithmeticError
        selfs = self.vec.copy()
        others = other.vec.copy()
        for k in others:
            if k in selfs:
                selfs[k] = others[k] + selfs[k]
            else:
                selfs[k] = others[k]
        for k in selfs:
            if not selfs[k] == 0:
                return Unit(selfs, "", self.factor*other.factor)
        return self.factor * other.factor
    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        unit = self.copy()
        orig = self.copy()
        for i in unit.vec:
            unit.vec[i] *= other
        unit.factor = unit.factor**other
        return unit

    def __truediv__(self, other):
        if type(other) == Quantity:
            return Quantity(self.factor, self)/other
        elif type(other) != Unit:
            return Quantity(self.factor/other, self)
        selfs= self.vec.copy()
        others=other.vec.copy()
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
        return One/self * other

    def __eq__(self, other):
        # print(self.factor, other.factor)
        if type(other) == Unit and other.factor == self.factor:
            return self / other == 1
        if self.factor != 1 or self.offset != 0:
            return 1*self == other
        else:
            return len(self.vec) == 0 and other == self.factor

    def __str__(self):
        strin = ""
        l=len(self.vec)
        # self.vec = sorted(self.vec.items(), key=lambda x:x[1], reverse=True)
        for k in sorted(self.vec):
            if self.vec[k] == 0:
                pass
            elif self.vec[k] != 1:
                strin +=(k + toSuperscript(self.vec[k]))
            else:
                strin +=(k)
        if self.factor != 1:
            return str(self.factor) + " "+ strin
        else:
            return strin

    def dotProduct(self, other):
        k=0
        for i in self.vec:
            try:
                k += self.vec[i]*other.vec[i]
            except KeyError as e:
                pass
        return k
    def orthogonal(self, other):
        for i in self.vec:
            try:
                if not self.vec[i]*other.vec[i] == 0:
                    return False
            except KeyError as e:
                pass
        return True
    def termsOf(self, other):
        return (1*self).termsOf(other)
    


class Quantity(object):
    """docstring for Quantity"""
    def __init__(self, value, unit, digits:int=0):
        if type(unit) == Quantity:
            self.unit = unit.unit
            self.value = unit.value*value # lmao
        else:
            self.unit = unit.copy()
            self.value = (value*unit.factor)+unit.offset
            self.unit.factor = 1
            self.unit.offset = 0
        self.digits = digits

    def __add__(self, other):
        if type(other) == Unit:
            return self + Quantity(1, other)
        if not other.unit == self.unit:
            raise ArithmeticError("Incompatible units: "+ simplify(self.unit)+ " and "+ simplify(other.unit))
        return Quantity(self.value+other.value, self.unit)
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -1 * other
    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
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
        return self * (1/other)

    def __round__(self, i):
        return Quantity(round(self.value, i), self.unit)
    def __str__(self):
        if self.digits > 0:
            val = round(self.value, self.digits)
        else:
            val = self.value
        return str(val)+" "+str(simplify(self.unit))
    def __eq__(self, other):
        if type(other) == Unit:
            return self == Quantity(1, other)
        return other.value == self.value and other.unit == self.unit
    def __pow__(self, other):
        return Quantity(self.value**other, self.unit**other)
    def termsOf(self, other,rnd: int=0)->str:
        if type(other) == Unit:
            return self.termsOf(1*other, rnd)
        elif type(other) == Quantity:
            if self.unit != other.unit:
                raise ArithmeticError("Incompatible units: "+ simplify(self.unit)+ " and "+ simplify(other.unit))
            val = self.value/other.value
            if rnd > 0:
                val = round(val, rnd)
            return (str(val)+" "+other.unit.name)
    def round(self, digits):
        return Quantity(self.value, self.unit, digits)


# prefix definitions
def pico(unit):
    return Unit.derived(unit, "p"+unit.name, 1e-12)
def nano(unit):
    return Unit.derived(unit, "n"+unit.name, 1e-9)
def micro(unit):
    return Unit.derived(unit, "μ"+unit.name, 1e-6)
def milli(unit):
    return Unit.derived(unit, "m"+unit.name, 1e-3)

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

# unit definitions: base
s = Unit({"s": 1}, "s")
m = Unit({"m": 1}, "m")
kg = Unit({"kg": 1}, "kg")
A = Unit({"A": 1}, "A")
K = Unit({"K": 1}, "K")
cd = Unit({"cd": 1}, "cd")
mol = 6.02214076e23

# unit definitions: derived
One = Unit({},"") # unitless unit; for 1/<unit>
Hz = Unit.derived(One/s, "Hz")
N = Unit.derived(kg*m/s/s, "N")
Pa = Unit.derived(N/m/m, "Pa")
J = Unit.derived(N*m, "J")
W = Unit.derived(J/s, "W")
C = Unit.derived(s*A, "C")
V = Unit.derived(W/A, "V")
F = Unit.derived(C/V, "F")
Ohm = Unit.derived(V/A, "Ω")
S = Unit.derived(One/Ohm, "S")
Wb = Unit.derived(V*s, "Wb")
T = Unit.derived(Wb/m/m, "T")
H = Unit.derived(Wb/A, "H")
Sv = Unit.derived(J/kg, "Sv")


# non-standard derived units: baseUnit = derivedUnit*factor + offset
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

Gm = giga(m)
Mm = mega(m)
km = kilo(m)
mm = milli(m)
um = micro(m)
nm = nano(m)
au = Unit.derived(m, "au", 149597870700)

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

kOhm = kilo(Ohm)
MOhm = mega(Ohm)
GOhm = giga(Ohm)

kHz = kilo(Hz)
MHz = mega(Hz)
GHz = giga(Hz)
THz = tera(Hz)

g = Unit.derived(kg, "g", 0.001)
mg = milli(g)
ug = micro(g)
ng = nano(g)


# units that printed answers can be expressed in
# includes all listed derived units except Sv because i find that J/kg is often more useful by itself
# ordering: a unit must always go before its inverse (i.e., s must go before Hz) so that the unit simplifier
# does not use units of 1/Hz for time!
# updating this list (via addUnits or setUnits, please) will change what values get simplified
units = [
    J, W, N, Pa, C, F, V, Ohm, S, Wb, T, H, kg, m, A, K, cd, s, Hz
]
def addBaseUnit(unit):
    units.append(unit)
def setUnits(us):
    units = us
def getUnits():
    return units

# units that will not be simplified; e.g., m/s² will not be simplified to N/kg
explicitUnits = [
    # m*m, m*m*m,
    # m/s, m/s**2,

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
    return (sum)**.5

def __simplify(unit, expU, units=units):
    """if you're curious, this function sequentially factors out the "closest" unit to the unit being tested;
    "closest" being defined via euclidean (ish) distance in 6D base-SI-unit space
    """
    if type(unit) != Unit:
        return ""
    for i in expU:
        if unit == i:
            return str(unit)
    d = getDistance(unit, units[0])
    closest = [units[0], False, 1]
    for i in units:
        order = 1
        goAgain = False
        if not unit.orthogonal(i):
            if unit.dotProduct(i) > 0:
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
                d1 = getDistance(unit, One/i)
                d2 = d1 -1
                while d2 < d1 or goAgain:
                    goAgain = False
                    d2 = getDistance(unit, One/(i**(order+1)))
                    if d2 < d1:
                        order+=1
                        d1 = d2
                        goAgain = True
                if d1 < d:
                    d = d1
                    closest[0] = i
                    # print(i)
                    closest[1]=True
                    closest[2]=order
              
    if (closest[2])==0:
          return str(closest[0])
    else:
        name = closest[0].name
    if d == 0:
        s=""
        if closest[1]:
            s = "⁻"
        u = s+name
        for i in range(closest[2]-1):
            u+= " "
            u+= (s+name)
        return u
    if closest[1]:
        return ("⁻"+name+" ")*closest[2] +__simplify(unit*(closest[0]**closest[2]), expU)
    # print("closest:", closest[0], closest[2])
    return ((closest[0]**closest[2]).name+" ")+ __simplify(unit/(closest[0]**closest[2]), expU)

def simplify(unit,expU=explicitUnits):
    # print(unit)
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
    for i in units:
        if units[i] == 0:
            pass
        if units[i] == 1:
            strn+=i
        else:
            strn+=(i+toSuperscript(units[i]))
    return strn


# todo: conversion factors
# todo: readme
if __name__ == '__main__':
    print("checking units...")
    assert (1.5*V) * (10*mA) == 15*mW
    assert (373.15*K) == (100*degC)
    assert C/m3 == Pa/V
    assert 1*F*V + A*s == 2*C
    assert 3*L-L == round((m/20)*(m/5)*(m/5), 15)
    assert L / (m*m*m) == 1/1000
    assert (T/Pa/V*N*Hz) == 1
    assert (kg*Wb/T/J*Hz**2) == 1
    assert (Pa/V/A/Wb/N*W*H*C*m**2*Hz) == 1
    assert ((kPa/V*Sv**3/C*N/W**3*H**2/W*A/Hz**3*g)==s**3/A**3)
    assert (1) == 1
    assert((N*s**2/m**4) == kg/m3)
    print("all tests passed")
