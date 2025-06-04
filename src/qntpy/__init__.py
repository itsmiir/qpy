"""qntpy is a Python implementation of physical quantities.

The core of `qntpy`'s functionality is the `Quantity` class,
which represents a physical quantity able to be acted upon like
any number. A physical quantity is made up of two parts:
1. The `value`. This is a number (an `ndarray`) with an associated
   uncertainty.
2. The `unit`. This is a representation of a physical unit. The implementation
   of units in `qntpy` is according to the International System of Units (SI),
   although non-SI units and quantities are included in qntpy.
"""

from .core.quantity import *
from .constants import *
from .info.information import *
from .constants.us import *
