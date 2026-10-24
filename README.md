# DuraPy

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.1.3-blue.svg)](pyproject.toml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**A unified Python toolbox for STEM workflows — from linear algebra and physics to chemistry, electronics, aerospace, and robotics.**

DuraPy brings scientific computing, engineering utilities, and domain-specific solvers together under one coherent API. It features a custom unit/quantity system, a growing set of domain modules, and performance-minded components like [DracoLIX](https://github.com/draconis-engineering/DracoLIX) for numerical work.

## Highlights

- **Type-safe physical quantities** — `Quantity`, `Unit`, `Dimension`, and `Constant` with dimensional awareness and operator overloading
- **Domain coverage** — Math, physics, chemistry, bioinformatics, electronics/circuits, aerospace, robotics/controls, ML utilities, and crypto
- **Circuit simulation** — Modified Nodal Analysis (MNA) for DC/AC, RLC analysis, filters, power factor, and component models
- **Aerospace & fluid dynamics** — Bernoulli, Reynolds, Mach, lift/drag, rocket equations, and gas laws
- **Chemistry toolkit** — Full periodic table (118 elements), formula parsing, stoichiometry, reaction balancing, acid/base, and gas laws
- **Clean, composable API** — Reusable primitives with domain-specific facades where it makes sense

## Quick Start

### Installation

```bash
pip install durapy
```

Or install from source:

```bash
git clone https://github.com/draconis-engineering/durapy.git
cd durapy
pip install -e .
```

### Usage

```python
from durapy.unimath import linalg
from durapy.uniphys import mechanics, thermodynamics
from durapy.unisky import mach_number, reynolds_number

# Linear algebra
A = linalg.Matrix([[1, 2], [3, 4]])
print("det(A) =", A.det)

# Physics (returns Quantity objects)
print("Torque:", mechanics.torque(0.3, 50))
P, V, n, T = thermodynamics.ideal_gas_law(V=0.022414, n=1.0, T=273.15)
print(f"STP pressure: {P:.2f} Pa")

# Aerospace
print(mach_number(340))
print("Re:", reynolds_number(60, 1.5, 1.5e-5))
```

More examples can be found in [`examples/`](examples/).

## Module Overview

| Module | Purpose |
| --- | --- |
| `durapy.shared` | Core primitives: `Quantity`, `Unit`, `Dimension`, `Constant`, color systems, exceptions |
| `durapy.unimath` | Linear algebra (with DracoLIX backend), algebra, geometry, coordinate systems, number theory, trigonometry |
| `durapy.uniphys` | Physics: mechanics, thermodynamics, fluid dynamics, acoustics, electromagnetics, astrophysics, nuclear, quantum |
| `durapy.unisky` | Aerospace/spaceflight: aerodynamics, propulsion, gas laws, Bernoulli, rocket equations (built on `uniphys`) |
| `durapy.unichem` | Chemistry: periodic table, formula parsing/molar mass, stoichiometry, balancing, acid/base, gas laws |
| `durapy.unipower` | Electronics: component models, MNA circuit solver (DC/AC), RLC/filters, power analysis |
| `durapy.uniops` | Robotics/mechatronics: kinematics, dynamics, PID controllers |
| `durapy.unibio` | Bioinformatics: sequence tools, ORFs, GC content, melting temp, translation |
| `durapy.unicogni` | ML/NLP utilities and activation/loss functions |
| `durapy.unicrypto` | Cryptography primitives |
| `durapy.uniCLI` | CLI framework utilities |

## Documentation

- [Examples](examples/README.md) — Runnable, up-to-date usage examples
- [Changelog](docs/CHANGELOG.md) — Release history and notable changes
- [TODO](docs/TODO.md) — Tracked improvements and known gaps

## Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/draconis-engineering/durapy).

## License

Distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
