"""DuraPy Examples - UniPhys (mechanics, thermodynamics, fluid dynamics)"""

from durapy.uniphys import mechanics, thermodynamics, fluid_dynamics, acoustics
from durapy.shared.constants import C, G, GAS_CONSTANT

# Mechanics
print("Torque (F=50 N, r=0.3 m):", mechanics.torque(0.3, 50))
print("KE (m=2 kg, v=10 m/s):", mechanics.kinetic_energy(2, 10))
print("PE (m=5 kg, h=10 m):", mechanics.potential_energy(5, 10))
print("E=mc^2 (m=1 kg):", mechanics.einstein_mass_energy_equivalence(1))

# Thermodynamics (now returning Quantity objects)
print("\nWork (F=100 N, d=5 m):", thermodynamics.work(100, 5))
print("Heat capacity (m=2 kg, c=4184 J/kg/K):", thermodynamics.heat_capacity(2, 4184))
print("Carnot efficiency (Th=600 K, Tc=300 K):", thermodynamics.carnot_efficiency(600, 300))
print("ΔU = Q + W (Q=100 J, W=-30 J):", thermodynamics.internal_energy(100, -30))
print("Van der Waals pressure:", thermodynamics.van_der_waals_pressure(1.0, 0.0224, 273.15, 0.138, 3.87e-5))

# Ideal gas law (canonical in uniphys returns tuple)
P, V, n, T = thermodynamics.ideal_gas_law(V=0.022414, n=1.0, T=273.15)
print(f"\nIdeal gas: V=0.022414 m^3, n=1 mol, T=273.15 K -> P = {P:.2f} Pa")

# Fluid dynamics
print("\nDynamic pressure (v=50 m/s):", fluid_dynamics.dynamic_pressure(50))
print("Reynolds number (v=2 m/s, L=0.1 m, nu=1.5e-5):", fluid_dynamics.reynolds_number(2, 0.1, 1.5e-5))

# Acoustics
print("\nSpeed of sound (air, 293 K):", acoustics.sound_speed(293))
print("Wavelength at 440 Hz:", acoustics.wavelength_from_frequency(440))
print("Frequency for 0.78 m wavelength:", acoustics.frequency_from_wavelength(0.78))
