from qntpy.core.dimension import Dim, DimVec

def test_validate_inputs():
    flag: bool
    try:
        flag = False
        vec1 = DimVec({Dim.L: 2, Dim.J: 3, 'Dim.I': 0})
    except ValueError:
        flag = True
    assert flag is True, "Case 1 failed!"
    try:
        flag = False
        vec2 = DimVec({Dim.L: 2, Dim.J: 3, Dim.I:'0'})
    except ValueError:
        flag = True
    assert flag is True, "Case 2 failed!"
    vec3 = DimVec({Dim.L: 4, Dim.I: 0, Dim.M: -2})
    vec4 = DimVec({Dim.L: 4,           Dim.M: -2})
    assert vec3 == vec4

def test_inversion():
    vec1 = DimVec({Dim.L: 3, Dim.J: 2, Dim.I: 0})
    vec2 = DimVec({Dim.L:-3, Dim.J:-2, Dim.I: 0})
    vec1.invert()
    assert vec1 == vec2