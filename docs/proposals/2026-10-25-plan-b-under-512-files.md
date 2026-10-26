# Plan B: get the shipped plugin under 512 files

**Status:** proposal, nothing executed. **Date:** 2026-10-25. **Source of every number:**
`python -X utf8 scripts/simulate_plan_b.py` (read-only, stdlib; output pasted at the end).

The plugin directory holds a plugin with more than 512 files for a reviewer. The listing's
plugin path is the repo root, so every tracked file ships: **1,056**. PR #26
(`refactor/plugin-subfolder`) moves the plugin to `plugins/dax-for-agents/` and still ships
**673** (that branch predates `dax-feedback`; rebased on main it is **674**). Either way the
479 one-file-per-function cards have to be bundled. Packaging tricks are out:
`measure_plugin.py` counts `git ls-files` and flags `export-ignore`.

## Before / after

| scenario | files shipped | margin |
|---|---|---|
| now: root = plugin path | 1,056 | −544 |
| **B-sub** (PR #26 merges), bundle `library/` + `concepts/` | **180** | 332 |
| B-root step 1: bundle `library/` + `concepts/` only | 562 | −50 |
| B-root step 2: + move `docs/examples-es/` to a tag | 462 | 50 |
| **B-root step 3**: + bundle `examples/` | **367** | 145 |
| B-root step 4: + bundle `notes/` (not proposed) | 337 | 175 |
| B-root, move every dev folder out instead (rejected) | 193 | 319 |

## What runs and what does not

What an installed plugin reads or runs, worked out from the six `SKILL.md` files and the one
script they tell the agent to run (`inject_example.py`):

- **runtime (661):** `.claude-plugin/` 3 (loader; `dax-feedback` reads the version),
  6 `SKILL.md`, 2 `NOTICE`, `dax-lib/catalog.{md,json}` + `refresh-daxlib.ps1`,
  `generated/` 516 (catalog.md, concepts.md, catalog.json, 479 cards, 34 concepts),
  `notes/` 31 (★), `examples/<category>/` 99 (▶), `scripts/inject_example.py`.
- **keep on main, never read by an agent (15):** LICENSE, README, PRIVACY (the manifest's
  `privacyPolicyUrl` is `blob/main/PRIVACY.md`), CHANGELOG + the two release-please files,
  `.gitattributes`, `.gitignore`, `.github/` 7.
- **dev only (380):** `lab/` 203, `docs/` 114 (100 of them `docs/examples-es/`), `scripts/` 30,
  `evals/` 16, inside `skills/` 11 (sync/fetch/refresh tooling, its README, 4 `test_*.py`,
  `overrides.json`, `examples/README.md`), plus CLAUDE.md, CONTRIBUTING.md, FICHA.md, INDEX.md,
  `.agentic-board/config.json`, `.claude/agents/experto.md`.

Runtime links that point *outside* `skills/` and will not resolve in B-sub (PR #26 has to
handle them anyway): `dax-reference` → `lab/README.md`, `docs/design.md`;
`dax-udf-authoring` → `lab/blancos/README.md`. `inject_example.py` takes `lab/contoso` if it
is on disk, otherwise downloads `lab-contoso.zip` from the latest release. **The release zips
are a runtime dependency.** `lab-assets.yml` builds them with `git archive HEAD:lab/<name>`,
so `lab/` has to stay on main.

## Bundling design (`generated/library/` + `generated/concepts/`)

**Constraint that shapes it:** the sync cannot run. Upstream returns 404 and every surviving
copy is older than `@323524c` (decision of 2026-08-27). So bundling is a **re-layout of the
tree as it is**, not a regeneration, and it has to be provably lossless.

- **Grouping:** by `catalog.json` `primaryCategory`, 16 empty → `uncategorized`; any group
  over 230 KiB (90 % of 256 KiB) splits, in alphabetical order and by bytes, into even parts that each stay under 230 KiB. That gives **17 function bundles**
  (`info` splits in two, largest `functions-financial` 177.6 KiB) + **2 concept bundles**
  (one would be 241 KiB, too close). Alphabetical packing gives 7 files but the largest is at
  230 KiB, with no headroom. Category wins: it matches the catalog's `Cat` column, and a wrong
  guess still lands in related functions.
- **Location:** a new `generated/bundles/` (`functions-<category>.md`, `concepts-N.md`).
  It is a new directory on purpose: a stale `library/filter.md` path then fails loudly
  instead of opening the whole *filter category* in place of the FILTER card.
- **Format:** each card is copied **verbatim** between `<a id="<slug>"></a>` +
  `<!-- card: <slug> -->` and `<!-- /card -->`. The only edit is a card-to-card link,
  `./abs.md` → `./functions-math-and-trig.md#abs` (1,232 such links: 1,118 `./x.md` +
  114 `../library/x.md`; the 99 `../../examples/…` links are untouched), which reverses on
  split. A section anchor (one link, `./if.md#examples`) rides along as the link title
  (`"section:examples"`), since every card in a bundle has its own Examples heading. Six cards
  have no final newline; their marker says `no-final-newline`, so the split drops exactly the
  newline the bundle added. **Simulated round trip, compared byte for byte: 0 of 513 cards
  differ.**
- **Catalog pointer:** `catalog.md` gets a `Card` column holding `bundle:first-last`
  (CALCULATE → `functions-filter:587-757`). The agent does `Read offset=587 limit=171`, the
  same one hop as today. Cost: +15,661 chars (~3.9k tokens) on a 72.5 KB catalog. The longest
  card is 374 lines. `concepts.md` gets the same pointer. Fallback documented in SKILL.md:
  `Grep "card: <slug>"` in `generated/bundles/`. A bundle is never read whole (the largest is
  5,093 lines).

**What changes**

- **`dax-reference/SKILL.md`:** step 2 (open via the `Card` column with offset/limit, never
  a whole bundle), the concepts path, and the Layout table. Steps 3–4 change only in B-root
  (examples). **`dax-feedback/SKILL.md`:** "give its path" becomes bundle + slug.
- **Generator output contract:** a new module `skills/dax-reference/scripts/bundle_cards.py`
  with `bundle(trees) -> files` and `split(files) -> trees`, where `trees` is the
  `{stem: markdown}` dict that `sync_query_docs.py` already builds per subdirectory. Wiring:
  - `write_library` calls `bundle()` before its atomic swap, so the weekly `sync-check`
    (which only writes if upstream ever returns) emits bundles too.
  - `refresh_local_metadata.py` does split → edit → bundle, and recomputes the pointers
    because line numbers move whenever a card changes.
  - `bundle_cards.py --check` (a gate in `check_all.py` and `validate-skills.yml`) proves
    split∘bundle is identity, and that every catalog pointer's first line is its anchor.
- **Validators read through `split()`:** `validate_skills.py` (catalog ↔ cards ↔ notes;
  add `library`/`concepts` to its stale-directory list), `check_doc_claims.py`,
  `check_function_names.py`, `summarize_sync_diff.py`.
- **Tests that break:** 106 tests build or read per-card paths —
  `test_sync_query_docs` 68/247, `test_summarize_sync_diff` 17/28,
  `test_refresh_local_metadata` 14/21, `test_check_doc_claims` 3/56,
  `test_fetch_from_learn` 3/43, `test_check_function_names` 1/8. Most are fixed by a fixture
  that writes `trees` through `bundle()`. New tests: round trip, split boundaries, link
  reversal, the pointer check.
- **Decision record:** an addendum to the 2026-08-27 freeze. The content stays at `@323524c`
  and untouched; only the file layout changes. That is proven by the round trip, not
  asserted.

**Effort (B-sub):** module + tests 0.5 d, sync/refresh wiring 0.5 d, validators 0.5 d,
fixing the 106 tests 1 d, SKILL.md/catalog/decision/migration commit 0.5 d → **≈ 3 days**.

## B-root (Anthropic never answers): bundle + move only what is inert

1. **Move `docs/examples-es/` (100) to the tag `archive/examples-es-2026-08-25`.** It is a
   frozen copy, nothing runs it, and `check_doc_claims.py` only lists it in a skip list.
   Breaks: the link in `docs/decisions/2026-08-25-english-as-the-repository-language.md`
   → repoint it to the tag's tree URL, and drop the skip entry. Reversible with
   `git checkout archive/examples-es-2026-08-25 -- docs/examples-es`. A tag beats an orphan
   `dev-assets` branch here: the snapshot is immutable, gets no CI runs, and cannot drift.
2. **Bundle `examples/` per category** (4 files, largest 100.9 KiB; `README.md` stays).
   `scripts/examples_io.py` is already "the only definition of that format", shared by
   `check_examples.py`, `lab/check_lab.py` and `lab/dump_examples.py`. It learns to read and
   write sections. Also touched: `render_readme_assets.py`, `check_doc_claims.py`, and the
   card's runnable-examples link, which `refresh_local_metadata` owns
   (`../../examples/<cat>.md#<fn>`, 99 cards). Risk: `dump_examples` writes engine results
   back, and that path only runs against a live engine. It needs a fixture test before the
   migration. **+1–1.5 d.**
3. `notes/` stays one file per note. It is hand-written, diffed by humans and read by 12
   scripts (evals, lab, gates). Bundling it saves only 30 files.

Result **367 files** (margin 145, under the ≤ 400 target), with `lab/`, `scripts/`,
`evals/`, `docs/` and CI all still on main, so the repo stays developable in one checkout.

**Rejected: moving every dev folder to `dev-assets` or a sibling repo (193).** It breaks:
- `lab-assets.yml`, which archives `HEAD:lab/<name>` into the release zips that SKILL.md and
  `inject_example.py` download, so runtime breaks;
- `validate-skills.yml` (runs `scripts/check_*.py`) and `evals.yml`;
- `check_examples.py`, which reads the lab models;
- `check_all.py`;
- README links to `docs/decisions/…` (3) and `evals/hallucination/runs`;
- the SKILL.md links above.

Each one can be fixed with a cross-repo checkout, but every gate change becomes two PRs in
lockstep. It buys 174 more files than needed.

## Execution order

1. Land `bundle_cards.py` + `--check` + tests (no layout change yet; the gate passes
   trivially).
2. Route the validators and `refresh_local_metadata` through `split()`, and fix the 106
   tests.
3. Migration commit: bundle `generated/`, add the `Card` column, update the two SKILL.md
   files and the decision addendum. Check: `check_all.py` green,
   `measure_plugin.py plugins/dax-for-agents` (B-sub) → 180.
4. *(B-root only)* Tag and remove `docs/examples-es/`, fix the one link → 462.
5. *(B-root only)* Teach `examples_io` the sections, add the fixture test for `dump_examples`,
   bundle `examples/` → `measure_plugin.py .` → 367.
6. Re-run the evals (`evals/run_evals.py --model`) to confirm the agent still finds a card in
   one hop through offset/limit.

Every step is a normal PR on main. Reverting the migration commit restores the per-card
tree (the round trip guarantees it is byte-identical).

## Recommendation

Do **steps 1–3 now**. They are needed in both futures and take B-sub to **180**. Hold steps
4–5 (B-root, **367**) until it is clear PR #26 will not be accepted: they cost ~1.5 days
more and touch the lab tooling. Do not move `lab/`, `scripts/` or `evals/` off main.
**Main risk:** the agent reading a whole bundle (up to 178 KiB ≈ 45k tokens) instead of the
offset/limit slice. Mitigate it with the pointer column, the warning header inside each
bundle, and an eval case that checks the read stays under ~400 lines.

## Simulator output

<details><summary><code>python -X utf8 scripts/simulate_plan_b.py</code> (2026-10-25, main @ cfbf703)</summary>

```text
## 1. Tracked files at the repo root (all ship today): 1058

| folder         | files | runtime | keep (listing/CI/release) | dev only |
|----------------|-------|---------|---------------------------|----------|
| (root files)   | 12    | 0       | 8                         | 4        |
| .agentic-board | 1     | 0       | 0                         | 1        |
| .claude        | 1     | 0       | 0                         | 1        |
| .claude-plugin | 3     | 3       | 0                         | 0        |
| .github        | 7     | 0       | 7                         | 0        |
| docs           | 115   | 0       | 0                         | 115      |
| evals          | 16    | 0       | 0                         | 16       |
| lab            | 203   | 0       | 0                         | 203      |
| scripts        | 31    | 0       | 0                         | 31       |
| skills         | 669   | 658     | 0                         | 11       |
| TOTAL          | 1058  | 661     | 15                        | 382      |

## 2. Inside skills/, by rule

| class   | files | rule                                                   |
|---------|-------|--------------------------------------------------------|
| dev     | 5     | sync/fetch/refresh tooling + its README (maintainer)   |
| dev     | 4     | unit tests                                             |
| dev     | 1     | index for humans; no SKILL.md points at it             |
| dev     | 1     | generator input                                        |
| runtime | 516   | catalog.md, concepts.md, cards (catalog.json: scripts) |
| runtime | 99    | read when the catalog row is flagged ▶                 |
| runtime | 31    | read when the catalog row is flagged ★                 |
| runtime | 6     | skill entry point                                      |
| runtime | 2     | attribution, linked from SKILL.md (CC BY 4.0)          |
| runtime | 2     | dax-lib SKILL.md reads catalog.md/json                 |
| runtime | 1     | named by dax-lib + dax-lib-install                     |
| runtime | 1     | the agent runs it (SKILL.md)                           |

## 3. Bundles (in memory; target 230 KiB = 90% of 256 KiB)

| bundle set           | files | cards | largest KiB | <= 256 KiB |
|----------------------|-------|-------|-------------|------------|
| library_by_category  | 17    | 479   | 177.6       | OK         |
| library_alphabetical | 7     | 479   | 230.1       | OK         |
| concepts             | 2     | 34    | 124.2       | OK         |
| examples             | 4     | 99    | 100.9       | OK         |
| notes                | 1     | 31    | 77.1        | OK         |

| generated/bundles/<file>.md  | cards | KiB   | lines |
|------------------------------|-------|-------|-------|
| concepts-1                   | 14    | 124.2 | 1797  |
| concepts-2                   | 20    | 123.7 | 2449  |
| functions-aggregation        | 22    | 49.2  | 1519  |
| functions-date-and-time      | 24    | 63.3  | 1694  |
| functions-filter             | 35    | 166.5 | 3435  |
| functions-financial          | 51    | 177.6 | 5093  |
| functions-info-1             | 39    | 145.6 | 4424  |
| functions-info-2             | 33    | 143.0 | 4112  |
| functions-information        | 43    | 93.7  | 2993  |
| functions-logical            | 15    | 40.0  | 1269  |
| functions-math-and-trig      | 49    | 95.7  | 3293  |
| functions-other              | 6     | 17.4  | 536   |
| functions-parent-and-child   | 5     | 12.7  | 311   |
| functions-relationship       | 4     | 18.0  | 344   |
| functions-statistical        | 44    | 94.6  | 2899  |
| functions-table-manipulation | 31    | 100.9 | 2651  |
| functions-text               | 21    | 73.4  | 1805  |
| functions-time-intelligence  | 41    | 136.4 | 3539  |
| functions-uncategorized      | 16    | 37.4  | 1033  |

round trip (split each bundle, compare with the card on disk): 0 card(s) differ
catalog pointer: CALCULATE -> `functions-filter:587-757`  (Read offset=587 limit=171)
catalog pointer: ABS -> `functions-math-and-trig:5-67`  (Read offset=5 limit=63)
extra catalog.md size of a 'bundle:first-last' column: 15661 chars (~3915 tokens); longest card 374 lines
card-to-card links rewritten on bundle, reversed on split: 1232 ('../library/x.md' 114, './x.md' 1118)
hand-written links that name a card path: 3 (docs 3)

## 4. Scenarios

| scenario                                         | files shipped | margin to 512 |
|--------------------------------------------------|---------------|---------------|
| NOW: root (main)                                 | 1058          | -546          |
| B-root 1: bundle library+concepts                | 564           | -52           |
| B-root 2: 1 + move docs/examples-es              | 464           | 48            |
| B-root 3: 2 + bundle examples  <- proposed       | 369           | 143           |
| B-root 4: 3 + bundle notes                       | 339           | 173           |
| B-root 5: 1 + move every dev folder (rejected)   | 193           | 319           |
| B-sub: origin/refactor/plugin-subfolder as it is | 673           | -161          |
| B-sub model: main's skills/ + 5 PR files         | 674           | -162          |
| B-sub 1: bundle library+concepts  <- proposed    | 180           | 332           |
| B-sub 2: + examples                              | 85            | 427           |
| B-sub 3: + examples + notes                      | 55            | 457           |

## 5. B-root moves

| glob               | files | destination                        | why                                                                      |
|--------------------|-------|------------------------------------|--------------------------------------------------------------------------|
| docs/examples-es/* | 100   | tag archive/examples-es-2026-08-25 | frozen Spanish snapshot; nothing runs it; check_doc_claims only skips it |

tracked files > 256 KiB today: 0
```

</details>
