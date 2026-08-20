#!/usr/bin/env python3
"""Leer y escribir los ficheros de `dax-reference/examples/`.

Un ejemplo es un par: un bloque ```dax y el bloque ```result que trajo el motor. Este modulo
es la unica definicion de ese formato — lo usan el gate (`check_examples.py`), el runner
(`lab/check_lab.py`) y el registrador (`lab/dump_examples.py`), para que los tres entiendan
exactamente lo mismo y no se separen con el tiempo.

Comparar RENDERIZADO y no estructura es deliberado: lo que falla se lee en el diff igual que
lo escribio quien lo autorizo, sin traducir tuplas de Python en la cabeza.
"""
import datetime
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_DIR = os.path.join(ROOT, "dax-reference", "examples")

BLANK = "(blank)"
# La cadena vacia NO es un blanco, y en DAX esa diferencia decide resultados. Sin marcarla
# se renderiza como nada entre dos barras y se lee como si faltara la celda.
EMPTY = "(empty)"
ERROR_PREFIX = "ERROR: "

# Un ejemplo declara `model: ninguno` cuando NO lee datos del modelo — aritmetica, texto,
# logica. Se ejecuta contra contoso porque hace falta un motor, no ese modelo.
NO_MODEL = "ninguno"

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_BLOCK = re.compile(r"```(dax|result)\n(.*?)```", re.S)

# Seis decimales: suficiente para que SQRT(2) y PMT() se distingan de verdad, y corto para
# que el ruido de coma flotante del motor (744415.2800000007) no entre en el fichero.
DECIMALS = 6


def render_value(v):
    if v is None:
        return BLANK
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        r = round(v, DECIMALS)
        if r == int(r):
            return str(int(r))
        return f"{r:.{DECIMALS}f}".rstrip("0")
    if isinstance(v, datetime.datetime):
        if (v.hour, v.minute, v.second, v.microsecond) == (0, 0, 0, 0):
            return v.strftime("%Y-%m-%d")
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, datetime.date):
        return v.strftime("%Y-%m-%d")
    if v == "":
        return EMPTY
    return str(v)


def render_result(columns, rows):
    """El texto que va dentro de un bloque ```result."""
    lines = [" | ".join(str(c).strip("[]") for c in columns)]
    lines += [" | ".join(render_value(v) for v in row) for row in rows]
    return "\n".join(lines)


def render_error(message):
    """Una consulta que aborta a proposito. Se guarda solo la primera linea, sin la
    posicion (`Query (3, 12)`), que cambia al reindentar la consulta sin cambiar nada."""
    first = str(message).splitlines()[0]
    return ERROR_PREFIX + re.sub(r"^Query \(\d+, \d+\) ", "", first).strip()


def parse_frontmatter(text):
    """Lee el frontmatter YAML plano `clave: valor`. No hay anidamiento aqui a proposito."""
    m = _FRONTMATTER.search(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def parse_blocks(text):
    """Los pares (dax, result) en el orden en que aparecen.

    Un bloque ```dax sin su ```result detras devuelve result=None, que es exactamente lo
    que el gate tiene que cazar: un ejemplo sin numero medido.
    """
    blocks = [(kind, body.rstrip("\n")) for kind, body in _BLOCK.findall(text)]
    pairs = []
    i = 0
    while i < len(blocks):
        kind, body = blocks[i]
        if kind != "dax":
            i += 1
            continue
        if i + 1 < len(blocks) and blocks[i + 1][0] == "result":
            pairs.append((body, blocks[i + 1][1]))
            i += 2
        else:
            pairs.append((body, None))
            i += 1
    return pairs


def parse(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return parse_frontmatter(text), parse_blocks(text)


def example_files(root=EXAMPLES_DIR):
    """Todo `<categoria>/<stem>.md`. El README del propio arbol no es un ejemplo."""
    out = []
    if not os.path.isdir(root):
        return out
    for category in sorted(os.listdir(root)):
        cat_dir = os.path.join(root, category)
        if not os.path.isdir(cat_dir):
            continue
        for name in sorted(os.listdir(cat_dir)):
            if name.endswith(".md"):
                out.append(os.path.join(cat_dir, name))
    return out
