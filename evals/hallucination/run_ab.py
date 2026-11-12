#!/usr/bin/env python3
"""Measure the one thing the README promises: does the reference stop invented functions?

    "It stops your agent from inventing functions that don't exist."

Nothing measured that. `evals/cases.yaml` measures ROUTING — which skill fires for a
prompt — and a perfect router is perfectly compatible with an agent that still writes
`PREVIOUSYEARTOTAL`. Issue #10.

## The shape

Every question is asked twice, of the same model:

    arm A   the question alone
    arm B   the question, plus the catalogue rows for its category

Arm B is deliberately NOT the card that holds the answer. Handing over the answer would
measure obedience, not invention. The rows are the first hop `SKILL.md` documents — "read
catalog.md, find the function" — so arm B knows what exists and still has to choose.

## The metric is mechanical, and that is the point

No model judges another. Every `NAME(` in an answer is extracted and looked up in
`catalog.json`. A name that is not among the 479 is an invented function. It is objective,
it costs nothing, and it can be re-run on a saved transcript forever.

    python evals/hallucination/run_ab.py --limit 3          # a few questions
    python evals/hallucination/run_ab.py                    # the whole bank
    python evals/hallucination/run_ab.py --regime info      # one regime
    python evals/hallucination/run_ab.py --replay out.json  # re-count, no API calls
    python evals/hallucination/run_ab.py --out r.json --resume   # finish an interrupted run

A live run asks a `claude-*` model through the Claude Code CLI (`claude -p`), with the
login you already have there. This script reads no API key at all. Saved runs of other
providers (the DeepSeek runs in runs/) re-count with --replay.
"""
import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # evals/, for claude_cli
ROOT = os.path.dirname(os.path.dirname(HERE))
CATALOG = os.path.join(ROOT, "skills", "dax-reference", "generated", "catalog.json")
QUESTIONS = os.path.join(HERE, "questions.yaml")

# A name followed by `(` is a function call. Dots are part of the name: INFO.VIEW.TABLES
# is one function, and splitting on the dot would report three inventions per mention.
_CALL_RE = re.compile(r"\b([A-Z][A-Z0-9_]*(?:\.[A-Z0-9_]+)*)\s*\(")

# Statements and keywords. The `(` rule already excludes most of them — `VAR x =` and
# `ORDER BY` carry no parenthesis — but these do get written with one often enough that
# counting them would put a permanent, identical bias in BOTH arms and make the
# difference between the arms harder to read, not easier.
KEYWORDS = frozenset({
    "EVALUATE", "DEFINE", "MEASURE", "VAR", "RETURN", "ORDER", "BY", "START", "AT",
    "COLUMN", "TABLE", "FUNCTION", "ASC", "DESC", "IN", "NOT", "AND", "OR",
})


def catalog_names(path=CATALOG):
    with open(path, encoding="utf-8") as f:
        catalog = json.load(f)
    return {f["name"].upper() for f in catalog["functions"]}, catalog


_FENCE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.S)
_INLINE = re.compile(r"`([^`\n]+)`")


def code_spans(text):
    """The parts of an answer that are CODE: fenced blocks and inline spans.

    Only these are searched for calls, and the reason is a false positive that survived
    into a published number. Prose puts capitalised words in front of parentheses all the
    time — "along ROWS (the default axis)", "BLANKS (…)" — and a bare `NAME\\s*\\(` rule
    reads both as function calls. Opus 5 scored two inventions that way and had invented
    nothing; the counter had.

    Restricting to code loses nothing real. A model naming a function it believes in
    writes it in a fence or in backticks — every genuine invention the pilot caught
    (`EVALUATE TMSCHEMA_MEASURES()`, `EXPAND(AXIS(Rows), …)`, `AXIS(Dates[Year])`) is
    inside code, because that is what naming a function looks like.
    """
    return _FENCE.findall(text or "") + _INLINE.findall(text or "")


def called_functions(text):
    """Every distinct NAME( in the answer's CODE, keywords removed. Order preserved."""
    seen, out = set(), []
    for span in code_spans(text):
        for name in _CALL_RE.findall(span):
            if name in KEYWORDS or name in seen:
                continue
            seen.add(name)
            out.append(name)
    return out


def invented(text, names):
    """The called functions that are not among the catalogue's."""
    return [f for f in called_functions(text) if f not in names]


