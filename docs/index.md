# zoo-argowf-runner

`zoo-argowf-runner` is a [ZOO-Project](https://github.com/ZOO-Project) runner that executes CWL Application Packages on Kubernetes using **Argo Workflows**.

## Overview

The package provides `ZooArgoWorkflowsRunner`, which submits a CWL Application Package to an Argo Workflows `WorkflowTemplate`, monitors the resulting `Workflow`, and maps its outputs back to ZOO-Project. It builds on shared foundations from [zoo-runner-common](https://zoo-project.github.io/zoo-runner-common/) rather than reimplementing runner plumbing from scratch.

## Architecture

```
zoo-runner-common: BaseRunner (abstract)
        │
        └── ZooArgoWorkflowsRunner (this package)
                │
                ▼
        Argo Workflows WorkflowTemplate ("calrissian-runner")
                │
                ▼
        Calrissian Job — runs the CWL Application Package on Kubernetes
```

`ZooArgoWorkflowsRunner` inherits most of its interface unchanged from `BaseRunner` — this package only adds what's specific to Argo Workflows: submitting the `Workflow`, monitoring it, and translating its outputs.

## Where to go next

- **[Installation](getting-started/installation.md)**
- **[Quick Start](getting-started/quickstart.md)** — a working ZOO service using `ZooArgoWorkflowsRunner`
- **[Runner Guide](user-guide/runner.md)** — environment variables and the Argo `WorkflowTemplate` interface
- **[Handlers Guide](user-guide/handlers.md)** — implementing a custom `ExecutionHandler`
- **[API Reference](api/runner.md)**