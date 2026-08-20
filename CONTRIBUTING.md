# Contributing

## This repository is private and stays private

**Nobody makes this repository public, publishes it, or ships it to any registry or
marketplace without the owner asking for it in that instruction.** Not a contributor, not an
automated run, not a "the checklist looked complete" judgement call.

The repo is assembled partly from a private repo of client work, so going public is a
one-way door: once a commit is visible it is visible, and the git history goes with it. The
owner reviews first and decides.

This is not a soft preference. `publish` is in the autonomous runs' irreversible list, so the
tool layer refuses it; this line is here so the intent is written down where a human reads it
too.

## The one rule that matters

**Everything under `dax-reference/generated/` is generated. Never edit it by hand.** Your
change would be silently erased by the next sync, which replaces that whole directory in one
move. Everything beside it — `SKILL.md`, `NOTICE`, `overrides.json`, `notes/` — is yours to
edit and the sync never touches it. CI fails if anything generated turns up outside
`generated/`, because a copy there is never refreshed again.

If a generated card is wrong, the fix is one of:

- **Wrong upstream** → fix it in
  [`MicrosoftDocs/query-docs`](https://github.com/MicrosoftDocs/query-docs) and let the weekly
  sync pick it up.
- **Wrong parse** → fix `dax-reference/scripts/sync_query_docs.py`.
- **Right but incomplete** → that is what `dax-reference/notes/` is for. Write a note.

## Writing a note

Notes are the reason this repo exists. They hold what Microsoft's docs do not say: the trap,
the "you meant the other function", the performance cost.

Create `dax-reference/notes/<function>.md` (lowercase, matching the card filename). Use the
headings that apply — skip the ones that don't:

```markdown
## Trampa: <nombre corto>
Qué falla, cuándo, y cuál es el síntoma observable.

## No confundir con
La función que probablemente querías, y cómo saber cuál es cuál.

## Coste
Qué le pasa al rendimiento y bajo qué volumen.
```

Rules:

- **Only write a note when you have something the docs don't say.** A note that paraphrases the
  official description is noise and makes the ★ flag meaningless.
- **Show it, don't claim it.** The 30 notes already here each carry the query that
  demonstrates the trap and the number it returned, measured against a real model. A note
  is the one place in this repo where the content is an assertion rather than derived from
  a source — so it has to bring its own evidence. If you cannot reproduce the behaviour,
  do not write the note.
- Be concrete. "Puede ser lento" is useless; "1M de transiciones de contexto en un iterador
  sobre 1M de filas" is a note.
- A note without its matching `generated/library/<function>.md` **fails CI** — check the spelling.
- Notes attach to **functions**, not to concepts. A conceptual page is Microsoft's prose;
  if you have field knowledge about `EVALUATE`, it belongs in a note on the function it
  bites on, where the ★ flag will actually surface it.

## Skills

Each skill is one top-level folder with a `SKILL.md`. Frontmatter needs:

- `name` — kebab-case, **identical to the folder name**.
- `description` — third person, **starts with "Use when …"**, describes *when* to reach for it
  (symptoms and triggers), not what it does.

Keep the `dax-` prefix even though the plugin is already called `dax`: the repo has to work as
flat skills too, where a bare `reference/` folder explains nothing.

Add the skill to [INDEX.md](INDEX.md), list its path in the `skills` array of
[`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), and give it at least one
routing case in `evals/cases.yaml`, or CI fails.

The manifest list is not optional bookkeeping. Because the skills sit flat at the repo
root instead of under `skills/`, that array *is* the plugin: a folder left out of it
ships invisible, and Claude Code says nothing — when none of the listed paths resolve it
quietly scans `skills/`, which does not exist here, and the plugin installs with zero
skills. `scripts/check_plugin_manifest.py` is what turns that silence into a red build.

## Scope

This repo is **the DAX language**. Not modeling, not visuals, not Fabric operations, not
performance tuning. Those are covered better elsewhere and the README links to them.

A pull request that widens the scope will be declined, however good it is. The one-sentence
identity is the asset.

## Licensing

Contributions are MIT. Do **not** paste content from GPL-licensed sources — notably
[data-goblin/power-bi-agentic-development](https://github.com/data-goblin/power-bi-agentic-development),
which is GPL-3.0. Link to it instead.

Content derived from `query-docs` is CC BY 4.0 and confined to the generated folders covered by
[`dax-reference/NOTICE`](dax-reference/NOTICE). Keep it that way.

## Commits

Conventional Commits, in English. `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
Release notes and versioning are handled by release-please — do not edit `CHANGELOG.md` by hand.