def category_rows(catalog, category):
    """`name — summary` for every function in one catalogue category.

    What arm B is given. Names and one-liners, not cards: enough to know what exists,
    not enough to be told the answer.
    """
    rows = [f"- {f['name']}: {f['summary']}"
            for f in catalog["functions"]
            if category in (f.get("category") or []) or f.get("primaryCategory") == category]
    return "\n".join(rows)


SYSTEM = ("You are a Power BI developer answering a colleague. Be brief: name the DAX "
          "functions involved and show a short snippet. Do not hedge with lists of "
          "alternatives you are unsure about.")


# ---------------------------------------------------------------------------
# Who answers
# ---------------------------------------------------------------------------
#
# A live run goes through the Claude Code CLI (`claude -p`, see evals/claude_cli.py), with
# the login the person running it already has. This script never reads, passes or prints
# an API key -- the plugin directory holds any plugin whose files read one from the
# environment, and the two eval runners were the only files that did.
#
# Other providers are replay-only. The DeepSeek runs of 2026-08-29 in runs/ still re-count
# with --replay, and check_eval_claims.py recounts them in CI; asking DeepSeek again would
# need its key, which is exactly what this file no longer holds.

PROVIDER = "claude-code"


def check_model(model):
    """Live runs are Claude models only. Anything else stops the run, naming --replay."""
    if not model.startswith("claude-"):
        raise SystemExit(
            f"ERROR: '{model}' cannot run live: only claude-* models do, through the "
            f"Claude Code CLI. A saved run of any model still re-counts with --replay.")


def user_message(question, reference):
    return question if not reference else (
        f"{question}\n\n---\nDAX functions available in this category, from the "
        f"language reference:\n\n{reference}")


def ask(model, question, reference=None, timeout=180):
    import claude_cli
    return claude_cli.ask(model, SYSTEM, user_message(question, reference), timeout=timeout)


def describe(exc):
    """A failure in the words the CLI used, so a login problem and a rate limit differ."""
    return f"{type(exc).__name__}: {exc}"


def summarise(records, names):
    """Per-regime counts for both arms. Never averaged across regimes: see questions.yaml."""
    by_regime = {}
    for rec in records:
        slot = by_regime.setdefault(rec["regime"], {"n": 0, "A": 0, "B": 0,
                                                    "A_q": 0, "B_q": 0})
        slot["n"] += 1
        for arm in ("A", "B"):
            bad = invented(rec[arm]["text"], names)
            slot[arm] += len(bad)
            slot[arm + "_q"] += 1 if bad else 0
    return by_regime


def silent(records):
    """Answers with no text at all, per arm.

    A silent answer is the one failure this metric cannot survive quietly: it scores zero
    inventions, which is the best possible result, for not having said anything. Reported
    on its own line rather than folded into the totals -- a run with silences is a run
    whose number means less, and that has to be visible without reading the JSON.
    """
    return {arm: sum(1 for r in records if not (r[arm]["text"] or "").strip())
            for arm in ("A", "B")}


def report(records, names):
    print()
    print(f"{'question':<22} {'regime':<8} {'invented A':>11} {'invented B':>11}")
    print("-" * 56)
    for rec in records:
        a = invented(rec["A"]["text"], names)
        b = invented(rec["B"]["text"], names)
        print(f"{rec['id']:<22} {rec['regime']:<8} {len(a):>11} {len(b):>11}")
        if a:
            print(f"{'':<22} A invented: {', '.join(a)}")
        if b:
            print(f"{'':<22} B invented: {', '.join(b)}")
    print()
    by_regime = summarise(records, names)
    print(f"{'regime':<10} {'questions':>9} {'A invented':>11} {'B invented':>11} "
          f"{'A q. with':>10} {'B q. with':>10}")
    print("-" * 68)
    for regime in sorted(by_regime):
        s = by_regime[regime]
        print(f"{regime:<10} {s['n']:>9} {s['A']:>11} {s['B']:>11} "
              f"{s['A_q']:>10} {s['B_q']:>10}")
    total_a = sum(s["A"] for s in by_regime.values())
    total_b = sum(s["B"] for s in by_regime.values())
    print("-" * 68)
    print(f"{'TOTAL':<10} {len(records):>9} {total_a:>11} {total_b:>11}")

    quiet = silent(records)
    if quiet["A"] or quiet["B"]:
        print(f"\nWARNING: {quiet['A']} answer(s) in arm A and {quiet['B']} in arm B are "
              f"EMPTY. An empty answer scores zero inventions for not having answered, so "
              f"both arms are understated and the run cannot be compared with a clean one.")
    return total_a, total_b


