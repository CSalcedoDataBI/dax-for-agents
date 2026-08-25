# dax-lib-install Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fifth skill, `dax-lib-install`, that fetches a third-party DAX UDF `dax-lib` already found in the daxlib.org index, checks its license, installs it against a real model, proves it runs, and leaves it attributed — replacing `dax-lib`'s current "point at the install route, do a human copies it" step 4.

**Architecture:** One new skill folder (`dax-lib-install/SKILL.md`), a small hand-off edit to `dax-lib/SKILL.md`, registration in `.claude-plugin/plugin.json` and `INDEX.md` (the two places that make a skill folder actually load and actually discoverable — both are gate-enforced, not optional), and reconciling every doc that currently states "4 skills" now that there are 5.

**Tech Stack:** Markdown (skill prose), JSON (`plugin.json`), TMDL (the attribution format the installed function carries), `gh api` (fetching real package code from `daxlib/daxlib`), the `powerbi-modeling-mcp` `function_operations` tool (live install), Python (the repo's existing gate scripts — no new code is written for this task).

## Global Constraints

- Every new/edited skill frontmatter needs `name` == folder name, kebab-case, and `description` starting with `"Use when"` — enforced by `scripts/validate_skills.py`.
- Every skill folder must be listed in `.claude-plugin/plugin.json`'s `skills` array as `"./<folder>"` — enforced by `scripts/check_plugin_manifest.py`. A folder present on disk but missing from this list ships invisible with no error from Claude Code itself.
- Every skill folder's name must appear as plain text somewhere in `INDEX.md` — enforced by `scripts/validate_skills.py`.
- Any prose sentence with a number immediately next to `skills?\b` (or its Spanish word forms, e.g. `cuatro`/`cinco`) is checked against the real skill count by `scripts/check_doc_claims.py`. A **historical** sentence describing a past, dated observation must be reworded to avoid the adjacency pattern rather than have its number changed — changing it would misstate what was actually true then.
- Attribution for an installed third-party function lives on the function itself (TMDL `///` doc comment + `annotation` key/values), never in a separate notices file — per the approved spec.
- All the gates (`check_no_credentials`, `check_doc_claims`, `check_examples`, `check_plugin_manifest`, `check_workflow_cost`, `validate_skills`) and the full `pytest`/`unittest` suite must be green before this is done.

---

### Task 1: Write the `dax-lib-install` skill and make it discoverable

**Files:**
- Create: `dax-lib-install/SKILL.md`
- Modify: `INDEX.md`

**Interfaces:**
- Produces: a skill folder named `dax-lib-install` whose frontmatter `name` is `dax-lib-install`, referenced by that exact string somewhere in `INDEX.md`. Later tasks (2, 3) depend on this folder existing and this name being final.

- [ ] **Step 1: Create the skill file**

Create `dax-lib-install/SKILL.md` with exactly this content:

````markdown
---
name: dax-lib-install
description: Use when a DAX UDF already published on daxlib.org (found via the dax-lib index) needs to be actually installed against a real model — not just documented. Fetches the real function body from the daxlib/daxlib registry, checks its declared license, installs it (modeling MCP if connected, else a direct TMDL edit), runs a real DAX query to confirm it executes, and leaves it attributed on the function itself (author, license, source URL) so it is never mistaken for original work. Triggers on "install this UDF", "bring in the daxlib function", "add TimeSeries.MovingAverage to my model", "vendor this DAX package".
---

# DAX Lib Install — bring a published UDF into a real model, attributed

**`dax-lib` finds it. This skill installs it.** `dax-lib` is deliberately an index —
it never carries third-party DAX code (see its own `NOTICE`). The moment a real
answer is "yes, use this one," the work moves here.

This is not `dax-udf-authoring`: that skill is for writing *your own* function from
scratch. This one is for installing *someone else's*, already-published one — which
means it also owns the paperwork a copy-paste would skip: checking the license,
proving the function runs on this exact model, and leaving a record of where it
came from that survives the function being copied on its own later.

## Workflow

1. **Resolve.** You need three things from `dax-lib`'s index: `packageId`, `version`,
   and the **exact function name** — not the whole package. Install only what is
   needed now; a package can ship several functions (`TimeSeries.MovingAverage`
   ships 7 — `Simple`, `Weighted`, `LinearWeighted`, `Exponential`,
   `DoubleExponential`, `Triangular`, `Geometric`) and the rest stay undeployed.

2. **Fetch the real code.**
   ```
   gh api repos/daxlib/daxlib/contents/packages/<first-letter>/<packageId-lowercase>/<version>/lib/functions.tmdl
   ```
   Same path convention `dax-lib/scripts/refresh-daxlib.ps1` already reads for the
   index — used here to read a function *body*, not just its name. Pull only the
   `function '<name>' = ...` block requested out of the file; the package's other
   functions are not your concern.

3. **Check the license.** Look for a declared license in `manifest.daxlib` and for a
   `LICENSE` file next to it in the package's version directory. If one exists,
   record it verbatim. If none exists — the common case, per `dax-lib`'s own
   `NOTICE`: *"individual packages declare no license of their own"* — install
   anyway, but the attribution carries `UNLICENSED - VERIFY BEFORE SHIPPING` in
   capitals, and your final report to the user repeats that warning unhedged. Do
   not soften it into a footnote.

4. **Install.** Prefer a live connection through the modeling MCP
   (`function_operations` → `Create`) when one is available. Fall back to a direct
   TMDL file edit — a `createOrReplace function` block, per `dax-udf-authoring`'s
   documented syntax — only when nothing live is reachable. Same order of
   preference `dax-udf-authoring` and the report-planning skill already use for
   model changes: live tooling first, hand-written TMDL last.

5. **Test.** Run one real DAX query against the connected model that calls the
   newly installed function and confirms it executes without error. No invented
   expected value — the test is "does this run, in this model, on this
   compatibility level, against these real column names." A copy-pasted
   third-party function is exposed to exactly the same failure modes an
   originally-authored one is (a model below the compatibility level DAX UDFs
   require fails the same way regardless of who wrote the function).

6. **Report.** One message: what was installed (function, package, version,
   author), the exact source URL (not just the package id), the license that
   applies (or the unlicensed warning), and the result of the test query. No
   silent success.

## Attribution

The `functions.tmdl` pulled from `daxlib/daxlib` already carries two annotations
the registry itself stamps:

```tmdl
annotation DAXLIB_PackageId = TimeSeries.MovingAverage
annotation DAXLIB_PackageVersion = 0.1.1
```

Keep these as-is — they are the registry's own record. Add the three facts the raw
file does not carry: who wrote it, what license applies, and exactly where it came
from. Attribution lives **on the function itself**, not in a separate manifest, so
it survives if the function is later exported or copied on its own:

```tmdl
/// Installed from daxlib.org — package TimeSeries.MovingAverage v0.1.1, author Tate Bowman.
/// License: UNLICENSED - VERIFY BEFORE SHIPPING.
/// Source: https://github.com/daxlib/daxlib/tree/main/packages/t/timeseries.movingaverage
function 'TimeSeries.MovingAverage.Simple' =
        ( ... )
    annotation DAXLIB_PackageId = TimeSeries.MovingAverage
    annotation DAXLIB_PackageVersion = 0.1.1
    annotation DAXLIB_Author = Tate Bowman
    annotation DAXLIB_License = UNLICENSED - VERIFY BEFORE SHIPPING
    annotation DAXLIB_SourceUrl = https://github.com/daxlib/daxlib/tree/main/packages/t/timeseries.movingaverage
```

If the package's original doc comment exists (the `///` line already in its
`functions.tmdl`, e.g. *"Returns a simple moving average..."*), keep it as a second
paragraph below the attribution block. The attribution is prepended, never
overwrites the description of what the function does.

