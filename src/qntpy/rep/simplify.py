from qntpy.rep.rep import to_superscript
from qntpy.core.unit import Unit
from qntpy.core.units import base_units, derived_units, m, s, J, kg
from qntpy.core.quantity import Quantity
from qntpy.util.exceptions import IncommensurableError

_explicit_units = {
    
}

_units_to_use = base_units + derived_units # in order of priority

def get_dist_squared(unit1: Unit, unit2: Unit) -> float:
    return (unit2.vec - unit1.vec).mag2
   
def dot_product(unit: Unit, other: Unit) -> int:
    total: int = 0
    for dim in unit.vec:
        try:
            total += unit.vec[dim]*other.vec[dim]
        except KeyError:
            pass
    return total

def orthogonal(unit_1, unit_2: Unit | Quantity) -> bool:
    return not dot_product(unit_1, unit_2) # we're working with ints, so shouldn't be a problem

def __simplify(unit: Unit, expl_units: dict[Unit, str]):
    """if you're curious, this function sequentially factors out the "closest" unit to the unit being tested;
    "closest" being defined via euclidean (ish) distance in 7D base-SI-unit space.
    
    Args:
    - unit: the `Unit` to simplify. If not `isinstance` `Unit`, then an empty string will be returned.
    - expl_units: a `dict` of `[Unit, str]` pairs. Any unit matching one of these units will be represented like this.
    """
    if not isinstance(unit, Unit):
        return ""
    for unit_to_check in expl_units:
        if unit == unit_to_check:
            return expl_units[unit_to_check]
    _units: tuple[Unit] = tuple(filter(lambda x: dot_product(unit, x), _units_to_use))
    
    closest_unit_dist = get_dist_squared(unit, _units[-1]) + 1 # it is guaranteed that at least one unit will have a smalller dist than this
    closest_unit = _units[-1]
    closest_unit_is_negative = False
    closest_unit_exponent = 1
    closest_unit_symbol = _units[-1].symbol
    for unit_to_check in _units:
        symbol = unit_to_check.symbol
        unit_is_negative = False
        exponent = 1
        go_again = False
        if dot_product(unit, unit_to_check) < 0:
            unit_to_check = unit_to_check.invert()
            unit_is_negative = True
        distance_btwn = get_dist_squared(unit, unit_to_check)
        dist_betwn_2 = distance_btwn - 1
        while dist_betwn_2 < distance_btwn or go_again:
            go_again = False
            dist_betwn_2 = get_dist_squared(unit, (unit_to_check**(exponent+1)))
            if dist_betwn_2 < distance_btwn:
                exponent += 1
                distance_btwn = dist_betwn_2
                go_again = True
        if distance_btwn < closest_unit_dist:
            closest_unit_dist = distance_btwn
            closest_unit = unit_to_check
            closest_unit_exponent = exponent
            closest_unit_symbol = symbol
            closest_unit_is_negative = unit_is_negative
    
    s = "⁻" if closest_unit_is_negative else ''  
    if closest_unit_dist == 0:
        u = s+closest_unit_symbol
        for i in range(closest_unit_exponent-1):
            u += " "
            u += (s+closest_unit_symbol)
        return u
    return (s+closest_unit_symbol+" ") * closest_unit_exponent + __simplify(unit / (closest_unit**closest_unit_exponent), expl_units)

def simplify(value: Quantity | Unit, exp_units: list=_explicit_units) -> str:
    if isinstance(value, Quantity):
        return f"{str(value.value)} {simplify(value.unit, exp_units)}"
    elif isinstance(value, Unit):
        if value.vec.is_empty():
            return ""
        units = {}
        strn = __simplify(value, exp_units)
        # fill out the units dict
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
        unitkeys_sorted = sorted(units, key=lambda k: units[k], reverse=True)
        for i in unitkeys_sorted:
            if units[i] == 0:
                pass
            elif units[i] == 1:
                strn+=i
            else:
                strn+=(i+to_superscript(units[i]))
            strn += " "
        return strn.strip()
    else:
        try:
            return value.__simplify__(exp_units)
        except AttributeError:
            return str(value)
