# Contributing to DuraPy

Thank you for taking the time to contribute! We welcome contributions of all kinds, including bug fixes, new features, documentation updates, and feedback.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and welcoming to all maintainers and contributors.

## How Can I Contribute?

### Reporting Bugs

- Check the **Issues** tab to ensure the bug hasn't already been reported.
- If it is a new bug, open an issue using the bug report template.
- Provide a clear description, steps to reproduce, and your environment setup.

### Suggesting Enhancements

- Open an issue outlining your proposed change.
- Explain the use case and why this enhancement would be valuable to the community.

### Submitting Pull Requests (PRs)

1. **Fork the Repository:** Create your own copy of the repository on your account.
2. **Create a Branch:** Use a descriptive branch name (e.g., `feature/add-login` or `fix/typo-in-readme`).
3. **Keep it Focused:** Make sure your PR addresses a single issue or feature.
4. **Write Tests:** If you are adding code, include tests that cover your changes.
5. **Run Linting:** Ensure your code matches the existing style guidelines.
6. **Submit:** Open a PR against the `main` branch. Provide a clear description of your changes in the PR template.

## Development Setup

To set up your local development environment:

```bash
# Clone your fork
git clone https://github.com/draconis-engineering/durapy.git
cd durapy

# We strongly recommend using uv to manage virtual enviroments
uv sync
```

## Commit Message Guidelines

We recommend using clear and descriptive commit messages. Following the **Conventional Commits** specification is highly encouraged:

- `feat: add user authentication`
- `fix: resolve crash on startup`
- `docs: update setup instructions`
