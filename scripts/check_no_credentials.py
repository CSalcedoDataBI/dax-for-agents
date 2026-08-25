#!/usr/bin/env python3
"""Falla si algo con forma de credencial aparece en el arbol o en la historia.

El motivo es el de siempre: publicar un repositorio
publica todos sus commits. Un nombre de cliente filtrado es un problema de confidencialidad
y se arregla reescribiendo la historia; una credencial filtrada es un problema de seguridad
y hay que **rotarla**, porque desde el segundo en que se publica hay que darla por conocida.
Este barrido se hacia a mano antes de cada revision. Ahora no.

Ejecutar:
    python scripts/check_no_credentials.py            # el arbol de trabajo
    python scripts/check_no_credentials.py --history  # + todos los blobs alcanzables

Dos formas de vigilar, porque no todo lo que hay que encontrar tiene forma reconocible:

- **Patrones.** Un token de GitHub o una clave de AWS se delatan por su prefijo y su
  longitud. Con eso basta y no hay que saber cual es el valor.
- **Huellas.** Un GUID de inquilino o de aplicacion es indistinguible de cualquier otro
  GUID. Escribirlo en la lista para vigilarlo seria publicarlo el dia que el repositorio
  sea publico, asi que en `forbidden-digests.txt` va su SHA-256 y nunca el valor.

El informe **jamas reproduce lo que encuentra**: dice donde esta y cuanto mide. Un aviso
que copia el secreto a la consola y al log de CI lo ha filtrado una vez mas.
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_objects import (  # noqa: E402
    blob_texts, commit_identities, commit_messages, historical_paths, ref_texts)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGESTS_PATH = os.path.join(ROOT, "scripts", "forbidden-digests.txt")
ACCEPTED_PATH = os.path.join(ROOT, "scripts", "accepted-history.txt")

ETIQUETA_HUELLA = "valor vigilado por huella"

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}

# Los patrones se escriben para que su propio texto fuente no encaje con ellos: asi el
# guardia no necesita excluirse a si mismo, que es la excepcion que luego tapa una fuga.
PATTERNS = [
    ("PAT clasico de GitHub", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    ("token de GitHub (oauth, app o refresh)", re.compile(r"\bgh[ousr]_[A-Za-z0-9]{36}\b")),
    ("PAT de grano fino de GitHub", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("clave de acceso de AWS", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("token de Slack", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("clave de API de Google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("clave privada PEM", re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----")),
    # El secreto de cliente de Azure AD v2 lleva "8Q~" incrustado y ronda los 40 caracteres.
    ("secreto de cliente de Azure AD",
     re.compile(r"\b[A-Za-z0-9~._\-]{2,4}8Q~[A-Za-z0-9~._\-]{30,40}\b")),
    ("contrasena en cadena de conexion",
     re.compile(r"(?i)\b(?:password|pwd)\s*=\s*(?P<v>[^\s;,\"'<>&]{6,})")),
    ("secreto asignado en claro",
     re.compile(r"(?i)\b(?:client[_-]?secret|api[_-]?key|access[_-]?token|"
                r"secret[_-]?key)\s*[:=]\s*[\"']?(?P<v>[A-Za-z0-9~._\-+/]{20,})")),
    ("cabecera Authorization con token",
     re.compile(r"(?i)\bbearer\s+(?P<v>[A-Za-z0-9\-._~+/]{20,}={0,2})")),
]

# Lo que un ejemplo de documentacion tiene derecho a escribir. Sin esto la unica salida
# seria dejar de documentar como se ve una cadena de conexion.
#
# Son dos reglas y no una a proposito. Un marcador se reconoce por CONTENER su marca
# (`<...>`, `${...}`, `TU_`), pero palabras como "secret" o "token" aparecen dentro de
# valores autenticos, asi que solo valen cuando son el valor ENTERO: descartar todo lo
# que las contenga en algun sitio abriria un agujero del tamano de la mitad de los tokens.
PLACEHOLDER_CONTAINS = re.compile(
    r"(?i)<[^>]*>|\$\{|\$[A-Za-z_]|%[A-Za-z_]+%|\byour[_-]|\btu[_-]|_here\b|"
    r"ejemplo|example|placeholder|redact|dummy|sample|changeme|xxxx")
PLACEHOLDER_EXACT = re.compile(
    r"(?i)^[\W_]*(?:x+|\*+|\.+|-+|_+|password|contrasena|secret|token|"
    r"clave|key|value|valor|string|abc\d*|123\d*)[\W_]*$")


def _es_marcador(valor):
    return bool(PLACEHOLDER_CONTAINS.search(valor) or PLACEHOLDER_EXACT.match(valor))

# Un GUID, o cualquier cadena larga sin espacios, es candidato a comparar por huella.
CANDIDATO = re.compile(r"[A-Za-z0-9][A-Za-z0-9~._\-]{7,}")

# Un nombre vigilado casi nunca viaja solo. Aparece incrustado: en una rama
# (`issue-9-copiar-dax-lib-desde-<nombre>-con-su`), en una ruta, en un slug. Comparar solo
# el token entero dejaba pasar exactamente ese caso, que es el mas frecuente de todos.
#
# Asi que se comparan tambien los TRAMOS CONTIGUOS de sus segmentos. Sigue siendo huella
# contra huella: el valor vigilado no se escribe aqui ni en ningun otro sitio, y un tramo
# que no este en la lista no deja rastro. El limite de segmentos existe porque el numero de
# tramos crece con el cuadrado y una linea patologica no debe costar sin tope.
MAX_SEGMENTOS = 12
MIN_TRAMO = 8  # el mismo umbral que CANDIDATO: no se vigila nada mas corto


def tramos(token):
    """El token y cada tramo contiguo de sus segmentos, sin repetir.

    `a-b-c` produce `a-b-c`, `a-b`, `b-c` (y los sueltos, si llegan al minimo). El
    separador se conserva, de modo que el tramo reconstruye el texto original tal cual
    y su huella coincide con la del valor vigilado.
    """
    partes = re.split(r"([-_.])", token)
    segmentos = partes[::2]
    if len(segmentos) > MAX_SEGMENTOS:
        return
    vistos = set()
    for i in range(0, len(partes), 2):
        for j in range(i, len(partes), 2):
            tramo = "".join(partes[i:j + 1])
            if len(tramo) >= MIN_TRAMO and tramo not in vistos:
                vistos.add(tramo)
                yield tramo


def load_digests(path):
    """Un SHA-256 en hexadecimal por linea; blancos y # se ignoran.

    Una linea que no sea un digest es un error y no un aviso: significa que alguien pego
    el valor en vez de su huella, que es justo lo que este fichero existe para impedir.
    """
    out = set()
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not re.fullmatch(r"[0-9a-fA-F]{64}", line):
                raise ValueError(
                    f"{path}:{n} no es un SHA-256 hexadecimal. Este fichero guarda "
                    f"HUELLAS, nunca valores: use "
                    f"python -c \"import hashlib,sys;"
                    f"print(hashlib.sha256(sys.argv[1].lower().encode()).hexdigest())\" "
                    f"<valor>")
            out.add(line.lower())
    return out


def load_accepted(path):
    """SHAs de objetos historicos cuyos hallazgos POR HUELLA ya estan rendidos.

    Existe por una asimetria real entre las dos cosas que vigila este barrido:

    - Una **credencial** en la historia se arregla: se ROTA. El hallazgo es accionable, y
      por eso no se puede aceptar nunca — ningun SHA exime a un patron.
    - Un **nombre** en la historia no se rota. Una vez publicado no hay push que lo
      deshaga, y reescribir la historia tampoco: los objetos que dejan de estar
      referenciados siguen sirviendose por SHA. Lo unico que cabe hacer con el es rendir
      cuentas de donde esta.

    Sin esta distincion el guardia solo se podria satisfacer desactivandolo, que es
    exactamente como mueren los guardias. Con ella conserva los dientes para lo nuevo: un
    nombre que reaparezca lo hace en un objeto distinto, con un SHA que no esta aqui.

    El ARBOL no consulta esta lista. Ahi no hay nada que rendir: si el nombre esta en el
    arbol, se quita.
    """
    out = set()
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if not re.fullmatch(r"[0-9a-fA-F]{7,40}", line):
                raise ValueError(f"{path}:{n} no es un SHA de git.")
            out.add(line.lower())
    return out


def _aceptado(hit, sha, accepted):
    """Solo un hallazgo POR HUELLA y sobre un objeto rendido deja de contar."""
    if hit["label"] != ETIQUETA_HUELLA or not sha:
        return False
    sha = sha.lower()
    return any(sha.startswith(a) or a.startswith(sha) for a in accepted)


def _redact(line, start, end):
    """La linea con el hallazgo sustituido por su longitud. Nunca devuelve el valor."""
    largo = end - start
    fuera = f"{line[:start]}[REDACTADO {largo} caracteres]{line[end:]}"
    return fuera.strip()[:160]


def find_in_text(text, digests=frozenset()):
    """Genera un hallazgo por (linea, motivo). Ningun hallazgo contiene el valor."""
    for n, line in enumerate(text.splitlines(), 1):
        for label, rx in PATTERNS:
            for m in rx.finditer(line):
                valor = m.group("v") if "v" in rx.groupindex else m.group(0)
                if _es_marcador(valor):
                    continue
                yield {"line": n, "label": label,
                       "text": _redact(line, m.start(), m.end())}
        if digests:
            for m in CANDIDATO.finditer(line):
                for tramo in tramos(m.group(0)):
                    if hashlib.sha256(tramo.lower().encode()).hexdigest() in digests:
                        # Se tacha el candidato entero y no solo el tramo: senalar el
                        # tramo exacto seria decir cual de todos encajo, que es una pista
                        # sobre el valor vigilado en un log que puede ser publico.
                        yield {"line": n, "label": "valor vigilado por huella",
                               "text": _redact(line, m.start(), m.end())}
                        break


def scan_tree(root, digests, skip=frozenset()):
    """Hallazgos del arbol de trabajo. `skip` son rutas absolutas."""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if path in skip:
                continue
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            for h in find_in_text(text, digests):
                hits.append(dict(h, file=path))
    return hits


def scan_history(root, digests, skip=frozenset(), accepted=frozenset()):
    """Hallazgos de todos los blobs alcanzables Y de todos los mensajes de commit.

    Los mensajes se anadieron por el mismo motivo que las rutas, y el motivo
    es peor aqui: un token pegado por descuido en un mensaje de commit se publica igual que
    uno en un fichero, y ademas no se puede arreglar borrandolo — se rota. Un mensaje no es
    un blob ni tiene ruta, asi que recorrer blobs no lo veia. `skip` no le aplica: no hay
    ruta que eximir.
    """
    hits = []
    for sha, path, text in blob_texts(root, skip=skip):
        for h in find_in_text(text, digests):
            if not _aceptado(h, sha, accepted):
                hits.append(dict(h, path=path, blob=sha))
    for sha, message in commit_messages(root):
        for h in find_in_text(message, digests):
            if not _aceptado(h, sha, accepted):
                hits.append(dict(h, path=f"(mensaje del commit {sha[:9]})", blob=sha))
    for sha, quien in commit_identities(root):
        for h in find_in_text(quien, digests):
            if not _aceptado(h, sha, accepted):
                hits.append(dict(h, path=f"(identidad del commit {sha[:9]})", blob=sha))
    # Las RUTAS: su hermano de nombres las mira desde el principio y este no las miraba.
    # Un token en un nombre de fichero se publica igual, y GitHub lo pinta en el listado.
    for ruta in historical_paths(root):
        for h in find_in_text(ruta, digests):
            hits.append(dict(h, path=f"(ruta {ruta})", blob=""))
    for ref, texto in ref_texts(root):
        for h in find_in_text(texto, digests):
            hits.append(dict(h, path=f"(ref {ref})", blob=""))
    return hits


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    history = "--history" in argv
    digests = load_digests(DIGESTS_PATH) if os.path.exists(DIGESTS_PATH) else set()
    accepted = load_accepted(ACCEPTED_PATH)

    report = [(os.path.relpath(h["file"], ROOT).replace("\\", "/"), h)
              for h in scan_tree(ROOT, digests)]
    if history:
        report += [(f"{h['path']}@{h['blob'][:9]}", h)
                   for h in scan_history(ROOT, digests, accepted=accepted)]

    if report:
        print("CREDENTIAL CHECK FAILED — esto no puede llegar a un repositorio publico:")
        for where, h in report:
            print(f"  {where}:{h['line']}  [{h['label']}]  {h['text']}")
        print(f"\n{len(report)} hallazgo(s). Si alguno es real, lo primero no es borrarlo: "
              f"es ROTAR la credencial. Borrarla del arbol no la borra de la historia, y "
              f"borrarla de la historia no la borra de donde ya se haya copiado. "
              f"Si es un ejemplo de documentacion, use un marcador (<TU_CLAVE>).")
        return 1
    alcance = "arbol e historia" if history else "arbol"
    rendidos = (f", {len(accepted)} objetos historicos rendidos" if history and accepted
                else "")
    print(f"OK: sin credenciales en el {alcance} "
          f"({len(PATTERNS)} patrones, {len(digests)} huellas{rendidos}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
