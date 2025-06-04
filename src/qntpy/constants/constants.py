from qntpy.core.quantity import Quantity
from qntpy.core.units import *

# SI defining constants
delta_v_Cs = 9192631770 * Hz
c = 299792458 * m/s
h = 6.62607015e-34 * J*s
e = 1.602176634e-19 * C
k = 1.380649e-23 * J/K
N_A = 6.02214076e23 / mol
K_cd = 683 * lm/W

G = Quantity(6.67430e-11, N*m2/kg**2) # gravitational constant

g_earth = Quantity(9.80665, m/s/s) # avg surface gravity on earth

mu_0 = Quantity(1.25663706212e-6, N/A/A) # vacuum magnetic permeability
e_0 = One/(mu_0*c**2) # vacuum electric permittivity
k_e = Quantity(8.9875517923e9, N*m2/C**2)

m_e = Quantity(9.1093837015e-31, kg) # electron mass
m_p = Quantity(1.67262192369e-27, kg) # proton mass
m_n = Quantity(1.67492749804e-27, kg) # neutron mass

# planck units
l_planck = Quantity(1.616255e-35, m)
m_planck = Quantity(2.176434e-8, kg)
t_planck = Quantity(5.391247e-44, s)
T_planck = Quantity(1.416784e+32, K)
E_planck = m_planck*c**2

def help():
    print("constant:   variable name: value")
    print("--------------------------------")
    print("speed of light:         c:", c)
    print("Planck constant:        h:", h)
    print("Boltzmann constant:     k:", k)
    print("elementary charge:      e:", e)
    print("gravitational constant: G:", G)
    print()
    print("vacuum permeability: mu_0:", mu_0)
    print("vacuum permittivity:  e_0:", e_0)
    print("Coulomb constant:     k_e:", k_e)
    print()
    print("electron mass:        m_e:", m_e)
    print("proton mass:          m_p:", m_p)
    print("neutron mass:         m_n:", m_n)
    print()
    print("mean gravity of earth:  g_earth:", g)
    print()
    print("Planck length:   l_planck:", l_planck)
    print("Planck masss:    m_planck:", m_planck)
    print("Planck time:     t_planck:", t_planck)
    print("Planck temp.:    T_planck:", T_planck)
    print("Planck energy:   E_planck:", E_planck)

if __name__ == '__main__':
    help()
