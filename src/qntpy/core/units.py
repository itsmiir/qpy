from qntpy.core.unit import Unit
from qntpy.core.dimension import Dim, DimVec
from qntpy.rep import rep

# dimension vectors: base
LENGTH = DimVec({Dim.L: 1})
TIME = DimVec({Dim.T: 1})
MASS = DimVec({Dim.M: 1})
ELECTRIC_CURRENT = DimVec({Dim.I: 1})
THERMODYNAMIC_TEMPERATURE = DimVec({Dim.THETA: 1})
AMOUNT_OF_SUBSTANCE = DimVec({Dim.N: 1})
LUMINOUS_INTENSITY = DimVec({Dim.J: 1})

# unit definitions: base
m = Unit(LENGTH, "m")
s = Unit(TIME, "s")
kg = Unit(MASS, "g")
A = Unit(ELECTRIC_CURRENT, "A")
K = Unit(THERMODYNAMIC_TEMPERATURE, "K")
mol = Unit(AMOUNT_OF_SUBSTANCE, "mol")
cd = Unit(LUMINOUS_INTENSITY, "cd")
One = Unit(DimVec({}),"") # unitless unit; for 1/<unit>
base_units = (m, s, kg, A, K, mol, cd)


# unit definitions: derived
Hz = Unit.derived(s.invert(), "Hz")
N = Unit.derived(kg*m/s/s, "N")
Pa = Unit.derived(N/m/m, "Pa")
J = Unit.derived(N*m, "J")
W = Unit.derived(J/s, "W")
C = Unit.derived(s*A, "C")
V = Unit.derived(W/A, "V")
F = Unit.derived(C/V, "F")
Ohm = Unit.derived(V/A, "Ω")
S = Unit.derived(Ohm.invert(), "S")
Wb = Unit.derived(V*s, "Wb")
T = Unit.derived(Wb/m/m, "T")
H = Unit.derived(Wb/A, "H")
Sv = Unit.derived(J/kg, "Sv")

derived_units = (Hz, N, Pa, J, W, C, V, F, Ohm, S, Wb, T, H, Sv)

rad = One
sr = One
lm = cd * sr

# unit definitions: approved others
L = Unit.derived(m*m*m, 'L', 1e-3)
degC = Unit.derived(K, '°C', 1, 273.15)


# _l = locals()
# for prefix in rep._prefices:
#     try:
#         int(prefix)
#     except ValueError:
#         if prefix != '':
#             exec(f"""def {prefix}(unit: Unit) -> Unit:
#                      return unit.with_prefix(rep.prefix_to_exponent('{prefix}',unit.is_kg()))""", globals(), _l)