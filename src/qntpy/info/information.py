from qntpy.core.unit import Unit
from qntpy.core.dimension import Dim, DimVec

bit = Unit(DimVec({}))# Unit({"b": 1}, "b")
nybble = 4 * bit # Unit.derived(bit, "nybble", 4)
byte = 8 * bit # Unit.derived(bit, "B", 8)

# add_base_unit(bit)

kB = 1e3 *  byte # units.kilo(byte)
MB = 1e6 *  byte # units.giga(byte)
TB = 1e9 *  byte # units.tera(byte)
PB = 1e12 * byte # Unit.derived(TB, "PB", 1000)
EB = 1e15 * byte # Unit.derived(TB, "EB", 1000)

KiB = 2**10 * byte # Unit.derived(byte,"KiB", 1024)
MiB = 2**10 * KiB  # Unit.derived(KiB, "KiB", 1024)
GiB = 2**10 * MiB  # Unit.derived(MiB, "GiB", 1024)
TiB = 2**10 * GiB  # Unit.derived(GiB, "TiB", 1024)
PiB = 2**10 * TiB  # Unit.derived(TiB, "PiB", 1024)
EiB = 2**10 * PiB  # Unit.derived(PiB, "EiB", 1024)

def help():
    print("data units; base unit = bit (b)")
    print("--------------------------------")
    print("included units:")
    print("byte, kB, MB, GB, TB, PB, EB")
    print("KiB, MiB, GiB, TiB, PiB, EiB")
    print("note: kilobyte et al. scale by 1000, kibibyte et al. scale by 1024")
    print("---------------------------------")
    print("example:")
    print()
    print(">>> from qpy.quantity import *")
    print(">>> from qpy.information import *")
    print(">>> storageDensity = 12*MB/kg")
    print(">>> print(storageDensity*150*g).termsOf(KiB)")
    print("1757.8125 KiB")

if __name__ == "__main__":
    help()

