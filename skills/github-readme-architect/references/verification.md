# Verification and helper use

Run the helper with Python 3.9+ (standard library only):

```bash
python3 /absolute/path/to/github-readme-architect/scripts/check_readme.py /path/to/repository --inventory
python3 /absolute/path/to/github-readme-architect/scripts/check_readme.py /path/to/repository --readme docs/README.md
```

It reads without writing, running project code, or making network requests. Exit 0 means no heuristic findings, 1 means review findings, and 2 means an input/read error. Inventory honors Git exclusions (tracked files remain visible) or uses ignore-aware `rg` outside a Git root. It skips common generated and sensitive paths and out-of-root symlink targets. Output is bounded with `--limit`; count is inventory metadata, not proof of content review. It never reads inventoried source files. Git and `rg` are optional for checking a README, but one is needed for inventory. No README yet? Inventory manually first; run the checker after drafting.

The checker detects missing ordinary inline/reference local paths, repository escapes, unclosed fences, and several possible credential patterns. Credential findings print only type/location. Its parser is intentionally heuristic: manually inspect HTML, complex/shortcut references, anchors, Markdown rendering, and relative links in other documents. External links are counted, never fetched. It cannot prove privacy, technical accuracy, working commands, or correct diagrams. Do not blindly copy inventory paths into a public README; filenames themselves may be private.

## Required human/model review

- **Paths and Markdown:** resolve links from the README's directory, including case, spaces and fragment targets. Check heading anchors/duplicates and image alt text. Confirm linked public artifacts exist and are suitable for release. Review tables and fenced blocks in a renderer when available.
- **Interfaces and commands:** inspect actual package scripts, CLI arguments, module names, config parsing, working directories and prerequisites. Distinguish commands executed successfully now, historically reported successful, statically supported but untested, and unavailable. Do not invent versions from installed local packages. Inspect test hooks before running; skip checks requiring installs, secrets, paid services, destructive writes, or expensive workloads unless authorized.
- **Claims and architecture:** map each important feature and Mermaid edge to owning implementation. Mark partial/stub/optional components accurately. Render Mermaid if a safe existing renderer is available; otherwise report syntax review only. No dependency installation merely for presentation checks.
- **Metrics:** compare table numbers directly with result artifacts and configuration. Verify split, denominator, units, scope, model/checkpoint revision, baseline comparability and selection criteria. If missing, qualify or omit. Explain private evidence without exposing private records. A result file is evidence of reported results, not successful reproduction.
- **History:** retain chronological ordering and original phase names when supported. Keep historical results separate from current behavior. Do not turn planned milestones into completed work or invent reasons for changes.
- **Privacy:** inspect README additions and diff for secrets and sensitive provenance. Review environment examples, URL credentials/query strings, notebook outputs, local home paths, personal identifiers and data samples. Use placeholders or public aggregate summaries. Never report discovered secret values.
- **Scope:** Audit leaves the repository untouched. Other modes change the README only. Preserve unrelated local edits and attribution. Check diff and final status; do not commit, publish, license, or fix code as part of documentation work.

## Validation report format

Briefly state root/revision if available, inspection coverage, mode, changed file (or no changes for Audit), static checks, actual execution checks, metric sources and remaining limits. Report failed checks and recommended corrections directly. A tool's successful exit is never a substitute for the evidence ledger.

Audit findings should include priority (high: misleading results/security or unusable primary setup; medium: incorrect features/architecture or significant omissions; low: navigation/presentation), README location, owning source, impact, and actionable correction. Distinguish unsupported from demonstrably false.