def save(path, model, provider, records):
    """Write the run file. Called after every question, not at the end.

    A 144-call run takes long enough to be killed by something -- a closed session, a
    timeout, a laptop lid. Twice now that has thrown away everything, including calls that
    were paid for. Writing as it goes costs one small file write per question and makes an
    interruption free.
    """
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"model": model, "provider": provider, "records": records}, f,
                  ensure_ascii=False, indent=2)


def already_answered(path):
    """Questions a previous run of this file finished, by id.

    Only complete ones: a question whose arms are both present is done. A partial record
    is re-asked rather than kept, because half a question is not a cheaper question -- it
    is one arm compared against nothing.
    """
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            saved = json.load(f)
    except (OSError, ValueError):
        return {}
    return {r["id"]: r for r in saved.get("records", [])
            if r.get("A") is not None and r.get("B") is not None}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, help="ask only the first N questions")
    ap.add_argument("--regime", help="classic | window | info | visual")
    ap.add_argument("--model", default=os.environ.get("EVAL_MODEL",
                                                      "claude-haiku-4-5-20251001"))
    ap.add_argument("--out", help="write every answer to this JSON file")
    ap.add_argument("--replay", help="re-count a saved run, making no API calls")
    ap.add_argument("--resume", action="store_true",
                    help="keep the answers already in --out and ask only what is missing")
    args = ap.parse_args(argv)

    names, catalog = catalog_names()

    if args.replay:
        with open(args.replay, encoding="utf-8") as f:
            saved = json.load(f)
        print(f"replaying {len(saved['records'])} question(s) from {args.replay} "
              f"(model {saved.get('model', '?')}) — no API calls.")
        report(saved["records"], names)
        return 0

    with open(QUESTIONS, encoding="utf-8") as f:
        questions = yaml.safe_load(f)["questions"]
    if args.regime:
        questions = [q for q in questions if q["regime"] == args.regime]
    if args.limit:
        questions = questions[:args.limit]
    if not questions:
        print("no questions selected.")
        return 2

    check_model(args.model)
    provider = PROVIDER

    print(f"model {args.model} ({provider}) · {len(questions)} question(s) · 2 arms "
          f"each = {len(questions) * 2} calls")
    done = already_answered(args.out) if args.resume else {}
    if done:
        print(f"  resuming: {len(done)} question(s) already answered in {args.out}")
    records = [done[q["id"]] for q in questions if q["id"] in done]
    tokens_in, tokens_out = 0, 0
    consecutive = 0
    for q in questions:
        if q["id"] in done:
            continue
        rows = category_rows(catalog, q["category"])
        rec = {"id": q["id"], "regime": q["regime"], "category": q["category"],
               "question": q["question"]}
        for arm, reference in (("A", None), ("B", rows)):
            try:
                text, usage = ask(args.model, q["question"], reference)
                consecutive = 0
            except Exception as exc:                          # noqa: BLE001
                consecutive += 1
                print(f"  {q['id']} arm {arm}: FAILED - {describe(exc)}")
                text, usage = "", {}
            rec[arm] = {"text": text}
            tokens_in += usage.get("input_tokens", 0)
            tokens_out += usage.get("output_tokens", 0)
        if consecutive >= 4:
            # Four in a row is not a bad connection, it is a condition: not logged in,
            # no usage left, a model the account cannot reach. Carrying on writes 140 more
            # empty answers into a file that then reports a perfect score, which is the
            # failure `silent()` exists to make visible -- and this stops it being
            # produced at all.
            print(f"\n{consecutive} calls failed in a row. Stopping: this is a condition, "
                  f"not a blip, and a run of empty answers is not a measurement.")
            if args.out and records:
                save(args.out, args.model, provider, records)
                print(f"the {len(records)} question(s) already answered are kept in "
                      f"{args.out}; re-run with --resume once it is fixed.")
            return 2
        records.append(rec)
        if args.out:
            save(args.out, args.model, provider, records)
        a = len(invented(rec["A"]["text"], names))
        b = len(invented(rec["B"]["text"], names))
        print(f"  {q['id']:<22} A={a} B={b}", flush=True)

    total_a, total_b = report(records, names)
    print(f"\ntokens: {tokens_in} in, {tokens_out} out")

    if args.out:
        save(args.out, args.model, provider, records)
        print(f"answers written to {args.out} — re-count with --replay")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
