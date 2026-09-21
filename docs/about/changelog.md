# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/); this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `hatch` environment configuration and test scripts (`pytest`, `pytest-cov`)
- `ruff` for linting and formatting
- This documentation site

### Changed
- Reformatted the codebase with `ruff`

## [v0.2.0] - 2026-01-23
### Added
- Published on PyPI: `pip install zoo-argowf-runner`
- `zoo-runner-common` and `zoo-template-common` as dependencies

### Changed
- Extracted shared logic into `zoo-runner-common`, removing `zoo_helpers.py` entirely
- `ZooArgoWorkflowsRunner` now inherits from `BaseRunner`; runner focuses solely on Argo-specific logic

## [v0.1.0] - 2023-01-01
### Added
- Initial release — Argo Workflows-based ZOO runner for Calrissian CWL jobs

---

See [GitHub Releases](https://github.com/ZOO-Project/zoo-argowf-runner/releases) for full version history.

[Unreleased]: https://github.com/ZOO-Project/zoo-argowf-runner/compare/v0.2.0...HEAD
[v0.2.0]: https://github.com/ZOO-Project/zoo-argowf-runner/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/ZOO-Project/zoo-argowf-runner/releases/tag/v0.1.0