from uncertainties import ufloat as _ufloat
from numpy import pi as _pi

from qntpy.constants.fund import *
from qntpy.core.units import *

sigma = (_pi**2 / 60) * k**4 / (hbar**3*c**2) # Stefan-Boltzmann constant