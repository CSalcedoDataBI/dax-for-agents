# Maintaining `dax-reference/generated/`

For maintainers. An agent answering a DAX question never needs this page; the skill
itself is [`../SKILL.md`](../SKILL.md).

## Regenerating

Clone the upstream docs, then point the sync at the DAX folder:

```bash
python scripts/sync_query_docs.py /path/to/query-docs/query-languages/dax --write
```

Without `--write` it only reports; nothing on disk is touched.

It parses the 15 category index files to build the function → category map, parses the 479
function files, then picks up every remaining page — anything that is neither a function nor a
category index — as a concept. Cross-links are rewritten to local paths and all three indexes
are stamped with the upstream commit SHA.

The concept rule is mechanical rather than a list of filenames, so a page Microsoft adds is
picked up on the next sync. If it lands in a docs directory the sync does not read, the run
says so instead of quietly leaving it out.

## What stops a bad generation

Four gates in the sync, all before anything is written, plus one check that runs on its own:

| Gate | Fails when |
|---|---|
| No category | A function gets none from the category indexes, the filename rules, `toc.yml`, or `overrides.json`. The exceptions are named in `overrides.json`, so a swap that keeps the total unchanged still fails — and a name left there after upstream classifies it fails too |
| Orphan note | A `notes/<fn>.md` has no card. The catalog would flag ★ and send a reader to a file that is not there |
| Unrouted work | The reverse, and the one that fails silently: a `notes/` or `examples/` file the cards and catalogue do not point at. Nothing is broken, the work simply cannot be found. **Not a sync gate:** checked separately by `refresh_local_metadata.py --check`, in CI |
| Broken cross-link | Any relative link in a card resolves to nothing |
| Count deviation | The function or concept count moved more than 5% since the last sync. Override with `--accept-count-change` for a real upstream release |

Plus a coverage floor of 90% as a coarse net against a total parser collapse.

The new tree is built in a scratch directory and only then swapped into place, so a failure
part-way leaves the previous `generated/` exactly as it was. `notes/` and `examples/` are read
to set the ★ and ▶ flags and the `examples:` count, and never written.

Those two flags are the only part of `generated/` that does not come from upstream, which
matters now that the upstream is gone and the tree is frozen (see
[the decision record](../../../../../docs/decisions/2026-08-27-generated-is-frozen-at-323524c.md)).
`scripts/refresh_local_metadata.py` rewrites exactly that half — the two frontmatter fields,
the block they point at, and the two indexes — plus the `returns` of any function named in
`overrides.json`, the only way a return type the parser misread can be corrected while the
sync cannot run. It touches no Microsoft prose. It imports its
placement and formatting from the sync, so the two writers cannot drift apart, and
`--check` runs it in CI as a gate.

A weekly CI job compares the upstream SHA against the stamped one. When it moves, the job
sparse-clones the DAX folder, regenerates through the four gates, runs the repo's own
checks, and opens a pull request — one branch, `sync/query-docs`, replaced on every run.

That pull request touches every file whether or not any DAX changed, because each card
names the commit it came from. So its body classifies the diff before anyone reads it:
the functions that actually changed, and the count that only moved their stamp. The first
real run was 516 files and **zero** substantive changes, which is one sentence to read
instead of a wall.

## `inject_example.py` — an example to open, without building a project

Not part of the sync. When a user asks for a `.pbip` example of something no lab page covers,
this adds the agent's measures and one page to the `lab/contoso` master and zips it. How and
when to use it is in the [`SKILL.md`](../SKILL.md#when-someone-asks-for-an-example-to-open);
`test_inject_example.py` checks the shape, offline. The numbers were checked once, by opening
the CALCULATE-vs-KEEPFILTERS result in Power BI Desktop on 2026-10-05.
