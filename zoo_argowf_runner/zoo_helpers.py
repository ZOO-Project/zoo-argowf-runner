# Description: Helper classes for the zoo-argowf-runner
import os
import attr
import inspect
import cwl_utils
from cwl_utils.parser import load_document_by_yaml


# useful class for hints in CWL
@attr.s
class ResourceRequirement:
    coresMin = attr.ib(default=None)
    coresMax = attr.ib(default=None)
    ramMin = attr.ib(default=None)
    ramMax = attr.ib(default=None)
    tmpdirMin = attr.ib(default=None)
    tmpdirMax = attr.ib(default=None)
    outdirMin = attr.ib(default=None)
    outdirMax = attr.ib(default=None)

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


class CWLWorkflow:
    def __init__(self, cwl, workflow_id):
        self.raw_cwl = cwl
        parsed_cwl = load_document_by_yaml(cwl, "io://")

        # Ensure self.cwl is always a list
        if not isinstance(parsed_cwl, list):
            parsed_cwl = [parsed_cwl]

        self.cwl = parsed_cwl
        self.workflow_id = workflow_id

    def get_version(self):

        return self.raw_cwl.get("s:softwareVersion", "")

    def get_label(self):

        return self.get_workflow().label

    def get_doc(self):

        return self.get_workflow().doc

    def get_workflow(self) -> cwl_utils.parser.cwl_v1_0.Workflow:
        # returns a cwl_utils.parser.cwl_v1_0.Workflow)
        ids = [elem.id.split("#")[-1] for elem in self.cwl]

        return self.cwl[ids.index(self.workflow_id)]

    def get_object_by_id(self, id):
        ids = [elem.id.split("#")[-1] for elem in self.cwl]
        return self.cwl[ids.index(id)]

    def get_workflow_inputs(self, mandatory=False):
        inputs = []
        for inp in self.get_workflow().inputs:
            if mandatory:
                if inp.default is not None or inp.type == ["null", "string"]:
                    continue
                else:
                    inputs.append(inp.id.split("/")[-1])
            else:
                inputs.append(inp.id.split("/")[-1])
        return inputs

    @staticmethod
    def has_scatter_requirement(workflow):
        return any(
            isinstance(
                requirement,
                (
                    cwl_utils.parser.cwl_v1_0.ScatterFeatureRequirement,
                    cwl_utils.parser.cwl_v1_1.ScatterFeatureRequirement,
                    cwl_utils.parser.cwl_v1_2.ScatterFeatureRequirement,
                ),
            )
            for requirement in workflow.requirements
        )

    @staticmethod
    def get_resource_requirement(elem):
        """Gets the ResourceRequirement out of a CommandLineTool or Workflow

        Args:
            elem (CommandLineTool or Workflow): CommandLineTool or Workflow

        Returns:
            cwl_utils.parser.cwl_v1_2.ResourceRequirement or ResourceRequirement
        """
        resource_requirement = []

        # look for requirements
        if elem.requirements is not None:
            resource_requirement = [
                requirement
                for requirement in elem.requirements
                if isinstance(
                    requirement,
                    (
                        cwl_utils.parser.cwl_v1_0.ResourceRequirement,
                        cwl_utils.parser.cwl_v1_1.ResourceRequirement,
                        cwl_utils.parser.cwl_v1_2.ResourceRequirement,
                    ),
                )
            ]

            if len(resource_requirement) == 1:
                return resource_requirement[0]

        # look for hints
        if elem.hints is not None:
            resource_requirement = [
                ResourceRequirement.from_dict(hint)
                for hint in elem.hints
                if hint["class"] == "ResourceRequirement"
            ]

            if len(resource_requirement) == 1:
                return resource_requirement[0]

    def eval_resource(self):
        resources = {
            "coresMin": [],
            "coresMax": [],
            "ramMin": [],
            "ramMax": [],
            "tmpdirMin": [],
            "tmpdirMax": [],
            "outdirMin": [],
            "outdirMax": [],
        }

        for elem in self.cwl:
            if isinstance(
                elem,
                (
                    cwl_utils.parser.cwl_v1_0.Workflow,
                    cwl_utils.parser.cwl_v1_1.Workflow,
                    cwl_utils.parser.cwl_v1_2.Workflow,
                ),
            ):
                if resource_requirement := self.get_resource_requirement(elem):
                    for resource_type in [
                        "coresMin",
                        "coresMax",
                        "ramMin",
                        "ramMax",
                        "tmpdirMin",
                        "tmpdirMax",
                        "outdirMin",
                        "outdirMax",
                    ]:
                        if getattr(resource_requirement, resource_type):
                            resources[resource_type].append(
                                getattr(resource_requirement, resource_type)
                            )
                for step in elem.steps:
                    if resource_requirement := self.get_resource_requirement(
                        self.get_object_by_id(step.run[1:])
                    ):
                        multiplier = (
                            int(os.getenv("SCATTER_MULTIPLIER", 2))
                            if step.scatter
                            else 1
                        )
                        for resource_type in [
                            "coresMin",
                            "coresMax",
                            "ramMin",
                            "ramMax",
                            "tmpdirMin",
                            "tmpdirMax",
                            "outdirMin",
                            "outdirMax",
                        ]:
                            if getattr(resource_requirement, resource_type):
                                resources[resource_type].append(
                                    getattr(resource_requirement, resource_type)
                                    * multiplier
                                )
        return resources