## What this does not do

- Does not resolve dependencies between packages, manage upgrades, or maintain a
  lockfile. One named function, one named version, on request.
- Does not decide FOR the user whether an unlicensed package is safe to ship. It
  installs it, proves it runs, and says so loudly — the shipping decision is
  the user's.
- Does not touch `dax-lib`'s own index or `NOTICE`. The index stays code-free.

## Errors

| Failure | What to do |
|---|---|
| `gh api` can't reach the package path (renamed, deleted, wrong version) | Stop, report the exact path tried, do not guess at a substitute |
| Requested function name isn't in the fetched `functions.tmdl` | Stop, list the functions that *are* in that file |
| No live model connection and no local TMDL folder to edit | Stop — this installs into a real target, it does not stage code with nowhere to land |
| Model's compatibility level is below what user-defined functions require | Report the exact required level; do not silently skip the install |
| Test query errors after install | Report the raw engine error; do not roll back automatically, but never claim success |
````

- [ ] **Step 2: Update INDEX.md — opening line**

In `INDEX.md`, change:
```markdown
Cuatro skills, una sola idea: **el lenguaje DAX**. Nada de modelado, visuales ni operaciones —
```
to:
```markdown
Cinco skills, una sola idea: **el lenguaje DAX**. Nada de modelado, visuales ni operaciones —
```

