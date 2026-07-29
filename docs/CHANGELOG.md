# DURAPY CHANGELOG

## 29.07.2026

- Removed @requires_square decorator from `unimath`.`linalg`, since it messed up type checking
- Removed CuPy imports, since they are not universally supported. DracoLIX will soon be in charge of HPC anyway.

- Fixed some invalid __ init __ files to avoid things like "from durapy import unicli.unicli"

- Added stronger/consistent typing all troughout the DuraPy codebase
- Added input validation to `unimath`.`linalg` - especially for matrix operations, replacing the deficient requires_square decorators
