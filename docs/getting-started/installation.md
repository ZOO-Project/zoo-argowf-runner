# Installation

## Requirements

- Python 3.8 or higher
- A running Argo Workflows installation, reachable from wherever the runner executes
- A Kubernetes cluster with an RWX-capable storage class

## From PyPI

```bash
pip install zoo-argowf-runner
```

`zoo-runner-common` is installed automatically as a dependency.

## From source

```bash
git clone https://github.com/ZOO-Project/zoo-argowf-runner.git
cd zoo-argowf-runner
pip install -e .
```

Use `-e` (editable mode) if you're developing against this runner — see [Contributing](../development/contributing.md) for the full dev setup.

## Verify

```bash
python -c "from zoo_argowf_runner.runner import ZooArgoWorkflowsRunner; print('OK')"
```

## Next

- [Quick Start](quickstart.md)