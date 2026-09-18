# Runner Guide

`ZooArgoWorkflowsRunner` inherits from `BaseRunner` in [zoo-runner-common](https://zoo-project.github.io/zoo-runner-common/) and adds the Argo-specific `execute()` implementation.

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `STORAGE_CLASS` | Kubernetes RWX storage class. | `standard` |
| `DEFAULT_VOLUME_SIZE` | Calrissian default RWX volume size. | `12Gi` |
| `DEFAULT_MAX_CORES` | Calrissian default max cores. | `4` |
| `DEFAULT_MAX_RAM` | Calrissian default max RAM. | `4Gi` |
| `ARGO_WF_ENDPOINT` | Argo Workflows API endpoint. | `http://localhost:2746` |
| `ARGO_WF_TOKEN` | Argo Workflows API token — see below. | — |
| `ARGO_WF_SYNCHRONIZATION_CM` | Synchronization ConfigMap (key `workflow`). | — |
| `ARGO_CWL_RUNNER_TEMPLATE` | `WorkflowTemplate` that runs the CWL. | `argo-cwl-runner` |
| `ARGO_CWL_RUNNER_ENTRYPOINT` | Entrypoint template within it. | `calrissian-runner` |

Retrieve `ARGO_WF_TOKEN` with:

```bash
kubectl get -n ns1 secret argo.service-account-token -o=jsonpath='{.data.token}' | base64 --decode
```

## The Argo WorkflowTemplate interface

Argo Workflows must expose a `WorkflowTemplate` (or `ClusterWorkflowTemplate`) with this interface:

**Inputs:** `parameters` (JSON), `cwl` (JSON), `max_ram`, `max_cores`, `entry_point`.

**Outputs:** `results` (stdout), `log` (stderr), `usage-report`, `stac-catalog`, `feature-collection`.

**Artifacts:** `tool-logs`, `calrissian-output`, `calrissian-stderr`, `calrissian-report`.

See the [`example`](https://github.com/ZOO-Project/zoo-argowf-runner/tree/develop/example) folder in the repository for a complete `WorkflowTemplate` implementing this interface.

## Caveat: additional volumes

If the `WorkflowTemplate` declares a volume (e.g. a ConfigMap for `cwl-wrapper` config), that volume must **also** be declared on the calling `Workflow` — Argo doesn't propagate volume declarations back to the caller. Use `zoo_argowf_runner.volume.VolumeTemplates`:

```python
from zoo_argowf_runner.volume import VolumeTemplates

VolumeTemplates.create_config_map_volume(
    name="cwl-wrapper-config-vol",
    config_map_name="cwl-wrapper-config",
    items=[{"key": "main.yaml", "path": "main.yaml", "mode": 420}],
    default_mode=420,
    optional=False,
)
```

Keep the `items` keys in sync between the `WorkflowTemplate` and the caller — a mismatch is a common cause of "volume not found" errors at runtime.

## See also

- [API Reference](../api/runner.md)
- [Handlers Guide](handlers.md)