- [ ] **Step 3: Update INDEX.md — routing diagram**

Change:
```markdown
Pregunta sobre DAX
  ├─ ¿qué hace esta función? ¿cuál uso?  → dax-reference
  ├─ ¿ya existe un UDF para esto?        → dax-lib
  ├─ voy a escribir un UDF               → dax-udf-authoring
  └─ rolling / running total / ranking   → dax-window-functions

¿Rendimiento? → no está aquí. Usa el plugin de data-goblin (ver README).
```
to:
```markdown
Pregunta sobre DAX
  ├─ ¿qué hace esta función? ¿cuál uso?  → dax-reference
  ├─ ¿ya existe un UDF para esto?        → dax-lib
  ├─ ese UDF ya existe: instálalo        → dax-lib-install
  ├─ voy a escribir un UDF               → dax-udf-authoring
  └─ rolling / running total / ranking   → dax-window-functions

¿Rendimiento? → no está aquí. Usa el plugin de data-goblin (ver README).
```

- [ ] **Step 4: Update INDEX.md — catálogo table**

After the `dax-lib` row, add a new row:
```markdown
| **`dax-lib-install`** | Trae de verdad el código de un UDF que `dax-lib` ya encontró: lo instala contra el modelo, lo prueba con una consulta real, y lo deja atribuido (autor, licencia, URL) en el propio `FUNCTION`. | ✅ |
```
So the table reads, in order: `dax-reference`, `dax-lib`, `dax-lib-install`, `dax-udf-authoring`, `dax-window-functions`.

- [ ] **Step 5: Update INDEX.md — convención 6**

Change:
```markdown
6. **Las cuatro skills van listadas por ruta en `.claude-plugin/plugin.json`.** Al estar
```
to:
```markdown
6. **Las cinco skills van listadas por ruta en `.claude-plugin/plugin.json`.** Al estar
```

- [ ] **Step 6: Run the structural validator — expect it to still fail (plugin.json not updated yet)**

Run: `python scripts/validate_skills.py`
Expected: passes the frontmatter and INDEX.md checks for `dax-lib-install` specifically (no error mentioning that folder). It is fine if this is the only check run here — `check_plugin_manifest.py` (Task 2) is a separate script and is expected to still fail until Task 2 lands.

- [ ] **Step 7: Commit**

```bash
git add dax-lib-install/SKILL.md INDEX.md
git commit -m "feat(dax-lib-install): add the skill and index it"
```

---

### Task 2: Register the skill in the plugin manifest

