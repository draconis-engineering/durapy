"""DuraPy Examples - UniChem"""

from durapy import unichem

# Periodic table
H = unichem.get_element("H")
print("Element:", H.symbol, H.name, "Z=", H.atomic_number, "Molar mass:", H.atomic_mass, "g/mol")

# Formula parsing & molar mass
water = unichem.parse_formula("H2O")
print("\nH2O formula:", water)
print("Molar mass:", unichem.molar_mass("H2O"), "g/mol")

glucose = unichem.parse_formula("C6H12O6")
print("Glucose molar mass:", unichem.molar_mass("C6H12O6"), "g/mol")

# Mass percent
comp = unichem.mass_percent("CO2")
print("\nMass % in CO2:", comp)

# Empirical formula
emp = unichem.empirical_formula_from_percent({"C": 40.0, "H": 6.7, "O": 53.3})
print("Empirical formula from %:", emp)

# Balancing reactions
rxn = unichem.balance_reaction("H2 + O2 -> H2O")
print("\nBalanced:", rxn.balanced_string)

# Stoichiometry
yield_res = unichem.percent_yield(actual=8.5, theoretical=10.0)
print("Percent yield:", yield_res)

# Gas law (returns full tuple)
P, V, n, T = unichem.ideal_gas_law(V=0.022414, n=1.0, T=273.15)
print(f"\nIdeal gas (STP): P={P:.2f} Pa, V={V} m^3, n={n} mol, T={T} K")

# Acid/base
print("pH of 0.01 M HCl:", unichem.ph(0.01))
print("pOH of 0.01 M NaOH:", unichem.poh(0.01))
pH, pOH = unichem.ph_poh_from_conc(1e-4)
print(f"1e-4 M acid: pH={pH}, pOH={pOH}")

# Molarity
print("\nMolarity (0.5 mol in 2 L):", unichem.molarity(0.5, 2.0), "mol/L")
