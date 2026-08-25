# Contributing

## This repository is public, and that is one-way

This repo is public and stands on its own: what is here is the whole thing, and it is the
source of truth for itself. It is not assembled from anywhere else and does not sync from
anywhere else.

Being public is a one-way door, which is why it is worth saying out loud rather than
assuming everyone remembers. **A commit that is visible stays visible**, and the git history
goes with it — a file deleted three months ago is one `git log -p` away, and the services
that index GitHub read all of it. So nothing private goes in: no client name, no model from
a real engagement, no credential, not even in a commit that "will be fixed in the next one".

Two gates hold the line, and they are not optional:

```bash
python scripts/check_no_credentials.py            # el arbol de trabajo. Corre en cada PR
python scripts/check_no_credentials.py --history  # + todos los blobs alcanzables
```

The short mode is the cheap one and guards the daily work. The long one walks every object
any reference can reach; run it after any history rewrite. The lab scenarios under `lab/`
are **synthetic on purpose** — generated data, Microsoft's fictional "Contoso" — so that a
claim about DAX can be reproduced without anyone's real numbers.

## The one rule that matters

**Everything under `skills/dax-reference/generated/` is generated. Never edit it by hand.** Your
change would be silently erased by the next sync, which replaces that whole directory in one
move. Everything beside it — `SKILL.md`, `NOTICE`, `overrides.json`, `notes/` — is yours to
edit and the sync never touches it. CI fails if anything generated turns up outside
`generated/`, because a copy there is never refreshed again.

If a generated card is wrong, the fix is one of:

- **Wrong upstream** → fix it in
  [`MicrosoftDocs/query-docs`](https://github.com/MicrosoftDocs/query-docs) and let the weekly
  sync pick it up.
- **Wrong parse** → fix `skills/dax-reference/scripts/sync_query_docs.py`.
- **Right but incomplete** → that is what `skills/dax-reference/notes/` is for. Write a note.

## Writing a note

Notes are the reason this repo exists. They hold what Microsoft's docs do not say: the trap,
the "you meant the other function", the performance cost.

Create `skills/dax-reference/notes/<function>.md` (lowercase, matching the card filename). Use the
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
- **Show it, don't claim it.** The 31 notes already here each carry the query that
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

Each skill is one folder under `skills/` with a `SKILL.md`. Frontmatter needs:

- `name` — kebab-case, **identical to the folder name**.
- `description` — third person, **starts with "Use when …"**, describes *when* to reach for it
  (symptoms and triggers), not what it does.

Keep the `dax-` prefix even though the plugin is already called `dax` and `skills/` already
supplies the context. Renaming to `skills/reference/` would touch the cross-links in all
five `SKILL.md`, `evals/cases.yaml`, and any reference already installed elsewhere. Four
characters do not buy that.

Add the skill to [INDEX.md](INDEX.md), list its path in the `skills` array of
[`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), and give it at least one
routing case in `evals/cases.yaml`, or CI fails.

The manifest list is not optional bookkeeping, but be precise about what it protects
today. Under `skills/` the default scan would find the folders on its own, so a path left
out of the array no longer ships an invisible skill the way it did when they sat flat at
the repo root. What the array still buys is a reviewable diff: the set that gets published
is written down in one place instead of inferred from a directory listing.
`scripts/check_plugin_manifest.py` keeps the manifest and the tree in step, and the README
explains the Claude Code version floor that comes with this layout.

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
[`skills/dax-reference/NOTICE`](skills/dax-reference/NOTICE). Keep it that way.

## Commits

Conventional Commits, in English. `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
Release notes and versioning are handled by release-please — do not edit `CHANGELOG.md` by hand.
