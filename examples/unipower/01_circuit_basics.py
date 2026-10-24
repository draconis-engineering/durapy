"""DuraPy Examples - UniPower (electronics)"""

from durapy.unipower import (
    ohms_law,
    volt_divider,
    power_dissipation,
    capacitor_charge,
    rc_time_constant,
)
from durapy.unipower import resistor, inductor, capacitor

# Ohm's law
V, I, R = ohms_law(v=9, r=1000)
print(f"Ohm's law: V={V} V, I={I*1000:.1f} mA, R={R} Ω")

# Power
P = power_dissipation(v=12, r=10)
print("Power dissipation (12V across 10Ω):", P)

# Voltage divider
vout = volt_divider(5, 1000, 2000)
print("Voltage divider (5V, R1=1k, R2=2k):", vout)

# Resistor color code
r = resistor.Resistor(band_1="brown", band_2="black", band_3="red", band_4="gold")
print("\nResistor:", r)
print("Value:", r.value, r.tolerance)

# Capacitor/inductor
c = capacitor.Capacitor(capacitance=1e-6, voltage_rating=50)
print("\nCapacitor:", c)
l = inductor.Inductor(inductance=10e-3)
print("Inductor:", l)

# RC time constant
tau = rc_time_constant(1e-6, 1000)
print("\nRC time constant (1µF, 1kΩ):", tau)
print("Charge after 1τ:", capacitor_charge(1e-6, 5, 0.001))
