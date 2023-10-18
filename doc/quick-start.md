### quick start guide
first, open a command line and install quantipy with the following command:
```
pip install qntpy
```
once the module is installed, open up a new python window, and create some quantities by multiplying a `Unit` with a scalar ([here's](units.md) a list of all the units you can use): 
```py
>>> from qntpy import *
>>> mass = 10*kg
>>> velocity = 5.4*m/s
>>> area = 4.22*m**2
>>> power = 10*W
```
now that we have some quantities, we can do all sorts of things with them.
```py
>>> velocity
5.4 s⁻¹m
>>> velocity.value
5.4
>>> mass.unit
kg
>>> mass * velocity
54.0 Ns
>>> area**0.5
2.0542638584174138 m
>>> power*hr
36000.0 J
```
you will see that quantipy automatically converts units to their most simple form. `kg*m/s = N*s`. we can do more with this. let's find out how much kinetic energy our mass has:
```py
>>> KE = 1/2*m*v**2
>>> KE
145.8 J
```
wow! 145.8 joules! that's pretty cool, but i live in the united states, and i want to know how much that is in freedom units. we can do that with the `termsOf` method:
```py
>>> KE.termsOf(Btu)
'0.13819171683777923 Btu'
```
you can pass any equivalent unit to this function. for example; the isochoric heat capacity of water:
```py
>>> C_V = 4.157*kJ/kg/K
>>> C_V.termsOf(Btu/lbm/R)
'0.9928823986839923 Btu/lbm/R'
```
let's try to express it in other units:
```py
>>> C_V.termsOf(kcal/kg)
ArithmeticError: Incompatible units: Jkg⁻¹K⁻¹ and Jkg⁻¹
```
whoa! we get an error because those units aren't the same. the same thing will happen if you try to add quantities with incompatible units.
