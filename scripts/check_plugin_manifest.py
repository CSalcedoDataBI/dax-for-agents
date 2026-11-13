#!/usr/bin/env python3
"""Fail if the plugin manifest, the skills on disk and the shipped folder disagree.

The plugin is `plugins/dax-for-agents/`, and that folder is all the Anthropic plugin
directory receives: the lab, the evals, the maintainer scripts and their tests stay in the
repository. Three things are checked:

1. `plugins/dax-for-agents/.claude-plugin/plugin.json` names each skill by path. A skill
   missing from that list ships invisible without Claude Code complaining -- when none of
   the listed paths exist the default scan runs instead. Before skills had their own
   folder that fallback found nothing, and the plugin installed, reported success, and
   loaded zero skills.
2. The root marketplace points at that folder, so `/plugin install` and the directory read
   the same files.
3. Every file in the folder is a type the directory accepts from an organization that is
   not Verified -- Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO -- with no
   `.claude/` and no second `.claude-plugin/`. v0.9.0 was refused for a `.ps1` and
   ten `.py` files sitting inside `skills/`.

Run: python scripts/check_plugin_manifest.py
"""
import os
import subprocess
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = "plugins/dax-for-agents"

# The types the directory takes from an organization that is not Verified.
ALLOWED = (".md", ".txt", ".json", ".yaml", ".yml",
           ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico")

# Verified by bisection against the published CLI: 2.1.141 loads zero skills from these
# paths, 2.1.142 loads all four. Below the floor the plugin installs and does nothing.
MIN_CLAUDE_CODE = "2.1.142"


def skill_dirs(root):
    """Every skills/ directory of the plugin holding a SKILL.md, relative to the plugin.

    Same rule validate_skills uses, and the same shape plugin.json spells: comparing
    a bare folder name against a "./skills/x" entry would report every skill missing.
    """
    base = os.path.join(root, PLUGIN_DIR, "skills")
    return sorted("skills/" + d for d in (os.listdir(base) if os.path.isdir(base) else [])
                  if os.path.isfile(os.path.join(base, d, "SKILL.md")))


def shipped_files(root):
    """Files in the plugin folder, relative to it, posix. Tracked plus untracked-not-ignored
    when `root` is a git checkout (so a local `.publish-*` scratch dir does not count),
    every file on disk otherwise."""
    plugin = os.path.join(root, PLUGIN_DIR)
    if os.path.exists(os.path.join(root, ".git")):
        out = subprocess.run(["git", "-C", root, "ls-files", "-co", "--exclude-standard",
                              "--", PLUGIN_DIR], capture_output=True, text=True,
                             encoding="utf-8", check=True).stdout
        return sorted(p[len(PLUGIN_DIR) + 1:] for p in out.splitlines()
                      if p and os.path.exists(os.path.join(root, p)))
    found = []
    for dirpath, _, names in os.walk(plugin):
        for n in names:
            found.append(os.path.relpath(os.path.join(dirpath, n), plugin).replace(os.sep, "/"))
    return sorted(found)


def type_errors(files):
    errors = []
    for rel in files:
        parts = rel.split("/")
        if ".claude" in parts[:-1]:
            errors.append(f"{PLUGIN_DIR}/{rel}: a .claude/ folder inside the plugin is "
                          f"refused by the directory")
        elif ".claude-plugin" in parts[1:-1] or (parts[0] == ".claude-plugin"
                                                 and parts[-1] not in ("plugin.json", "icon.png")):
            errors.append(f"{PLUGIN_DIR}/{rel}: the only .claude-plugin/ the directory "
                          f"accepts is the plugin's own, with plugin.json and the icon")
        elif not rel.lower().endswith(ALLOWED):
            errors.append(f"{PLUGIN_DIR}/{rel}: not a type the directory accepts "
                          f"({', '.join(ALLOWED)}). Keep scripts outside the plugin, "
                          f"under scripts/")
    return errors


def check(root):
    """Every disagreement between the manifest pair, the tree and the type rule."""
    errors = []
    plugin_rel = f"{PLUGIN_DIR}/.claude-plugin/plugin.json"
    market_rel = ".claude-plugin/marketplace.json"

    plugin, market = None, None
    for rel, label in ((plugin_rel, "plugin"), (market_rel, "marketplace")):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            errors.append(f"{rel} is missing")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{rel} is not valid JSON: {e}")
            continue
        if label == "plugin":
            plugin = loaded
        else:
            market = loaded
    if plugin is None or market is None:
        return errors

    declared = plugin.get("skills")
    if not isinstance(declared, list) or not declared:
        # A string form would load too, but only the array can be checked entry by entry
        # against the tree, and being checkable is the point.
        errors.append("plugin.json has no 'skills' array. The default scan of skills/ "
                      "would cover for it, but silently -- the list is what makes the "
                      "set of shipped skills reviewable.")
        declared = []

    on_disk = skill_dirs(root)
    listed = []
    for entry in declared:
        if not isinstance(entry, str) or not entry.startswith("./"):
            errors.append(f"plugin.json skills entry {entry!r} must be a path starting "
                          f"with './' (a bare name fails manifest validation)")
            continue
        name = entry[2:].rstrip("/")
        listed.append(name)
        if not os.path.isfile(os.path.join(root, PLUGIN_DIR, name, "SKILL.md")):
            errors.append(f"plugin.json lists './{name}' but {PLUGIN_DIR}/{name}/SKILL.md "
                          f"does not exist. Claude Code falls back to the default scan "
                          f"instead of failing, so this goes unnoticed.")

    for missing in sorted(set(on_disk) - set(listed)):
        errors.append(f"{PLUGIN_DIR}/{missing}/SKILL.md exists but is not listed in "
                      f"plugin.json skills -- it would ship invisible")

    # `/plugin install dax-for-agents@dax-for-agents` is spelled out of these two names. If the entry
    # names a different plugin, the README's install line points at nothing.
    entries = market.get("plugins")
    if not isinstance(entries, list) or not entries:
        errors.append("marketplace.json lists no plugins")
        return errors
    names = [e.get("name") for e in entries if isinstance(e, dict)]
    if plugin.get("name") not in names:
        errors.append(f"plugin.json name {plugin.get('name')!r} is not among the "
                      f"marketplace entries {names!r}")
    for entry in entries:
        if isinstance(entry, dict) and entry.get("name") == plugin.get("name"):
            if entry.get("source") != f"./{PLUGIN_DIR}":
                errors.append(f"marketplace entry '{entry.get('name')}' has source "
                              f"{entry.get('source')!r}; the plugin lives in "
                              f"{PLUGIN_DIR}/, so it has to be './{PLUGIN_DIR}'")
            if "skills" in entry:
                errors.append("the marketplace entry also declares 'skills'. Keep the "
                              "list in plugin.json alone -- two sources of truth for the "
                              "same thing drift, and only one of them is read.")
            if "version" in entry:
                errors.append("the marketplace entry declares 'version'. plugin.json "
                              "wins, and release-please only bumps that one, so this "
                              "copy would freeze at whatever it says today.")

    errors += type_errors(shipped_files(root))
    return errors


def main(root=ROOT):
    if not os.path.isdir(os.path.join(root, ".claude-plugin")):
        print(f"ERROR: no .claude-plugin/ under {root} - nothing to check.",
              file=sys.stderr)
        return 2
    errors = check(root)
    if errors:
        print("PLUGIN MANIFEST CHECK FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: plugin manifest lists {len(skill_dirs(root))} skill(s), all present; "
          f"{len(shipped_files(root))} files in {PLUGIN_DIR}/, all of an accepted type "
          f"(needs Claude Code >= {MIN_CLAUDE_CODE}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
