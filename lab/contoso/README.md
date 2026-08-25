# contoso — the model 30 of the 31 field notes were measured against

The other three scenarios exist to demonstrate a trap that Contoso **cannot** demonstrate. This
one is the opposite: it is the model where almost everything else was measured.

Until now it lived on one machine. Twenty-nine field notes carried the footer *"Measured against
Contoso Retail (FactSales 126,524 rows, 137 products…)"* and the reader had the query, the
number, and **no way to run either**. That was most of the hand-written content in the repo
resting on something nobody else could open.

## The model

A star schema of seven tables plus `_Measures`:

| table | rows | what it is |
|---|---|---|
| `FactSales` | **126,524** | one order line (`OrderKey` + `LineNumber`) |
| `DimProduct` | **137** | product, with `Brand`, `CategoryName`, `Color`, `Price` |
| `DimCustomer` | 12,000 | customer |
| `DimStore` | 25 | store — `CloseDate` blank except for closed ones |
| `DimDate` | — | **2023-01-01 to 2024-12-31**, one row per day |
| `DimCurrency` · `DimCurrencyExchange` | — | currency and exchange rate |

The figures in bold are the ones the notes' footers cite, and
[`check_lab.py`](../check_lab.py) checks them before running any query: if the model stops being
the one they describe, there is no point continuing.

## The report's ten pages

Six exist because a trap from the field notes **cannot be shown in text** — it only lives inside
a visual. The other four, added later, show live what each of the skills that existed when they
were built contributed, one by one, to a real scenario (the 3-month moving average measured in
[`dax-reference/notes/window.md`](../../skills/dax-reference/notes/window.md)). Both groups share
the same visual language: a note textbox on top, a real data visual underneath, against measures
persisted in `_Measures.tmdl` — never against a loose query.

### The first six: traps that only live in a visual

Each page name links to a screenshot of it, so the trap can be read here without opening
Power BI. The screenshot is not a test: it is what the page looked like on the day it was
captured, and only the `.pbip` proves it still looks that way.

| page | what you see, and cannot be told |
|---|---|
| [ALLSELECTED - respeta el slicer, ignora el interno](../screenshots/contoso-allselected-slicer.webp) | Select 2-3 brands: one column changes and the other does not move. A DAX query has no slicer |
| [SELECTEDVALUE - la tarjeta que no distingue dos casos](../screenshots/contoso-selectedvalue-tarjeta.webp) | With no selection and with two brands the card says the same thing. It does not distinguish "did not choose" from "chose several" |
| [RANKX - 1 en todas las filas de la matriz](../screenshots/contoso-rankx-matriz.webp) | The middle column is 1 on all 58 rows, because the matrix already brought a single brand into context |
| [SUMX - el Total que no cuadra con sus filas](../screenshots/contoso-sumx-total.webp) | The first column's Total is not the sum of the column. It is evaluated again, without the row filters |
| [El blanco borra la categoria; el cero la dibuja](../screenshots/contoso-blanco-desaparece.webp) | Two charts with the same division: the left one is missing fourteen bars |
| [FORMAT - el 9 va despues del 10](../screenshots/contoso-format-ordena-mal.webp) | The same figure as a number and as a string. It sorts the second one by sales |

Open them with the `.pbip`. **No test checks the drawing**, and the first two also need you to
move the slicer with the mouse.

### The other four: what each skill contributed

