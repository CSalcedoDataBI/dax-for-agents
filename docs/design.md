# dax-for-agents — design

**Date:** 2026-08-06 (condensed from the original design spec)
**Status:** a dated record. Counts here are what was true when it was written.

## Why this exists

A market study (2026-08-06) found that the ecosystem of agent tooling for Power BI is well
covered on *tooling* and empty on the *language*:

| Project | License | Covers |
|---|---|---|
| `microsoft/skills-for-fabric` | MIT | Fabric. No DAX as a language |
| `data-goblin/power-bi-agentic-development` | GPL-3.0 | Many plugins; its `dax` skill is performance only |
| `MicrosoftDocs/Agent-Skills` | CC BY 4.0 | Azure skills. None for Power BI, DAX, M or Fabric |
| `MinaSaad1/pbi-cli` | MIT | A TOM + PBIR CLI. An execution layer |
| `daxlib/daxlib` | MIT | A UDF package registry, not a language reference |

Nobody had a DAX language reference an agent can consume. The human reference is owned and
strong (SQLBI: `dax.guide`, `daxpatterns.com`), so this repo does not compete there.

The raw material is reusable: `MicrosoftDocs/query-docs` (CC BY 4.0 docs, MIT code), 540 DAX
`.md` files — 479 function pages plus 34 conceptual pages once the category indexes and
include fragments are set aside (see
[the decision](decisions/2026-08-13-concept-count-34-not-61.md)).

**Identity:** the canonical DAX language reference for AI agents — 479 functions with
signature, semantics and the traps the documentation does not mention.

## Decisions

| Decision | Value | Reason |
|---|---|---|
| Repository and marketplace name | `dax-for-agents` | No collisions on GitHub; `dax-library` collided with the `daxlib` organization |
| Plugin name | `dax` | The plugin name prefixes every skill for good |
| Packaging | Flat skills first, plugin manifest at release | The wrapper is two small JSON files; reversible |
| Root license | MIT | A contribution, not a product |
| Derived content license | `NOTICE` with CC BY 4.0 inside `dax-reference/` | Mirrors Microsoft's own split between content and code licenses |
| Access architecture | Flat index plus cards read on demand | No scripts or permissions at query time |
| Scope | DAX only | Power Query M lives in its own repository |

## What is in and what is out

In: `dax-reference` (new, derived from `query-docs`, CC BY 4.0, attributed), `dax-lib`
(derived from `daxlib/daxlib`, MIT), `dax-udf-authoring` and `dax-window-functions`. They are
all *language*: how to write a UDF, how window functions work, which UDFs already exist.

Out:

- A performance-tuning skill: it was adapted from a GPL-3.0 plugin, which does not belong in an
  MIT repository, and that plugin already ships it. The README links to it instead.
- Skills tied to one client's context, and skills that are not DAX (star-schema design,
  date slicers, and similar). They would break the identity sentence.

## Agent query flow

For a question about a specific function the agent reads `catalog.md` once, finds the
function, then reads that function's card from `library/`. Conceptual questions go straight to
`concepts/`. Hand-written field notes under `notes/` are never overwritten by the sync.

The layout was later superseded: everything generated lives under
`dax-reference/generated/` — see
[the decision](decisions/2026-08-11-generated-tree-single-swap.md).
