"""DuraPy Examples - UniSky (aerospace)"""

from durapy.unisky import (
    mach_number,
    dynamic_pressure,
    lift_drag_equation,
    aspect_ratio,
    wing_loading,
    glide_ratio,
    reynolds_number,
    ideal_gas_law,
    bernoullis_equation,
    tw_ratio,
    rocket_thrust_equation,
    specific_impulse_by_thrust,
)

# Flight basics
print(mach_number(340))  # ~1.0 at sea level
print("Dynamic pressure (v=100 m/s):", dynamic_pressure(100))
print("Reynolds number (v=60 m/s, c=1.5 m, nu=1.5e-5):", reynolds_number(60, 1.5, 1.5e-5))

# Wing performance
ar = aspect_ratio(wingspan=10, wing_area=16)
print(f"\nAspect ratio: {ar:.2f}")
wl = wing_loading(15000, 16)  # N / m^2
print(f"Wing loading: {wl:.1f} N/m^2")
gl = glide_ratio(lift=8000, drag=500)
print(f"Glide ratio L/D: {gl:.1f}")

# Lift/drag
L = lift_drag_equation(coeff=0.4, dynamic_pressure=dynamic_pressure(80)._value, ref_area=16)
print("Lift (Cl=0.4, v=80 m/s):", L)

# Gas law (UniSky returns a friendly string)
print("\nIdeal gas law (solve for P):", ideal_gas_law(V=0.05, n=2.0, T=350))

# Bernoulli (solve for missing variable)
print("Bernoulli (solve for v2):", bernoullis_equation(P1=150000, v1=30, h1=10, P2=120000, h2=10, rho=1000))

# Rocketry
print("\nT/W ratio (thrust=50000 N, weight=40000 N):", tw_ratio(50000, 40000))
F = rocket_thrust_equation(mdot=15, v_e=2800, p_e=80000, p_a=101325, a_e=0.5)
print(f"Rocket thrust: {F:.0f} N")
Isp = specific_impulse_by_thrust(thrust=F, fuel_mass_flow_rate=15)
print(f"Specific impulse: {Isp:.1f} s")