| page | what it shows |
|---|---|
| [dax-lib - ya existe, pero solo el indice](../screenshots/contoso-dax-lib-indice.webp) | `TimeSeries.MovingAverage` is already published on daxlib.org; the index says what exists, it does not bring the code |
| [dax-reference - MOVINGAVERAGE no aplica aqui](../screenshots/contoso-dax-reference-appliesto.webp) | Native `MOVINGAVERAGE` is `appliesTo: [visual-calculation]` only; a matrix without a filter proves the `WINDOW` alternative does work as a measure |
| [dax-window-functions - la trampa medida, en vivo](../screenshots/contoso-dax-window-media-movil.webp) | Pin the `Year` slicer to 2024: `Media 3M (rota)` separates from `Media 3M (corregida)` around January-February, with no visible error. The interactive demonstration of `window.md`'s finding |
| [dax-udf-authoring - reutilizable, no un one-off](../screenshots/contoso-dax-udf-reutilizable.webp) | The two measures on the previous page are wrappers over a single persisted function (`Contoso.Lab.MediaMovil3M_Corregida`); this matrix calls it twice with a different `months` parameter |

`Contoso.Lab.MediaMovil3M` and `Contoso.Lab.MediaMovil3M_Corregida` live in
[`functions.tmdl`](./Contoso.SemanticModel/definition/functions.tmdl) — new with these four
pages, and they require `compatibilityLevel: 1702` (previously 1606), also new here.


## Where the data comes from

The same as the other three scenarios, and this was the first to do it:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="FactSales.parquet"]))
```

`DataBaseUrl` is a real M parameter pointing at
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) — a
**public** repository, **MIT** licence, **100% synthetic** data (not one real person, not one
real company). No authentication, no SQL Server, no local paths: it refreshes on anyone's
machine. To use a fork, a branch or a local mirror, you change that single value.

The Parquet files are **not copied into the repo**: they are ~2 MB and already live somewhere
public. What is versioned are the ~20 KB of TMDL.

## How it is used

1. Open `Contoso.pbip` in Power BI Desktop and **refresh** — opening a PBIP loads the model
   without data, you have to ask for it.
2. Run any note's query in the DAX query view, or let the runner run them all:

```bash
python lab/check_lab.py contoso localhost:<port>
```

That first checks the model is the one the notes declare, and then runs **the 39 queries**
published in the field notes, comparing them against
[`notes_expected.py`](../notes_expected.py).

The queries are **not copied** into the runner: it reads them from each note's own `.md`. If
someone edits a note's query and the result changes, it goes red. That is the point — a note
whose number no longer comes out of the engine is lying.

To regenerate the expected values after touching a note:

```bash
python lab/dump_notes.py localhost:<port> > lab/notes_expected.py
```

Whatever it prints has to be **looked at** against the table the note publishes before accepting
it: that script moves results into code, it does not decide whether they are the right ones.

## Two queries that fail on purpose

`removefilters` and `values` publish an **engine error** as their result, not a number:

| note | what the engine rejects |
|---|---|
| `removefilters` | `REMOVEFILTERS function cannot be used as a table expression` |
| `values` | `A table of multiple values was supplied where a single value was expected` |

The runner expects them. If one day the engine stopped rejecting them, both would be lying and
the scenario goes red — which is exactly what should happen.

## What was left out when it was brought over

The semantic model is **identical byte for byte** to the master it came from, with two deliberate
omissions:

- **`cultures/es-ES.tmdl`** — 400 KB of display-name translations. It was by far the largest file
  in the model and it changes no DAX result.
- **The master's report.** It carries personal and company brand images in `StaticResources`, and
  this repository is public. Here the report holds only the pages described above: the queries
  run against the model, not against the report.

## Limits, stated

- **The date table is not marked** as a date table. The time-intelligence notes (`DATESYTD`,
  `SAMEPERIODLASTYEAR`, `PREVIOUSMONTH`, `DATEADD`) were measured that way and reproduce that
  way. Marking it would change the model relative to the one that produced the numbers.
- **Refreshing needs internet.** If `raw.githubusercontent.com` is not reachable, this scenario
  cannot be run — nor can any other in the lab. It is the price of not putting the data in the
  repo, and all four pay it equally.
- **No performance figure comes from here.** At 126,524 rows everything resolves in milliseconds
  and any comparison would fall inside the noise; that is what [`rendimiento`](../rendimiento/)
  is for.
