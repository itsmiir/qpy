"""Contains logic for Units, the basis of physical calculation.
"""
from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from qntpy.core.quantity import Quantity
from qntpy.core.dimension import DimVec, Dim
from qntpy.rep import rep

class Unit(object):
    """Represents a physical unit.
    
    The easiest way to create a new unit is to multiply some base units together. For example, a
    unit of delta-v for a spacecraft could be created like so:
    ```
    from qntpy import m, s
    dv_unit = m / s
    ```
    `dv_unit` can now be used as an alias for `m/s`. If you want your unit to have a custom 
    symbol, use `Unit.derived`:
    ```
    >>> from qntpy import m, s
    >>> dv_unit = Unit.derived(m/s, "deev")
    ```
    You can also make units from scratch, but using either multiplication of primitive units or
    `Unit.derived` is usually simpler and cleaner.
    
    """
    def __init__(self, 
                 vec: DimVec[Dim, int], 
                 symbol: str, 
                 factor: float=1, 
                 offset: float=0,
                 ) -> Unit:
        """Create a new unit, and return it. 
        
        
        The `vec` parameter is a `DimVec` (`dict` wrapper) of `{`Dim`: int}` where each key represents a base unit, and each value represents
        the power to which that unit is raised. For example, the unit `N` (newton) has the `vec`
        ```
        {Dim.M: 1, Dim.L: 1, Dim.T: -2}.
        ```
        
        By default, qntpy utilizes the following base units:
        - `s`: Time [T], equal to one second.
        - `kg`: Mass [M], equal to one kilogram.
        - `m`: Length [L], equal to one meter.
        - `A`: Electric current [I], equal to one ampere.
        - `K`: Thermodynamic temperature [Θ], equal to one kelvin.
        - `mol`: Amount of substance [N], equal to one mol.
        - `cd`: Luminous intensity [J], equal to one candela.
        
        Additionally, the `qntpy.information` module defines:
        - `b`: Information, equal to one bit.
        
        Additionally, the `qntpy.currency` module defines:
        - `$`: Currency, equal to one United States dollar (by default the module updates currency
        conversions once per day via an API).
        
        However, the module supports user-defined base units that can be added to the vector.
        
        ---
        The new unit has the symbol `symbol`, and is equal to the linear combination of base units defined
        in its `vec`, TIMES `factor`. For example, the unit `kN` (kilonewton) has `factor` equal to `1000`.
        
        Zero of the new unit is equal to the linear combination of base units defined in its `vec`, TIMES 
        `offset`. For example, the unit `degC` (degrees Celsius) has `factor` equal to `1` and `offset` equal
        to `273.15`.
        
        Args:
        - vec: A linear combination of base units that the new unit comprises.
        - symbol: The symbol for the unit.
        - factor: One of the new unit is equal to `factor` + `offset` * `base_unit`.
        - offset: 0 * the new unit = `offset` * `base_unit`.
        """
        self.vec = vec.copy()
        for i in vec:
            if vec[i] == 0:
                del self.vec[i]
        self.symbol = symbol
        self.factor = factor
        self.offset = offset

    @staticmethod
    def derived(base_unit: Unit, symbol: str, factor:float=1, offset:float=0) -> Unit:
        """Create a new derived unit, and return it.
        
        The new unit has the symbol `symbol`, is equal to `factor * base_unit`, and
        `0 * new_unit` is equal to `offset * base_unit`.
        
        Args:
        - base_unit: [`Unit`] The unit on which to base this one.
        - symbol: [`str`] The symbol for the unit.
        - factor: [`float`] One of the new unit is equal to `factor` * `base_unit`.
        - offset: [`float`] 0 * the new unit = `offset` * `base_unit`.
        """
        new_unit = deepcopy(base_unit)
        new_unit.factor = base_unit.factor*factor
        new_unit.offset = base_unit.offset+offset
        new_unit.symbol = symbol
        return new_unit

    def __mul__(self, other: Any) -> Unit | Quantity:
        if type(other) != Unit:
            try:
                return Quantity(other, self)
            except:
                raise ArithmeticError(f"Cannot multiply instance of Unit with instance of class {type(other)}!")
        selfs = self.vec.copy()
        others = other.vec.copy()
        for k in others:
            if k in selfs:
                selfs[k] = others[k] + selfs[k]
            else:
                selfs[k] = others[k]
        for k in selfs:
            if not selfs[k] == 0:
                return Unit(selfs, rep.concat_symbols(self.symbol, other.symbol, rep.Op.MUL), self.factor*other.factor)
        return self.factor * other.factor
    def __rmul__(self, other: Any) -> Unit | Quantity:
        return self * other

    def __pow__(self, other: float) -> Unit:
        unit = deepcopy(self)
        for i in unit.vec:
            unit.vec[i] *= other
        unit.factor = unit.factor**other
        return unit
    def __neg__(self) -> Unit:
        return -1*self
    def __pos__(self) -> Unit:
        return self
    def __truediv__(self, other: Any) -> Unit | Quantity:
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
                return Unit(selfs,self.symbol+"/"+other.symbol, self.factor/other.factor)
        return self.factor / other.factor
        # return Unit({}, "", self.factor/other.factor)
    def __rtruediv__(self, other: Any) -> Unit | Quantity:
        return One/self * other

    def __eq__(self, other: Any) -> bool:
        if type(other) == Unit and other.factor == self.factor:
            return self / other == 1
        if self.factor != 1 or self.offset != 0:
            return 1*self == other
        else:
            return len(self.vec) == 0 and other == self.factor

    def __str__(self) -> str:
        
    def __repr__(self) -> str:
        return str(self)
    def __float__(self) -> float:
        return self.factor
    def __int__(self) -> int:
        return int(float(self))
    def _dot_product(self, other: Unit) -> int:
        k=0
        for i in self.vec:
            try:
                k += self.vec[i]*other.vec[i]
            except KeyError as e:
                pass
        return k
    def _orthogonal(self, other: Unit | Quantity) -> bool:
        for i in self.vec:
            try:
                if not self.vec[i]*other.vec[i] == 0:
                    return False
            except KeyError as e:
                pass
        return True
    def terms_of(self, other: Unit | Quantity, rnd: int=-1) -> str:
        return (1*self).terms_of(other, rnd)
    
    
    # prefix definitions
    @staticmethod
    def pico(unit: Unit):
        return Unit.derived(unit, "p"+unit.abbrev, 1e-12)
    def nano(unit):
        return Unit.derived(unit, "n"+unit.abbrev, 1e-9)
    def micro(unit):
        return Unit.derived(unit, "μ"+unit.abbrev, 1e-6)
    def milli(unit):
        return Unit.derived(unit, "m"+unit.abbrev, 1e-3)

    def kilo(unit):
        return Unit.derived(unit, "k"+unit.abbrev, 1e3)
    def mega(unit):
        return Unit.derived(unit, "M"+unit.abbrev, 1e6)
    def giga(unit):
        return Unit.derived(unit, "G"+unit.abbrev, 1e9)
    def tera(unit):
        return Unit.derived(unit, "T"+unit.abbrev, 1e12)
    def peta(unit):
        return Unit.derived(unit, "P"+unit.abbrev, 1e15)
