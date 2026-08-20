#!/usr/bin/env python3
"""Ejecuta las consultas del laboratorio y las compara con el resultado publicado.

Cada escenario declara sus consultas y lo que deben devolver. Si el número cambia, la
comprobación falla — así una nota deja de ser una afirmación y pasa a ser un test.

NO se ejecuta en CI, y es deliberado: hace falta un motor tabular con los datos cargados, y
CI no tiene Power BI Desktop. Es una herramienta local para el momento en que se toca un
escenario o se sospecha de una nota.

Uso:
    # abre lab/<escenario>/<Nombre>.pbip en Power BI Desktop, refresca, y luego:
    python lab/check_lab.py claves-huerfanas localhost:50409
    python lab/check_lab.py blancos          localhost:50542
    python lab/check_lab.py contoso          localhost:57190

    # sin puerto, busca las instancias locales de Power BI Desktop y las lista:
    python lab/check_lab.py claves-huerfanas

El escenario `contoso` ademas ejecuta la consulta de cada nota de campo y la compara con
`notes_expected.py`. Es lo que convierte «afirmacion con evidencia citada» en test.
"""
import glob
import os
import re
import sys

# {escenario: [(descripcion, consulta DAX, {columna: valor esperado})]}
CHECKS = {
    "claves-huerfanas": [
        (
            "de que lado se ve la fila en blanco",
            """
            EVALUATE
            ROW(
              "filas_en_DimProducto",       COUNTROWS(DimProducto),
              "VALUES_del_lado_UNO",        COUNTROWS(VALUES(DimProducto[ProductoKey])),
              "VALUES_del_lado_MUCHOS",     COUNTROWS(VALUES(Ventas[ProductoKey])),
              "ALLNOBLANKROW_del_lado_UNO", COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))
            )
            """,
            {
                "filas_en_DimProducto": 3,
                "VALUES_del_lado_UNO": 4,
                "VALUES_del_lado_MUCHOS": 4,
                "ALLNOBLANKROW_del_lado_UNO": 3,
            },
        ),
        (
            "limpiar la fila en blanco pierde las unidades huerfanas",
            """
            EVALUATE
            ROW(
              "total_Ventas",              SUM(Ventas[Unidades]),
              "suma_por_producto_visible", SUMX(VALUES(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades]))),
              "suma_sin_fila_en_blanco",   SUMX(ALLNOBLANKROW(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades])))
            )
            """,
            {
                "total_Ventas": 110,
                "suma_por_producto_visible": 110,
                "suma_sin_fila_en_blanco": 60,
            },
        ),
        (
            "las medidas de las tres paginas",
            """
            EVALUATE
            ROW(
              "Productos",         [Productos],
              "lado_uno",          [Valores del lado uno],
              "lado_muchos",       [Valores del lado muchos],
              "sin_fila_blanco",   [Productos sin fila en blanco],
              "total",             [Unidades],
              "suma_por_producto", [Suma por producto],
              "suma_sin_blanco",   [Suma sin fila en blanco]
            )
            """,
            {
                "Productos": 3,
                "lado_uno": 4,
                "lado_muchos": 4,
                "sin_fila_blanco": 3,
                "total": 110,
                "suma_por_producto": 110,
                "suma_sin_blanco": 60,
            },
        ),
    ],
    "blancos": [
        (
            "AVERAGE y AVERAGEX saltan el blanco; SUM/COUNTROWS no",
            """
            EVALUATE
            ROW(
              "AVERAGE",             AVERAGE(Tiendas[Metros]),
              "AVERAGEX",            AVERAGEX(Tiendas, Tiendas[Metros]),
              "SUM_entre_COUNTROWS", DIVIDE(SUM(Tiendas[Metros]), COUNTROWS(Tiendas))
            )
            """,
            {"AVERAGE": 200, "AVERAGEX": 200, "SUM_entre_COUNTROWS": 120},
        ),
        (
            "un + 0 mueve el denominador de 3 a 5",
            """
            EVALUATE
            ROW(
              "AVERAGEX_columna",      AVERAGEX(Tiendas, Tiendas[Metros]),
              "AVERAGEX_con_COALESCE", AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0)),
              "AVERAGEX_con_mas_cero", AVERAGEX(Tiendas, Tiendas[Metros] + 0)
            )
            """,
            {
                "AVERAGEX_columna": 200,
                "AVERAGEX_con_COALESCE": 120,
                "AVERAGEX_con_mas_cero": 120,
            },
        ),
        # Lo de arriba comprueba el DAX; esto comprueba las MEDIDAS, que es lo que la
        # pagina dibuja. No es la misma afirmacion: una medida puede estar escrita de otra
        # forma, o renombrada, y el informe seguiria ensenando un numero que nadie mide.
        (
            "las medidas de la pagina mas-cero",
            """
            EVALUATE
            ROW(
              "AVERAGEX",  [Media con AVERAGEX],
              "COALESCE",  [Media con COALESCE],
              "mas_cero",  [Media con mas cero]
            )
            """,
            {"AVERAGEX": 200, "COALESCE": 120, "mas_cero": 120},
        ),
        (
            "las medidas de la pagina denominador",
            """
            EVALUATE
            ROW(
              "Media",        [Media],
              "MediaTodas",   [Media por todas las filas],
              "Filas",        [Filas],
              "FilasMetros",  [Filas con metros]
            )
            """,
            {"Media": 200, "MediaTodas": 120, "Filas": 5, "FilasMetros": 3},
        ),
    ],
    # Aqui se comprueban los VALORES, no los tiempos. Un umbral en milisegundos dentro de
    # un test seria una promesa falsa: depende de la maquina. Lo que si tiene que seguir
    # siendo cierto es que las dos formas de cada par devuelven lo mismo — sin eso,
    # comparar sus tiempos no significa nada, y el escenario entero deja de sostenerse.
    "rendimiento": [
        (
            "el modelo trae los dos millones de filas",
            """
            EVALUATE
            ROW(
              "filas",      COUNTROWS(Ventas),
              "categorias", DISTINCTCOUNT(Ventas[CategoriaKey]),
              "total",      SUM(Ventas[Importe])
            )
            """,
            {"filas": 2000000, "categorias": 20, "total": 1001000000},
        ),
        (
            "grupo A: las tres formas que el motor resuelve igual dan lo mismo",
            """
            EVALUATE
            ROW(
              "A1_FILTER",           [Alto FILTER],
              "A1_predicado",        [Alto predicado],
              "A2_por_tabla",        [Categoria por tabla],
              "A2_por_columna",      [Categoria por columna],
              "A3_cruce_por_tabla",  [Cruce por tabla],
              "A3_cruce_por_columnas", [Cruce por columnas]
            )
            """,
            {
                "A1_FILTER": 190100000,
                "A1_predicado": 190100000,
                "A2_por_tabla": 50900000,
                "A2_por_columna": 50900000,
                "A3_cruce_por_tabla": 642600000,
                "A3_cruce_por_columnas": 642600000,
            },
        ),
        (
            "grupo B: la version cara devuelve lo mismo que la barata",
            """
            EVALUATE
            ROW(
              "B1_con_medida",  [Suma con medida],
              "B1_con_columna", [Suma con columna],
              "B2_con_medida",  [Alto con medida],
              "B2_predicado",   [Alto predicado]
            )
            """,
            {
                "B1_con_medida": 1001000000,
                "B1_con_columna": 1001000000,
                "B2_con_medida": 190100000,
                "B2_predicado": 190100000,
            },
        ),
        # La tabla Tiempos no calcula nada: es la medicion, versionada. Comprobarla no
        # comprueba que los tiempos sean ciertos --eso lo dijo el cronometro-- sino que el
        # dato que grafica la pagina sigue siendo el que se midio y no otro.
        (
            "la tabla Tiempos trae las cuatro medianas medidas",
            """
            EVALUATE
            ROW(
              "casos",       COUNTROWS(Tiempos),
              "ms_maximo",   MAX(Tiempos[MedianaMs]),
              "ms_minimo",   MIN(Tiempos[MedianaMs]),
              "memoria_max", MAX(Tiempos[PicoMemoriaKB])
            )
            """,
            {"casos": 4, "ms_maximo": 873, "ms_minimo": 3, "memoria_max": 197342},
        ),
    ],
    # Contoso no demuestra ninguna trampa por si mismo: es el modelo contra el que se
    # midieron 29 de las 30 notas, y esta en el repo para que esas notas se puedan
    # EJECUTAR. Lo que se comprueba aqui es que el modelo es el que dicen sus pies; las
    # consultas de las notas van aparte, en run_notes().
    "contoso": [
        (
            "el modelo es el que declara el pie de las notas",
            """
            EVALUATE
            ROW(
              "filas_FactSales", COUNTROWS(FactSales),
              "productos",       COUNTROWS(DimProduct),
              "fecha_min",       FORMAT(MIN(DimDate[Date]), "yyyy-mm-dd"),
              "fecha_max",       FORMAT(MAX(DimDate[Date]), "yyyy-mm-dd"),
              "unidades",        SUM(FactSales[Quantity])
            )
            """,
            {
                "filas_FactSales": 126524,
                "productos": 137,
                "fecha_min": "2023-01-01",
                "fecha_max": "2024-12-31",
                "unidades": 180224,
            },
        ),
            # Estas montan las trampas VISUALES, y por eso se comprueban antes de dibujarlas:
        # si una no hace lo que se cree, se descubre aqui y no en la pagina trece.
        (
            "las medidas de las paginas de informe",
            """
            EVALUATE
            ROW(
              "rank_matriz_distintos", COUNTROWS(DISTINCT(
                  SELECTCOLUMNS(VALUES(DimProduct[Brand]), "r", [Ranking en la matriz]))),
              "rank_bien_distintos",   COUNTROWS(DISTINCT(
                  SELECTCOLUMNS(VALUES(DimProduct[Brand]), "r", [Ranking bien]))),
              "marca_sin_seleccion",   [Marca seleccionada],
              "suma_con_columna",      ROUND([Suma con columna], 2)
            )
            """,
            # rank_matriz_distintos = 1 ES la afirmacion entera: un solo valor de ranking
            # distinto en todas las marcas. rank_bien_distintos y suma_con_columna se
            # ejecutan para que un error las rompa, pero no se afirma su valor: dependen de
            # cuantas marcas tenga el modelo y de una cifra con decimales.
            {
                "rank_matriz_distintos": 1,
                "marca_sin_seleccion": "(sin un valor unico)",
            },
        ),
        # El supuesto del que depende la pagina del blanco contra el cero, y que estuvo a
        # punto de tumbarla: sin acotar la fecha, las 58 marcas venden TODAS y los dos
        # graficos salen identicos. Un mes deja solo 4 huecos; una semana deja 14, y ese
        # contraste si se ve. Si el 14 cambia, la pagina deja de ensenar lo que dice.
        (
            "en la semana del 26 de agosto hay 14 marcas sin ventas",
            """
            EVALUATE
            VAR ConMargen =
                ADDCOLUMNS(
                    VALUES(DimProduct[Brand]),
                    "divide", [Margen de una semana con DIVIDE],
                    "cero",   [Margen de una semana con cero]
                )
            RETURN
            ROW(
              "marcas",          COUNTROWS(VALUES(DimProduct[Brand])),
              "en_blanco",       COUNTROWS(FILTER(ConMargen, ISBLANK([divide]))),
              "con_cero_blanco", COUNTROWS(FILTER(ConMargen, ISBLANK([cero])))
            )
            """,
            {"marcas": 58, "en_blanco": 14, "con_cero_blanco": None},
        ),
    ],
}


