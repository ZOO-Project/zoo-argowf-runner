# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added GitHub Issue and Pull Request templates to standardise contributions
- Added a placeholder test to satisfy CI until full unit tests are available
- Added `hatch` environment configuration and test scripts (`pytest`, `pytest-cov`)
- Added `ruff` for linting and code formatting
- Added a `LICENSE` file

### Changed
- Reformatted the codebase with `ruff` for consistent style
- Updated the build configuration
- Updated `README.md` to remove version-specific details

### Fixed
- Applied `ruff` auto-fixes across the codebase

## [v0.2.0] - 2026-01-23
### Added
- Package is now officially available on PyPI: `pip install zoo-argowf-runner`
- Added `zoo-runner-common` as an official dependency for shared runner functionality
- Added `zoo-template-common` as a dependency for reusable template utilities

### Changed
- Major architectural improvement: modularized the codebase by extracting shared logic into `zoo-runner-common`, eliminating duplicated code including full removal of `zoo_helpers.py`
- `ArgoWFRunner` now inherits from `BaseRunner` (from `zoo-runner-common`) for common methods
- Adopted shared `ZooConf`, `ZooInputs`, `ZooOutputs`, and `CWLWorkflow` classes from `zoo-runner-common`
- Implements the `ExecutionHandler` interface from `zoo-runner-common`; runner now focuses solely on Argo Workflows-specific logic
- Updated to support `zoo-runner-common` v0.1.2 and its new import paths
- Reuse of `ZooStub` aligned with updated `zoo-runner-common` integration
- Updated tests to align with `zoo-runner-common` v0.1.2

## [v0.1.0] - 2023-01-01
### Added
- Initial release of `zoo-argowf-runner`
- Zoo runner plugin enabling the ZOO-Project to submit jobs as Argo Workflows
- Support for running Calrissian CWL jobs via an Argo Workflows `WorkflowTemplate` or `ClusterWorkflowTemplate`
- Configurable environment variables: `STORAGE_CLASS`, `DEFAULT_VOLUME_SIZE`, `DEFAULT_MAX_CORES`, `DEFAULT_MAX_RAM`, `ARGO_WF_ENDPOINT`, `ARGO_WF_TOKEN`, `ARGO_WF_SYNCHRONIZATION_CM`, `ARGO_CWL_RUNNER_TEMPLATE`, `ARGO_CWL_RUNNER_ENTRYPOINT`
- Support for retrieving job outputs and artifacts (results, log, usage-report, stac-catalog, feature-collection, tool-logs) from Argo Workflows steps

[Unreleased]: https://github.com/ZOO-Project/zoo-argowf-runner/compare/v0.2.0...HEAD
[v0.2.0]: https://github.com/ZOO-Project/zoo-argowf-runner/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/ZOO-Project/zoo-argowf-runner/releases/tag/v0.1.0