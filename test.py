from quantity import *
from us import *
from information import *
from currency import *

throughput = 60*GB/s
value = 0.025*BTC/PiB
energyUsage = 6*Btu/GB
efficiency = .76*W/W
runtime = 5*yr
energyCost = .142*USD/kWh
totalEnergy = throughput*energyUsage*runtime
wastedEnergy = totalEnergy*(1-efficiency)
totalData = throughput*runtime
revenue = totalData*value
cost = totalEnergy*energyCost
print("total used energy:", totalEnergy.termsOf(GWh, 6))
print("cost of used energy:",(cost).termsOf(kUSD, 3))
print("cost of wasted energy:", (wastedEnergy*energyCost).termsOf(kUSD, 3))
print("profit over "+str(runtime.termsOf(yr))+":", (revenue - cost).termsOf(kUSD, 3))