**Files:**
- Modify: `.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: the folder `dax-lib-install/` created in Task 1 (checked by path, not by any function signature).
- Produces: a plugin manifest where `dax-lib-install` loads as part of the `dax` plugin. Later tasks do not depend on any new interface here — this is a pure registration step.

- [ ] **Step 1: Add the skill to the manifest**

In `.claude-plugin/plugin.json`, change:
```json
  "skills": [
    "./dax-reference",
    "./dax-lib",
    "./dax-udf-authoring",
    "./dax-window-functions"
  ]
```
to:
```json
  "skills": [
    "./dax-reference",
    "./dax-lib",
    "./dax-lib-install",
    "./dax-udf-authoring",
    "./dax-window-functions"
  ]
```

- [ ] **Step 2: Run the plugin manifest gate**

Run: `python scripts/check_plugin_manifest.py`
Expected: `OK: plugin manifest lists 5 skill(s), all present (needs Claude Code >= 2.1.142).`

- [ ] **Step 3: Run the structural validator again — expect full pass now**

Run: `python scripts/validate_skills.py`
Expected: exits 0, no error mentioning `dax-lib-install`.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat(dax-lib-install): register in plugin.json"
```

---

### Task 3: Hand off from dax-lib's own workflow

**Files:**
- Modify: `dax-lib/SKILL.md`

**Interfaces:**
- Consumes: `dax-lib-install` as a skill name to reference by name (no code interface — this is a prose cross-link, matching INDEX.md convention 4: "Cross-links by name, not by path").

- [ ] **Step 1: Update the "Pairs with" line**

In `dax-lib/SKILL.md`, change:
```markdown
Pairs with **`dax-udf-authoring`** (how to write your own when none fits) and
**`dax-reference`** (what the built-in functions do).
```
to:
```markdown
Pairs with **`dax-lib-install`** (actually install what this index found),
**`dax-udf-authoring`** (how to write your own when none fits), and
**`dax-reference`** (what the built-in functions do).
```

- [ ] **Step 2: Replace workflow step 4 with the hand-off**

In `dax-lib/SKILL.md`, change:
```markdown
4. **Point at the install route**, do not paste code you do not have:
   - **Tabular Editor 3** → DAX Package Manager → search the package id → Install.
   - **Manually** → open the package `url` and copy its `functions.tmdl`.
5. **If nothing fits**, say so and route to `dax-udf-authoring`.
```
to:
```markdown
4. **If the user wants it installed**, not just documented, route to
   **`dax-lib-install`** — do not fetch, paste, or install the code yourself.
   That skill owns the fetch, the license check, the install, and the attribution.
5. **If nothing fits**, say so and route to `dax-udf-authoring`.
```

- [ ] **Step 3: Run the structural validator**

Run: `python scripts/validate_skills.py`
Expected: exits 0 — this task only edits prose inside an existing, already-valid `SKILL.md`, so nothing about its frontmatter or INDEX.md membership changes.

- [ ] **Step 4: Commit**

```bash
git add dax-lib/SKILL.md
git commit -m "feat(dax-lib): hand off installation to dax-lib-install"
```

---

### Task 4: Reconcile every "4 skills" claim to 5

**Files:**
- Modify: `README.md` (two spots: the inventory table and the version-floor prose)
- Modify: `docs/REVIEW.md` (two spots: the current-state inventory table, and a historical sentence that must be reworded without changing its number)

**Interfaces:**
- None — pure prose reconciliation, checked by `scripts/check_doc_claims.py`.

- [ ] **Step 1: README.md — inventory table**

Change:
```markdown
| **4 skills** | routed by `INDEX.md`, ~650 tokens of descriptions always on |
```
to:
```markdown
| **5 skills** | routed by `INDEX.md`, ~650 tokens of descriptions always on |
```
(Leave the token estimate as-is unless a later step's gate run flags it — `~650 tokens` is an estimate, out of `check_doc_claims.py`'s scope by its own docstring, so it is not touched here.)

