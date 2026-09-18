# Quick Start

A minimal ZOO service built with `ZooArgoWorkflowsRunner`, adapted from the `water_bodies` example in the repository's `tests/` folder.

## 1. Implement an ExecutionHandler

```python
from loguru import logger
from zoo_argowf_runner.runner import ExecutionHandler, ZooArgoWorkflowsRunner


class ArgoWFRunnerExecutionHandler(ExecutionHandler):
    def __init__(self, conf):
        self.conf = conf

    def get_pod_env_vars(self):
        return {"A": "1", "B": "1"}

    def get_pod_node_selector(self):
        return None

    def get_secrets(self):
        pass

    def get_additional_parameters(self):
        return {
            "s3_bucket": "results",
            "sub_path": self.conf["lenv"]["usid"],
            "region_name": "it-rom",
            "endpoint_url": "http://minio.ns1.svc.cluster.local:9000",
        }

    def handle_outputs(self, log, output, usage_report, tool_logs, **kwargs):
        execution = kwargs.get("execution")
        tool_logs = execution.get_tool_logs()
        # map tool_logs into self.conf["service_logs"] for ZOO to expose
```

## 2. Wire it up in a ZOO service

`service.py` must implement `{workflow_id}(conf, inputs, outputs)`:

```python
import os, pathlib, yaml

try:
    import zoo
except ImportError:
    from zoo_runner_common.zoostub import ZooStub
    zoo = ZooStub()


def water_bodies(conf, inputs, outputs):
    with open(
        os.path.join(pathlib.Path(__file__).parent.absolute(), "app-package.cwl")
    ) as stream:
        cwl = yaml.safe_load(stream)

    runner = ZooArgoWorkflowsRunner(
        cwl=cwl,
        conf=conf,
        inputs=inputs,
        outputs=outputs,
        execution_handler=ArgoWFRunnerExecutionHandler(conf=conf),
    )
    exit_status = runner.execute()

    if exit_status == zoo.SERVICE_SUCCEEDED:
        outputs = runner.outputs
        return zoo.SERVICE_SUCCEEDED

    conf["lenv"]["message"] = zoo._("Execution failed")
    return zoo.SERVICE_FAILED
```

## What `runner.execute()` does

1. Validates parameters and calls `handler.pre_execution_hook()`.
2. Merges `handler.get_additional_parameters()` with the CWL processing parameters.
3. Submits the workflow, monitors it, and reports progress back to ZOO.
4. Retrieves outputs, logs, and artifacts, then calls `handler.handle_outputs()`.

See the [Runner Guide](../user-guide/runner.md) for the env vars this depends on (`ARGO_WF_ENDPOINT`, etc.) and the [full example](https://github.com/ZOO-Project/zoo-argowf-runner/tree/develop/tests/water_bodies) in the repository.