#!/usr/bin/env python3
"""Fail if a workflow breaks the Actions cost rules.

The account has 3.000 Actions minutes a month. These three rules are the ones that can
be checked mechanically, and each one was already broken in this repo when the gate was
written — found by reading six files by hand, which is exactly the check that does not
scale:

  R3  Every job declares timeout-minutes. GitHub's default is 360: a single hung job
      spends 12% of the month. Four of the six workflows here had no limit at all.
  R7  Scheduled jobs run weekly at most. A cron is the spend that happens while nobody
      is working. `stale` was firing daily to apply a 60-day threshold.
  R5  runs-on is ubuntu. Windows bills x2 and macOS x10 against the same quota.

Run: python scripts/check_workflow_cost.py
"""
import os
import re
import sys
import glob

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# Anything past this is the 360-minute default wearing a number. 10 for a normal job,
# 20 for a heavy build, 30 for an agent that thinks; nothing here needs an hour.
MAX_TIMEOUT = 60

_FIXED_FIELD_CHARS = set("0123456789")
# The whole `${{ ... }}`, not just the key, so the value can be substituted back into
# the label it came from: `ubuntu-${{ matrix.version }}` is a runner, `22.04` is not.
_MATRIX_REF = re.compile(
    r"\$\{\{\s*matrix(?:\.([A-Za-z0-9_-]+)|\[['\"]([A-Za-z0-9_-]+)['\"]\])\s*\}\}")
_CRON_NAMES = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT",
               "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
               "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"}


def _is_single_value(field):
    """True for one pinned value. Ranges, lists and steps are several days.

    GitHub takes POSIX cron, where day-of-week may be a name: `* * * * MON` is a
    perfectly good weekly schedule and rejecting it would be the gate inventing a
    violation. `?` is Quartz, not POSIX, so it stays rejected.
    """
    if not field:
        return False
    if set(field) <= _FIXED_FIELD_CHARS:
        return True
    return field.upper() in _CRON_NAMES


def cron_is_weekly_or_rarer(expr):
    """True when this cron fires at most about once a week.

    Every field has to be pinned to one value except exactly one of day-of-month and
    day-of-week, which stays `*`:

        17 6 * * 1     weekly, Mondays        -> True
        17 6 * * MON   the same thing         -> True
        0  3 1 * *     monthly, the 1st       -> True
        30 1 * * *     daily                  -> False
        0  3 * * 1-5   five times a week      -> False
        0  3 */2 * *   every other day        -> False
        0  3 5 * 1     the 5th OR any Monday  -> False

    That last one is the trap: with both day fields restricted, cron fires when EITHER
    matches, not both. "Weekly" is not a thing you can read off a field being non-`*` —
    it is `1-5` and `*/2` passing that made this rule fail its own purpose.

    The month field is not examined at all: whatever it says, it can only narrow the
    schedule further. `0 3 * 1,6 1` is Mondays in two months, which is rarer than
    weekly, and rejecting it would be the gate complaining about a saving.
    """
    fields = str(expr).split()
    if len(fields) != 5:
        return False                      # not a cron we understand: do not wave it through
    minute, hour, dom, _month, dow = fields
    for field in (minute, hour):
        if not _is_single_value(field):
            return False                  # '*', '*/15', '1,13' - more than once a day
    if (dom == "*") == (dow == "*"):
        return False                      # both '*' is daily; both pinned is an OR
    if dom != "*":
        # A list of days of the month is still monthly-ish: `1,15` is twice a month,
        # rarer than weekly. Four is where it meets weekly, and a range or a step
        # ('1-15', '*/2') is a lot more than four.
        days = dom.split(",")
        return len(days) <= 4 and all(_is_single_value(d) for d in days)
    return _is_single_value(dow)          # two days a week is twice the weekly budget