# Rutas donde vive la DLL de ADOMD.NET. `pip install pyadomd` NO basta: el paquete es un
# puente a .NET y necesita encontrar el ensamblado, que instalan Power BI Desktop y SSMS.
# Sin esto el import falla con un mensaje que no dice cual de las dos cosas falta.
ADOMD_GLOBS = [
    r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.AnalysisServices.AdomdClient\*",
    r"C:\Program Files\Microsoft.NET\ADOMD.NET\*",
    r"C:\Program Files (x86)\Microsoft.NET\ADOMD.NET\*",
]


def connect(data_source):
    """Devuelve una conexion pyadomd, poniendo antes ADOMD.NET en sys.path."""
    for pattern in ADOMD_GLOBS:
        for path in sorted(glob.glob(pattern), reverse=True):
            if path not in sys.path:
                sys.path.append(path)
    try:
        from pyadomd import Pyadomd
    except ImportError:
        print("ERROR: falta pyadomd (pip install pyadomd) o el proveedor ADOMD.NET.\n"
              "El proveedor lo instalan Power BI Desktop y SSMS; no viene con pip.\n"
              "Alternativa sin dependencias: pega las consultas del README del escenario en\n"
              "la vista de consulta DAX de Power BI Desktop y compara a mano.", file=sys.stderr)
        raise
    return Pyadomd(f"Provider=MSOLAP;Data Source={data_source};")


