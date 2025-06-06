from qntpy.rep.rep import to_superscript
from qntpy.core.unit import Unit
from qntpy.core.units import base_units, derived_units, m, s
from qntpy.core.quantity import Quantity
from qntpy.util.exceptions import IncommensurableError

_explicit_units = [
    # m*m, m*m*m,
    # m/s, m/s**2,
]
_units = base_units + derived_units

def get_distance(unit1: Unit, unit2: Unit) -> float:
        d = unit2/unit1
        sum = 0
        if type(d) != Unit:
            return 0
        for i in d.vec:
            sum+=(d.vec[i]**2)
        return (sum)**.5
    
def __simplify(unit: Unit, expU: tuple[Unit]):
    """if you're curious, this function sequentially factors out the "closest" unit to the unit being tested;
    "closest" being defined via euclidean (ish) distance in 7D base-SI-unit space
    """
    if type(unit) != Unit:
        return ""
    for i in expU:
        if unit == i:
            return str(unit)
    d = get_distance(unit, _units[0])
    closest = [_units[0], False, 1]
    for i in _units:
        order = 1
        goAgain = False
        if not unit._orthogonal(i):
            if unit._dot_product(i) > 0:
                d1 = get_distance(unit, i)
                d2 = d1 - 1
                while d2 < d1 or goAgain:
                    goAgain = False
                    d2 = get_distance(unit, (i**(order+1)))
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
                d1 = get_distance(unit, 1/i)
                d2 = d1 -1
                while d2 < d1 or goAgain:
                    goAgain = False
                    d2 = get_distance(unit, 1/(i**(order+1)))
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
        name = closest[0].symbol
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
    return ((closest[0]**closest[2]).symbol+" ")+ __simplify(unit/(closest[0]**closest[2]), expU)

def simplify(value: Quantity | Unit, expU=_explicit_units):
    if isinstance(value, Quantity):
        return str(value.value)+" "+ simplify(value.unit, expU)
    elif isinstance(value, Unit):
        if len(value.vec) == 0:
            return ""
        units = {}
        strn = __simplify(value, expU)
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
                strn+=(i+to_superscript(units[i]))
        return strn
    return str(value)
