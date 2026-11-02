# Project-specific README design

Choose sections for the repository's real audience and workflows. Keep concise prose, consistent heading depth, and a useful top-to-bottom reading path. Use tables for comparisons, Mermaid for connections, and collapsible blocks for optional detail. Avoid decorative badge walls, empty headings, repeated results, and generic filler.

## Section menu

| Section | Include when supported |
| --- | --- |
| Header and overview | Clear title, concrete tagline, purpose, current maturity and scope. Only verified technology, license, release, or CI badges; CI badges must refer to an existing workflow and branch. Add a TOC for a long document. |
| Problem and motivation | Documented problem, objectives, intended users, and constraints. Do not invent deficiencies in prior work or claim novelty without sources. |
| Features and status | Actual capabilities and important design choices. Separate implemented, partial, experimental, and planned work. A file or stub is not a completed capability. |
| Quick start | Shortest useful supported path with prerequisites and required data/services. Link to fuller setup below if needed. |
| Architecture | Component responsibilities and execution/data flow. Diagram only actual nodes and edges; mark any optional or planned components distinctly. Explain important configuration, storage, integrations, and failure behavior. |
| Repository structure | Curated tree of significant existing files/directories with responsibilities. Omit dependency/generated trees; label illustrative omitted descendants. Respect case and repository-relative paths. |
| Tech stack | Group verified languages/frameworks, algorithms/models, storage, APIs/orchestration, evaluation/testing, and deployment. Distinguish runtime, development, optional, and experimental dependencies. Imports show use, not necessarily installation or version. |
| Data and processing | Sources/formats, acquisition constraints, transformations, labels/features, validation, frozen splits, provenance, output artifacts, availability and licensing restrictions. Use aggregates and safe examples. |
| Implementation | Important algorithms, stages, module interactions, schemas and design tradeoffs. Recorded rationale versus inferred intent. Include equations/pseudocode only where explanatory. |
| Development phases | Verified chronological milestones, objective, deliverables, findings and status. Preserve established phase numbering and order. With no chronology use Implementation Components. Do not infer dates from modification times. |
| Experiments and evaluation | Baselines, configs, dataset/split/coverage, methods, metrics, comparisons, selection criteria, failed runs and lessons only when recorded. Point to existing public reports. Present incomparable runs separately and avoid unsupported “best” claims. |
| Installation/configuration | Supported runtime and version constraints, package manager, environment, dependencies and services. Derive commands from actual manifests and interfaces. Use placeholder environment values; explain required versus optional variables. |
| Usage/reproduction | Actual CLI/API inputs and outputs, application startup, inference/training/evaluation where relevant, tests, and reproduction commands. State working directory, prerequisites, required artifacts, and untested status. Label costly/long-running operations. |
| Results and outputs | What is produced, where it goes, how to inspect it, known capabilities and limits. Distinguish committed artifacts from outputs created by a run. Do not link nonexistent future artifacts as existing files. |
| Limitations/issues | Concrete unresolved technical gaps, data/environment dependencies, coverage and reproducibility constraints with evidence. Avoid speculative vulnerability claims. |
| Roadmap | Completed, in progress, planned with evidence; checkboxes are optional. Suggested future work must be distinguishable from the project's recorded commitments. |
| Contributors/references/license | Existing attribution and verified citations; preserve credits. Verify license file and scope; never assign a license because a manifest or template suggests one. If absent, state no license file was found when relevant. |

## Domain lenses

- **Research/ML:** distinguish paper intent from code; raw versus derived data; split leakage controls; validation versus reserved test; normalization and metric denominators; artifact/model revision and run configuration. Show what can be reproduced without private data or proprietary access.
- **Backend/agents:** document route/tool contracts, orchestration, persistence, external dependencies, configuration, retries and error handling. Do not equate retrieval scores or successful tool calls with answer correctness.
- **Libraries/CLI:** prioritize installation, public interfaces, a small realistic example, supported platforms, configuration and tests.
- **Monorepos:** explain package relationships, shared tooling, per-package prerequisites, working directories, and existing package README links.
- **Early prototypes:** lead with supported scope and unfinished work. Do not portray a scaffold as a production deployment.

## Presentation safeguards

Use fenced commands with the right language and actual entry points. Provide placeholders such as `YOUR_API_KEY`; never realistic-looking credentials. A copy-ready example can still be untested: say so adjacent to the commands. Link existing files relatively, with public durable sources for external references. GitHub README anchors should follow rendered headings; check duplicate headings and punctuation. Mermaid should remain readable without relying on color alone. No images or badges are required for polish.
