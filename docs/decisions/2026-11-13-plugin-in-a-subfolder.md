# The plugin moves to `plugins/dax-for-agents/`, and only text ships

- **Date:** 2026-11-13
- **Status:** accepted
- **Supersedes:** the repo-root plugin path, and #26 (same move, written before the cards
  were bundled; closed in favour of this one)

## Context

v0.9.0 (`d99623f`) measured 467 files and no holds, and the Anthropic plugin directory still
refused it. The directory's policy changed: an organization that is not Verified may ship only
Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO images, no `.claude/` folder and no
`.claude-plugin/` other than the plugin's own. With the plugin path at the repository root,
119 of the 467 files broke that rule: the lab's PBIP and TMDL, every validator, the evals,
the SVG diagrams, the maintainer scripts inside `skills/dax-reference/scripts/` and
`skills/dax-lib/scripts/refresh-daxlib.ps1` (also refused on its own, as a redirected package
registry).

The options weighed were: keep the root and split the repository in two, so that only text
stayed in it; wait for a Verified organization; or give the plugin its own folder, as
`powerquery-m-for-agents` and `agentic-board` already do. The maintainer chose the third.

## Decision

- `plugins/dax-for-agents/` is the plugin: `.claude-plugin/plugin.json` and the icon,
  `skills/`, a README with the runs/sends/fetches disclosure and `LICENSE.md`. The root
  `.claude-plugin/marketplace.json` points at it (`"source": "./plugins/dax-for-agents"`).
- Every script moves out: the sync pipeline and its tests to `scripts/dax-reference/`, the
  daxlib refresh to `scripts/dax-lib/`. The skills name them by their repository URL.
- `inject_example.py` was the one script a skill ran for the person who installed the plugin.
  It stays in the repository and the skill links to it; it runs from a clone.
- The two `NOTICE` files become `NOTICE.md`, because a file without an extension is not on
  the accepted list.
- Links from the plugin to `lab/` and `docs/` become GitHub URLs: those folders do not ship.
- `scripts/check_plugin_manifest.py` now also fails when any file in the plugin folder is
  of a type the directory refuses, so the rule is checked on every pull request instead of
  discovered in the portal.

## Consequences

- The plugin folder measures **168 files, 0 blocking, 0 held** (`measure_plugin.py`).
- The directory cannot change the repository or the plugin path of a submission, so this is a
  **new submission**, with its own review. Whether the current listing (0.7.0 live, 0.8.1 in
  review, 0.9.0 refused) is withdrawn or migrated is the maintainer's decision, not this one.
- Someone who installs the plugin loses nothing they could run before except
  `inject_example.py`, which needs a clone now. The four ready-made lab zips are unchanged.
- The root `PRIVACY.md` stays where the current listing's `privacyPolicyUrl` points.
