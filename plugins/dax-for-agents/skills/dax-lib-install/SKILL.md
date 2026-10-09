---
name: dax-lib-install
description: Use when installing a DAX UDF from daxlib.org into a live model or PBIP folder after dax-lib found it. Fetches the function body with gh api, asks before writing, records author, license and source on the function, installs it, and test-runs it. Triggers on "install this UDF", "bring in the daxlib function", "add the daxlib function to my model", "vendor this DAX package".
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
   gh api -H "Accept: application/vnd.github.raw"      repos/daxlib/daxlib/contents/packages/<first-letter-lowercase>/<packageId-lowercase>/<version>/lib/functions.tmdl
   gh api repos/daxlib/daxlib/commits/main --jq .sha    # the commit you read it at
   ```
   Without the `Accept` header the contents API returns a JSON envelope with the file
   base64-encoded, not the TMDL.
   Same path convention `dax-lib/scripts/refresh-daxlib.ps1` already reads for the
   index — used here to read a function *body*, not just its name. Pull only the
   `function '<name>' = ...` block requested out of the file; the package's other
   functions are not your concern.

3. **Check the license.** The daxlib manifest schema has no license field, so there is
   no per-package declaration (see `dax-lib`'s `NOTICE`): the upstream repository carries
   a single MIT license naming SQLBI, and reading a contribution as covered by it is a
   convention, not a documented agreement. If the package's version directory has its
   own `LICENSE`, record it verbatim. Otherwise the attribution carries
   `Repo MIT (SQLBI); no per-package license - VERIFY BEFORE SHIPPING`, and your final
   report to the user repeats that warning unhedged. Do not soften it into a footnote.

4. **Confirm before writing.** Check the model's compatibility level (UDFs need 1702 or
   later) and run `EVALUATE INFO.USERDEFINEDFUNCTIONS()`: if a function with that name
   already exists, stop and ask — installing would replace it. Then show the user the
   function body, the license line and the target model, and install only on a yes.

5. **Install.** Prefer a live connection through the modeling MCP
   (`function_operations` → `Create`) when one is available. Fall back to editing the
   model's TMDL on disk — a bare `function '<name>' = ...` block in the PBIP
   `definition/` folder; `createOrReplace` is TMDL *view* script syntax, not file
   syntax — only when nothing live is reachable, and only with Desktop closed on that
   model, or its in-memory copy overwrites the edit. Live tooling first, hand-written
   TMDL last.

6. **Test.** Run one real DAX query against the connected model that calls the
   newly installed function and confirms it executes without error. No invented
   expected value — the test is "does this run, in this model, on this
   compatibility level, against these real column names." A copy-pasted
   third-party function is exposed to exactly the same failure modes an
   originally-authored one is (a model below the compatibility level DAX UDFs
   require fails the same way regardless of who wrote the function).

7. **Report.** One message: what was installed (function, package, version,
   author), the exact source URL — the version path at the commit SHA from step 2,
   not just the package id, the license that
   applies (or the no-per-package-license warning), and the result of the test query. No
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
/// License: Repo MIT (SQLBI); no per-package license - VERIFY BEFORE SHIPPING.
/// Source: https://github.com/daxlib/daxlib/blob/<sha>/packages/t/timeseries.movingaverage/0.1.1/lib/functions.tmdl
function 'TimeSeries.MovingAverage.Simple' =
        ( ... )
    annotation DAXLIB_PackageId = TimeSeries.MovingAverage
    annotation DAXLIB_PackageVersion = 0.1.1
    annotation DAXLIB_Author = Tate Bowman
    annotation DAXLIB_License = Repo MIT (SQLBI); no per-package license - VERIFY BEFORE SHIPPING
    annotation DAXLIB_SourceUrl = https://github.com/daxlib/daxlib/blob/<sha>/packages/t/timeseries.movingaverage/0.1.1/lib/functions.tmdl
```

If the package's original doc comment exists (the `///` line already in its
`functions.tmdl`, e.g. *"Returns a simple moving average..."*), keep it as a second
paragraph below the attribution block. The attribution is prepended, never
overwrites the description of what the function does.

## What this does not do

- Does not install a whole package — one named function per request.
- Does not resolve dependencies between packages, manage upgrades, or maintain a
  lockfile. One named function, one named version, on request.
- Does not decide FOR the user whether a package without its own license is safe to ship. It
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
