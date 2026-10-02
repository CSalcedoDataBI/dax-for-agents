# Privacy policy — dax-for-agents

*Effective 2026-10-02. Maintainer: Cristóbal Salcedo — contacto@csalcedodatabi.com*

This policy covers the **dax-for-agents** plugin for Claude. The website
[csalcedodatabi.com](https://csalcedodatabi.com) has [its own policy](https://csalcedodatabi.com/privacidad).

## What the plugin collects

**Nothing.** The plugin is text: five skills, reference pages and an offline index. It ships
no hooks, no MCP server, no telemetry, no analytics and no background process. It has no
server of its own, so nothing you do with it reaches the maintainer.

## What it reads and sends

| When | What happens | Where it goes |
|---|---|---|
| Any skill is used | Claude reads Markdown and JSON from the installed plugin folder | Nowhere: local reads only |
| `dax-lib-install` installs a package you picked | Claude runs `gh api` with **your own** GitHub CLI login to download that package's `functions.tmdl`, then installs it in the model you are working on, after asking you | `api.github.com`, repository `daxlib/daxlib`, read-only. The request names the package; it carries no data from your model |
| You open a project under `lab/` | Power BI Desktop downloads the scenario's synthetic Parquet tables | `raw.githubusercontent.com`, repository `CSalcedoDataBI/SampleDataSets` |

Your semantic models, queries and conversations stay between you, Claude and the tools you
already use. The plugin keeps no copy of them and retains no data.

Maintainer scripts in this repository (for example the evaluation runner under `evals/`)
are **not** run by the plugin; they run only when a maintainer starts them by hand.

## Children

The plugin is a developer tool and is not directed at anyone under 18.

## Changes and contact

Changes to this policy are made in this file and recorded in the repository history.
Questions: contacto@csalcedodatabi.com.
