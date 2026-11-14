# dax-for-agents

The DAX language for AI agents: 479 built-in function cards and 34 conceptual pages derived
from Microsoft's documentation, with where each function is legal, whether it is
discouraged, and which of similar functions to pick; hand-written field notes measured against
a real model; the daxlib.org catalogue of ready-made UDFs; UDF authoring; and the window
family. An agent reads one index row and one card instead of guessing a signature.

Not performance tuning.

## Skills

| Skill | Use it when |
|---|---|
| `dax-reference` | You need what a DAX function does, its signature, or which one to reach for |
| `dax-lib` | Before writing a UDF from scratch — someone may have shipped it already |
| `dax-lib-install` | `dax-lib` found one and you want it *in* the model, licensed and attributed |
| `dax-udf-authoring` | Writing your own `FUNCTION`: parameter types, `VAL` vs `EXPR`, GA limits |
| `dax-window-functions` | `WINDOW` / `OFFSET` / `INDEX` / `RANK` — rolling, running totals, ranking |
| `dax-feedback` | A card, note or example here proved wrong — files one sanitized issue, after you approve it |

## Install

```bash
/plugin marketplace add CSalcedoDataBI/dax-for-agents
/plugin install dax-for-agents@dax-for-agents
```

Needs Claude Code 2.1.142 or later.

## What this plugin runs, sends and fetches

Installed, the plugin is text: six skills, their Markdown reference pages and JSON indexes.
It ships no scripts, no hooks, no agents, no MCP server, no telemetry and no background
process, and nothing it contains runs on its own.

| When | What happens | Where it goes |
|---|---|---|
| Any skill is used | Claude reads Markdown and JSON from the installed plugin folder | Nowhere: local reads only |
| `dax-lib-install` installs a package you picked | Claude runs `gh api` with **your own** GitHub CLI login to read that package's `functions.tmdl`, checks its declared licence, installs it in the model you are working on and runs one DAX query to confirm it executes | `api.github.com`, repository `daxlib/daxlib`, read-only |
| You ask `dax-feedback` to report a wrong card or note **and approve the drafted text** | Claude runs your own `gh issue create` with that text; without `gh` it hands you the text | A **public** issue on [CSalcedoDataBI/dax-for-agents](https://github.com/CSalcedoDataBI/dax-for-agents/issues), under your GitHub account |

The maintainer tools — the sync from Microsoft's docs, the daxlib index refresh, the script
that injects an example page into the Contoso lab, the lab itself and the evals — live in
[the repository](https://github.com/CSalcedoDataBI/dax-for-agents), outside this folder; they
are not installed with the plugin.

Privacy policy: [PRIVACY.md](https://github.com/CSalcedoDataBI/dax-for-agents/blob/main/PRIVACY.md).
License: [MIT](LICENSE.md). The function cards are derived from `MicrosoftDocs/query-docs`,
CC BY 4.0: [skills/dax-reference/NOTICE.md](skills/dax-reference/NOTICE.md).
