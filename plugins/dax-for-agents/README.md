# dax-for-agents

**The canonical DAX language reference for AI agents**: every function with its signature,
semantics, and the gotchas the documentation doesn't tell you. 479 function cards, 34
conceptual pages, hand-written field notes, the daxlib.org catalogue, UDF authoring and the
window family. Not performance tuning.

This folder is the plugin, and only this folder ships. The lab, the evals, the docs and the
maintainer tooling live in the rest of
[the repository](https://github.com/CSalcedoDataBI/dax-for-agents), which is also where the
full README, the contributing guide and the issue tracker are.

## Skills

| Skill | Use it when |
|---|---|
| `dax-reference` | You need what a DAX function does, its signature, or which one to reach for |
| `dax-lib` | Before writing a UDF from scratch — someone may have shipped it already |
| `dax-lib-install` | `dax-lib` found one and you want it *in* the model, licensed and attributed |
| `dax-udf-authoring` | Writing your own `FUNCTION`: parameter types, `VAL` vs `EXPR`, GA limits |
| `dax-window-functions` | `WINDOW` / `OFFSET` / `INDEX` / `RANK` — rolling, running totals, ranking |

## Install

Needs Claude Code 2.1.142 or newer.

```bash
/plugin marketplace add CSalcedoDataBI/dax-for-agents
```

```bash
/plugin install dax-for-agents@dax-for-agents
```

## What this plugin runs, sends and fetches

Installed, the plugin is text: skills, reference pages and an offline index. It ships no
hooks, no MCP server, no telemetry and no background process, and nothing it contains runs
on its own.

| When | What happens | Where it goes |
|---|---|---|
| Any skill is used | Claude reads Markdown and JSON from the installed plugin folder | Nowhere: local reads only |
| `dax-lib-install` installs a package you picked | Claude runs `gh api` to read that package's `functions.tmdl`, with **your own** GitHub CLI login, checks its declared licence, installs it in the model you are working on (through a modeling MCP if one is connected, otherwise as a TMDL edit) and runs one DAX query to confirm it executes | `api.github.com`, repository `daxlib/daxlib`, read-only |
| You ask for an example `.pbip` that no lab page covers | Claude runs `skills/dax-reference/scripts/inject_example.py`: it downloads `lab-contoso.zip` from the repository's latest release, adds the measures Claude wrote and one page, and hands you a zip. The script refuses any other download address and any line break that could add a Power Query source to the model | `github.com` release assets of `CSalcedoDataBI/dax-for-agents`, read-only. The request carries nothing from you |

`skills/dax-lib/scripts/refresh-daxlib.ps1` and the maintainer scripts under
`skills/dax-reference/scripts/` are **not** run by the plugin; each runs only when someone
types its command.

No personal data is collected, stored or sent anywhere. Full policy: [PRIVACY.md](PRIVACY.md).

## Licensing

| What | Licence |
|---|---|
| Code, skills and hand-written content | [MIT](LICENSE) © 2026 CSalcedoDataBI |
| `skills/dax-reference/generated/` | **CC BY 4.0** © Microsoft. See [`skills/dax-reference/NOTICE`](skills/dax-reference/NOTICE) |
| `skills/dax-lib/` | An offline index of [daxlib.org](https://daxlib.org). No package code is redistributed; licences vary per author. See [`skills/dax-lib/NOTICE`](skills/dax-lib/NOTICE) |
