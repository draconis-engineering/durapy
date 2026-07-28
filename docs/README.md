# DuraPy - An Open-Source Python Toolbox for STEM Workflows | By Draconis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

DuraPy is a growing toolbox for science, engineering, and STEM workflows. It brings together helpful utilities for mathematics, physics, robotics, chemistry-adjacent calculations, and more under one Python universal package.

## What makes it useful

- A practical math layer for geometry, trigonometry, and algebra
- Physics constants and helper modules for scientific exploration
- A lightweight foundation for future CLI tools and engineering utilities
- A simple package structure that is easy to extend

## Installation

```bash
pip install durapy
```

## Modules

DuraPy is composed of several submodules, each providing a specific set of functionality.

- MaxCompute: C++-based library for high-performance numerical computations
- Shared Library: a collection of shared utilities for all submodules
    - Color Systems - a collection of color systems and color space conversions, such as RGB, HEX, and CMYK
    - Constants, Numerical Value types, and Unit modules, for scientific calculations
    - Exceptions - Custom exception classes for error handling

- UniCLI - a command-line interface framework for making CLI tools
- UniCogni - Advanced AI/ML utilities for natural language processing and machine learning
- UniCrypto - Cryptographic utilities for encryption and decryption
- UniMath - Mathematical utilities for numerical computations
    - Basic Algebra - Tools for basic algebraic operations
    - Linear Algebra - Tools for linear algebra operations, built on top of NumPy + Custom types for Matrices and Vectors
    - Coordinate Systems - Custom types for representing points and vectors in N-dimensional space, such as Cartesian, polar, and spherical coordinates
    - Geometry, Number Theory and Trigonometry - Tools for geometric calculations and trigonometric functions
    - Decorators and Exceptions - utilities for decorators and exception handling, providing error-free and mathematically correct calculations

- UniOps - A framework built for mechatronics and robotics, providing kinematics and dynamics utilities
- UniPhys - A physics calculation library, providing calculation resources for a range of domains
    - Acoustics
    - Astrophysics
    - Electromagnetics
    - Fluid Dynamics
    - Mechanics
    - Nuclear Physics
    - Quantum Physics
    - Thermodynamics

- UniPower - An advanced electronics/electrical engineering library, providing electrical component models, circuit simulation, and power analysis tools
- UniSky - Aerospace/Spaceflight simulation and analysis tools

## Suggested next improvements

If you want to evolve the package further, the most impactful next steps are:

- Add more polished examples and tutorials
- Create a small CLI for common calculations
- Add documentation pages for each submodule
- Introduce a richer test suite and versioned release workflow

DuraPy is intentionally open-ended, so it can grow into whatever your STEM projects need next.
