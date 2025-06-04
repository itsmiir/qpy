from qntpy.core.unit import Unit
from qntpy.core.dimension import Dim, DimVec

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
kg = Unit(MASS, "kg")
A = Unit(ELECTRIC_CURRENT, "A")
K = Unit(THERMODYNAMIC_TEMPERATURE, "K")
mol = Unit(AMOUNT_OF_SUBSTANCE, "mol")
cd = Unit(LUMINOUS_INTENSITY, "cd")

One = Unit({},"") # unitless unit; for 1/<unit>
