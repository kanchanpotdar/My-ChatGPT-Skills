# My ChatGPT Skills

This repository contains the **My ChatGPT Skills** plugin (version **0.1.4**), a collection of seven reusable skills for ChatGPT and Codex. Each skill is a self-contained set of instructions that gives ChatGPT a repeatable way to handle a specific type of task.

## How to use these skills

Browse the skill folders and open the relevant `SKILL.md` file. Add the skill's instructions to the ChatGPT setup or workflow where you want to use it, then provide the task or request that the skill is designed to handle.

Skills are designed to be reusable. They can be refined over time as new use cases, commands, and quality requirements are added.

## Available skills

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

Each skill lives in its own folder under `skills/` and should include:

- `SKILL.md` — the instructions ChatGPT follows
- `README.md` — a brief description and usage guide

As new skills are added, this README will be updated with their purpose and links.

## Install as a local plugin

This repository includes a local marketplace catalog at `.agents/plugins/marketplace.json`. From the repository root, add it as a marketplace with:

```bash
codex plugin marketplace add .
```

Then open the Plugins Directory in the ChatGPT desktop app, select the `my-chatgpt-skills` marketplace, and install the plugin. Restart the app after adding or updating the plugin if it does not appear immediately.
