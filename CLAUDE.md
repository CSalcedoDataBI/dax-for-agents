# Agent instructions

This repository is **public**. Read
[CONTRIBUTING.md](CONTRIBUTING.md#this-repository-is-public-and-that-is-one-way) before
writing anything that leaves the working tree.

## Filing work: two boards, and the difference is not the board

| board | visibility | what goes there |
|---|---|---|
| [#47 — dax-for-agents — Roadmap público](https://github.com/users/CSalcedoDataBI/projects/47) | public | issues of this repo |
| [#39 — dax-for-agents — Interno](https://github.com/users/CSalcedoDataBI/projects/39) | private | internal work, as **draft items** |

Both are linked to this repository, so `agentic-board` offers both and the choice is yours
to get right.

**Do not reason about which board an issue goes on.** An issue in a public repository is
public the instant it is created — the board it sits on changes nothing about that. A
private board hides only status, priority, custom fields and ordering.

The decision is one step earlier, and it is about the *kind of item*:

- **Publishable** → an ordinary issue (`gh issue create`), then add it to **#47**.
- **Not publishable** → **never an issue.** A draft item on **#39**:

  ```bash
  gh project item-create 39 --owner CSalcedoDataBI --title "..." --body "..."
  ```

  A draft lives only inside the project. It has no issue number and never touches this
  repository.

> **If you would not publish it, it is not an issue.**

Not publishable means what the gates already refuse: a client name, a real engagement, a
credential, a private repository's contents — and also the softer cases the gates cannot
see, like "why we stopped working with X" or a finding about someone else's model.

When in doubt, file it as a draft on #39 and say so. Moving a draft up to a public issue
later costs nothing. The other direction is a one-way door: deleting an issue does not
unpublish it.

## Everything else

Conventions live in [INDEX.md](INDEX.md#conventions); the language decision and what stays
in Spanish on purpose are in
[the ADR](docs/decisions/2026-08-25-english-as-the-repository-language.md).
