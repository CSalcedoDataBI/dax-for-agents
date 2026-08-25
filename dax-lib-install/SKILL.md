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