- [ ] **Step 2: README.md — version-floor prose**

Change:
```markdown
The four skills sit flat at the repo root rather than under `skills/`, so that the
```
to:
```markdown
The five skills sit flat at the repo root rather than under `skills/`, so that the
```

- [ ] **Step 3: docs/REVIEW.md — current-state inventory table**

Change:
```markdown
| **4 skills** | `dax-reference`, `dax-lib`, `dax-udf-authoring`, `dax-window-functions` |
```
to:
```markdown
| **5 skills** | `dax-reference`, `dax-lib`, `dax-lib-install`, `dax-udf-authoring`, `dax-window-functions` |
```

- [ ] **Step 4: docs/REVIEW.md — reword the historical verification sentence**

This sentence describes a **dated, past observation** (bisecting Claude Code releases to find the version floor) made when there were 4 skills. Its number must not change — changing it would misstate what was actually measured that day. Reword to remove the literal `(4)` next to `skills` so the gate does not read it as a claim about today's tree.

Change:
```markdown
| El plugin instala y carga las 4 skills | instalado de verdad: `Skills (4) dax-lib, dax-reference, dax-udf-authoring, dax-window-functions`, ~647 tokens siempre encendidos |
```
to:
```markdown
| El plugin instala y carga las skills que declara | instalado de verdad, con las que había entonces: `Skills (4) dax-lib, dax-reference, dax-udf-authoring, dax-window-functions`, ~647 tokens siempre encendidos |
```

- [ ] **Step 5: Run the doc-claims gate**

Run: `python scripts/check_doc_claims.py`
Expected: `OK: prose agrees with the tree (479 cards, 34 concepts, 31 notes, 1 plugins, 4 scenarios, 5 skills, 11 terms, <N> tests, 6 workflows).` — confirm `5 skills` appears and there is no `DOC CLAIM CHECK FAILED` line. If the historical sentence in Step 4 still trips the gate, it means the literal digit `4` is still adjacent to `skills` somewhere in that line — remove the remaining adjacency (e.g. by rephrasing `Skills (4)` itself if the backtick-quoted code span is still being read as prose; the gate does not parse Markdown code spans specially) and rerun.

- [ ] **Step 6: Commit**

```bash
git add README.md docs/REVIEW.md
git commit -m "docs: reconcile skill count to 5 across README and REVIEW"
```

---

### Task 5: Full gate + test suite verification

**Files:** none (verification only).

**Interfaces:** none.

- [ ] **Step 1: Run all six gates**

```bash
python scripts/check_no_credentials.py
python scripts/check_doc_claims.py
python scripts/check_examples.py
python scripts/check_plugin_manifest.py
python scripts/check_workflow_cost.py
```
Expected: every one prints an `OK:` line and exits 0. If any fails, fix the specific file it names before continuing — do not proceed with a red gate.

- [ ] **Step 2: Run the full test suite**

```bash
python -m pytest -q
```
Expected: `<N> passed` (no failures), exit 0. This repo does not add pytest files for skill-prose changes — this step exists to confirm nothing in Tasks 1–4 broke an unrelated test (e.g. a test that counts skill folders or reads `plugin.json`).

- [ ] **Step 3: If all green, this task needs no commit** — it is a verification checkpoint, not a file change.

---

### Task 6: Manual dry run — install a real function, prove the workflow, remove it

