# Handlers Guide

`zoo_argowf_runner.handlers.ExecutionHandler` re-exports `ExecutionHandler` from [zoo-runner-common](https://zoo-project.github.io/zoo-runner-common/). It's the customization point for `ZooArgoWorkflowsRunner` — the runner calls into it at each stage of execution, so service-specific logic (credentials, output handling) doesn't need to touch the runner itself.

## Methods to implement

| Method | Called when | Typical use |
|---|---|---|
| `pre_execution_hook()` | Before submission | Validate environment |
| `get_additional_parameters()` | Building processing parameters | Service-specific values (bucket, region, credentials) |
| `get_pod_env_vars()` | Building the pod spec | Env vars for the Calrissian pod |
| `get_pod_node_selector()` | Building the pod spec | Constrain scheduling |
| `get_secrets()` | Building the pod spec | Attach Kubernetes secrets |
| `handle_outputs(log, output, usage_report, tool_logs, **kwargs)` | After execution | Map outputs into `conf`/`outputs` |
| `post_execution_hook(...)` | After `handle_outputs` | Cleanup, notifications |

## Example

```python
from zoo_argowf_runner.handlers import ExecutionHandler


class MyExecutionHandler(ExecutionHandler):
    def __init__(self, conf):
        self.conf = conf

    def get_pod_env_vars(self):
        return {"MY_ENV_VAR": "value"}

    def get_pod_node_selector(self):
        return None

    def get_secrets(self):
        return None

    def get_additional_parameters(self):
        return {"s3_bucket": "results", "sub_path": self.conf["lenv"]["usid"]}

    def handle_outputs(self, log, output, usage_report, tool_logs, **kwargs):
        # process outputs here
        pass
```

Pass it in when constructing the runner:

```python
runner = ZooArgoWorkflowsRunner(
    cwl=cwl,
    conf=conf,
    inputs=inputs,
    outputs=outputs,
    execution_handler=MyExecutionHandler(conf=conf),
)
```

## See also

- [API Reference](../api/handlers.md)
- [Quick Start](../getting-started/quickstart.md) for a complete, runnable example