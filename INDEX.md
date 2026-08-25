# Skills — index and routing

Five skills, one idea: **the DAX language**. No modeling, no visuals, no operations — there
are better repos for those, linked from the [README](README.md).

---

## Routing

```
A question about DAX
  ├─ what does this function do? which one do I use?  → dax-reference
  ├─ does a UDF for this already exist?               → dax-lib
  ├─ that UDF exists: install it                      → dax-lib-install
  ├─ I am going to write a UDF                        → dax-udf-authoring
  └─ rolling / running total / ranking                → dax-window-functions

Performance? → not here. Use data-goblin's plugin (see the README).
```

## Catalogue

| Skill | Use it when | Status |
|---|---|---|
| **`dax-reference`** | Language reference: what a function does, its signature, which context it applies in, whether it is discouraged, and the traps the docs leave out. **479 function cards + 34 conceptual pages** (evaluation context, query statements, operators, glossary, best practices) derived from `MicrosoftDocs/query-docs`, plus **31 field notes** measured against a real model. | ✅ |
| **`dax-lib`** | Index of the [daxlib.org](https://daxlib.org) catalogue: what exists, who wrote it, and where to get it. **Search it before writing a UDF.** It redistributes no package code. | ✅ |
| **`dax-lib-install`** | Actually brings in the code of a UDF `dax-lib` already found: installs it against the model, tests it with a real query, and leaves it attributed (author, licence, URL) inside the `FUNCTION` itself. | ✅ |
| **`dax-udf-authoring`** | The mechanics of a correct `FUNCTION`: parameter types, `VAL` vs `EXPR`, `TABLEOF`/`NAMEOF`, optional parameters, GA limits and parser bugs. | ✅ |
| **`dax-window-functions`** | `WINDOW` / `OFFSET` / `INDEX` / `RANK` / `ROWNUMBER` / `MOVINGAVERAGE` / `RUNNINGSUM`. ABS vs REL, `MATCHBY`, the default-relation gotcha. | ✅ |

## Conventions

Every skill follows the [agentskills.io](https://agentskills.io/specification) standard:

1. **One skill = one folder under `skills/`** with a `SKILL.md`. Supporting material in
   `scripts/`, `references/`, `evals/` inside that same folder.
2. **YAML frontmatter** with `name` (kebab-case, identical to the folder) and `description`
   (third person, starts with **"Use when …"**, describes *when* to reach for it).
3. **Token-efficient:** the `SKILL.md` is short; the heavy detail lives in separate files the
   agent reads only when a question needs them.
4. **Cross-link by name** (`` `dax-lib` ``), never by path.
5. **The `dax-` prefix stays**, even though the plugin is already called `dax` and `skills/`
   already supplies the context. Renaming to `skills/reference/` would touch the cross-links
   in the five `SKILL.md`, `evals/cases.yaml`, and any reference already installed elsewhere;
   the prefix costs four characters and does not pay for itself. Installed, they are
   `dax:dax-reference`, `dax:dax-lib`, `dax:dax-lib-install`, `dax:dax-udf-authoring` and
   `dax:dax-window-functions`.
6. **All five skills are listed by path in `.claude-plugin/plugin.json`.** Under `skills/` the
   default scan would find them anyway, so that list stopped being the difference between
   five skills and none — but it is still what makes the published set reviewable in a diff.
   CI checks it.
7. **The layout is [`microsoft/skills-for-fabric`](https://github.com/microsoft/skills-for-fabric)'s:**
   `skills/` as the single source, and the plugin manifest at the repo root. It is also what
   allows adding a second plugin later without duplicating a single skill.
8. **Everything written from here on is in English.** The reasoning, and the parts that stay
   in Spanish on purpose, are in
   [the decision record](docs/decisions/2026-08-25-english-as-the-repository-language.md).
