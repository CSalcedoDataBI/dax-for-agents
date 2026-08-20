---
name: dax-window-functions
description: Use when writing a DAX window function — WINDOW, OFFSET, INDEX, RANK, ROWNUMBER, MOVINGAVERAGE, RUNNINGSUM with ORDERBY/PARTITIONBY/MATCHBY — for rolling and trailing averages, running totals, prior-row or prior-year comparisons, or ranking within a partition. Covers ABS vs REL positioning, the ALLSELECTED relation default that silently returns blanks, and MATCHBY for fact tables. Triggers on "rolling average", "running total", "trailing N", "OFFSET returns blank", "ABS vs REL", "PARTITIONBY".
---

# DAX Window Functions — the navigation machinery

## Overview

The `WINDOW` family operates over a **relation** (a virtual table), not scalars: it is evaluated in the current filter context, **partitioned**, **sorted**, then **navigated** relative to the current row. This is the machinery inside rolling/trailing UDFs — see **`dax-udf-authoring`**.

**Per-function reference:** **`dax-reference`** carries each function's signature, return type and where it is legal. This skill is the working summary of how the family behaves together, plus the gotchas that bite.

## Pick the function

| Need | Function | Returns |
|---|---|---|
| Contiguous set of rows (rolling/trailing window) | `WINDOW` | table |
| Single row at a relative offset (prior/next, YoY) | `OFFSET` | row(s) |
| Single row at an absolute position (first/last) | `INDEX` | row |
| Rank within partition (ties allowed) | `RANK` | scalar |
| Unique row number (no ties) | `ROWNUMBER` | scalar |
| Moving avg / running sum **(visual calc ONLY)** | `MOVINGAVERAGE` / `RUNNINGSUM` | scalar |

Table-returning ones (`WINDOW/OFFSET/INDEX`) are wrapped in an aggregator (`AVERAGEX`, `SUMX`) or used as a `CALCULATE` filter.

## Shared positional tail (order is FIXED)

```
[, <relation>/<axis>][, <orderBy>][, <blanks>][, <partitionBy>][, <matchBy>][, <reset>]
```
Skip `relation` but keep `orderBy`: leave the slot empty → `OFFSET(-1, , ORDERBY(...))`.

## ABS vs REL — the crux of WINDOW

- **REL (relative):** offset from the **current row**. `-3,REL` = three rows back; `0,REL` = current.
- **ABS (absolute):** 1-based position from the **partition edge**. `1,ABS` = first; `-1,ABS` = last.

| Pattern | Bounds |
|---|---|
| Trailing N rows incl. current | `WINDOW(-(N-1), REL, 0, REL, ...)` |
| Running total | `WINDOW(1, ABS, 0, REL, ...)` |
| Everything after current | `WINDOW(0, REL, -1, ABS, ...)` |

```dax
-- Trailing 4-quarter avg (true cross-year window — no PARTITIONBY)
Trailing 4Q Avg =
AVERAGEX (
    WINDOW ( -3, REL, 0, REL,
        ALLSELECTED ( 'Date'[Year], 'Date'[Quarter Number] ),
        ORDERBY ( 'Date'[Year], ASC, 'Date'[Quarter Number], ASC ) ),  -- total order, no ties
    [Total Sales]
)
```
Add `PARTITIONBY('Date'[Year])` to **restart each year** instead.

## The gotchas (read before shipping)

| Gotcha | Effect | Fix |
|---|---|---|
| **`relation` omitted → defaults to `ALLSELECTED()`** of orderBy+partitionBy cols | Window only sees rows the filter context allows; a YoY offset returns **blank** if the prior year is filtered out by a slicer | Pass an explicit relation: `ALL('Date'[Year])` / wider `ALLSELECTED('Date')` |
| **orderBy not a total order** | Non-deterministic, or `ROWNUMBER` **errors** | Add a key column to `ORDERBY`, or use `MATCHBY` |
| **Bare fact table, keys don't identify the row** | `OFFSET`/`WINDOW` error | `MATCHBY( fact[OrderNo], fact[LineNo] )` — only **model columns** with lineage qualify (measure-derived cols don't) |
| **`RANK`/`ROWNUMBER` on total rows** | return **blank** | guard totals |
| **`MOVINGAVERAGE`/`RUNNINGSUM` in a measure** | not supported | use `AVERAGEX(WINDOW(...))` / `SUMX(WINDOW(1,ABS,0,REL,...))` |
| Out-of-range `delta`/`position` | empty table (not error) for `INDEX`/`OFFSET` | test for `COUNTROWS = 0` |

## CALCULATE + KEEPFILTERS

Window tables used as `CALCULATE` filters **overwrite** the column's filter by default. Wrap in `KEEPFILTERS(...)` to **intersect** with the existing context instead. Choose the `relation` to control *what the window sees*; `KEEPFILTERS` to control *how its rows combine* with the outer filter.

## Why prefer these over TOPN + FILTER

`OFFSET`/`WINDOW` target a **single sorted scan** of the relation; the classic `TOPN(N, FILTER(ALLSELECTED(...), col <= MAX(col)), col, DESC)` re-scans per current row (O(N²)-flavored) and you must hand-build a unique sort key. Prefer windows on CL ≥ 1600; reserve `TOPN+FILTER` for older compatibility levels. **Caveat:** SQLBI notes hand-tuned canonical DAX occasionally still wins — benchmark on large models, and keep the current row singular (`MATCHBY`) to avoid expensive apply-semantics fan-out.

## Availability

`WINDOW/OFFSET/INDEX/RANK/ROWNUMBER` → CL ≥ 1600 (Dec 2022+); measures, calc columns, calc tables, visual calcs. `MOVINGAVERAGE/RUNNINGSUM` + `reset`/`axis` → **visual calculations only**.
