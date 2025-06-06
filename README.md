## quantipy: units made easy
### TL;DR
quantipy gives your calculations:
- intuitive dimensional analysis
- effortless unit conversion
- automatic commensurability enforcement

see [here](https://github.com/itsmiir/qpy/blob/main/doc/quick-start.md) for a quick start guide, and [here](https://github.com/itsmiir/qpy/blob/main/doc/units.md) for a list of units and constants the package adds

---
### what is quantipy?

#### quantipy is a dimensional analysis module for engineering and physics calculations that allows you to manipulate physical quantities in an intutive way. it also enforces proper unit usage and prevents many unit errors.

### why quantipy?
there are several other python packages that provide support for quantities with units. here is a (non-exhaustive) list:
- [`astropy.units`](https://docs.astropy.org/en/latest/units)
- [`DimPy`](http://www.inference.org.uk/db410/)
- [`DUQ`](https://github.com/AAriam/duq)
- [`Magnitude`](https://juanreyero.com/open/magnitude/)
- [`numericalunits`](https://github.com/sbyrnes321/numericalunits)
- [`Pint`](https://pint.readthedocs.io/en/stable/index.html)
- [`Quantities`](https://python-quantities.readthedocs.io/en/latest/index.html)
- [`Scalar`](http://russp.us/scalar-guide.htm)
- [`sympy.physics.units`](https://docs.sympy.org/latest/modules/physics/units/index.html)

these packages serve a variety of purposes, and all have their strengths and weaknesses. depending on your application, one of these might be better for you--but quantipy has certain features that sets it apart from each of these. In short, **quantipy is ideal as a calculator for quick napkin calculations involving physical quantities.**
### how does it work?

here's a simple example-- let's say i want to find the the velocity of an object involved in an inelastic collision:
```py
from qntpy import *
m1 = 10*kg
m2 = 5*kg
v1 = 5.4*m/s
v2 = 3.2*m/s
pCombined = m1*v1 + m2*v2
m3 = m1 + m2
v3 = pCombined/m3
print(v3)
# 4.666666666666667 ms⁻¹
```
### ok, but how is that useful?

sure, that example didn't really need quantipy. but that's not all it can do: for example, take this calculation for the force of an electromagnet using the equation $F = (NI)^2\mu_0 \frac{A}{2l^2}$:
```py
from qntpy import *
from qntpy.constants import mu_0, g_earth
m_1 = 0.9*lbm
# quantipy will automatically convert every unit you enter into standard (SI) units
current = 3*A
length = 2*cm
turns = 5000
area = 100*mm**2
force = (turns*current)**2 * mu_0 * area / (2*(length**2))
print(force.round(4))
# 35.3429 N
print((m_1*g_earth).round(4))
# 4.0007 N
if (force > m_1*g_earth):
    print("magnet can lift load!")
else:
    print("magnet is underpowered :(")
# magnet can lift load!
```
a little more useful, huh?

### but wait, there's more!

quantipy includes other features too, such as commonly-used physics constants, the ability to represent a value in whatever base or derived units you want, and even currency conversion support, updated daily (with an API key):
```py
from qntpy import *
from qntpy.currency import *
price = 399*USD
data = 23*GiB
weight = 430*lbf

dataPerWeightCurrency = data/price/weight
print(dataPerWeightCurrency.termsOf(MB/(EUR*kN), 4))
# 34.3292 MB/EUR•kN
```
```py
from qntpy import *
import qntpy.constants as qc
mass = 3.043*MeVc2
num_electrons = mass / qc.m_e # call qc.constants() to see all available constants
print(round(num_electrons, 0))
# 6.0
```
### recovering values
you can recover the scalar values of quantipy quantities with the `value` field:
```py
from qntpy.constants import c
# c.value is a float
print(c.value)
# 299792458.0
```
### unit enforcement
quantipy automatically enforces proper usage of units in your calculations. trying to add incompatible units will throw an error:
```py
from qntpy import *

m1=10*kg
m2=12*m/s
print(m1+m2)

ArithmeticError: Incompatible units: kg and m/s
```
this feature will solve a surprising amount of calculation errors.
### defining custom units
you can even define your own custom constants with your own symbols and conversion factors and use them in your code!
```py
from qntpy import *
# the first argument is the commensurability of the new unit, the second is its unit symbol, the third is its value

# define a new unit "Fizz" equal to 12 m/kg, with the symbol "Fz"
Fizz = Unit.derived(m/kg, "Fz", 12)
value = 12000*m/kg
print(value.termsOf(Fizz))
# 1000.0 Fz
newValue = 1000*Fizz
print(newValue == value)
# True

```
built-in functions are also provided to automatically create prefixed units:
```py
kFizz = kilo(Fizz)
print(value.termsOf(kFizz))
# 1.0 kFz
```
these functions define a new derived unit whose symbol is the same as the original unit with the SI prefix added.

the included prefix functions are as follows:
function|value|prefix
---|---|---
`pico`|$10^{-12}{}$|`p`
`nano`|$10^{-9}{}$|`n`
`micro`|$10^{-6}{}$|`μ`
`milli`|$10^{-3}{}$|`m`
`kilo`|$10^{3}{}$|`k`
`mega`|$10^{6}{}$|`M`
`giga`|$10^{9}{}$|`G`
`tera`|$10^{12}{}$|`T`
`peta`|$10^{15}{}$|`P`

### non-absolute units
```py
# define a new unit "Buzz" equal to 2 J, but "0 Buzzes" is equal to 11 J.
Buzz = Unit.derived(J, "Bz", 2, 11)
```
this may seem like a weird and arbitrary feature, but it's how quantipy is able to work with units like degrees Celsius, which aren't based on absolute scales.
```py
print(0*Buzz)
# 11 J
```
be careful how you use non-absolute units; for example, the expression "`12*degC / kg`" is actually equal to "`285.15 K / kg`". it's preferred to use absolute units (kelvins and rankines) for conversion factors. non-absolute units are mostly added for completeness, and so you can convert between them:
```py
print((43*degF).termsOf(K), (16*degF).termsOf(degC))
# 279.2611111111111 K -8.888888888888857 ⁰C
```
### currency units
in addition to normal physics and engineering units, several currencies are defined by quantipy via the [APILayer Exchange Rates Data API](https://apilayer.com/marketplace/exchangerates_data-api). you can access them by importing `qntpy.currency` and adding your APILayer API key to the `api_key.txt` file that is generated by the module--this file lives under `site-packages/qntpy/` in your python environment folder. you can reference currencies in code with their [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency codes and use them as you would other units.
```py
import qntpy.currency as cncy
print(cncy.BTC.termsOf(cncy.EUR))
# '26369.10595485628 EUR'
```
### more information

for a full list of units and constants added by quantipy, see [here](https://github.com/itsmiir/qpy/blob/main/doc/units.md).

### appendix: package structure


`qntpy`: top-level package.
- `compat`: compatibility with other scientific computing systems.
- `constants`: helpful constants from a variety of disciplines
- `core`: core functionality.
- `currency`: currency units.
- `info`: information and data.
- `repr`: code for displaying and formatting values.
- `util`: helper code and miscellaneous functions.