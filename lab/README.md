# lab — evidence you can run

The field notes in [`dax-reference/notes/`](../skills/dax-reference/notes/) each carry the query
that demonstrates the trap and the number it returned. This directory is the other half of that
promise: **the models to run them against**.

> The prose here is English; the model, column and page names are not. They are the strings you
> will see on screen and the ones `check_lab.py` compares literally — see
> [the language decision](../docs/decisions/2026-08-25-english-as-the-repository-language.md).

## Why it exists

For two different reasons, and it is worth not mixing them.

**The first: the base model.** Thirty of the thirty-one notes were measured against Contoso
Retail, and that model lived on one machine. The reader had the query and the number, and no way
to run either. Now it is here: [`contoso`](./contoso/).

**The second: what Contoso cannot show.** While writing the first notes, three were not written
because the base model could not demonstrate them — and a note you cannot demonstrate does not
get written:

| Could not be demonstrated | Why | Scenario that solves it |
|---|---|---|
| The blank row of a relationship with orphan keys | Contoso's referential integrity is intact | [`claves-huerfanas`](./claves-huerfanas/) |
| `AVERAGE` vs `AVERAGEX` with blanks | No numeric column has blanks | [`blancos`](./blancos/) |
| Any performance figure | 126,524 rows resolve in milliseconds | [`rendimiento`](./rendimiento/) |

All three have their scenario now. The performance one also **disproved** what it set out to
find: it was built to show that `FILTER` over a whole table is expensive, and it turned out not
to be. What costs is the context transition. The numbers are in its
[README](./rendimiento/README.md).

## What the models look like

**All four connect the same way.** What is versioned here are `.pbip` files of a few kilobytes;
the rows live outside, in Parquet published in
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) — a
**public** repo, **MIT** licence, **100% synthetic** data. Each model reads them over
`raw.githubusercontent.com`:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

`DataBaseUrl` is a **real M parameter** (`IsParameterQuery`), so every partition stays clear of
the privacy firewall, and pointing at a fork, a branch or a local mirror is one value to change.

| scenario | published folder | size | rows |
|---|---|---|---|
| [`blancos`](./blancos/) | `dax-lab/blancos` | 1 KB | 5 |
| [`claves-huerfanas`](./claves-huerfanas/) | `dax-lab/claves-huerfanas` | 2 KB | 3 + 4 |
| [`rendimiento`](./rendimiento/) | `dax-lab/rendimiento` | 385 KB | 2,000,000 |
| [`contoso`](./contoso/) | `contoso-retail` | 2.2 MB | 126,524 + dimensions |

That the pattern is identical across all four is not cosmetic. **What this repo publishes are
the `.pbip` files**, and a `.pbip` is only worth anything if it refreshes on the machine of
whoever downloads it: no authentication, no SQL Server, no local paths, no credentials to ask
for. One source per scenario would be one source to fix per scenario.

**The price is that all four need internet to refresh.** If `raw.githubusercontent.com` is not
reachable, there is no data. That is accepted in exchange for the repo not carrying the
megabytes and for there being nothing to configure.

The data is still readable without opening Power BI: the two behaviour scenarios are five and
seven hand-picked rows, and they are written out row by row in each README. Living in a Parquet
file rather than in the TMDL does not hide them — it publishes them.

## How to use them

1. Open the scenario's `.pbip` in Power BI Desktop and **refresh**. Opening a PBIP loads the
   model without data: you have to ask for it. There is nothing to configure; the first time,
   Power BI asks for the web source's privacy level and **Anonymous/Public** is enough.
2. Run the queries from that scenario's `README.md` in the DAX query view.
3. Compare against the published results table.

In `contoso`, step 2 means the queries from the **field notes**, which live in
[`dax-reference/notes/`](../skills/dax-reference/notes/) and are not repeated in its README.

Each scenario's `.gitignore` excludes `.pbi/`, the local Power BI Desktop cache (a few megabytes
of binary per model). Only text is versioned.

## The reports, and the limit of what gets checked

