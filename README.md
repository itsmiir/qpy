### what is qpy?

qpy is a dimensional analysis module for engineering and physics applications that allows you to manipulate quanities in an intutive way. it also enforces proper unit usage and prevents many unit errors.

### how does it work?

here's a simple example-- let's say i want to find the the velocity of an object involved in an inelastic collision:
```py
from qpy import *
m1 = 10*kg
m2 = 5*kg
v1 = 5.4*m/s
v2 = 3.2*m/s
pCombined = m1*v1 + m2*v2
m3 = m1 + m2
v3 = pCombined/m3
print(v3)
# >>> 4.666666666666667 ms⁻¹
```
### ok, but how is that useful?

sure, that example didn't really need qpy. but that's not all it can do: for example, take this calculation for the force of an electromagnet using the equation $F = (NI)^2\mu_0 \frac{A}{2l^2}$:
```py
from qpy import *
m_1 = 0.9*lbm
g = 9.8*m/s**2
I = 3*A
l = 2*cm
turns = 5000
area = 100*mm**2
F = (turns*I)**2 * mu_0 * area / (2*(l**2))
print(F.round(4))
print((m_1*g).round(4))
if (F > m_1*g):
    print("magnet can lift load!")
else:
    print("magnet is underpowered :(")
# >>> 35.3429 N
# >>> 4.0007 N
# >>> magnet can lift load!
```
a little more useful, huh?

### but wait, there's more!

qpy includes other features too, such as helpful physics constants, the ability to represent a value in whatever base or derived units you want, and even currency conversion support, updated daily (with an API key):
```py
from qpy import *
from qpy.currency import *
price = 399*USD
data = 23*GiB
weight = 430*lbf

dataPerWeightCurrency = data/price/weight
print(dataPerWeightCurrency.termsOf(MB/(EUR*kN), 4))
# >>> 34.3292 MB/EUR•kN
```
```py
from qpy import *
mass = 3.043*MeVc2
num_electrons = mass / m_e # call constants.help() to see all available constants
print(round(num_electrons, 0))
# >>> 6.0
```
