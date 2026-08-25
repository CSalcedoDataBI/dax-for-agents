# dax-lib-install — a fifth skill that installs a third-party DAX UDF with attribution

Status: approved by the owner in conversation on 2026-08-24, pending implementation plan.

## The problem

`dax-lib` is deliberately an **index only**. Its own `NOTICE` and `SKILL.md` say so in
as many words: it tells an agent what exists, who wrote it, and where to get it — it
never carries or vendors third-party DAX code, because the moment it did, the index
would also be a copyright liability the maintainer never agreed to.

That is the right call for the index. It is the wrong call for the *agent's workflow*
once a real answer is "yes, use this": today `dax-lib`'s own step 4 says *"point at the
install route, do not paste code you do not have"* — Tabular Editor 3's DAX Package
Manager, or a manual copy of `functions.tmdl` from the registry. Both routes hand the
work back to a human. Nothing in the library actually fetches the real code, installs
it against a real model, tests that it runs, and leaves it attributed well enough that
nobody downstream mistakes it for original work.

This was found for real, this session: `dax-lib` correctly identified that
`TimeSeries.MovingAverage` (Tate Bowman, v0.1.1) already solves a trailing-average need
on Contoso. The agent (this session) chose to write an equivalent function from scratch
instead — a legitimate choice, but one `dax-lib`'s current workflow *forces*, because it
has no path to actually install the third-party one.

## What this is not

- **Not a change to `dax-lib`'s contract.** It stays index-only. `NOTICE` and the "It
  does not carry the DAX code" line are untouched.
- **Not a replacement for `dax-udf-authoring`.** That skill is for writing *your own*
  function from scratch. This one is for installing *someone else's*, already-published
  one, with the paperwork that implies.
- **Not a package manager.** It installs one named function from one named package
  version, on request. It does not resolve dependencies, does not manage upgrades, does
  not maintain a lockfile.

## Architecture

One new skill, `dax-lib-install`, sibling to the existing four
(`dax-lib`, `dax-reference`, `dax-window-functions`, `dax-udf-authoring`), same
directory shape (`SKILL.md` + `NOTICE` if needed), same language (English, matching
every existing skill's name and content — corrected mid-design after an initial
Spanish-name draft).

```
dax-lib  (index) --finds a candidate-->  agent decides to install
                                              |
                                              v
                                     dax-lib-install (this skill)
                                     resolve -> fetch -> license check
                                     -> install -> test -> report
```

`dax-lib`'s workflow step 4 changes from a manual pointer to an explicit hand-off:

```diff
- 4. **Point at the install route**, do not paste code you do not have:
-    - **Tabular Editor 3** → DAX Package Manager → search the package id → Install.
-    - **Manually** → open the package `url` and copy its `functions.tmdl`.
+ 4. **If the user wants it installed**, not just documented, route to
+    **`dax-lib-install`** — do not fetch, paste, or install the code yourself.
+    That skill owns the fetch, the license check, the install, and the attribution.
```

## Step-by-step workflow (dax-lib-install)