This is the "testing" the approved spec calls for: not an automated CI gate (none of this
library's skills have one — they are prose), but a real, observed run of the six-step
workflow against a real package and a real model, done once during implementation so the
skill is not shipped unverified.

**Files:** none tracked — this task installs a function into a **live** Power BI Desktop
model over the modeling MCP, runs a query, and then **removes** the function again. It
must leave no permanent change in `lab/contoso` or any other tracked `.SemanticModel`:
vendoring a real third-party function permanently into the shared lab model is a separate
decision this plan does not make.

**Interfaces:** none — this exercises Task 1's documented workflow, it does not produce
an interface for later tasks.

- [ ] **Step 1: Connect to a live local Power BI Desktop instance**

Use the `powerbi-modeling-mcp` `connection_operations` tool, `Connect` operation, against
any currently open local instance (`Data Source=localhost:<port>`). If none is open, open
`lab/contoso/Contoso.pbip` in Power BI Desktop first and wait for it to load.

- [ ] **Step 2: Follow the dax-lib-install workflow for TimeSeries.MovingAverage.Simple**

Resolve: `packageId = TimeSeries.MovingAverage`, `version = 0.1.1`, function name =
`Simple`. Fetch with:
```bash
gh api repos/daxlib/daxlib/contents/packages/t/timeseries.movingaverage/0.1.1/lib/functions.tmdl --jq '.content' | base64 -d
```
Extract only the `TimeSeries.MovingAverage.Simple` block. Check `manifest.daxlib` at
`packages/t/timeseries.movingaverage/0.1.1/manifest.daxlib` for a license field — expect
none, per `dax-lib`'s own `NOTICE`. Build the attributed TMDL body per Task 1's
"Attribution" section, with `DAXLIB_License = UNLICENSED - VERIFY BEFORE SHIPPING`.

- [ ] **Step 3: Install it via the modeling MCP**

Call `function_operations` with `operation: Create` and the attributed function
definition (name, description carrying the attribution comment, expression body,
annotations). Confirm the tool reports success and `function_operations` with
`operation: List` shows `TimeSeries.MovingAverage.Simple` present.

- [ ] **Step 4: Test it with a real query**

Use `dax_query_operations`, `operation: Execute`, with a query that calls the installed
function against a real table/column/measure in the connected model (for example,
`DimDate[YearMonth]`, `DimDate`, and `[Total Sales]` if connected to `lab/contoso`).
Confirm the query returns rows with no engine error.

- [ ] **Step 5: Confirm the attribution round-trips**

Call `function_operations` with `operation: ExportTMDL` for the installed function's
name and visually confirm the exported TMDL contains all five annotations
(`DAXLIB_PackageId`, `DAXLIB_PackageVersion`, `DAXLIB_Author`, `DAXLIB_License`,
`DAXLIB_SourceUrl`) and the `///` attribution comment.

- [ ] **Step 6: Remove it — leave the model exactly as it was**

Call `function_operations` with `operation: Delete` and the installed function's
reference. Confirm with `operation: List` that it no longer appears. Do not run
`database_operations` `ExportToTmdlFolder` or otherwise write this test install to any
tracked `.SemanticModel/definition/` file — this step exists to prove the workflow
works, not to ship the function.

- [ ] **Step 7: No commit** — nothing tracked changed in this task by design. Record the
  observed result (install succeeded, test query returned rows, attribution round-tripped,
  removal succeeded) in the PR description for Task 1–4's branch, as the evidence that
  the skill was verified before shipping.

---

## Self-review notes

- **Spec coverage:** every numbered step in the spec's "Step-by-step workflow" (resolve,
  fetch, license, install, test, report) is reproduced verbatim in Task 1's `SKILL.md`
  content; the attribution format matches the spec's TMDL example exactly; the
  hand-off edit to `dax-lib/SKILL.md` matches the spec's diff exactly; the error table
  matches the spec's error-handling table exactly; the "what this does not do" section
  covers the three "not a..." bullets from the spec's "What this is not" section.
- **Placeholder scan:** none found — every task step has literal file content or a
  literal command with an expected result string.
- **Type consistency:** the function names (`TimeSeries.MovingAverage.Simple`), package
  id (`TimeSeries.MovingAverage`), version (`0.1.1`), and author (`Tate Bowman`) are the
  same across Task 1's skill content and Task 6's dry run — this is deliberate: Task 6
  exercises the exact example the skill file documents.
