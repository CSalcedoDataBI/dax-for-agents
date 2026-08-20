#!/usr/bin/env python3
"""Rellena el bloque ```result de los ejemplos que aun no lo tienen.

Ejecuta cada consulta contra un modelo abierto y escribe debajo lo que devolvio. NO decide
si el ejemplo era buena idea ni si el numero tiene sentido: eso lo mira quien lo escribio,
antes de aceptar el diff.

Uso:
    # con el escenario abierto y refrescado en Power BI Desktop
    python lab/dump_examples.py localhost:<puerto> [fichero.md ...]

Sin ficheros, recorre todos los de `dax-reference/examples/`. Los que ya tienen result se
dejan intactos; para rehacer uno, borra su bloque ```result y vuelve a ejecutar.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))

import examples_io as io
from check_lab import connect

_DAX_BLOCK = re.compile(r"```dax\n(.*?)```", re.S)


def measure(data_source, query):
    """Devuelve el texto del bloque result: la tabla, o el error si la consulta aborta."""
    try:
        with connect(data_source) as c:
            with c.cursor().execute(query) as cur:
                columns = [d.name for d in cur.description]
                rows = cur.fetchall()
        return io.render_result(columns, rows)
    except Exception as e:
        return io.render_error(e)


def fill(path, data_source):
    """Escribe el result que falte. Devuelve cuantos bloques se rellenaron."""
    text = open(path, encoding="utf-8").read()
    pairs = io.parse_blocks(text)
    pending = [q for q, r in pairs if r is None]
    if not pending:
        return 0

    measured = {}
    for query in pending:
        measured[query] = measure(data_source, query)

    # Se reescribe recorriendo los bloques dax en orden y anadiendo el result detras del que
    # no lo tenga. Insertar por posicion y no por texto evita que dos ejemplos con la misma
    # consulta (que los hay: la misma llamada con otro contexto) se pisen entre si.
    out, last, done = [], 0, 0
    seen = 0
    for m in _DAX_BLOCK.finditer(text):
        query = m.group(1).rstrip("\n")
        has_result = pairs[seen][1] is not None
        seen += 1
        out.append(text[last:m.end()])
        last = m.end()
        if not has_result:
            out.append("\n\n```result\n" + measured[query] + "\n```")
            done += 1
    out.append(text[last:])
    open(path, "w", encoding="utf-8", newline="\n").write("".join(out))
    return done


def main(argv):
    if len(argv) < 2:
        print(f"Uso: {argv[0]} <servidor:puerto> [fichero.md ...]", file=sys.stderr)
        return 2
    data_source = argv[1]
    paths = argv[2:] or io.example_files()
    total = 0
    for path in paths:
        n = fill(path, data_source)
        total += n
        rel = os.path.relpath(path, os.path.dirname(HERE)).replace("\\", "/")
        print(f"{'rellenados ' + str(n) if n else 'ya completo '}  {rel}")
    print(f"\n{total} bloque(s) result escritos. MIRALOS antes de aceptarlos.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