def run(scenario, data_source):
    try:
        connect(data_source)
    except ImportError:
        return 2

    failures = 0
    for label, query, expected in CHECKS[scenario]:
        with connect(data_source) as c:
            with c.cursor().execute(query) as cur:
                names = [d.name.strip("[]") for d in cur.description]
                row = dict(zip(names, next(iter(cur.fetchall()))))
        bad = {k: (row.get(k), v) for k, v in expected.items() if row.get(k) != v}
        if bad:
            failures += 1
            print(f"FALLA  {label}")
            for k, (got, want) in bad.items():
                print(f"       {k}: obtuvo {got!r}, esperaba {want!r}")
        else:
            print(f"ok     {label}")
    return 1 if failures else 0


def run_notes(data_source):
    """Ejecuta la consulta de cada nota y la compara con `notes_expected.py`.

    La consulta se lee del propio .md, no se copia aqui: si alguien la edita, lo que corre
    es la version editada, y el esperado que ya no cuadre sale rojo. Es justo lo que se
    quiere — una nota cuyo numero dejo de salir del motor esta mintiendo.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from notes_expected import NOTES
    from dump_notes import NOTES_DIR, dax_blocks, round_value

    failures = 0
    for name in sorted(NOTES):
        blocks = dax_blocks(os.path.join(NOTES_DIR, name + ".md"))
        expected = NOTES[name]
        if len(blocks) != len(expected):
            failures += 1
            print(f"FALLA  {name}: la nota tiene {len(blocks)} consulta(s) y "
                  f"notes_expected.py espera {len(expected)}. Regenera con dump_notes.py.")
            continue
        for i, (query, want) in enumerate(zip(blocks, expected)):
            tag = f"{name}[{i}]" if len(blocks) > 1 else name
            try:
                with connect(data_source) as c:
                    with c.cursor().execute(query) as cur:
                        rows = [tuple(round_value(v) for v in r) for r in cur.fetchall()]
                got = (rows[:5], len(rows))
            except Exception as e:
                got = ("error", re.sub(r"^Query \(\d+, \d+\) ", "",
                                       str(e).splitlines()[0]).strip()[:70])
            # Un esperado ("error", ...) se cumple si el motor aborta con ESE mensaje. Si
            # la consulta pasa a devolver filas, la nota que publica el error esta obsoleta.
            if isinstance(want, tuple) and want and want[0] == "error":
                ok = isinstance(got, tuple) and got[0] == "error" and want[1] in got[1]
            else:
                ok = got == tuple(want)
            if ok:
                print(f"ok     {tag}")
            else:
                failures += 1
                print(f"FALLA  {tag}")
                print(f"       esperaba {want!r}")
                print(f"       obtuvo   {got!r}")
    return failures


def run_examples(data_source, model="contoso"):
    """Ejecuta los ejemplos de `dax-reference/examples/` y los compara con su bloque result.

    `model` dice QUE escenario esta abierto en `data_source`. Se ejecuta lo que declara ese
    modelo y lo que declara `ninguno` —aritmetica, texto, logica— que corre contra cualquier
    motor. Lo demas se salta y se dice cuanto, para que un «todo verde» sobre un solo modelo
    no se lea como cobertura completa.
    """
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "scripts"))
    import examples_io as exio

    failures = saltados = corridos = 0
    for path in exio.example_files():
        fm, pairs = exio.parse(path)
        rel = os.path.relpath(path, exio.ROOT).replace("\\", "/")
        declared = fm.get("model", exio.NO_MODEL)
        if declared not in (exio.NO_MODEL, model):
            saltados += 1
            continue
        for i, (query, want) in enumerate(pairs, 1):
            corridos += 1
            if want is None:
                failures += 1
                print(f"FALLA  {rel} [{i}]: consulta sin bloque result")
                continue
            try:
                with connect(data_source) as c:
                    with c.cursor().execute(query) as cur:
                        got = exio.render_result([d.name for d in cur.description],
                                                 cur.fetchall())
            except Exception as e:
                got = exio.render_error(e)
            if got == want:
                print(f"ok     {rel} [{i}]")
            else:
                failures += 1
                print(f"FALLA  {rel} [{i}]")
                for line in ("esperaba:\n" + want).splitlines():
                    print(f"       {line}")
                for line in ("obtuvo:\n" + got).splitlines():
                    print(f"       {line}")
    print(f"\n{corridos} consulta(s) ejecutadas, {failures} falla(s), "
          f"{saltados} fichero(s) saltados por pedir otro modelo.")
    return failures


def local_instances():
    """Puertos de las instancias locales de Power BI Desktop, leyendo su propio rastro.

    Cada ventana abierta deja un workspace bajo AppData con un fichero que contiene el
    puerto en texto plano. Es lo mismo que consultan las herramientas externas, y evita
    depender de una de ellas solo para averiguar un numero.
    """
    import socket
    local = os.environ.get("LOCALAPPDATA", "")
    tail = os.path.join("Microsoft", "Power BI Desktop", "AnalysisServicesWorkspaces",
                        "*", "Data", "msmdsrv.port.txt")
    # Dos instalaciones posibles y dos rutas distintas: la del instalador (MSI) y la de la
    # Microsoft Store, que vive dentro del sandbox del paquete. Mirar solo la primera hace
    # que el modo sin puerto diga "no hay nada abierto" con Power BI Desktop delante.
    patterns = [
        os.path.join(local, tail),
        os.path.join(local, "Packages", "Microsoft.MicrosoftPowerBIDesktop_*",
                     "LocalCache", "Local", tail),
    ]
    ports = []
    for path in [p for pattern in patterns for p in glob.glob(pattern)]:
        try:
            with open(path, encoding="utf-16-le") as f:
                text = f.read()
        except (OSError, UnicodeError):
            continue
        found = re.search(r"\d{3,5}", text)
        if not found:
            continue
        # Una ventana cerrada deja su carpeta atras, asi que el fichero sigue ahi con un
        # puerto que ya no escucha. Sin esta comprobacion la lista es mayormente ruido.
        with socket.socket() as probe:
            probe.settimeout(0.2)
            if probe.connect_ex(("127.0.0.1", int(found.group(0)))) == 0:
                ports.append(found.group(0))
    return sorted(set(ports))


def main(argv):
    # `examples` no es un escenario del laboratorio: es un modo que recorre
    # dax-reference/examples/ contra el escenario que ya tengas abierto.
    if len(argv) > 1 and argv[1] == "examples":
        if len(argv) < 3:
            print(f"Uso: {argv[0]} examples <servidor:puerto> [modelo abierto]",
                  file=sys.stderr)
            return 2
        return 1 if run_examples(argv[2], argv[3] if len(argv) > 3 else "contoso") else 0

    if len(argv) < 2 or argv[1] not in CHECKS:
        print(f"Uso: {argv[0]} <{' | '.join(CHECKS)} | examples> [servidor:puerto]",
              file=sys.stderr)
        return 2
    scenario = argv[1]
    if len(argv) > 2:
        failures = run(scenario, argv[2])
        if scenario == "contoso" and failures == 0:
            print("--- consultas de las notas de campo ---")
            failures = 1 if run_notes(argv[2]) else 0
        return failures

    ports = local_instances()
    if not ports:
        print(f"No hay ninguna instancia local de Power BI Desktop abierta.\n"
              f"Abre lab/{scenario}/*.pbip, refresca, y vuelve a ejecutar.", file=sys.stderr)
        return 2
    print("Instancias locales encontradas (no se sabe cual es cual, prueba la que toque):",
          file=sys.stderr)
    for port in ports:
        print(f"    python {argv[0]} {scenario} localhost:{port}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