The four scenarios carry **thirteen pages**, one per trap, and they exist for the traps that
**only live inside a visual**: the blank that erases a bar while the zero draws it, the unnamed
category of a broken relationship, `ALLSELECTED` changing depending on whether the filter came
from a slicer, `RANKX` returning 1 on every row of a matrix. A README can talk about those; it
cannot show them.

What is checked automatically: **the measures**. Every one of the twenty-three that feed the
pages is in [`check_lab.py`](./check_lab.py) with its expected value, so if a number changes it
goes red.

What is **not** checked automatically: **the drawing**. No test knows whether the bar was
painted. That is verified by opening the `.pbip`, and on the two pages with a slicer you also
have to move the slicer — a DAX query has no slicer, which is exactly why those pages exist.

Those thirteen are the **visual-only trap** pages. `contoso` carries four more, of a different
kind: one per skill in the library, showing what each contributed to the real scenario in
[`window.md`](../skills/dax-reference/notes/window.md). See
[`lab/contoso/README.md`](./contoso/README.md#the-other-four-what-each-skill-contributed).

And this is not a theoretical precaution. While building them, looking at the drawing found
three things no query would have found: a chart that came out **empty** because a column in the
values well was missing its `Aggregation` wrapper, a table that stopped at the header because of
one `"active": true` too many, and two pages whose design assumed a contrast the data did not
have. All three open the report **without a single error**.


## Structure

```
lab/
  check_lab.py              runs and compares — the runner
  notes_expected.py         what each note's query returns against contoso
  dump_notes.py             regenerates notes_expected.py against an open model
  build_datasets.py         produces the Parquet for the three synthetic scenarios
  <scenario>/
    README.md               what it demonstrates, the queries, and the measured results
    <Name>.pbip             the project you open
    <Name>.SemanticModel/   TMDL: tables, relationships and expressions.tmdl (DataBaseUrl)
    <Name>.Report/          the report
    .gitignore              excludes .pbi/
```

[`build_datasets.py`](./build_datasets.py) is what produces the Parquet for `blancos`,
`claves-huerfanas` and `rendimiento`. It exists so the published files are not an opaque binary:
anyone who doubts that the Parquet says what the README says regenerates it and compares. The
generation is **deterministic** — no randomness and no dates — so two runs give the same thing.

```bash
python lab/build_datasets.py <destination-directory>
```

It writes files and nothing else; publishing the destination is a separate, manual step.

A `.pbip` declares **report** artifacts, and it is the report that links to the model through
`definition.pbir`. A `.pbip` pointing straight at the `SemanticModel` opens Power BI Desktop in a
state with no tables — verified while building the first scenario.

## Checking without opening anything by hand

[`check_lab.py`](./check_lab.py) runs each scenario's queries and compares them against the
published result. If a number changes, it fails.

```bash
python lab/check_lab.py claves-huerfanas localhost:<port>
```

With no port, it finds the local Power BI Desktop instances that **are listening** and lists them
with the command already assembled.

`contoso` does one more thing: it runs **the 39 queries published in the field notes** and
compares them against [`notes_expected.py`](./notes_expected.py). The queries are not copied
there — it reads them from each note's own `.md`, so editing a note changes what runs. That is
what turns a note from "an assertion with cited evidence" into a test.

```bash
python lab/check_lab.py contoso localhost:<port>
```

It needs `pyadomd` **and** the ADOMD.NET provider, which does not come from pip: Power BI Desktop
and SSMS install it. The runner looks for it in the GAC on its own; if it is missing, it says so
by name.

**It does not run in CI**, and that is deliberate: it needs a tabular engine with the data
loaded, and CI has no Power BI Desktop. It is a local tool for when a scenario is touched or a
note is under suspicion.

### Validating the project structure

That the model loads on your machine does not prove the `.pbip` is valid. If you have
[`pbir-cli`](https://github.com/pbir-cli/pbir-cli):

```bash
pbir validate "lab/claves-huerfanas/ClavesHuerfanas.Report"
```

All four scenarios pass as **Valid**. It was worth checking: the first version loaded and
refreshed perfectly in Power BI Desktop and still had **two schema errors** (`themeCollection`
missing from `report.json`, `$schema` missing from `definition.pbism`). Tolerated today is not
the same as correct tomorrow.
