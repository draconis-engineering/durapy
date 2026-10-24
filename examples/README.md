# DuraPy Examples

A collection of clean, runnable examples demonstrating DuraPy's modules.

## Quick start

```bash
# From the repository root (with dependencies installed)
PYTHONPATH=src python examples/unimath/01_vectors_matrices.py
```

## Available examples

| Example | Description |
| --- | --- |
| `unimath/01_vectors_matrices.py` | Vectors, matrices, dot products, determinants, trig & number theory |
| `uniphys/01_mechanics_thermo_fluids.py` | Mechanics, thermodynamics (Quantity returns), fluid dynamics, acoustics |
| `unisky/01_aerospace_basics.py` | Mach, Reynolds, lift/drag, Bernoulli, rocket equations, gas law |
| `unichem/01_chemistry_basics.py` | Periodic table, formulas, stoichiometry, balancing, gas law, pH |
| `unipower/01_circuit_basics.py` | Ohm's law, power, voltage dividers, components, RC circuits |
| `uniops/01_pid_control.py` | PID controller usage and kinematics module overview |
| `uniCLI/01_cli_basics.py` | Console helpers and progress bars |

## Tips

- Many physics functions now return `Quantity` objects from `durapy.shared.numval_types`. You can access `.value` or convert as needed.
- `uniphys.thermodynamics.ideal_gas_law` and `uniphys.fluid_dynamics` are the canonical implementations; `unisky` and `unichem` provide thin wrappers.
- For linear algebra, DuraPy is migrating toward DracoLIX, but the current `unimath.linalg` API still works for most use cases.