1. **Resolve.** Inputs: `packageId`, `version` (both from `dax-lib`'s `catalog.json`),
   and the **exact function name** needed — not the whole package. A package can ship
   several functions (`TimeSeries.MovingAverage` ships 7); this skill installs the one
   asked for, nothing else, per the owner's explicit choice to keep model surface
   minimal.
2. **Fetch the real code.** `gh api
   repos/daxlib/daxlib/contents/packages/{first-letter}/{packageId-lowercase}/{version}/lib/functions.tmdl`
   — the same path convention `dax-lib/scripts/refresh-daxlib.ps1` already reads for the
   index, used here to read the *function body*, not just its name. Extract the single
   `function '<name>' = ...` block requested; leave the rest of the file's other
   functions alone.
3. **Check the license.** Look for `manifest.daxlib`'s license field (if any) and a
   `LICENSE` file in the package's version directory. If a license is declared, record
   it verbatim. If none is declared — the documented common case, per `dax-lib`'s own
   NOTICE — proceed to install anyway, but the attribution carries
   `UNLICENSED - VERIFY BEFORE SHIPPING` in capitals, and the skill's final report to the
   user repeats that warning plainly, unhedged.
4. **Install.** Prefer a live connection through the modeling MCP (`function_operations`
   `Create`) when one is available — mirrors exactly what this session did for
   `Contoso.Lab.MediaMovil3M`. Fall back to a direct TMDL file edit
   (`createOrReplace function` block, following `dax-udf-authoring`'s documented TMDL
   syntax) when no live connection exists. Same preference order
   `dax-udf-authoring` and `powerbi-report-planning` already document: modeling
   skill/MCP first, hand-written TMDL only when nothing live is reachable.
5. **Test.** Run one real DAX query against the connected model that calls the newly
   installed function and confirms it executes without error. No invented expected
   value, no synthetic case — the test is "does this run, in this user's model, on this
   compatibility level, against these real column names," which is exactly the class of
   failure a copy-pasted third-party function is likely to hit (see the
   `compatibilityLevel` 1606→1702 failure this session hit while installing an
   originally-authored function — a third-party one is exposed to the identical risk).
6. **Report.** One message: what was installed (function, package, version, author),
   where it came from (the exact GitHub URL, not just the package id), what license
   applies (or the unlicensed warning), and the result of the test query. No silent
   success — every install is a paper trail.

## Attribution mechanics

The real `functions.tmdl` pulled from `daxlib/daxlib` already carries two annotations
stamped by the registry itself:

```tmdl
annotation DAXLIB_PackageId = TimeSeries.MovingAverage
annotation DAXLIB_PackageVersion = 0.1.1
```

`dax-lib-install` preserves these as-is — they are the registry's own record, not
something to reinvent — and adds the three facts the raw file doesn't carry: who wrote
it, what license applies, and exactly where it came from. Attribution lives **on the
function itself** (a `///` doc comment plus TMDL `annotation` key/values), not in a
separate manifest file, so it survives if the function is later exported or copied on
its own:

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

When the package's original doc comment (the `///` line already in its `functions.tmdl`,
e.g. *"Returns a simple moving average..."*) exists, it is kept as a second paragraph
below the attribution block — the description of *what it does* stays; the *where it
came from* is prepended, never overwritten.

## Error handling

| Failure | Behavior |
|---|---|
| `gh api` can't reach the package path (renamed, deleted, wrong version) | Stop, report the exact path tried, do not guess at a substitute function |
| Requested function name isn't in the fetched `functions.tmdl` | Stop, list the functions that *are* in that file, let the caller re-choose |
| No live model connection and no local TMDL folder | Stop — this skill installs into a real target, it does not stage code with nowhere to land |
| Model's `compatibilityLevel` is below what user-defined functions require | Same failure this session hit installing an original function: report the exact required level, do not silently skip the install |
| Test query errors after install | Report the raw engine error; do not roll back automatically (leaves evidence for debugging), but the report must not claim success |

## Testing (of the skill itself, not of what it installs)

Since this ships as a skill (prose + a documented procedure), "testing" here means: a
dry run against a real package (`TimeSeries.MovingAverage.Simple`, already verified real
this session) into a real local scratch model, confirming steps 1–6 all produce the
exact artifacts described above, before the skill is considered done. This is a manual
verification pass during implementation, not an automated CI gate — no other skill in
this library has one either; skills are prose, and `validate_skills.py` already checks
frontmatter/structure for all of them.

## Open items intentionally left to the implementation plan

- Exact wording of the new `dax-lib-install/SKILL.md` (frontmatter `description`,
  trigger phrases) — drafted during implementation, following the same voice as the
  other four.
- Whether `dax-lib`'s `catalog.md`/`README` need a one-line pointer to the new skill
  (likely yes, small edit).
