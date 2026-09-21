# Contributing

`zoo-argowf-runner` uses [Hatch](https://hatch.pypa.io/) for development. Full contributor guidelines (branching, commit style, code standards, release process) live in [`CONTRIBUTING.md`](https://github.com/ZOO-Project/zoo-argowf-runner/blob/develop/contributing.md) at the repository root — this page covers just the essentials to get running.

!!! warning "Base branch"
    Always open Pull Requests against `develop`, not `main`.

## Setup

```bash
git clone https://github.com/ZOO-Project/zoo-argowf-runner.git
cd zoo-argowf-runner
pip install hatch
hatch shell
```

## Workflow

```bash
git checkout -b feature/your-feature-name
# make changes
hatch run test:test          # run tests
hatch run test:test --cov    # with coverage (aim for >80%)
```

If you touch environment variables or the Argo `WorkflowTemplate` interface, update the [Runner Guide](../user-guide/runner.md#caveat-additional-volumes) too — the API reference regenerates automatically from docstrings, so keep those current in the source.

## Code standards

- [PEP 8](https://peps.python.org/pep-0008/), type hints on public methods, Google-style docstrings
- Lint with [`ruff`](https://docs.astral.sh/ruff/) before committing
- Tested on Python 3.10+ (package supports 3.8+)

## Getting help

[Open an issue](https://github.com/ZOO-Project/zoo-argowf-runner/issues) for bugs or feature requests.