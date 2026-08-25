---
name: dax-lib
description: Use when looking for an EXISTING published DAX user-defined function before writing one — moving averages, format strings, SVG visuals, KPI/variance, RFM or ABC classification, unit conversion, model audit/metadata, sample data, time intelligence. Offline index of the DAX Lib registry (daxlib.org) — what exists, who wrote it, and where to get it. Triggers on "is there a UDF for", "find an existing DAX function", "ready-made", "already exists", "daxlib", "DAX package".
---

# DAX Lib — index of published DAX UDFs

**Before authoring a UDF from scratch, check here — someone may have already shipped it.**

This is an **offline index** of [DAX Lib](https://daxlib.org), the package registry for DAX
user-defined functions. It tells you what exists, who wrote it and what it does, so the agent
can answer "does this already exist?" without a network round trip.

**It does not carry the DAX code.** The code lives at the registry, which is where it stays
current. See [`NOTICE`](./NOTICE).

Pairs with **`dax-lib-install`** (actually install what this index found),
**`dax-udf-authoring`** (how to write your own when none fits), and
**`dax-reference`** (what the built-in functions do).

## Files

| File | Use |
|---|---|
| `catalog.md` | Human index — one row per package: id, latest version, author, functions, description. **Scan this first.** |
| `catalog.json` | Machine index — every version, with `functions[]`, `tags[]`, `isLatest`, `url`. Use for keyword/tag search. |
| `scripts/refresh-daxlib.ps1` | Rebuild the index from `daxlib/daxlib`. |

## Workflow

1. **Identify the need** — "trailing moving average", "waterfall SVG", "RFM segmentation".
2. **Search the index.** Grep `catalog.md`, or query `catalog.json` by `tags` / `functions` /
   `description`. Tags are coarse (`DAX,UDF,SVG,TIMESERIES,…`) — match on description and
   function names too.
3. **Report what you found**: package id, author, the function signature from `functions[]`,
   and the `url` to its source. Say plainly that the code has to come from the registry.
4. **If the user wants it installed**, not just documented, route to
   **`dax-lib-install`** — do not fetch, paste, or install the code yourself.
   That skill owns the fetch, the license check, the install, and the attribution.
5. **If nothing fits**, say so and route to `dax-udf-authoring`.

## Example

```
Need: trailing N-period moving average over a dynamic date column.
catalog.json → id "TimeSeries.MovingAverage" (latest 0.1.1), tags TIMESERIES,
  functions: Simple, Weighted, LinearWeighted, Exponential, DoubleExponential,
             Triangular, Geometric
url → https://github.com/daxlib/daxlib/tree/main/packages/t/timeseries.movingaverage
```

`TimeSeries.MovingAverage.Simple( dateColumn, timeSeriesTable, lookbackPeriods, expression )`
is built on native `WINDOW` (see **`dax-window-functions`**), which is generally cheaper than a
hand-rolled `TOPN + CALCULATETABLE`. It needs a fixed date column, so it does not fit a model
whose grain is a dynamic period axis.

## Refresh

```powershell
pwsh ./scripts/refresh-daxlib.ps1
```

Shallow-clones `daxlib/daxlib@main`, reads each package's `manifest.daxlib`, parses the function
names out of its `functions.tmdl`, and rewrites `catalog.json` + `catalog.md` stamped with the
upstream commit. **It keeps no `.tmdl` file.**

**Why a script and not WebFetch:** daxlib.org is a JavaScript SPA — a plain HTTP GET returns the
empty app shell. GitHub is the source of truth.

## Notes

- The index is a snapshot; the registry is live. Check `source` in `catalog.json` for how old it
  is, and prefer the registry when a version matters.
- All versions are indexed (`isLatest` flags the newest per package). Prefer the latest unless
  reproducing a specific one.
- Some `manifest.daxlib` files still point their `$schema` at the old `sql-bi/daxlib` path — the
  repo was renamed to `daxlib/daxlib`. Harmless.
- **Licensing varies per author.** The upstream repo is MIT, but individual packages declare no
  license of their own — check the package before reusing its code in a product.
