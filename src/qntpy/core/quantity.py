from __future__ import annotations
from copy import deepcopy
from typing import Any, TYPE_CHECKING

from uncertainties.core import AffineScalarFunc
# from uncertainties.unumpy import uarray, umatrix
import numpy as np
from numpy.typing import ArrayLike


from qntpy.core.defs import Unit
from qntpy.core import defs
from qntpy.util import exceptions as exc

if TYPE_CHECKING:
    from qntpy.core.unit import Unit


_HANDLED_FUNCTIONS = {}

_PASSTHROUGH_FUNCTIONS = [
    np.size,
    np.shape,
    np.ndim,
    
]

_PASSTHROUGH_W_UNIT_FUNCTIONS = [
    np.sum,
    np.ravel,
    np.moveaxis,
    np.rollaxis,
    np.swapaxes,
    np.transpose,
    np.permute_dims,
    np.atleast_1d,
    np.atleast_2d,
    np.atleast_3d,
    np.broadcast,
    np.broadcast_to,
    np.broadcast_arrays,
    np.expand_dims,
    np.squeeze,
    np.tile,
    np.repeat,
    np.delete,
    np.insert,
]

class Quantity(object):   
    """Represents a physical quantity; i.e., a `Unit` with an associated numerical value.
    
    "The value of a quantity is generally expressed as the product of a number and a unit. The unit
    is a particular example of the quantity concerned which is used as a reference, and the number
    is the ratio of the value of the quantity to the unit." -*The International System of Units*
    """
    
    @staticmethod
    def get_value(obj) -> Any:
        if isinstance(obj, Quantity):
            return obj.value
        else:
            return obj
        
    @staticmethod
    def get_unit_or_self(obj) -> Unit | Any:
        """Return the Unit associated with this object if it is a quantity, or if not, return the object."""
        if isinstance(obj, Quantity):
            return obj.unit
        else:
            return obj
    
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
    
    def __init__(self, value: ArrayLike | Quantity, unit: 'Unit' | Quantity, digits: int=0, **kwargs) -> Quantity:
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
        if isinstance(self.value, np.ndarray):
            val = self.value      
        else:
            if self.value.std_dev == 0:
                val = self.value.nominal_value
            else:
                val = self.value
            # val /= 10**self.unit.prefix
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
    
    def is_scalar(self) -> bool:
        return np.size(self.value) == 1
    
    def copy(self) -> Quantity:
        return Quantity(deepcopy(self.value), self.unit.copy(), self.digits)
    
    def invert(self) -> Quantity:
        return Quantity(1 / self.value, self.unit.invert(), self.digits, bypass_checks=True)
    
    def implements(np_func):
        def decorator(func):
            _HANDLED_FUNCTIONS[np_func] = func
            return func
        return decorator
    
    def __array_function__(self, func, types, args, kwargs):
        if func not in _HANDLED_FUNCTIONS:
            return NotImplemented
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return _HANDLED_FUNCTIONS[func](*args, **kwargs)

    def __array_ufunc__(self, ufunc: function, method, *inputs, **kwargs):
        if method == '__call__':
            new_inputs = (Quantity.get_value(i) for i in inputs)
            units = (Quantity.get_unit_or_self(i) for i in inputs)
            outputs = ufunc(*new_inputs, **kwargs)
            out_unit = ufunc(*units, **kwargs)
            return outputs * Quantity.get_unit_or_self(out_unit)
    
    # @implements(np.sum)
    # def sum(self):
    #     if self.is_scalar():
    #         return self.value
    #     else:
    #         return np.sum(self.value) * self.unit
        
    # @implements(np.concatenate)
    # def concatenate(values, **kwargs):
    #     pass
    
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
    