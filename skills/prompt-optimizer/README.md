# Prompt Optimizer v2.0

Prompt Optimizer v2.0 turns rough instructions into clear, efficient, reusable prompts by treating them as work specifications. It adapts the amount of structure to the task instead of making every prompt unnecessarily long.

## What it does

- Identifies the user's actual objective and required context
- Corrects unclear wording while preserving technical details
- Detects missing information and asks up to three focused questions
- Structures prompts with requirements, constraints, output format, and success criteria when useful
- Removes repetition and unnecessary wording without changing the intent
- Selects answer, transformation, creation, decision, action, or reusable-workflow structure
- Adds steelmanning, stakeholder review, premortems, and verification only when justified
- Defines tool boundaries, stop rules, escalation, and reporting for agentic workflows

## Usage

Use the instructions in [`SKILL.md`](./SKILL.md) as the skill definition for your AI assistant. Provide an informal request, and the assistant will either ask targeted clarification questions or return a copy-ready optimized prompt followed by a short explanation of what improved.

The skill supports these logical commands:

- `/optimize` — optimize using the standard workflow
- `/quick` — optimize immediately using reasonable assumptions
- `/detailed` — include explicit requirements, constraints, and output specifications
- `/compact` — produce the shortest effective prompt
- `/revise` — update the previously generated prompt
- `/run` — execute the latest finalized prompt when possible

## Default behavior

The default language is English, with a professional and direct tone. Accuracy takes priority over clarity, and clarity takes priority over brevity.
