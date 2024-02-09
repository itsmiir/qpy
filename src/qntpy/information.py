from .quantity import *

bit = Unit({"b": 1}, "b")
nybble = Unit.derived(bit, "nybble", 4)
byte = Unit.derived(bit, "B", 8)

addBaseUnit(bit)

kB = kilo(byte)
MB = mega(byte)
GB = giga(byte)
TB = tera(byte)
PB = peta(byte)
EB = Unit.derived(TB, "EB", 1000)

KiB = Unit.derived(byte,"KiB", 1024)
MiB = Unit.derived(KiB, "MiB", 1024)
GiB = Unit.derived(MiB, "GiB", 1024)
TiB = Unit.derived(GiB, "TiB", 1024)
PiB = Unit.derived(TiB, "PiB", 1024)
EiB = Unit.derived(PiB, "EiB", 1024)
