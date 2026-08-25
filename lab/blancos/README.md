# Blanks in a numeric column

## What it demonstrates

The average functions **skip blanks**: they divide by the rows that have a value, not by all of
them. That much is documented. What is not is how easy it is to break without noticing: it takes
only an expression that turns the blank into a zero — a `COALESCE` added "to be safe", or even a
`+ 0` — for the denominator to change and the average to drop.

Contoso cannot show this because no numeric column has blanks. That is why this note was not
written at first.

## The model

One table, five rows, two with blank square metres:

| TiendaKey | Nombre | Metros |
|---|---|---|
| 1 | Centro | 100 |
| 2 | Norte | 200 |
| 3 | Sur | 300 |
| 4 | Este | *(blank)* |
| 5 | Oeste | *(blank)* |

100 + 200 + 300 = 600. Over **3** that is 200; over **5** it is 120. The numbers are chosen so
you can tell at a glance which of the two denominators was used.

## 1. Who counts and who does not

```dax
EVALUATE
ROW(
  "filas",               COUNTROWS(Tiendas),
  "con_metros",          COUNT(Tiendas[Metros]),
  "en_blanco",           COUNTBLANK(Tiendas[Metros]),
  "SUM",                 SUM(Tiendas[Metros]),
  "AVERAGE",             AVERAGE(Tiendas[Metros]),
  "AVERAGEX",            AVERAGEX(Tiendas, Tiendas[Metros]),
  "SUM_entre_COUNTROWS", DIVIDE(SUM(Tiendas[Metros]), COUNTROWS(Tiendas))
)
```

| expression | result | denominator |
|---|---|---|
| `COUNTROWS(Tiendas)` | **5** | |
| `COUNT(Tiendas[Metros])` | **3** | |
| `COUNTBLANK(Tiendas[Metros])` | **2** | |
| `SUM(Tiendas[Metros])` | **600** | |
| `AVERAGE(Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** | 3 |
| `DIVIDE(SUM(...), COUNTROWS(...))` | **120** | 5 |

**`AVERAGE` and `AVERAGEX` give the same thing.** That contradicts the intuition that the
iterator "walks every row and therefore counts the empty ones": it does not, it skips the blank
exactly like `AVERAGE`. The one that departs is `SUM / COUNTROWS`, which divides by 5.

> This trap is also **drawn**: page «1. Quien cuenta y quien no» of the report
> ([screenshot](../screenshots/blancos-denominador.webp)). Open it with the `.pbip` and look, because that is
> where you see what the query result does not show.

## 2. How it breaks by accident

```dax
EVALUATE
ROW(
  "AVERAGE",               AVERAGE(Tiendas[Metros]),
  "AVERAGEX_columna",      AVERAGEX(Tiendas, Tiendas[Metros]),
  "AVERAGEX_con_COALESCE", AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0)),
  "AVERAGEX_con_mas_cero", AVERAGEX(Tiendas, Tiendas[Metros] + 0)
)
```

| expression | result |
|---|---|
| `AVERAGE(Tiendas[Metros])` | **200** |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** |
| `AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0))` | **120** |
| `AVERAGEX(Tiendas, Tiendas[Metros] + 0)` | **120** |

There is the trap. **`Tiendas[Metros] + 0` moves the average from 200 to 120.** The `+ 0`
changes no existing value: all it does is turn the blank into a zero, and with that the blank
starts counting in the denominator.

The `COALESCE` is worse because it looks deliberate and defensive. Whoever writes it believes
they are preventing an error; what they are doing is changing the definition of the metric.

Neither result is wrong — they depend on whether "no data" means "not applicable" or "zero".
What is wrong is that the difference is hidden inside a `+ 0`.

> This trap is also **drawn**: page «2. El + 0 que mueve el denominador» of the report
> ([screenshot](../screenshots/blancos-mas-cero.webp)). Open it with the `.pbip` and look, because that is
> where you see what the query result does not show.

## Where the data comes from

Those five rows are a **1 KB** Parquet file published in
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (public, MIT,
synthetic), which the model reads the same way as the other three scenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Tiendas.parquet"]))
```

There is one detail the source **has to** preserve, which is why not any source will do: the
blank travels as `null` inside the Parquet and Power Query hands it over as `null`, so the column
arrives in DAX blank and not as zero. If the source turned the gap into a zero, the scenario
would stop demonstrating anything — `AVERAGE` would give 120 and there would be no difference to
show.

They are regenerated with [`build_datasets.py`](../build_datasets.py), which writes them out one
by one.

## How to reproduce it

1. Open `Blancos.pbip` in Power BI Desktop.
2. **Refresh** — opening a PBIP loads the model without data, you have to ask for it. It needs
   internet; there are no credentials to give.
3. Paste the queries into the DAX query view, or let the runner execute them:

```bash
python lab/check_lab.py blancos localhost:<port>
```

Measured on 2026-08-12 with the two queries above, exactly as written.
