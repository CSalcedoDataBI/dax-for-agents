# rendimiento — what actually costs, over two million rows

This scenario exists because nothing could be measured on Contoso: 126,524 rows resolve in
milliseconds and any comparison fell inside the noise.

And it came out the opposite of what it set out to find. It was built to demonstrate that
`FILTER` over a whole table is expensive — the advice everyone repeats — and **it is not**. What
costs is something else.

## The model

One table, `Ventas`, with **2,000,000 rows**. In the other two synthetic scenarios the data is
five or seven hand-picked rows because the anomaly reads at a glance; here the volume **is** the
scenario: below a few million rows a good plan and a bad one cost the same and there is nothing
to compare.

| column | what it is |
|---|---|
| `VentaKey` | 1..2,000,000, unique |
| `Importe` | 1..1000, spread with a prime step |
| `CategoriaKey` | 20 distinct values — cardinality 1 in 100,000 |

The measures come **in pairs, and the two in each pair return the same number**. Without that,
comparing times would say nothing about performance.

## Where the data comes from

A Parquet file published in
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (public, MIT,
synthetic), read the same way as in the other three scenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

**It weighs 385 KB, not 8.9 MB**, and that difference has a concrete cause. `VentaKey` is two
million distinct, consecutive values: the Parquet dictionary is useless for it, and with plain
snappy that column leaves the file at 8.9 MB — four times the whole of Contoso. Encoded as
**deltas** (`DELTA_BINARY_PACKED`) it drops 23×, because the step from one row to the next is
always 1. The other two columns keep their dictionary.

That Power Query reads that encoding is **verified, not assumed**: it is what refreshes this
model. The other two columns were left on dictionary encoding because they gained nothing from
the change.

Dropping `VentaKey` would have made the file smaller still — no measure uses it — and it **was
not done**: the times published below were measured with it, and a model without it would be a
different model. The nine values in the final table were re-measured after changing the source
and come out identical.

It is regenerated with [`build_datasets.py`](../build_datasets.py), deterministically:
`Importe = (i × 7919) mod 1000 + 1` and `CategoriaKey = i mod 20 + 1`.

## How it was measured

- **Cold**: `ClearCache` before every run. Without that you measure the cache, not the plan.
- **Three runs** per measure, taking the **median**.
- What is published are **ratios and orders of magnitude**, not absolute times: a number in
  milliseconds ages with the hardware; that one form costs ~290 times another does not.
- Engine metrics (duration, peak memory, storage-engine queries), not client wall time.

## What does NOT cost

The six measures in group A, **all six together and cold**:

| | |
|---|---|
| duration | **5 ms** |
| peak memory | 1,027 KB |
| storage-engine queries | 3 |

And inside that are the three forms the usual advice treats as expensive:

| pair | the two forms | result |
|---|---|---|
| A1 | `FILTER(ALL(Ventas), Ventas[Importe] > 900)` vs the predicate `Ventas[Importe] > 900` | 190,100,000 |
| A2 | filtering the **table** by category vs filtering the **column** (20 values) | 50,900,000 |
| A3 | a predicate comparing **two columns** against each other, over the table vs over the columns | 642,600,000 |

**The engine pushes the predicate down to storage in all three cases**, including the one that
compares two columns against each other. Wrapping the table in a `FILTER` costs nothing here.

## What DOES cost

The **context transition**: referencing a *measure* where there is row context forces that row
to become a filter, two million times.

| measure | cold median | peak memory | SE queries |
|---|---|---|---|
| `SUMX(Ventas, [Total])` | **871 ms** | **197,300 KB** | 2 |
| `SUMX(Ventas, Ventas[Importe])` | **3 ms** | 0 KB | 1 |
| `CALCULATE([Total], FILTER(ALL(Ventas), [Total] > 900))` | **873 ms** | **197,342 KB** | 2 |
| `CALCULATE([Total], Ventas[Importe] > 900)` | within group A's 5 ms | — | — |

**≈ 290×**, and from zero to ~193 MB of memory. Both pairs return the same number as their cheap
version: 1,001,000,000 and 190,100,000.

> This trap is also **drawn**: page «2. Lo que cuesta cada forma (medido, no calculado)» of the
> report. Open it with the `.pbip` and look, because that is where you see what the query result
> does not show.

## What this means

The bulk is not in `FILTER`, nor in passing it a table instead of a column. It is in **what is
inside the predicate**. A predicate over columns is resolved by the storage engine in one pass; a
**measure** inside forces the formula engine to materialise and to transition context row by row.

The rule these numbers support is not "don't use FILTER over tables", but:

> **Do not put a measure where you are going to iterate two million rows.**

See [`sumx`](../../skills/dax-reference/notes/sumx.md) and
[`calculate`](../../skills/dax-reference/notes/calculate.md) for the mechanism, which is the same
one that makes `SUMX` with a measure return a different number from `SUMX` with the expression
written out. Here you also see what it costs.

## The queries

```dax
EVALUATE
{
  ("A1 FILTER",             [Alto FILTER]),
  ("A1 predicado",          [Alto predicado]),
  ("A2 por tabla",          [Categoria por tabla]),
  ("A2 por columna",        [Categoria por columna]),
  ("A3 cruce por tabla",    [Cruce por tabla]),
  ("A3 cruce por columnas", [Cruce por columnas]),
  ("B1 con medida",         [Suma con medida]),
  ("B1 con columna",        [Suma con columna]),
  ("B2 con medida",         [Alto con medida])
}
```

| measure | value |
|---|---|
| A1 (both) | 190,100,000 |
| A2 (both) | 50,900,000 |
| A3 (both) | 642,600,000 |
| B1 (both) | 1,001,000,000 |
| B2 | 190,100,000 |

Those values are stable and [`check_lab.py`](../check_lab.py) checks them. **The times are not
checked automatically**: they depend on the machine, and a threshold in a test would be a false
promise. What the runner guarantees is that the pairs still return the same thing, which is the
condition without which comparing times means nothing.

> This trap is also **drawn**: page «1. Los pares devuelven el mismo numero» of the report. Open
> it with the `.pbip` and look, because that is where you see what the query result does not show.

## Limits, stated

- **One model, one machine, one engine.** These numbers came out of Power BI Desktop on a
  laptop. The ~290× ratio is what gets published because it is what survives a change of
  hardware; the milliseconds are there for context, not to be quoted.
- **That it does not cost here does not mean it never costs.** `FILTER` over a table can cost a
  lot with more columns, with relationships in between, or with predicates the engine cannot push
  down. What was measured is what is claimed: in this model, with these predicates, it does not
  cost.
- **Refreshing needs internet**, like the other three scenarios. Two million rows fit in 385 KB
  of Parquet, so the download is not the bottleneck; loading them into the engine does take a few
  seconds.
