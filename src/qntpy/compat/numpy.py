"""Interop between `Quantity` objects and `numpy`.

The Quantity class implements `__array_function__` and `__array_ufunc__`, `numpy` handlers that allow
Quantities to be passed to numpy functions that accept arrays. Additionally, the `Quantity` class's operators
support numpy arithmetic (+, -, *, /, @) via passthrough. 


"""

import numpy as np

# Implementations of numpy array functions. Ufuncs are handled by operating on the value and then the Unit.


# Functions that simply get passed the array value of the Quantity. This
# applies mainly to functions that query properties of the array.
PASSTHROUGH_FUNCTIONS = [
    np.size,
    np.shape,
    np.ndim,
    
]

# Functions that get passed the value of the Quantity, and then return
# a new Quantity with with the same unit as the original. This mostly
# applies to functions which transform the structure of the array itself.
PASSTHROUGH_W_UNIT_FUNCTIONS = [
    np.sum,
    np.concatenate,
    np.ravel,
    np.moveaxis,
    np.rollaxis,
    np.swapaxes,
    np.transpose,
    np.permute_dims,
    np.atleast_1d,
    np.atleast_2d,
    np.atleast_3d,
    # np.broadcast,
    np.broadcast_to,
    np.broadcast_arrays,
    np.expand_dims,
    np.squeeze,
    np.tile,
    np.repeat,
    np.delete,
    np.insert,
]

# Functions that require custom implementations. These functions are dynamically
# added to this dict via a decorator, and are defined in the Quantity class itself.
# These functions are those that require special implementations and are not ufuncs:

HANDLED_FUNCTIONS = {}
