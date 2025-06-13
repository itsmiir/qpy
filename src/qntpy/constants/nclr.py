from uncertainties import ufloat as _ufloat
from numpy import pi as _pi

from qntpy.constants.fund import *
from qntpy.core.units import *

m_alpha = _ufloat(6.6446573450e-27, # alpha partice mass
                 0.0000000021e-27) * kg
r_alpha = _ufloat(1.6785e-15, # alpha particle rms charge radius
                  0.0021e-15) * m 
a_0 = hbar/(alpha*m_e*c) # Bohr radius
r_e = alpha**2*a_0 # classical electron radius
lambda_c = _ufloat(2.42631023538e-12, # Compton wavelength
                   0.00000000076e-12) * m
g_d = _ufloat(0.8574382335, # deuteron g factor
              0.0000000022)
