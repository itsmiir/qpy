"""Contains logic for Units, the basis of physical calculation."""
from __future__ import annotations

from typing import Any

from uncertainties.core import AffineScalarFunc

from qntpy.core import defs
from qntpy.core.dimension import DimVec, Dim
from qntpy.core.quantity import Quantity
from qntpy.util.exceptions import InvalidUnitError, IncommensurableError
from qntpy.rep import rep


class Unit:
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
    vec: DimVec[Dim, int]
    factor: float | AffineScalarFunc
    offset: float | AffineScalarFunc
    symbol: str
    prefix: int
    
    def __new__(cls, 
                vec: DimVec[Dim, int], 
                symbol: str | None=None, 
                factor: float | AffineScalarFunc=1, 
                offset: float | AffineScalarFunc=0,
                prefix: int=0, 
                ) -> float | AffineScalarFunc | Unit:
        return factor if vec.is_empty() else super().__new__(cls)
    def __init__(self, 
                 vec: DimVec[Dim, int], 
                 symbol: str | None=None, 
                 factor: float | AffineScalarFunc=1, 
                 offset: float | AffineScalarFunc=0,
                 prefix: int=0,
                 ) -> None:
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
        self.vec: DimVec = vec.copy()
        self._symbol: str = symbol
        self.factor = factor
        self.offset = offset
        self.prefix: int = prefix

    @property
    def symbol(self):
        if self.is_kg():
            self._symbol = 'g'
        if self._symbol is None:
            from qntpy.rep.simplify import simplify
            self._symbol = simplify(self)
        if rep.exponent_to_abbrev(self.prefix, self.is_kg()) == '':
            return self._symbol
        else:
            if len(self._symbol) <= 1:
                return f'{rep.exponent_to_abbrev(self.prefix, self.is_kg())}{self._symbol}'
            else:
                return f'{rep.exponent_to_abbrev(self.prefix, self.is_kg())}({self._symbol})'
    
    @symbol.setter
    def _set_symbol(self):
        raise NotImplementedError('Unit symbols cannot be manually modified')

    @property
    def std_dev(self) -> float:
        """Return the standard deviation of the `factor` of this Unit."""
        if isinstance(self.factor, AffineScalarFunc):
            return self.factor.std_dev
        else: return 0

    @staticmethod
    def derived(base_unit: Unit, symbol: str=None, factor:float=1, offset:float=0) -> Unit:
        """Create a new derived unit, and return it.
        
        The new unit has the symbol `symbol`, is equal to `factor * base_unit`, and
        `0 * new_unit` is equal to `offset * base_unit`.
        
        Args:
        - base_unit: [`Unit`] The unit on which to base this one.
        - symbol: [`str`] The symbol for the unit.
        - factor: [`float`] One of the new unit is equal to `factor` * `base_unit`.
        - offset: [`float`] 0 * the new unit = `offset` * `base_unit`.
        """
        new_unit = base_unit.copy()
        if isinstance(base_unit, Quantity):
            new_unit.factor = base_unit.unit.factor*factor
            new_unit.offset = base_unit.unit.offset+offset
            new_unit.prefix = base_unit.unit.prefix
        else:
            new_unit.factor = base_unit.factor*factor
            new_unit.offset = base_unit.offset+offset
            new_unit.prefix = base_unit.prefix
        new_unit._symbol = symbol
        return new_unit
        
    def __quantity__(self) -> Quantity:
        return Quantity(1, self, bypass_checks=True)

    def __add__(self, other: Any) -> Quantity:
        if isinstance(other, (Unit, Quantity)):
            return Quantity(1, self, bypass_checks=True) + Quantity(1, other, bypass_checks=True)
        else:
            raise IncommensurableError(f"Unit {str(self)} is incommensurable with {str(other)}")
        
    def __sub__(self, other: Any) -> Quantity:
        if isinstance(other, (Unit, Quantity)):
            return 1*self - 1*other
        else:
            raise IncommensurableError(f"Unit {str(self)} is incommensurable with {str(other)}")

    def __mul__(self, other: Any) -> Unit | Quantity:
        from qntpy.core.quantity import Quantity
        if type(other) != Unit:
            try:
                return Quantity(other, self)
            except ValueError:
                raise ArithmeticError(f"Cannot multiply instance of Unit with instance of class {type(other)}!")
        selfs = self.vec.copy()
        others = other.vec.copy()
        for k in others:
            if k in selfs:
                selfs[k] = others[k] + selfs[k]
            else:
                selfs[k] = others[k]
        return Unit(selfs, None, self.factor*other.factor, 0, self.prefix+other.prefix)
    def __rmul__(self, other: Any) -> Unit | 'Quantity':
        return self * other

    def __pow__(self, other: int) -> Unit:
        if other == 1:
            return self
        unit = self.copy()
        for i in unit.vec:
            new_power = unit.vec[i]*other
            if int(new_power) == new_power:
                unit.vec[i] = new_power
            else:
                raise InvalidUnitError(f"({self})**({other}) would have non-integral dimensions!")
        unit.factor = unit.factor**other
        unit._symbol = None
        return unit
    
    def __neg__(self) -> Unit:
        return -1*self
    def __pos__(self) -> Unit:
        return self
    def __abs__(self) -> Unit:
        return self
    
    def __truediv__(self, other: Any) -> Any:
        from qntpy.core.quantity import Quantity
        if type(other) == Quantity:
            return self.__quantity__()/other
        elif type(other) != Unit:
            return Quantity(1/other, self)
        new_vec = self.vec - other.vec
        return Unit(vec=new_vec, symbol=None, factor=self.factor/other.factor, prefix=self.prefix - other.prefix)
    def __rtruediv__(self, other: Any) -> Unit | Quantity:
        return self.invert() * other
        
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Unit) and self.offset == other.offset and self.factor == other.factor and self.vec == other.vec

    def __str__(self) -> str:
        if self.factor != 1:
            return str(self.factor) + ' ' + self.symbol
        else:
            return self.symbol
        # from qntpy.rep.simplify import simplify
        # return simplify(self)
        
        # strin = ""
        # for k in self.vec:#sorted(self.vec):
        #     if self.vec[k] == 0:
        #         pass
        #     elif self.vec[k] != 1:
        #         strin +=(str(k) + rep.to_superscript(self.vec[k]))
        #     else:
        #         strin +=str(k)
        
        display_value = self.factor*10**(-self.prefix)
        
        if display_value != 1 or self.prefix != 0 or self.is_kg():
            return f"{str(display_value)+' ' if display_value != 1 else ''}{rep.exponent_to_abbrev(self.prefix, self.is_kg())}{strin}"
        else:
            return strin   
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.vec)}{', factor='+str(self.factor) if self.factor != 1 else ''}{', offset='+str(self.offset) if self.offset != 0 else ''})"
    
    def __float__(self) -> float:
        if self.vec.is_empty():
            return float(self.factor)
        raise IncommensurableError(f"Unit {str(self)} is not convertible to a float")
    def __int__(self) -> int:
        if self.vec.is_empty():
            return int(self.factor)
        raise IncommensurableError(f"Unit {str(self)} is not convertible to an integer")
    def __bool__(self) -> bool:
        return not self.vec.is_empty()

    def invert(self) -> Unit:
        """Return the reciprocal of this Unit.
        
        This method should always return the multiplicative inverse of the object it is called on.
        """
        new_dimvec = -self.vec
        new_factor = 1 / self.factor
        new_prefix = -self.prefix
        if self.is_kg():
            new_prefix = self.prefix
        return Unit(vec=new_dimvec, symbol=None, factor=new_factor, prefix=new_prefix)

    def is_kg(self) -> bool:
        return self.vec == DimVec({Dim.M: 1})
        
    def with_prefix(self, new_prefix: int) -> Unit:
        return Unit(self.vec.copy(), self._symbol, self.factor*(10**new_prefix), self.offset, self.prefix + new_prefix)

    def copy(self) -> Unit:
        return Unit(self.vec.copy(), self._symbol, self.factor, self.offset, self.prefix)
    
    __array_priority__ = 500

defs.Unit = Unit