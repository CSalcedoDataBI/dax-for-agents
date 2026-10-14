---
name: dax-feedback
description: "Use when this plugin proves wrong or incomplete while working in any project: a card or field note the engine contradicts, a wrong signature or appliesTo, an example that does not reproduce, a gap you had to measure or guess, or the user says \"report this to dax-for-agents\" / \"la ficha está mal\". Files one sanitized issue on its public repo, after showing it to the user."
---

# Report a finding back to dax-for-agents

The plugin is fixed in its own repository, never from the project you are in: not the
installed copy, not a local patch to a card. The way back is one issue on
`CSalcedoDataBI/dax-for-agents`, and the project carries on with its own workaround.

**That repository is public.** The issue is published the moment it is created and deleting
it does not unpublish it. Steps 3 and 5 are not optional.

## 1. Is it the plugin?

File only what is about the plugin's text or scripts: a card in `dax-reference`, a field
note, an example, a `dax-lib` index entry, a skill step that was wrong or missing. A bug in
the user's model, in Power BI or in another tool is not a finding for this repository.

## 2. Gather the evidence

- **The query that proves it**, standalone: `EVALUATE` with `DEFINE` and literals, so it runs
  on any model. A query that needs the user's tables is not evidence anyone else can rerun.
- **What the engine returned**, as a small table.
- **The engine:** Power BI Desktop version, or the service and its compatibility level.
- **What the plugin says**: the card or note path inside the plugin and the plugin version
  (`version` in its `.claude-plugin/plugin.json`).

No query because it is a gap or a wrong skill step? Say what you had to measure or guess.

## 3. Sanitize

Rewrite, do not redact with `***`:

- Tables, columns and measures become generic: `Sales[Amount]`, `'Date'[Date]`, `[Total]`.
- No project, client or company names, no real values, no file paths, server names, ports,
  process ids, emails, tenant or workspace ids.

Then search the body file with your Grep tool for what slips through: `[A-Za-z]:\\`,
`/Users/`, `/home/`, `localhost:\d+`, `@[\w-]+\.\w+`, GUIDs
(`[0-9a-f]{8}-[0-9a-f]{4}-`), and every table or project name you saw in this session.
Any hit: rewrite and search again.

## 4. Look for a duplicate

```bash
gh issue list -R CSalcedoDataBI/dax-for-agents --state all --search "<function or note name>"
```

An open issue on the same thing gets a comment with the new evidence, not a second issue.

## 5. Show it, then file it

Write the body to a temporary file with three sections — **What happens** (the claim, the
query, the result), **Why it matters** (what an agent would get wrong), **Done when** (a
checklist). Write it in the user's language; the maintainer reads English and Spanish.

Show the user the title and the full body, say it will be **public**, and wait for a yes.
Then, with the user's own GitHub CLI login:

```bash
gh issue create -R CSalcedoDataBI/dax-for-agents --title "<function>: <what is wrong, short>" --label <bug|documentation|enhancement> --body-file <file>
```

`bug` when a card or note is wrong, `documentation` when something is missing or unclear,
`enhancement` for a new capability. No `gh` or no login: give the user the title and body
and the link `https://github.com/CSalcedoDataBI/dax-for-agents/issues/new`.

## 6. Close

Give the user the issue link and the workaround the project is using meanwhile. Delete the
temporary body file.
