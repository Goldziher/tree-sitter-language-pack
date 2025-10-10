# Contributing to Tree-Sitter Language Pack

Thank you for your interest in contributing to tree-sitter-language-pack! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Adding Languages](#adding-languages)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Maintenance Tasks](#maintenance-tasks)

## Getting Started

Before contributing, please:

1. Check existing [issues](https://github.com/Goldziher/tree-sitter-language-pack/issues) and [pull requests](https://github.com/Goldziher/tree-sitter-language-pack/pulls) to avoid duplicating work
1. For significant changes, open an issue first to discuss your proposal
1. Ensure you have Python 3.10+ installed
1. Install [uv](https://github.com/astral-sh/uv) for dependency management

## Development Setup

### Prerequisites

- Python 3.10 or higher
- C compiler (gcc, clang, or MSVC)
- Git
- [uv](https://github.com/astral-sh/uv) package manager

### Initial Setup

1. **Fork and clone the repository**

    ```bash
    git clone https://github.com/YOUR_USERNAME/tree-sitter-language-pack.git
    cd tree-sitter-language-pack
    ```

1. **Install development dependencies**

    ```bash
    uv sync --no-install-project
    ```

1. **Generate AI rule documentation**

    ```bash
    npx -y ai-rulez@latest --update-gitignore
    ```

    This command refreshes `AGENTS.md`, `CLAUDE.md`, and the other AI guidance files while keeping the generated artifacts out of version control.

1. **Install prek hooks**

    ```bash
    uv tool install prek
    prek install
    prek install --hook-type commit-msg
    ```

1. **Clone language repositories**

    ```bash
    uv run --no-sync scripts/clone_vendors.py
    ```

1. **Build local extensions**

    ```bash
    PROJECT_ROOT=. uv run setup.py build_ext --inplace
    ```

## Development Workflow

### Running Tests

Run the test suite to ensure everything is working:

```bash
PROJECT_ROOT=. uv run --no-sync pytest tests
```

Run tests for a specific language:

```bash
PROJECT_ROOT=. uv run --no-sync pytest tests -k test_can_load_language[python]
```

### Code Quality Checks

The project uses several tools to maintain code quality:

- **Ruff** for linting and formatting
- **mypy** for type checking
- **prek** for automated checks

Run all checks manually:

```bash
# Run all linters and formatters managed by prek
prek run --all-files

# Type checking
uv run --no-sync mypy

# Linting without auto-fixes (optional)
uv run --no-sync ruff check

# Format code (optional when not using prek)
uv run --no-sync ruff format
```

### Building Distributions

To build source and wheel distributions:

```bash
# Build source distribution only
PROJECT_ROOT=. uv build --sdist

# Build wheel only
PROJECT_ROOT=. uv build --wheel

# Build both
PROJECT_ROOT=. uv build
```

## Adding Languages

### Adding a Pre-installed Language Package

Some languages are distributed as separate packages and installed as dependencies:

1. **Add the dependency**

    ```bash
    uv add tree-sitter-<language> --no-install-project
    ```

1. **Update the code**

    - Add the language to `InstalledBindings` literal type in `tree_sitter_language_pack/__init__.py`
    - Update the `installed_bindings_map` dictionary

1. **Clone vendors and rebuild**

    ```bash
    uv run --no-sync scripts/clone_vendors.py
    PROJECT_ROOT=. uv run setup.py build_ext --inplace
    ```

### Adding a Binary Wheel Language

Most languages are built from source and included in the wheel:

1. **Add language definition**

    Edit `sources/language_definitions.json`:

    ```json
    {
      "language_name": {
        "repo": "https://github.com/tree-sitter/tree-sitter-language",
        "rev": "commit-hash",
        "branch": "main",
        "directory": "path/to/src",
        "generate": false
      }
    }
    ```

    Fields:

    - `repo` (required): Repository URL
    - `rev` (required): Specific commit hash for reproducible builds
    - `branch` (optional): Branch name if not "main"
    - `directory` (optional): Path to src folder if not in root
    - `generate` (optional): Run tree-sitter generate command

1. **Update type definitions**

    Add the language to `SupportedLanguage` literal type in `tree_sitter_language_pack/__init__.py`

1. **Clone and build**

    ```bash
    uv run --no-sync scripts/clone_vendors.py
    PROJECT_ROOT=. uv run setup.py build_ext --inplace
    ```

1. **Update documentation**

    Add the language to the README.md language list with its license

1. **Test your addition**

    ```bash
    PROJECT_ROOT=. uv run --no-sync pytest tests -k test_can_load_language[language_name]
    ```

## Testing

### Writing Tests

When adding a new language, ensure it's covered by the existing parametrized tests in `tests/entry_point_test.py`.

For new functionality, add appropriate test cases following the existing patterns.

### Test Coverage

Ensure your changes maintain or improve test coverage. Run tests with coverage:

```bash
PROJECT_ROOT=. uv run --no-sync pytest tests --cov=tree_sitter_language_pack
```

## Code Style

### Python Code

- Follow PEP 8 with a line length of 120 characters
- Use type hints for all function signatures
- Add docstrings for public functions and classes
- Use meaningful variable names

### Commit Messages

We use conventional commits. Examples:

- `feat: add support for tree-sitter-language`
- `fix: correct parser initialization for language`
- `docs: update installation instructions`
- `chore: update dependencies`
- `test: add tests for new language`

## Submitting Changes

1. **Create a feature branch**

    ```bash
    git checkout -b feat/add-language-support
    ```

1. **Make your changes**

    - Follow the coding standards
    - Add tests for new functionality
    - Update documentation as needed

1. **Commit your changes**

    ```bash
    git add .
    git commit -m "feat: add support for new language"
    ```

1. **Push to your fork**

    ```bash
    git push origin feat/add-language-support
    ```

1. **Create a Pull Request**

    - Fill out the PR template completely
    - Link any related issues
    - Ensure CI checks pass

## Maintenance Tasks

### Updating Language Versions

To update language repositories to their latest versions:

```bash
# Update all languages
uv run --no-sync scripts/pin_vendors.py

# Update only missing revisions
uv run --no-sync scripts/pin_vendors.py --only-missing

# Update specific languages
uv run --no-sync scripts/pin_vendors.py --languages=python,rust,go
```

### Releasing New Versions

1. Update version in `pyproject.toml`
1. Ensure all tests pass
1. Create a git tag
1. Push the tag to trigger the release workflow

### CI/CD

The project uses GitHub Actions for:

- Running tests on multiple Python versions and platforms
- Building wheels for different architectures
- Publishing to PyPI on tagged releases

## Questions?

If you have questions or need help:

1. Check existing issues and discussions
1. Open a new issue with your question
1. Join the discussion in relevant PRs

Thank you for contributing to tree-sitter-language-pack!
