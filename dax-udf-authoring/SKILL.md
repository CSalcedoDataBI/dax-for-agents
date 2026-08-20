---
name: dax-udf-authoring
description: Use when AUTHORING your own DAX user-defined function — the mechanics of writing a FUNCTION — declaring parameter types (Scalar, AnyRef, ColumnRef, MeasureRef, CalendarRef), VAL vs EXPR evaluation, TABLEOF/NAMEOF, optional parameters and defaults, dot-notation naming, GA limitations and parser red-underline bugs. Not for finding an existing one (that is dax-lib) nor for what a built-in does (that is dax-reference). Triggers on "write a DAX UDF", "define a DAX FUNCTION", "ANYREF", "VAL vs EXPR", "TABLEOF", "optional parameter in a UDF".
---

# DAX UDF Authoring — the mechanics

## Overview

How to write a **correct** DAX user-defined function.

**Most problems should not be a UDF at all.** Reach for one when the same logic is repeated across
measures with only the column or measure reference changing. Do not reach for one to wrap a single
measure — see the per-row trap under Common mistakes. For window machinery inside a rolling or
trailing UDF, see **`dax-window-functions`**.

> **Before writing one from scratch:** search the **`dax-lib`** skill — an index of the
> [daxlib.org](https://daxlib.org) registry (55 packages, ~1,649 functions). `TimeSeries.MovingAverage`
> (SMA/WMA/EMA over native `WINDOW`) may already solve a rolling-average need. The index tells you
> what exists; the code comes from the registry.

**Per-function reference:** **`dax-reference`** carries the signature and semantics of each built-in.
This skill is about the mechanics of authoring your own, plus the gotchas that bite.

## Syntax — define once, two surfaces

```dax
-- DAX Query View (DEFINE) — for testing
DEFINE
    /// Descripción JSDoc (aparece en IntelliSense)
    /// @param {ANYREF} qtrCol - columna de trimestre fiscal
    /// @returns promedio de 4 trimestres
    FUNCTION Contoso.Scorecard.Example = ( qtrCol : ANYREF, metric : ANYREF, N : SCALAR INT64 = 4 ) =>
        <body>
```
```tmdl
-- TMDL view — saves to the model
createOrReplace
    /// Descripción
    function 'Contoso.Scorecard.Example' = ( qtrCol : ANYREF ) => <body>
```
Save from DQV: **"Update model with changes"** (all) or **"Update model: Add new function"** (cursor only).

## Parameter types — quick reference

| Type | Family | Default mode | VAL | EXPR | Use |
|---|---|---|---|---|---|
| `AnyVal` | Value | VAL | ✅ | ✅ | scalar or table (default if omitted) |
| `Scalar` | Value | VAL | ✅ | ✅ | scalars; combine with subtype |
| `Table` | Value | VAL | ✅ | ✅ | tables only |
| `AnyRef` | Expression | EXPR | ❌ | ✅ | any reference — **most permissive, our default** |
| `ColumnRef` | Expression | EXPR | ❌ | ✅ | model column only (`_Column`) |
| `MeasureRef` | Expression | EXPR | ❌ | ✅ | model measure only (`_Measure`) |
| `TableRef` / `CalendarRef` | Expression | EXPR | ❌ | ✅ | table / calendar reference |

Scalar subtypes: `Int64`, `Decimal`, `Double`, `String`, `DateTime`, `Boolean`, `Numeric`, `Variant`.

## VAL vs EXPR — the one that bites

- **VAL (eager):** arg evaluated **before** entering the function. Inherits filter **+ row** context. For simple scalars / already-filtered tables.
- **EXPR (lazy):** arg evaluated **inside** the function. Inherits **only filter** context. **Required** for all Ref types. Needed when `CALCULATE` must modify the arg's context.

```dax
-- ❌ doc_type as VAL → CALCULATE can't change its context
FUNCTION Bad = ( doc_type ) => CALCULATE ( SUMX(...), 'T'[DocType] = doc_type )
-- ✅ ANYREF implies EXPR → CALCULATE works
FUNCTION Good = ( doc_type : ANYREF ) => CALCULATE ( SUMX(...), 'T'[DocType] = doc_type )
```

## Utility functions

- `TABLEOF( columnRef )` → the parent table of a column/measure/calendar. Essential to iterate when you only have a `COLUMNREF`/`ANYREF`.
- `NAMEOF( ref )` → the table/column/measure name as text (cross-validation, error messages).
- Body type-checks: `ISNUMERIC ISINT64 ISDECIMAL ISSTRING ISBOOLEAN ISDATETIME` (+ `ISNUMBER/ISTEXT/...` aliases).

## Optional parameters

```dax
FUNCTION AddTax = ( amount : NUMERIC, taxRate : NUMERIC = 0.1 ) => amount * ( 1 + taxRate )
AddTax(100)      -- 110   AddTax(100,0.21) -- 121   AddTax(100,) -- 110 (empty arg = default)
```
Rules: optionals in any position; min arity = rightmost required param; default resolves where **defined**, not where called; a default cannot reference another optional param.

## Naming (Tabular Editor convention)

Dot-notation namespace: `Contoso.Scorecard.Rolling4QtrAvg`. Param suffixes: `_Column` `_Measure` `_Table` `_Calendar` `_Expr`.


## GA limitations & known bugs (June 2026, CL 1702+)

- Desktop-only authoring; no folders, no hide/show, no translations, no OLS transfer.
- **No recursion, no overloading, no explicit return type.**
- ⚠️ **`ColumnRef`/`MeasureRef`/`TableRef` may be rejected at some call sites → fall back to `ANYREF`.**
- ⚠️ **Red underlines on columns-as-`expr` are often false positives** — the code can still execute correctly. Validate by running, not by trusting IntelliSense.
- Inspect model UDFs: `EVALUATE INFO.USERDEFINEDFUNCTIONS()`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing a column but typed `SCALAR VAL` | Use `ANYREF` (EXPR) so `CALCULATE` can re-context it |
| Wrapping a per-row base measure in a UDF | Don't. The UDF body is evaluated **once per row** of the iteration instead of folding into a single scan, so the cost scales with cardinality — the regression can be orders of magnitude on a large fact table. Inline it and measure both |
| Calling `'Contoso.Scorecard.X'(...)` with quotes | No quotes on call: `Contoso.Scorecard.X(...)` |
| UDF references a measure that itself calls the UDF | Circular dependency — call the underlying base measure inside the UDF, not the consumer |
| Trusting the red underline | Execute the query and see; a parser complaint is not a runtime error |

## Validate before saving

Run the old and new expressions side by side: a diff query returning **0 rows**, plus a row-count sanity check, before trusting it. Then measure — a UDF that is correct and slower is not an improvement.

Red underlines are not the test: **run it**. The parser reports false positives on columns passed as `expr` (see GA limitations above).
