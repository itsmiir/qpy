from uncertainties import ufloat as _ufloat
from numpy import pi as _pi

from qntpy.constants.fund import *
from qntpy.core.units import *

mu_B = e*hbar / (2*m_e) # Bohr magneton
G_0 = 2*e**2 / (2*_pi*hbar) # G_0
K_J = 2*e/H # Josephson constant
Phi_0 = 2*_pi * hbar / (2*e) # magnetic flux quantum
mu_N = e*hbar/(2*m_p) # nuclear magneton
R_K = 2*_pi * hbar / e**2 # von Klitzing constant