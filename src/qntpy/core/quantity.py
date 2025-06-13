"""The Quantity class and associated fields and methods.


"""

from __future__ import annotations
from copy import deepcopy, copy
from typing import Any, TYPE_CHECKING, Sequence
from numbers import Number

import numpy as np
from numpy.typing import ArrayLike
from uncertainties.core import AffineScalarFunc

from qntpy.core.defs import Unit
from qntpy.core import defs
from qntpy.util import exceptions as exc
from qntpy.compat.numpy import HANDLED_FUNCTIONS, PASSTHROUGH_FUNCTIONS, PASSTHROUGH_W_UNIT_FUNCTIONS

if TYPE_CHECKING:
    from qntpy.core.unit import Unit



class Quantity(object):   
    """Represents a physical quantity; i.e., a `Unit` with an associated numerical value.
    
    "The value of a quantity is generally expressed as the product of a number and a unit. The unit
    is a particular example of the quantity concerned which is used as a reference, and the number
    is the ratio of the value of the quantity to the unit." -*The International System of Units*
    """
    
    @classmethod
    def get_value(cls, obj, return_none=False) -> Any:
        """Check if `obj` `isinstance` of this class (i.e., this class or its subclasses). If it is, return its `value`. If it isn't, return `obj` (or `None` if `return_none` is True)."""
        if isinstance(obj, cls):
            return obj.value
        else:
            return None if return_none else obj
        
    @staticmethod
    def get_unit_or_else(obj, return_none=False) -> Unit | None | Any:
        """Check if `obj` `isinstance` of this class (i.e., this class or its subclasses). If it is, return the object's `unit`. If not, return `obj` (or `None` if `return_none` is True)."""
        if isinstance(obj, Quantity):
            return obj.unit
        else:
            return None if return_none else obj
    
    @staticmethod
    def _handle_iterable(value: object) -> np.ndarray:
        """Shallow-copy an arbitrary `iterable` into an `ndarray`."""
        assert hasattr(value, '__iter__'), f"Value {str(value)} is not an iterator"
        temp = []
        for i in value:
            temp.append(copy(i))
        return np.array(temp)
    
    @staticmethod
    def _sanitize_value(value: object) -> tuple[Number | np.ndarray | AffineScalarFunc | None, Unit | None]:
        """Intake any object and sanitize it as a `Quantity` value.
        
        Returns a tuple of two values. The first value is the sanitized `value` to be passed to the Quantity initializer.
        The second is a modification that must be made to the `unit` of the quantity; i.e., if a `Quantity` is passed to
        this method.
        
        This function **does not** recursively investigate containers; i.e., a tuple of `Quantities` will be naively treated
        like a tuple and turned into an `ndarray`.
        
        Your custom class can implement compatibility by implementing this static method:
        ```
        class MyClass:
            def __quantity_value__(value: MyClass) -> tuple[float | ndarray | AffineScalarFunc | None, Unit | None]
        ```
        """
        if isinstance(value, (Number, np.number, AffineScalarFunc)):
            return (value, None)
        if isinstance(value, (Sequence, np.ndarray)):
            return Quantity._sanitize_value(np.array(value))
            
            
        else:
            try:
                return value.__class__.__quantity_value__(value)
            except AttributeError:
                return (None, None)

        
        
        
    
    def __new__(cls, value: ArrayLike, unit: 'Unit' | Quantity, digits: int=0, bypass_checks=False) -> Quantity | Any:
        if bypass_checks:
            return super().__new__(cls)
        # no bypass_checks
            
        if isinstance(value, Quantity):
            unit *= value.unit
            value = value.value
        # a Unit or n-dimensional value
        
        if isinstance(unit, Quantity):
            value *= unit.value
            unit = unit.unit
        # a Unit or n-dimensional unit and a Unit or n-dimensional value
        
        if np.array_equal(value, 1):
            if hasattr(unit, 'offset') and unit.offset != 0:
                return super().__new__(cls)
            else:
                return unit
        # a Unit or n-dimensional unit and a Unit or n-dimensional value not equal to 1
        
        
        if hasattr(unit, 'vec'):
            return super().__new__(cls)
        # an n-dimensional unit and a Unit or n-dimensional value not equal to 1
        
        else:   
            return value * unit       
    
    def __init__(self, value: ArrayLike | Quantity | AffineScalarFunc | Number | np.number, unit: 'Unit' | Quantity, digits: int=0, **kwargs) -> Quantity:
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
                self.value = value*self.unit.factor+self.unit.offset
                self.unit.factor = 1
                self.unit.offset = 0
            except AttributeError:
                self.unit = None
        self.digits = digits
        if type(value) == Quantity:
            self.value = value.value
            self.unit = value.unit * unit

    def __quantity__(self):
        return self

    def __add__(self, other):
        if type(other) == Unit:
            return self + Quantity(1, other)
        elif type(other) == Quantity:
            if not other.unit == self.unit and other.value != 0 and self.value != 0:
                raise exc.IncommensurableError(f"Incompatible units: {str(self.unit)} and {str(other.unit)}!")
            return Quantity(self.value+other.value, self.unit)
        else:
            if other == 0:
                return self
            else:
                raise exc.IncommensurableError("Incompatible units: "+str(self)+" and "+str(other))
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -other
    def __rsub__(self, other):
        return other + -self

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
    
    def __matmul__(self, other):
        if isinstance(other, Quantity):
            return self.value @ other.value * (self.unit * other.unit)
        else:
            return self.value @ other * self.unit
    def __rmatmul__(self, other):
        if isinstance(other, Quantity):
            return other.value @ self.value * (self.unit * other.unit)
        else:
            return other @ self.value * self.unit

    def __round__(self, i):
        return Quantity(round(self.value, i), self.unit)
    
    def __str__(self):
        if isinstance(self.value, np.ndarray):
            val = self.value      
        else:
            if isinstance(self.value, AffineScalarFunc):
                if self.value.std_dev == 0:
                    val = self.value.nominal_value
                else:
                    val = self.value
            else:
                val = self.value
            # val /= 10**self.unit.prefix
        return str(val)+" "+self.unit.symbol
    def __repr__(self):
        return F'{self.__class__.__name__}({str(self)})'
    def __float__(self):
        return self.value
    def __int__(self):
        return int(float(self))
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
    
    def is_scalar(self) -> bool:
        return np.size(self.value) == 1
    
    def copy(self) -> Quantity:
        """Returns a deep"""
        return Quantity(deepcopy(self.value), self.unit.copy(), self.digits)
    
    def with_value(self, value) -> Quantity:
        """Return a copy of this `Quantity` with its value replaced."""
        new_quantity = self.copy()
    
    def invert(self) -> Quantity:
        return Quantity(1 / self.value, self.unit.invert(), self.digits, bypass_checks=True)
    
    def implements(np_func):
        def decorator(func):
            HANDLED_FUNCTIONS[np_func] = func
            return func
        return decorator
    
    def __array_function__(self, func, types, args, kwargs):
        """Handle numpy array functions that aren't ufuncs.
        
        These are generally divided into two categories: functions that query properties about the array,
        and functions that operate on the data in the array. These functions are handled by passing the 
        `value` of the `Quantity` to the function, and then in the latter case, returning a Quantity made
        from the new array.
        """
        if func in PASSTHROUGH_FUNCTIONS:
            input_values = (Quantity.get_value(arg) for arg in args)
            return func(*input_values, **kwargs)    
        elif func in PASSTHROUGH_W_UNIT_FUNCTIONS:
            input_values = (Quantity.get_value(arg) for arg in args)
            # Ensure that the units are the same for each function.
            # Functions operating on arrays with incoherent units should be handled on a case-by-base basis (HANDLED_FUNCTIONS).
            for arg in args:
                unit = Quantity.get_unit_or_else(arg, None)
                if unit != self.unit:
                    return NotImplemented
            return func(*input_values, **kwargs) * self.unit
        elif func not in HANDLED_FUNCTIONS:
            return NotImplemented
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    def __array_ufunc__(self, ufunc: function, method, *inputs, **kwargs):
        if method == '__call__':
            new_inputs = (Quantity.get_value(i) for i in inputs)
            units = (Quantity.get_unit_or_else(i) for i in inputs)
            outputs = ufunc(*new_inputs, **kwargs)
            out_unit = ufunc(*units, **kwargs)
            return outputs * Quantity.get_unit_or_else(out_unit)
    
    # @implements(np.stack)
    # @implements(np.vstack)
    # @implements(np.hstack)
    # @implements(np.dstack)
    # @implements(np.unstack)
    # @implements(np.column_stack)
    
    # @implements(np.block)
    
    # @implements(np.split)
    # @implements(np.dsplit)
    # @implements(np.hsplit)
    # @implements(np.vsplit)
    # @implements(np.array_split)
    # @implements(np.append)
    