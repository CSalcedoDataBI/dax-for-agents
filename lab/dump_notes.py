#!/usr/bin/env python3
"""Regenera `lab/notes_expected.py` ejecutando las consultas de las notas.

Se usa cuando se toca la consulta de una nota, o cuando se sospecha que el modelo cambio.
Lo que imprime hay que MIRARLO contra la tabla que publica la nota antes de aceptarlo: este
script traslada resultados a codigo, no decide si son los correctos.

Uso:
    # con lab/contoso/Contoso.pbip abierto y refrescado en Power BI Desktop
    python lab/dump_notes.py localhost:<puerto> > lab/notes_expected.py
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(os.path.dirname(HERE), "dax-reference", "notes")

# Notas que se miden en OTRO escenario del laboratorio y no sobre Contoso. Su pie lo dice.
OTHER_SCENARIO = {"averagex"}

CABECERA = '''"""Lo que devuelve cada consulta publicada en `dax-reference/notes/` sobre `lab/contoso`.

Este fichero no repite las consultas: las lee `check_lab.py` del propio .md de la nota, que
es su unica fuente. Aqui solo viven los RESULTADOS, y por eso una nota deja de ser una
afirmacion citada y pasa a ser un test.

Cada entrada es `nota -> [por cada bloque ```dax de la nota, en orden]`, y cada bloque es:

  ([primeras filas], total_de_filas)   la consulta devuelve tabla
  ("error", "fragmento del mensaje")   la consulta ABORTA, y ese es el resultado publicado

Las dos entradas `("error", ...)` no son fallos del laboratorio. `removefilters` y `values`
ensenan a proposito una consulta que el motor rechaza; si algun dia dejara de rechazarla, la
nota estaria mintiendo y este fichero lo detecta.

Cuando la consulta devuelve cientos de filas (`RELATEDTABLE`, `EARLIER`) se fijan las cinco
primeras y el total. Es lo que la nota ensena, y evita 500 lineas de esperados aqui.

Regenerar tras tocar una nota:
    python lab/dump_notes.py localhost:<puerto> > lab/notes_expected.py
"""'''


def round_value(v):
    """Los flotantes del motor traen ruido de coma flotante (744415.2800000007)."""
    if isinstance(v, float):
        r = round(v, 2)
        return int(r) if r == int(r) else r
    return v


def dax_blocks(path):
    text = open(path, encoding="utf-8").read()
    return re.findall(r"```dax\n(.*?)```", text, re.S)


def main(argv):
    if len(argv) < 2:
        print(f"Uso: {argv[0]} <servidor:puerto>", file=sys.stderr)
        return 2
    sys.path.insert(0, HERE)
    from check_lab import connect

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    names = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(NOTES_DIR, "*.md"))
                   if "INDEX" not in os.path.basename(p))

    print(CABECERA)
    print("NOTES = {")
    for name in names:
        if name in OTHER_SCENARIO:
            continue
        blocks = dax_blocks(os.path.join(NOTES_DIR, name + ".md"))
        if not blocks:
            continue
        print(f'    "{name}": [')
        for query in blocks:
            try:
                with connect(argv[1]) as c:
                    with c.cursor().execute(query) as cur:
                        rows = [tuple(round_value(v) for v in r) for r in cur.fetchall()]
                print("        (")
                print("            [")
                for row in rows[:5]:
                    print(f"                {row!r},")
                print(f"            ], {len(rows)},")
                print("        ),")
            except Exception as e:
                msg = re.sub(r"^Query \(\d+, \d+\) ", "", str(e).splitlines()[0]).strip()
                print(f'        ("error", {msg[:70]!r}),')
        print("    ],")
    print("}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
