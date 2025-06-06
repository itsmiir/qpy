from qntpy.core import units
from qntpy.core.unit import Unit
# unit definition: us customary

# length
ft = Unit.derived(units.m, "ft", 0.3048)
inch = Unit.derived(units.m, "in", 0.0254)
thou = Unit.derived(inch, "thou", 1000)
mi = Unit.derived(ft, "mi", 5280)

# time
minute = Unit.derived(units.s, 'min', 60)
hr = Unit.derived(minute, 'hr', 60)

# area
inch2 = Unit.derived(inch**2, "(in²)")
ft2 = Unit.derived(ft**2, "(ft²)")
mi2 = Unit.derived(mi**2, "(mi²)")
acre = Unit.derived(units.m**2, "acre", 4046.873)

# volume
ft3 = Unit.derived(units.m**3, None, 0.02831685)
in3 = Unit.derived(inch**3, None)
tsp = Unit.derived(units.L, None, 4.92892159375e-3)
Tbsp = Unit.derived(tsp, None, 3)
cup = Unit.derived(Tbsp, None, 16)
pint = Unit.derived(cup, None, 2)
quart = Unit.derived(pint, None, 2)
gal = Unit.derived(quart, None, 4)

# velocity
fps = Unit.derived(ft/units.s, 'fps', 1)
mph = Unit.derived(mi/hr, 'mph', 1)

# energy
Btu = Unit.derived(units.J, None, 1055.056)

# power
hp = Unit.derived(units.W, None, 745.7)

# temperature
R = Unit.derived(units.K, 'R', 0.5555556)
degF = Unit.derived(units.degC, None, 0.5555555555555556, -17.77777777777778)

# force
lbf = 4.448222 * units.N # Unit.derived(units.N, 'lbf', 4.448222)

# mass
lbm =Unit.derived(units.kg, 'lbm',  0.4535924) # 0.4535924 * units.kg 
ton =           2000 * lbm
slug =   lbf*units.s**2/ft

# pressure
psi =  lbf/inch2
ksi =  1e3 * psi
Mpsi = 1e6 * ksi
