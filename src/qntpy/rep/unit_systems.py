from __future__ import annotations
from dataclasses import dataclass

from qntpy.core.quantity import Unit
from qntpy.util import testing

@dataclass
class UnitSystem(object):
    length: Unit,
    