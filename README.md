# My ChatGPT Skills

This repository contains the **My ChatGPT Skills** plugin (version **0.1.5**), a collection of eight reusable skills for ChatGPT and Codex. Each skill is a self-contained set of instructions that gives ChatGPT a repeatable way to handle a specific type of task.

## How to use these skills

Browse the skill folders and open the relevant `SKILL.md` file. Add the skill's instructions to the ChatGPT setup or workflow where you want to use it, then provide the task or request that the skill is designed to handle.

Skills are designed to be reusable. They can be refined over time as new use cases, commands, and quality requirements are added.

## How the collection works

The plugin packages instruction-based workflows under `skills/`. The portable [plugin manifest](./plugin.json) describes the package, the [Codex compatibility manifest](./.codex-plugin/plugin.json) points to the skills directory, and the [local marketplace catalog](./.agents/plugins/marketplace.json) exposes the repository as a local plugin source.

Each skill defines when it applies, how the assistant should work, and what it should deliver. Supporting references and helpers are loaded as needed. These are assistant workflows rather than a standalone application; document generation, research, and repository inspection depend on the tools and permissions available in the host.

## Available skills

### [GitHub README Architect](./skills/github-readme-architect/SKILL.md)

Generates, improves, updates, or audits GitHub READMEs by inspecting source code, tracing central workflows, and checking relevant available history. Covers architecture, setup, implementation status, experiments, results, and limitations only where evidence supports them. Historical conversations are optional.

| Mode | Behavior |
| --- | --- |
| Generate | Create a complete README when documentation is missing or inadequate. |
| Improve | Strengthen an existing README while preserving valuable material. |
| Update | Synchronize documentation with implementation using focused changes. |
| Audit | Return prioritized findings without modifying the target repository. |

Auto selects a mode from the request and repository state. In Codex, invoke `$github-readme-architect` when the skill is installed, or ask: “Update my README based on the latest implementation.” Slash invocation depends on host support.

The skill maintains an internal evidence ledger and distinguishes verified, inferred, planned, and unknown claims. Its optional Python checker inspects local Markdown paths, code fences, and possible credentials; it does not establish technical accuracy, execute project commands, or reproduce metrics. See its [verification guide](./skills/github-readme-architect/references/verification.md) for scope and limitations.

### [Repo Catch-Up](./skills/repo-catch-up/)

Reconstructs an existing project's purpose, architecture, progress, decisions, datasets, experiments, and open tasks before work resumes. Supports mixed repositories and folders without Git history, provides source evidence and coverage limits, and ends with a continuation brief. Inspects the target project read-only.

Example: “Use repo-catch-up on `/path/to/project` before we continue.” It returns an orientation with source references and a continuation brief; specify an authorized output path if you want the brief saved.

### [Prompt Optimizer](./skills/prompt-optimizer/)

Transforms rough, unstructured instructions into clear, precise, and reusable prompts for AI assistants. It identifies the user's objective, preserves important technical details, asks focused clarification questions when needed, and returns a copy-ready optimized prompt.

Supported logical commands include:

- `/optimize` — use the standard optimization workflow
- `/quick` — optimize immediately using reasonable assumptions
- `/detailed` — include explicit requirements, constraints, and output specifications
- `/compact` — produce the shortest effective prompt
- `/revise` — update the previously generated prompt
- `/run` — execute the latest finalized prompt when possible

### [ELI5](./skills/eli5/)

Creates simple visual HTML explainers for beginners, with large visuals and minimal text. Invoke it with `/eli5 <topic>`.

### [Grilling](./skills/grilling/)

Stress-tests plans and ideas through rounds of decision-tree questions. It activates only when the user explicitly says “grill.”

### [Idea Refine](./skills/idea-refine/)

Sharpens an existing idea into an actionable direction and ends with a one-page brief covering assumptions, MVP scope, and a “Not Doing” list.

### [Professional Report Generator](./skills/professional-report-generator/)

Researches a topic and creates a publication-ready Word report with structured findings, tables, citations, bibliography, and consistent formatting.

### [Teach Me](./skills/teach-me/)

An interactive learning and active-recall tutor for academic subjects, lecture notes, textbooks, PDFs, slides, technical concepts, and research papers. It teaches in manageable phases, evaluates recall, reinforces weak areas, and builds toward university-style examinations.

## Repository structure

```text
.
├── plugin.json                         Portable package metadata
├── .codex-plugin/plugin.json           Codex compatibility and skills path
├── .agents/plugins/marketplace.json    Local marketplace catalog
└── skills/
    ├── github-readme-architect/         README creation and auditing
    ├── repo-catch-up/                  Read-only project orientation
    ├── prompt-optimizer/               Prompt refinement
    ├── eli5/                          Visual HTML explanations
    ├── grilling/                      Explicit “grill” interviews
    ├── idea-refine/                    Idea refinement
    ├── professional-report-generator/ Research and Word reports
    └── teach-me/                      Interactive tutoring
```

Every skill has a `SKILL.md` entry point. Most also include a usage README; some have references, scripts, or optional `agents/openai.yaml` UI metadata. For example, README Architect separates its workflow, README design guidance, verification guidance, and read-only checker.

## Install as a local plugin

This repository includes a local marketplace catalog at `.agents/plugins/marketplace.json`. From the repository root, add it as a marketplace with:

```bash
codex plugin marketplace add .
```

Install from the added marketplace using the plugin interface available in your Codex host. Interface labels and refresh behavior can vary. Adding a marketplace registers a source; it does not by itself demonstrate that the plugin was installed or that every workflow works in that host.

## Local documentation checks

README Architect's helper requires Python 3.9+ and no third-party Python packages. From the repository root:

```bash
python3 skills/github-readme-architect/scripts/check_readme.py . --inventory
```

Inventory uses Git when run at a Git repository root, or `rg` for ignore-aware discovery otherwise. The helper makes no network requests and does not write files. Exit codes are `0` for no heuristic findings, `1` for review findings, and `2` for an input/read error. Manually review complex Markdown, anchors, external links, architecture claims, and sensitive information.

## Status and limitations

The repository contains eight skill definitions and their supporting resources. Skill availability does not establish output quality across all projects or hosts. Repository-wide benchmark results and an automated CI test suite are not included. README Architect has received a local synthetic-repository trial and focused checker tests; these are limited validation, not a cross-project benchmark.

Report generation requires the research and document tooling described in its skill. Other workflows likewise depend on accessible inputs and host capabilities. Logical slash commands in skill instructions are not guaranteed native commands in every client.

## Attribution and licensing

The package manifests identify Kanchan Potdar as the author and declare MIT. No repository-level license file is currently included. The ELI5 skill retains its own MIT declaration and upstream attribution to Thariq Shihipar; see its [metadata](./skills/eli5/SKILL.md). Preserve existing attribution when adapting skills.
