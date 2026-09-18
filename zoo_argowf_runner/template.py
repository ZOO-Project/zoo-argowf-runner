# Description: This file contains the functions to generate the Argo workflow templates.
from __future__ import annotations

from typing import List

from hera.workflows import (
    Workflow,
)
from hera.workflows.models import (
    Arguments,
    Artifact,
    ConfigMapKeySelector,
    Inputs,
    Outputs,
    ParallelSteps,
    Parameter,
    PersistentVolumeClaim,
    ScriptTemplate,
    SemaphoreRef,
    Synchronization,
    Template,
    TemplateRef,
    ValueFrom,
    Volume,
    WorkflowStep,
)


class WorkflowTemplates:
    """
    A collection of utility methods for generating Argo workflow templates.
    """

    @staticmethod
    def create_synchronization(
        sync_type: str,
        config_map_ref_key: str,
        config_map_ref_name: str | None = None,
        optional: bool | None = None,
    ) -> Synchronization:
        """
        Creates a synchronization object.

        Args:
            sync_type (str): The type of synchronization (e.g., 'semaphore').
            config_map_ref_key (str): The key within the ConfigMap.
            config_map_ref_name (Optional[str]): Name of the ConfigMap.
            optional (Optional[bool]): Whether the reference is optional.

        Returns:
            Synchronization: A synchronization object.
        """
        if sync_type == "semaphore":
            semaphore = SemaphoreRef(
                config_map_key_ref=ConfigMapKeySelector(
                    name=config_map_ref_name, key=config_map_ref_key, optional=optional
                )
            )
            return Synchronization(semaphore=semaphore)
        raise ValueError("Unsupported synchronization type")

    @staticmethod
    def create_workflow_step(
        name: str,
        parameters: list[Parameter] | None = None,
        artifacts: list[Artifact] | None = None,
        template: str | None = None,
        template_ref: TemplateRef | None = None,
        continue_on: dict | None = None,
        when: str | None = None,
    ) -> WorkflowStep:
        """
        Creates a workflow step.

        Args:
            name (str): Name of the workflow step.
            parameters (Optional[List[Parameter]]): List of parameters.
            artifacts (Optional[List[Artifact]]): List of artifacts.
            template (Optional[str]): Name of the template.
            template_ref (Optional[TemplateRef]): Template reference object.
            continue_on (Optional[Dict]): Conditions for continuing execution.
            when (Optional[str]): Condition for step execution.

        Returns:
            WorkflowStep: A workflow step object.
        """
        arguments = Arguments(parameters=parameters, artifacts=artifacts)

        return WorkflowStep(
            name=name,
            template=template,
            arguments=arguments,
            template_ref=template_ref,
            continue_on=continue_on,
            when=when,
        )

    @staticmethod
    def create_template(
        name: str,
        sub_steps: list[WorkflowStep] | None = None,
        inputs_parameters: list[dict] | Inputs | None = None,
        inputs_artifacts: list[dict] | Inputs | None = None,
        outputs_parameters: list[dict] | Outputs | None = None,
        outputs_artifacts: list[dict] | Outputs | None = None,
        script: ScriptTemplate | None = None,
    ) -> Template:
        """
        Creates a template for a workflow.

        Args:
            name (str): Name of the template.
            sub_steps (Optional[List[WorkflowStep]]): Substeps within the template.
            inputs_parameters (Optional[Union[List[Dict], Inputs]]): Input parameters.
            inputs_artifacts (Optional[Union[List[Dict], Inputs]]): Input artifacts.
            outputs_parameters (Optional[Union[List[Dict], Outputs]]): Output parameters.
            outputs_artifacts (Optional[Union[List[Dict], Outputs]]): Output artifacts.
            script (Optional[ScriptTemplate]): Script template.

        Returns:
            Template: A workflow template object.
        """
        steps = (
            [ParallelSteps(__root__=[sub]) for sub in sub_steps] if sub_steps else None
        )

        inputs = Inputs()
        outputs = Outputs()

        if isinstance(inputs_parameters, List):
            inputs.parameters = [
                Parameter(name=elem["name"]) for elem in inputs_parameters
            ]
        elif isinstance(inputs_parameters, Inputs):
            inputs = inputs_parameters

        if isinstance(inputs_artifacts, List):
            inputs.artifacts = [
                Artifact(name=elem["name"], from_expression=elem.get("from_expression"))
                for elem in inputs_artifacts
            ]
        elif isinstance(inputs_artifacts, Inputs):
            inputs = inputs_artifacts

        if isinstance(outputs_parameters, List):
            parameters = [
                Parameter(
                    name=elem["name"],
                    value_from=ValueFrom(
                        expression=elem.get("expression"), path=elem.get("path")
                    ),
                )
                for elem in outputs_parameters
            ]
            outputs.parameters = parameters
        elif isinstance(outputs_parameters, Outputs):
            outputs = outputs_parameters

        if isinstance(outputs_artifacts, List):
            outputs.artifacts = [
                Artifact(name=elem["name"], from_expression=elem.get("from_expression"))
                for elem in outputs_artifacts
            ]
        elif isinstance(outputs_artifacts, Outputs):
            outputs = outputs_artifacts

        return Template(
            name=name,
            steps=steps,
            inputs=inputs if inputs.parameters or inputs.artifacts else None,
            outputs=outputs if outputs.parameters or outputs.artifacts else None,
            script=script,
        )

    @staticmethod
    def generate_workflow(
        name: str,
        entrypoint: str,
        service_account_name: str | None = None,
        annotations: dict | None = None,
        inputs: dict | None = None,
        synchronization: Synchronization | None = None,
        volume_claim_template: list[PersistentVolumeClaim] | None = None,
        secret_volume: list[Volume] | None = None,
        config_map_volume: list[Volume] | None = None,
        templates: list[Template] | None = None,
        namespace: str | None = None,
    ) -> Workflow:
        """
        Generates an Argo Workflow.

        Args:
            name (str): Name of the workflow.
            entrypoint (str): Entrypoint template.
            service_account_name (Optional[str]): Service account for the workflow.
            annotations (Optional[Dict]): Workflow annotations.
            inputs (Optional[Dict]): Workflow inputs as key-value pairs.
            synchronization (Optional[Synchronization]): Workflow synchronization object.
            volume_claim_template (Optional[List[PersistentVolumeClaim]]): PVC templates.
            secret_volume (Optional[List[Volume]]): Secret volumes.
            config_map_volume (Optional[List[Volume]]): ConfigMap volumes.
            templates (Optional[List[Template]]): Workflow templates.
            namespace (Optional[str]): Kubernetes namespace for the workflow.

        Returns:
            Workflow: A fully constructed workflow object.
        """
        arguments = [
            Parameter(name=key, value=str(value))
            for key, value in (inputs or {}).items()
        ]

        volumes = []
        if secret_volume:
            volumes.extend(secret_volume)
        if config_map_volume:
            volumes.extend(config_map_volume)

        return Workflow(
            name=name,
            entrypoint=entrypoint,
            annotations=annotations,
            namespace=namespace,
            service_account_name=service_account_name,
            synchronization=synchronization,
            arguments=Arguments(parameters=arguments) if arguments else None,
            volume_claim_templates=volume_claim_template,
            volumes=volumes,
            templates=templates,
        )
