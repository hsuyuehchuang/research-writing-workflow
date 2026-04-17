# Skill Boundaries

This document defines which skills should live in the shared toolkit repository and which should remain inside project-specific repositories.

## Shared Skills

These belong in `research-writing-workflow` because they are reusable across multiple repositories:

- `mdwrite`
- Markdown math formatting rules
- research-note writing rules
- algorithm note templates
- appendix expansion rules
- Markdown to LaTeX publishing helpers

These are toolkit-level capabilities rather than project-owned knowledge.

## Repo-Local Skills

These should stay in the local repository when they depend on project-specific workflows, company context, or file structure.

Examples:

- `interview-company-prep`
- company-specific interview breakdown skills
- project-specific derivation conventions that only make sense in one repository
- repo-specific navigation or folder assumptions

## Current Recommendation

### Keep in `research-writing-workflow`

- the new `mdwrite`
- general research-note composition rules
- math-safe Markdown rules
- algorithm and decision-note templates

### Keep in `interview/.codex/skills`

- `interview-company-prep`

### Candidate for migration later

The old SAR-local derivation skill:

- `sar_research_note/.codex/skills/github-readme-math-physics-derivation/SKILL.md`

This skill contains valuable reusable rules, especially:

- GitHub-safe math writing
- derivation section rhythm
- table-of-contents expectations
- physically interpretable derivation writing

It should likely be merged into the shared toolkit in a later cleanup pass, but it does not need to be force-moved immediately.

## Practical Rule

If a skill answers the question:

> "Could I use this in both `sar_research_note` and `interview` or in a future repo?"

then it should probably live in `research-writing-workflow`.

If it answers the question:

> "Does this only make sense inside one repo or one company-specific workflow?"

then it should stay local.
