from uncertainties import ufloat as _ufloat
import numpy as _np

from qntpy.core import units as _units

# SI defining constants
delta_v_Cs = 9192631770 * _units.Hz
c = 299792458 * _units.m/_units.s
h = 6.62607015e-34 * _units.J/_units.Hz
e = 1.602176634e-19 * _units.C
k = 1.380649e-23 * _units.J/_units.K
N_A = 6.02214076e23 / _units.mol
K_cd = 683 * _units.lm/_units.W

# electron volt
eV = e*_units.V
keV = 1e3 *  eV
MeV = 1e3 * keV
GeV = 1e3 * MeV
TeV = 1e3 * GeV
PeV = 1e3 * TeV

# NIST fundamental physical constants (2022 CODATA recommended values)
Z_0 = _ufloat(376.730313412, # characteristic impedance of vacuum
               0.000000059) * _units.Ohm

G = _ufloat(6.67430e-11, # Newtonian constant of gravitation
           0.00015e-11) * _units.N*_units.m*_units.m/_units.kg**2 

hbar = h / (2*_np.pi) # reduced Planck constant

Ghbarc = G / (hbar * c) # Newtonian constant of gravitation over h-bar c

m_P = (hbar*c/G)**0.5 # Planck mass
l_P = hbar/(m_P*c)    # Planck length
m_Pc2 = m_P*(c**2)    # Planck mass-energy equivalent
T_P = m_Pc2/k         # Planck temperature
t_P = l_P/c           # Planck time

g_0 = 9.80665 * _units.m/_units.s/_units.s # avg surface gravity on earth

mu_0 = _ufloat(1.25663706127e-6, # vacuum magnetic permeability
               0.00000000020e-6) * _units.N / _units.A / _units.A
e_0 = 1 / (mu_0 * c**2) # vacuum electric permittivity
alpha = e**2 / (4*_np.pi*e_0*hbar*c) # fine-structure constant


k_e = 1 / (4*_np.pi*e_0) # Coulomb constant

m_e = _ufloat(9.1093837139e-31,  # electron mass
              0.0000000028e-31)  * _units.kg
m_p = _ufloat(1.67262192595e-27, # proton mass
              0.00000000052e-27) * _units.kg
m_n = _ufloat(1.67492750056e-27, # neutron mass
              0.00000000085e-27) * _units.kg


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
    print("mean gravity of earth:g_0:", g_0)
    print()
    print("Planck length:   l_planck:", l_P)
    print("Planck masss:    m_planck:", m_P)
    print("Planck time:     t_planck:", t_P)
    print("Planck temp.:    T_planck:", T_P)
    print("Planck energy:   E_planck:", m_Pc2)

if __name__ == '__main__':
    help()
