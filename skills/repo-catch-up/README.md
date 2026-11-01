# Repo Catch-Up

Brings an assistant up to speed on an existing repository or project folder before work resumes. Supports mixed source code, datasets, notebooks, PDFs, experiments, and saved outputs, with or without Git history.

## Usage

Ask: “Use repo-catch-up on `/path/to/project` before we continue.”

For a reusable handoff, specify an authorized destination: “Return the orientation and save the continuation brief to `/path/to/brief.md`.” Without a destination, the brief stays in chat.

The skill traces architecture and data flows, reconstructs progress and decisions from evidence, and separates recorded tasks from suggested next steps. It reports precise source pointers and inspection gaps. Large collections are inventoried broadly and inspected selectively, with samples and exclusions disclosed.

The target project stays read-only: no dependency installation, project execution, tests, training, fixes, or data edits. Existing results are distinguished from checks performed during inspection. Available access and extraction tools determine what can be read; missing or unreadable material is reported.

The continuation brief helps a later session resume after revalidating current sources. It does not provide automatic permanent memory.
