# Contributing to zoo-argowf-runner

Thank you for your interest in contributing to `zoo-argowf-runner`! This document provides guidelines for contributing to the project.

## Overview

`zoo-argowf-runner` is a Python library that acts as a plugin for the [ZOO-Project](https://github.com/ZOO-Project/ZOO-Project), enabling it to submit jobs as [Argo Workflows](https://argoproj.github.io/argo-workflows/). This allows the ZOO-Project to run an Application Package encoded in CWL as a Calrissian job on Kubernetes, orchestrated through Argo Workflows. The project uses [Hatch](https://hatch.pypa.io/) as its build and development tool.

---

> **Important:** Always open your Pull Request against the `develop` branch, **not** `main`.
> Pull Requests targeting `main` directly will not be accepted.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- [Hatch](https://hatch.pypa.io/latest/install/) (`pip install hatch`)
- Access to a Kubernetes cluster with [Argo Workflows](https://argoproj.github.io/argo-workflows/) installed (for integration testing)

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/ZOO-Project/zoo-argowf-runner.git
   cd zoo-argowf-runner
   ```

2. **Install Hatch**

   ```bash
   pip install hatch
   ```

3. **Enter the Default Development Environment**

   Hatch automatically creates and manages a virtual environment for you:

   ```bash
   hatch shell
   ```

   This installs all dependencies defined under `[tool.hatch.envs.default]` in `pyproject.toml`.

4. **Verify Installation**

   ```bash
   python -c "from zoo_argowf_runner import ArgoWFRunner; print('OK')"
   ```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use these prefixes:

- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `refactor/` — Code refactoring
- `test/` — Test additions or fixes

### 2. Make Changes

Follow the coding standards described in the [Code Standards](#code-standards) section below.

### 3. Run Tests

The project uses `pytest` for testing via a dedicated Hatch environment:

```bash
# Run tests
hatch run test:test

# Run tests quietly
hatch run test:test-q
```

Test dependencies (`pytest`, `pytest-cov`) are defined under `[tool.hatch.envs.test]` in `pyproject.toml`.

### 4. Update Documentation

- Update docstrings in the source code
- Update relevant sections of `README.md`
- If adding or changing environment variables (e.g. `ARGO_WF_ENDPOINT`, `ARGO_WF_TOKEN`), document them in the **Environment variables** section of `README.md`
- If changing the required Argo Workflows `WorkflowTemplate` interface (inputs/outputs/artifacts), update the corresponding section of `README.md` and the example under `example/`

### 5. Commit Changes

Write clear, conventional commit messages:

```bash
git add .
git commit -m "feat: add support for custom Argo Workflows synchronization configmap"
```

Commit types:

- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation only
- `style` — Formatting, no logic change
- `refactor` — Code restructuring
- `test` — Adding or updating tests
- `chore` — Maintenance, dependency updates

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:

- **Base branch set to `develop`** - this is required
- A clear title and description
- Reference to any related issues (`Closes #123`)
- A summary of what changed and why
- Notes on any breaking changes

> **Reminder:** The base branch of your PR must be `develop`, not `main`.
> `main` is only updated by maintainers when cutting a release from `develop`.

---

## Hatch Environments

The project defines two Hatch environments in `pyproject.toml`:

| Environment | Purpose | Key Command |
|---|---|---|
| `default` | Day-to-day development | `hatch shell` |
| `test` | Running tests | `hatch run test:test` |

---

## Code Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use **type hints** on all public methods
- Use **Google-style docstrings**
- Lint and format code with [`ruff`](https://docs.astral.sh/ruff/) before committing
- Minimum Python version: **3.10** (for testing); the package itself supports **3.8+**

**Good example:**

```python
def submit_argo_workflow(self, cwl_workflow: str, parameters: dict) -> str:
    """
    Submit a CWL workflow as an Argo Workflow run.

    Args:
        cwl_workflow: CWL document encoded in JSON format.
        parameters: Workflow input parameters in JSON format.

    Returns:
        The name of the submitted Argo Workflow.

    Raises:
        ValueError: If cwl_workflow is empty or invalid.
    """
    if not cwl_workflow:
        raise ValueError("cwl_workflow must not be empty")
    ...
```

### Error Handling

Catch specific exceptions and use structured logging via `loguru`:

```python
from loguru import logger

def load_config(self, path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"Config file not found: {path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {path}: {e}")
        raise
```

### Versioning

The package version is managed in `zoo_argowf_runner/__about__.py`. Do **not** manually edit the version; it is updated as part of the release process.

---

## Testing Guidelines

### Unit Tests

Place unit tests under `tests/` and name files `test_*.py`:

```python
# tests/test_runner.py
import unittest
from zoo_argowf_runner import ArgoWFRunner

class TestArgoWFRunner(unittest.TestCase):

    def test_initialization(self):
        """Test that the runner initializes correctly."""
        conf = {"lenv": {"message": ""}}
        runner = ArgoWFRunner(conf)
        self.assertIsNotNone(runner)
```

### Coverage

Aim for **>80%** code coverage. Run the coverage report with:

```bash
hatch run test:test --cov
```

`pytest-cov` is included as a test dependency in `pyproject.toml`.

---

## Argo Workflows Requirements for Testing

Integration tests rely on a Kubernetes cluster with an Argo Workflows `WorkflowTemplate` (or `ClusterWorkflowTemplate`) implementing the Calrissian job execution interface described in `README.md`. Before submitting a PR that touches the Argo Workflows interaction logic:

- Verify the input parameters (`parameters`, `cwl`, `max_ram`, `max_cores`, `entry_point`) are respected
- Verify the expected outputs (`results`, `log`, `usage-report`, `stac-catalog`, `feature-collection`) and artifacts (`tool-logs`, `calrissian-output`, `calrissian-stderr`, `calrissian-report`) are correctly retrieved
- If your change affects additional volumes (e.g. ConfigMaps) used by the CWL wrapper, refer to the **Caveats** section of `README.md` regarding declaring volumes on both the `WorkflowTemplate` and the calling `Workflow`

---

## Release Process

Releases are managed by project maintainers:

1. Ensure all changes are merged into `develop` and tested
2. Update the version in `zoo_argowf_runner/__about__.py`
3. Update `CHANGELOG.md` (if present)
4. Merge `develop` into `main`
5. Create and push a release tag
6. Build and publish the package:

   ```bash
   hatch build
   hatch publish
   ```

---

## Getting Help

- **Bug reports / feature requests**: [Open an issue](https://github.com/ZOO-Project/zoo-argowf-runner/issues)
- **Contact**: Email the maintainers

---

## Code of Conduct

We are committed to a welcoming and inclusive environment. When participating:

- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the project and community
- Show empathy towards other contributors

---

## License

By contributing, you agree that your contributions will be licensed under the **Apache License 2.0**, the same license as this project.

---

Thank you for contributing! 🎉