def _as_minutes(value):
    """The declared timeout as a number, or None if it is not one.

    `timeout-minutes: "120"` is a string to YAML, and letting an unreadable value skip
    the cap check meant the highest limit in the file was the one nobody looked at.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _runner_alternatives(job):
    """Every distinct machine this job can land on, as a list of label sets.

    The two shapes `runs-on` takes mean opposite things and collapsing them loses the
    check. A LIST is one machine that must carry all those labels at once, so
    `[ubuntu-latest, fast]` is an Ubuntu box with an extra tag, not two runners. A
    MATRIX is alternatives, so `os: [ubuntu-latest, windows-latest]` really is two
    machines and the Windows one has to be seen.

    `runs-on: ${{ matrix.os }}` parses as a plain string, so reading it literally would
    accuse the workflow of running on a machine called '${{ matrix.os }}'. A label that
    resolves from anywhere else (a job output, an input) cannot be read without running
    the workflow; it is dropped rather than falsely accused.
    """
    value = job.get("runs-on")
    if isinstance(value, dict):
        # The mapping form, `{group: gpu, labels: [windows-latest]}`. The group is
        # defined org-side and unreadable here, but the labels beside it are the same
        # labels as any other form, and skipping the whole mapping let them through.
        value = value.get("labels")
    if isinstance(value, str):
        base = [value]
    elif isinstance(value, list):
        base = [v for v in value if isinstance(v, str)]
    else:
        return []
    if not base:
        return []

    matrix = (job.get("strategy") or {}).get("matrix")
    matrix = matrix if isinstance(matrix, dict) else {}
    excluded = _matrix_excluded(matrix)

    # Every reference is substituted across the WHOLE label set at once. Expanding one
    # at a time leaves '${{ matrix.os }}-latest' half-resolved and reports a correct
    # Ubuntu matrix for not being Ubuntu.
    alternatives = [base]
    for key, ref in _matrix_keys(" ".join(base)):
        # Only the key the expression names. Taking every matrix value would read
        # `python-version: ["3.12"]` as a runner and flag it for not being ubuntu.
        axis, added = _matrix_values(matrix, key)
        gone = excluded.get(key, frozenset())
        candidates = [v for v in axis if v not in gone]
        candidates += added            # `include` runs after `exclude` and can re-add
        if not candidates:
            continue                   # key not in the matrix: leave it unresolved
        alternatives = [[label.replace(ref, value) for label in alt]
                        for alt in alternatives for value in candidates]

    resolved, seen = [], set()
    for alt in alternatives:
        # A label still holding an expression came from somewhere this cannot read.
        # Dropping just that label keeps the rest of the set checkable.
        readable = tuple(label for label in alt if "${{" not in label)
        if readable and readable not in seen:
            seen.add(readable)
            resolved.append(list(readable))
    return resolved


def _alternative_is_cheap(labels):
    """True when this machine does not bill against the GitHub-hosted quota.

    A self-hosted runner costs nothing, whatever else it is tagged with. Otherwise one
    Ubuntu label is enough: the rest of a list is extra requirements on the same box.
    """
    return any(label == "self-hosted" or label.startswith("ubuntu") for label in labels)


def _matrix_keys(label):
    """The (key, exact-text) pairs for every matrix reference in a label."""
    pairs = []
    for m in _MATRIX_REF.finditer(label):
        pairs.append((m.group(1) or m.group(2), m.group(0)))
    return pairs


def _matrix_values(matrix, key):
    """Values `key` takes, split into (axis, added-by-include).

    They stay apart because GitHub applies `include` AFTER `exclude`: an include entry
    can put back the very combination an exclude removed, so an excluded label is not
    proof the job never runs. A matrix can also introduce a runner with no axis behind
    it at all — `include: [{os: windows-latest}]` — and reading only `matrix[key]`
    walks straight past a job billed at double.
    """
    axis, added = [], []
    entries = matrix.get(key)
    if isinstance(entries, list):
        axis += [v for v in map(_as_label, entries) if v is not None]
    include = matrix.get("include")
    if isinstance(include, list):
        for combo in include:
            if isinstance(combo, dict):
                value = _as_label(combo.get(key))
                if value is not None:
                    added.append(value)
    return axis, added


def _as_label(value):
    """A matrix entry as the text it becomes in a label, or None if it is not one.

    `version: [22.04]` unquoted is a float to YAML, not a string. Dropping those left
    nothing to resolve, so `${{ matrix.os }}-${{ matrix.version }}` went unchecked
    entirely — a Windows job hidden behind an unquoted number.
    """
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, str):
        return None if "${{" in value else value
    if isinstance(value, (int, float)):
        return str(value)
    return None


def _matrix_excluded(matrix):
    """Values `exclude` removes outright, keyed by the axis they belong to.

    Keyed, because a value only means something inside its own axis: excluding
    `{tool: windows-latest}` says nothing about `os: windows-latest`, and a flat set of
    values would take the runner out of the os axis and report a Windows job as OK.

    Only single-key exclusions count. `exclude: [{os: windows-latest, py: '3.9'}]`
    drops one combination and leaves the Windows job running the other versions, so
    treating it as "no Windows here" would be the gate excusing the expensive case.
    """
    excluded = {}
    entries = matrix.get("exclude")
    if isinstance(entries, list):
        for combo in entries:
            if isinstance(combo, dict) and len(combo) == 1:
                ((key, only),) = combo.items()
                value = _as_label(only)
                if value is not None:
                    excluded.setdefault(key, set()).add(value)
    return excluded


def check_file(path, rel):
    """Return the cost-rule violations in one workflow file."""
    errors = []
    with open(path, encoding="utf-8") as f:
        try:
            wf = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            return [f"{rel}: invalid YAML ({e})"]
    if not isinstance(wf, dict):
        return [f"{rel}: not a workflow mapping"]

    # `on:` parses as the boolean True — YAML 1.1, and the reason this looks odd.
    triggers = wf.get("on", wf.get(True)) or {}
    if isinstance(triggers, dict):
        schedule = triggers.get("schedule") or []
        for entry in schedule if isinstance(schedule, list) else []:
            expr = entry.get("cron") if isinstance(entry, dict) else entry
            if not cron_is_weekly_or_rarer(expr):
                errors.append(f"{rel}: cron '{expr}' fires more often than weekly (R7). "
                              f"A schedule runs whether or not anyone is working.")

    jobs = wf.get("jobs") or {}
    if not isinstance(jobs, dict) or not jobs:
        # Nothing to check, and the file still counts towards "N workflows OK". A gate
        # that reports having looked at something it could not read is the failure mode
        # this whole script exists to prevent.
        return errors + [f"{rel}: no jobs — not a workflow this check can verify."]

    for name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        if "uses" in job:
            continue                      # reusable workflow: the limit lives in the callee
        declared = job.get("timeout-minutes")
        if declared is None:
            # ASCII on purpose: an em dash prints as a replacement char on a cp1252
            # Windows console, and a garbled failure message reads as a broken check.
            errors.append(f"{rel}: job '{name}' has no timeout-minutes (R3). The default "
                          f"is 360 min, 12% of the monthly quota on one hung run.")
        else:
            minutes = _as_minutes(declared)
            if minutes is None:
                errors.append(f"{rel}: job '{name}' sets timeout-minutes to "
                              f"'{declared}', which is not a number this check can read "
                              f"(R3). An unreadable limit is not a limit.")
            elif minutes < 1:
                errors.append(f"{rel}: job '{name}' sets timeout-minutes to {minutes} "
                              f"(R3). That is not a shorter limit, it is no limit.")
            elif minutes > MAX_TIMEOUT:
                errors.append(f"{rel}: job '{name}' allows {minutes} min, over the "
                              f"{MAX_TIMEOUT}-minute cap (R3).")
        for alternative in _runner_alternatives(job):
            if not _alternative_is_cheap(alternative):
                runner = ", ".join(alternative)
                errors.append(f"{rel}: job '{name}' runs on '{runner}' (R5). Windows "
                              f"bills x2 and macOS x10. If it is unavoidable, restrict "
                              f"the workflow to tag pushes and relax this check knowingly.")
    return errors


def workflow_paths(workflow_dir):
    """The files check_tree reads. main() reports the count from here and nowhere else,
    so what it says it checked is what it checked."""
    return sorted(glob.glob(os.path.join(workflow_dir, "*.yml")) +
                  glob.glob(os.path.join(workflow_dir, "*.yaml")))


def check_tree(workflow_dir):
    """Violations across every workflow, or None when there are no workflows to read."""
    paths = workflow_paths(workflow_dir)
    if not paths:
        return None
    errors = []
    for path in paths:
        errors += check_file(path, os.path.basename(path))
    return errors


def main(workflow_dir=WORKFLOWS):
    errors = check_tree(workflow_dir)
    if errors is None:
        print(f"ERROR: no workflows under {workflow_dir} - the check would pass "
              f"vacuously.", file=sys.stderr)
        return 2
    if errors:
        print("WORKFLOW COST CHECK FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    count = len(workflow_paths(workflow_dir))
    print(f"OK: {count} workflow(s) within the Actions cost rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
