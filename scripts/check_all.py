#!/usr/bin/env python3
"""Run locally exactly what CI runs, in CI's order, and say what failed.

Ten times in one session the list of gates was typed out by hand before a commit, and a
list typed by hand is a list that eventually gets typed short. That is the failure
`check_documented_gates.py` exists to catch in the README, and this is the same failure one
step earlier: in the habit rather than in the prose.

**The list is not written here.** It is read from `.github/workflows/`, through the same
function the README gate uses, so this runner cannot promise something CI does not run or
skip something it does. There is one definition of "what is checked", and both the
documentation and this command are downstream of it.

    python scripts/check_all.py            # everything CI runs
    python scripts/check_all.py --fast     # skip the test suites
    python scripts/check_all.py --local    # + the checks CI cannot run

`--local` adds what needs a machine CI does not have. Today that is `lab/check_engine.py`,
which compares the catalogue against the functions a real engine says exist and therefore
needs Power BI Desktop open. It is skipped, loudly, when nothing is listening — a check
that quietly does not run is worse than one that is absent.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_documented_gates as documented                       # noqa: E402


def local_only():
    """The commands CI cannot run, with what they need. Empty when it is not available."""
    sys.path.insert(0, os.path.join(ROOT, "lab"))
    try:
        import check_lab
        ports = check_lab.local_instances()
    except Exception:                                             # noqa: BLE001
        return [], "the lab tooling could not be loaded"
    if not ports:
        return [], "no Power BI Desktop instance is listening"
    return [f"python lab/check_engine.py localhost:{ports[0]}"], ""


def run(command):
    started = time.time()
    result = subprocess.run(command, shell=True, cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.returncode, (result.stdout or "") + (result.stderr or ""), \
        time.time() - started


def main(argv):
    fast = "--fast" in argv
    commands = list(documented.commands_in_workflows())
    if fast:
        commands = [c for c in commands if "unittest" not in c]

    if "--local" in argv:
        extra, why = local_only()
        commands += extra
        if not extra:
            print(f"NOTE: the engine check is not running — {why}.\n"
                  f"      Open lab/blancos/Blancos.pbip; it needs no refresh.\n")

    failures = []
    for command in commands:
        code, output, took = run(command)
        mark = "ok  " if code == 0 else "FAIL"
        # The last line of a gate is its verdict. The rest is only interesting when it broke.
        verdict = next((l for l in reversed(output.splitlines()) if l.strip()), "")
        print(f"{mark} {took:5.1f}s  {command}")
        if code == 0:
            print(f"          {verdict[:110]}")
        else:
            failures.append((command, output))

    print()
    if not failures:
        print(f"OK: {len(commands)} check(s) passed — the same ones CI runs.")
        return 0
    print(f"{len(failures)} of {len(commands)} check(s) FAILED:\n")
    for command, output in failures:
        print(f"--- {command}")
        for line in output.splitlines()[:25]:
            print(f"    {line}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
