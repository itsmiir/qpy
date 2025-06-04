from qntpy.core.unit import Unit

def commensurable(a: Unit, b: Unit) -> bool:
    return a.vec == b.vec