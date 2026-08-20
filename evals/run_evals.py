#!/usr/bin/env python3
"""Triggering evals for the dax-skills repo.

Static mode (default, no API): guards against routing rot. For each case it
verifies the expected skill exists and still shares vocabulary with a prompt
written to trigger it (catches a description that lost its keywords), reports a
ranking, flags cross-skill trigger collisions, and checks that each *-advisor
router references its same-prefix siblings. Hard-fails only on rot/structure so
CI stays stable.

Model mode (--model, needs ANTHROPIC_API_KEY): asks Claude which skill best
matches each prompt and reports real routing accuracy. Gated to a manual run.

Usage:
    python evals/run_evals.py            # static, exits non-zero on failure
    python evals/run_evals.py --model    # LLM-judge accuracy (costs tokens)
"""
import os
import re
import sys
import json
import glob

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("""a an the to of in on for and or with without via your you this that
into is are be can use used when how do does what which they their it its as at by
from not no only all any per each before after over under between within out off""".split())
WORD = re.compile(r"[a-z0-9]+")


def load_skills():
    skills = {}
    for skill_md in glob.glob(os.path.join(ROOT, "*", "SKILL.md")):
        txt = open(skill_md, encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", txt, re.S)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        name = fm.get("name")
        if name:
            skills[name] = {"description": (fm.get("description") or ""),
                            "body": m.group(2)}
    return skills


def keywords(desc):
    """Significant tokens + quoted phrases from a description, lowercased."""
    low = desc.lower()
    toks = {w for w in WORD.findall(low) if len(w) >= 3 and w not in STOP}
    phrases = {p.strip().lower() for p in re.findall(r'"([^"]{3,})"', desc)}
    return toks, phrases


def score(prompt, desc):
    p = prompt.lower()
    ptoks = {w for w in WORD.findall(p) if len(w) >= 3 and w not in STOP}
    toks, phrases = keywords(desc)
    s = len(ptoks & toks)
    s += 3 * sum(1 for ph in phrases if ph in p)  # quoted trigger phrase match = strong
    return s


def static_eval(skills, cases):
    fails, warns = [], []

    # cross-skill duplicate trigger phrases (ambiguous routing)
    phrase_owner = {}
    for name, d in skills.items():
        _, phrases = keywords(d["description"])
        for ph in phrases:
            if " " not in ph:  # single words aren't real trigger phrases
                continue
            phrase_owner.setdefault(ph, []).append(name)
    for ph, owners in phrase_owner.items():
        if len(owners) > 1:
            warns.append(f'trigger phrase "{ph}" shared by {owners}')

    # router coverage: a "<prefix>-advisor" must mention its same-prefix siblings
    for name, d in skills.items():
        if not name.endswith("-advisor"):
            continue
        prefix = name[: -len("-advisor")].rstrip("-")
        siblings = [s for s in skills
                    if s != name and s.startswith(prefix + "-")]
        for sib in siblings:
            if sib not in d["body"]:
                fails.append(f"router {name} does not reference sibling {sib}")

    # per-case ranking + rot check
    top1 = 0
    for c in cases:
        prompt, expect = c["prompt"], c["expect"]
        if expect not in skills:
            fails.append(f"case expects unknown skill: {expect}")
            continue
        own = score(prompt, skills[expect]["description"])
        if own == 0:
            fails.append(f"ROT: '{expect}' shares no vocabulary with its own "
                         f"prompt — description lost its trigger keywords")
            continue
        ranking = sorted(((score(prompt, s["description"]), n)
                          for n, s in skills.items()), reverse=True)
        best = ranking[0][1]
        rank = [n for _, n in ranking].index(expect) + 1
        if best == expect:
            top1 += 1
        elif rank > 2:
            warns.append(f"'{expect}' ranked #{rank} (top: {best}) for: {prompt[:55]}…")
        else:
            warns.append(f"'{expect}' ranked #{rank} behind '{best}' for: {prompt[:45]}…")

    n = len([c for c in cases if c["expect"] in skills])
    print(f"Static evals: {len(skills)} skills, {len(cases)} cases.")
    print(f"  heuristic top-1 routing: {top1}/{n}")
    for w in warns:
        print(f"  warn: {w}")
    if fails:
        print("FAILED:")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("  OK (no rot / structural failures).")
    return 0


# Los flags que un caso puede afirmar, con el tipo que deben tener. Un nombre fuera de esta
# lista es un error del fichero de casos, no algo que ignorar: un typo que "pasa" es peor que
# un caso que falta, porque parece cobertura.
KNOWN_FLAGS = {
    "discouragedInVisualCalculations": bool,
    "notes": bool,
    "returns": str,
    "primaryCategory": str,
}
RETRIEVAL_TOP_N = 3


def find_function(catalog, name):
    """La entrada del catálogo para `name`, sin distinguir mayúsculas. None si no está."""
    wanted = name.strip().upper()
    for entry in catalog.get("functions", []):
        if str(entry.get("name", "")).upper() == wanted:
            return entry
    return None


def retrieval_score(catalog, prompt, name):
    """Cuánto puntúa `name` contra el prompt. 0 = no comparte ni una palabra."""
    entry = find_function(catalog, name)
    if entry is None:
        return None
    return score(prompt, f"{entry.get('name','')} {entry.get('summary','')}")


def retrieval_rank(catalog, prompt, name):
    """Puesto de `name` al puntuar el prompt contra los resúmenes del catálogo. None si no está.

    El resumen es lo que un agente lee en catalog.md antes de abrir nada. Una ficha puede
    estar perfecta y ser inalcanzable si su resumen pierde las palabras que alguien
    escribiría — eso es exactamente lo que este ranking detecta.
    """
    entry = find_function(catalog, name)
    if entry is None:
        return None
    mine = retrieval_score(catalog, prompt, name)
    # Puesto por competicion: cuentan las que puntuan MAS, no las que empatan. Con
    # desempate alfabetico, DIVIDE caia al puesto 4 empatada con BITAND, BITOR y BITXOR —
    # el eval habria reportado un fallo de recuperacion donde solo habia una D tardia.
    better = sum(1 for e in catalog.get("functions", [])
                 if score(prompt, f"{e.get('name','')} {e.get('summary','')}") > mine)
    return better + 1


def accuracy_eval(catalog, cases, top_n=RETRIEVAL_TOP_N):
    """(codigo de salida, fallos) para los casos con expectFunction.

    Mide la BIBLIOTECA, no el enrutado entre skills: que la función exista, que se pueda
    encontrar a partir de lo que alguien escribiría, y que sus flags digan lo que el caso
    afirma.
    """
    fails = []
    if not cases:
        return 0, []
    if not catalog:
        # Con casos escritos y sin catálogo, devolver 0 seria afirmar que se comprobó algo.
        # Un PR que borre o no genere el catálogo tiene que ponerse rojo.
        return 1, [f"hay {len(cases)} caso(s) de exactitud y no hay catálogo legible en "
                   f"dax-reference/generated/catalog.json — genera la biblioteca antes"]

    for case in cases:
        name = case.get("expectFunction")
        if not name:
            # Dentro de accuracy: no hay casos "de otro tipo": esto es un caso mal escrito
            # (un expectFuncton, por ejemplo), y saltarlo lo deja sin comprobar en silencio.
            fails.append(f"caso sin expectFunction: {str(case)[:70]}…")
            continue
        entry = find_function(catalog, name)
        if entry is None:
            fails.append(f"'{name}' no está en el catálogo (prompt: {case['prompt'][:50]}…)")
            continue

        # El puesto cuenta las que puntúan MÁS. Si nadie puntúa, todas empatan a cero y la
        # esperada sale "primera" — un prompt que no comparte una sola palabra con el
        # catálogo pasaba como recuperación perfecta.
        if retrieval_score(catalog, case["prompt"], name) == 0:
            fails.append(f"'{name}' no comparte ni una palabra con «{case['prompt'][:45]}…» — "
                         f"no es alcanzable con esa redacción")
        elif retrieval_rank(catalog, case["prompt"], name) > top_n:
            rank = retrieval_rank(catalog, case["prompt"], name)
            fails.append(f"'{name}' sale en el puesto {rank} para «{case['prompt'][:45]}…» — "
                         f"su resumen perdió las palabras con las que se busca")

        for flag, expected in (case.get("expectFlag") or {}).items():
            if flag not in KNOWN_FLAGS:
                fails.append(f"'{flag}' no es un flag del catálogo (caso de '{name}'). "
                             f"Conocidos: {', '.join(sorted(KNOWN_FLAGS))}")
                continue
            got = entry.get(flag)
            if got != expected:
                fails.append(f"'{name}'.{flag} vale {got!r}, el caso espera {expected!r}")
    return (1 if fails else 0), fails


def model_eval(skills, cases):
    import urllib.request
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set"); return 2
    model = os.environ.get("EVAL_MODEL", "claude-haiku-4-5-20251001")
    catalog = "\n".join(f"- {n}: {d['description'][:200]}" for n, d in sorted(skills.items()))
    names = set(skills)
    correct, results = 0, []
    for c in cases:
        sys_prompt = ("You are a skill router. Given a user request and a catalog of "
                      "skills, reply with ONLY the single best-matching skill name, "
                      "exactly as written. No prose.")
        user = f"Catalog:\n{catalog}\n\nUser request: {c['prompt']}\n\nBest skill name:"
        body = json.dumps({
            "model": model, "max_tokens": 32,
            "system": sys_prompt,
            "messages": [{"role": "user", "content": user}],
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages", data=body,
            headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            ans = out["content"][0]["text"].strip().strip("`").split()[0].strip(".,")
        except Exception as e:  # noqa: BLE001
            ans = f"<error:{e}>"
        ok = ans == c["expect"]
        correct += ok
        if not ok:
            results.append(f"  ✗ got '{ans}' expected '{c['expect']}'  ({c['prompt'][:50]}…)")
        # guard against hallucinated names
        if ans not in names and not ans.startswith("<error"):
            results.append(f"    note: '{ans}' is not a real skill name")
    print(f"Model evals ({model}): accuracy {correct}/{len(cases)} = {correct/len(cases):.0%}")
    for r in results:
        print(r)
    # informational: don't fail CI on model accuracy (it's a quality signal)
    return 0


def load_catalog():
    """El catálogo generado, o None si la biblioteca aún no se ha construido."""
    path = os.path.join(ROOT, "dax-reference", "generated", "catalog.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def run_accuracy(all_cases):
    """Los casos de exactitud, si hay catálogo y casos. Devuelve el código de salida."""
    cases = all_cases.get("accuracy") or []
    if not cases:
        return 0
    catalog = load_catalog()
    code, fails = accuracy_eval(catalog, cases)
    print(f"Accuracy evals: {len(cases)} casos contra "
          f"{(catalog or {}).get('functionCount', 'ningún')} funciones.")
    if fails:
        print("FAILED:")
        for f in fails:
            print(f"  - {f}")
    else:
        print("  OK (función encontrada y flags correctos).")
    return code


def main():
    skills = load_skills()
    all_cases = yaml.safe_load(open(os.path.join(ROOT, "evals", "cases.yaml"),
                                    encoding="utf-8")) or {}
    cases = all_cases.get("cases", [])
    if "--model" in sys.argv:
        sys.exit(model_eval(skills, cases))
    # Los dos se ejecutan siempre: el enrutado lleva al skill correcto, la exactitud
    # comprueba que dentro haya la respuesta correcta. Fallar uno basta para fallar.
    routing = static_eval(skills, cases)
    accuracy = run_accuracy(all_cases)
    sys.exit(routing or accuracy)


if __name__ == "__main__":
    main()
