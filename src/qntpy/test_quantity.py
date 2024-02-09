from quantity import *

def main():
    # unit definition
    Isp = Unit.derived(s, "Isp", 30570322.995110463)
    assert Isp == 30570322.995110463*s
    assert yr.termsOf(Isp) != None
    assert (repr((Isp))) == "Isp"
    
    # unit equivalence
    assert W == J/s
    assert m2 == m**2 
    assert m2 == m*m
    
    # quantities
    assert 1*J+1*kJ == 1001*J
    assert 1*J-1*J != 1*s-1*s 
    # 0 J should not equal 0 s; the most likely
    # outcome is that rounding errors will lead
    # to false equivalence
    assert ((1*N*J/m)**0.5) == 1*N
    
    # functions
    assert kilo(J) == kJ
    
    # odd units
    assert 0*degC == 273.15*K
    
    # simplification
    assert repr(10*W) == repr(10*(A*m*kg/C/C*V/s*m)**0.5*A)
    # unit simplification doesn't have a single solution,
    # so i have had to make some arbitrary decisions about
    # representation
    # for example m*Hz is forcibly displayed as m/s
    assert repr(1*m/s) == "1.0 s⁻¹m"
    # todo: find a way to reverse that
    
    

    print("quantity/unit tests passed! yay :)")

if __name__ == "__main__":
    main()