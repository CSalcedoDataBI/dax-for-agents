#!/usr/bin/env python3
"""Fail if the plugin manifest and the skills on disk disagree.

The skills sit flat at the repo root, not under `skills/`, so nothing is discovered
automatically: `.claude-plugin/plugin.json` names each one by path and that list IS the
plugin. A skill missing from it ships invisible, and Claude Code does not complain --
the docs are explicit that when none of the listed paths exist the default scan runs
instead, which here finds nothing at all. That is a plugin that installs, reports
success, and loads zero skills. It was reproduced before this check existed.

Run: python scripts/check_plugin_manifest.py
"""
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_DIR = os.path.join(ROOT, ".claude-plugin")

# Verified by bisection against the published CLI: 2.1.141 loads zero skills from these
# paths, 2.1.142 loads all four. Below the floor the plugin installs and does nothing.
MIN_CLAUDE_CODE = "2.1.142"


def skill_dirs(root):
    """Every top-level directory holding a SKILL.md -- the same rule validate_skills uses."""
    return sorted(d for d in os.listdir(root)
                  if os.path.isfile(os.path.join(root, d, "SKILL.md")))


def check(root):
    """Every disagreement between the manifest pair and the tree, as a list of strings."""
    errors = []
    plugin_path = os.path.join(root, ".claude-plugin", "plugin.json")
    market_path = os.path.join(root, ".claude-plugin", "marketplace.json")

    plugin, market = None, None
    for path, label in ((plugin_path, "plugin"), (market_path, "marketplace")):
        if not os.path.exists(path):
            errors.append(f".claude-plugin/{label}.json is missing")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f".claude-plugin/{label}.json is not valid JSON: {e}")
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
        errors.append("plugin.json has no 'skills' array. Nothing sits under skills/, so "
                      "without it the plugin installs and loads zero skills.")
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
        if not os.path.isfile(os.path.join(root, name, "SKILL.md")):
            errors.append(f"plugin.json lists './{name}' but {name}/SKILL.md does not "
                          f"exist. Claude Code falls back to the default scan instead of "
                          f"failing, so this goes unnoticed.")

    for missing in sorted(set(on_disk) - set(listed)):
        errors.append(f"{missing}/SKILL.md exists but is not listed in plugin.json "
                      f"skills -- it would ship invisible")

    # `/plugin install dax@dax-for-agents` is spelled out of these two names. If the entry
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
            if entry.get("source") != "./":
                errors.append(f"marketplace entry '{entry.get('name')}' has source "
                              f"{entry.get('source')!r}; the skills live at the repo "
                              f"root, so it has to be './'")
            if "skills" in entry:
                errors.append("the marketplace entry also declares 'skills'. Keep the "
                              "list in plugin.json alone -- two sources of truth for the "
                              "same thing drift, and only one of them is read.")
            if "version" in entry:
                errors.append("the marketplace entry declares 'version'. plugin.json "
                              "wins, and release-please only bumps that one, so this "
                              "copy would freeze at whatever it says today.")
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
    print(f"OK: plugin manifest lists {len(skill_dirs(root))} skill(s), all present "
          f"(needs Claude Code >= {MIN_CLAUDE_CODE}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
