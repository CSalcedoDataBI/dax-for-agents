"""Lo que devuelve cada consulta publicada en `dax-reference/notes/` sobre `lab/contoso`.

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
"""
NOTES = {
    "all": [
        (
            [
                (4301, 91795, 180224),
            ], 1,
        ),
    ],
    "allselected": [
        (
            [
                ('Sony', 1192, 8386, 2411),
                ('Apple', 1219, 8386, 2411),
            ], 2,
        ),
    ],
    "blank": [
        (
            [
                (20, True, False, True, False),
            ], 1,
        ),
    ],
    "calculate": [
        (
            [
                ('SUMX con la MEDIDA', 180224),
                ('SUMX con la EXPRESIÓN', 24690688),
                ('total real', 180224),
            ], 3,
        ),
    ],
    "concatenatex": [
        (
            [
                ('sin orderBy', 'Apple, Nintendo, Lutron, Microsoft, Sony'),
                ('orderBy ventas DESC', 'Sony, Microsoft, Nintendo, Lutron, Apple'),
                ('orderBy alfabético', 'Apple, Lutron, Microsoft, Nintendo, Sony'),
            ], 3,
        ),
    ],
    "count": [
        (
            [
                (None, 25, 25),
            ], 1,
        ),
    ],
    "countrows": [
        (
            [
                (25, None),
            ], 1,
        ),
    ],
    "dateadd": [
        (
            [
                ('periodo actual (1-15 mar 2024)', 15, 436666.83),
                ('DATEADD -1 MONTH', 15, 421591.51),
                ('PREVIOUSMONTH', 29, 802337),
            ], 3,
        ),
    ],
    "datesytd": [
        (
            [
                ('2024-01', 7483, 7483, None),
                ('2024-02', 7059, 14542, 7059),
                ('2024-03', 7978, 22520, 7059),
            ], 3,
        ),
        (
            [
                ('2024-01', 7483, 7483, 7483),
                ('2024-02', 7059, 14542, 7059),
                ('2024-03', 7978, 22520, 7978),
            ], 3,
        ),
    ],
    "divide": [
        (
            [
                (True, 0),
            ], 1,
        ),
    ],
    "earlier": [
        (
            [
                ('Electrónica', 'Dell', 46, 137),
                ('Electrónica', 'Microsoft', 46, 137),
                ('Electrónica', 'Acer', 46, 137),
                ('Electrónica', 'Lenovo', 46, 137),
                ('Electrónica', 'HP', 46, 137),
            ], 62,
        ),
    ],
    "filter": [
        (
            [
                (3450, None, 11102, None),
            ], 1,
        ),
    ],
    "find": [
        (
            [
                ('comparar sony con Sony', 'TRUE'),
                ('FIND sony en Sony Bravia', '-1'),
                ('SEARCH sony en Sony Bravia', '1'),
                ('filas filtrando en minuscula', '9'),
                ('filas filtrando en mayuscula', '9'),
            ], 5,
        ),
        (
            [
                ('filas con Brand = sony', 9),
                ('filas con Brand = sony', 9),
            ], 2,
        ),
    ],
    "format": [
        (
            [
                ('tipo de [Ventas]', 'NUMERO'),
                ('comparar 9 y 10 como texto', '9 va DESPUES de 10'),
                ('comparar 9 y 10 como número', '9 va ANTES de 10'),
                ('tipo de FORMAT([Ventas])', 'TEXTO'),
                ('FORMAT devuelve', '19.903.678'),
            ], 5,
        ),
    ],
    "lookupvalue": [
        (
            [
                ('filas con Brand = Sony', '9'),
                ('ProductName distintos entre ellas', '8'),
                ('LOOKUPVALUE de ProductName', 'SIN RESULTADO'),
                ('LOOKUPVALUE de Brand', 'Sony'),
                ('LOOKUPVALUE de CategoryName', 'SIN RESULTADO'),
            ], 5,
        ),
    ],
    "maxx": [
        (
            [
                ('MAXX real sobre DimProduct', '3804,72'),
                ('filas de la tabla vacía', 'BLANK'),
                ('MAXX sobre tabla vacía', 'BLANK'),
                ('MAXX + 0', '0,00'),
                ('MAXX = 0', 'IGUAL A CERO'),
            ], 6,
        ),
    ],
    "previousmonth": [
        (
            [
                ('periodo actual (1-15 mar 2024)', 15, 436666.83),
                ('PREVIOUSMONTH', 29, 802337),
                ('DATEADD -1 MONTH', 15, 421591.51),
            ], 3,
        ),
        (
            [
                ('contexto: min', '2024-02-15'),
                ('contexto: max', '2024-03-10'),
                ('PREVIOUSMONTH: min', '2024-01-01'),
                ('PREVIOUSMONTH: max', '2024-01-31'),
                ('PREVIOUSMONTH: días', '31'),
            ], 5,
        ),
    ],
    "rankx": [
        (
            [
                ('Sony', 1273417.32, 1, 1),
                ('Microsoft', 1164898.94, 1, 2),
                ('Nintendo', 1131477.23, 1, 3),
                ('Lutron', 1066213.09, 1, 4),
                ('Apple', 744415.28, 1, 5),
            ], 5,
        ),
    ],
    "related": [
        (
            [
                (1, 101201.01),
                (2, 123431.55),
                (3, 117268.74),
                (4, 133867.8),
                (5, 94498.88),
            ], 137,
        ),
    ],
    "relatedtable": [
        (
            [
                (1, 190),
                (2, 230),
                (3, 30),
                (4, 160),
                (5, 24),
            ], 137,
        ),
    ],
    "removefilters": [
        ("error", 'REMOVEFILTERS function cannot be used as a table expression. It can ap'),
        (
            [
                ('Apple', 744415.28, 0.11, 0.11, 0.04),
                ('Sony', 692829.8, 0.1, 0.1, 0.03),
                ('Jabra', 489943.26, 0.07, 0.07, 0.02),
            ], 3,
        ),
    ],
    "sameperiodlastyear": [
        (
            [
                ('2024-01', 7483, 7272, None),
                ('2024-02', 7059, 6782, None),
            ], 2,
        ),
    ],
    "search": [
        (
            [
                ("SEARCH sony en 'Sony Bravia'", '1'),
                ("FIND sony en 'Sony Bravia'", '-1'),
            ], 2,
        ),
    ],
    "selectedvalue": [
        (
            [
                ('un valor', 'Black', 1),
                ('dos valores', '-- alternativa --', 2),
                ('CERO valores', '-- alternativa --', 0),
            ], 3,
        ),
        (
            [
                (None, True, 0, True),
            ], 1,
        ),
    ],
    "sumx": [
        (
            [
                ('SUMX con la MEDIDA', 180224),
                ('SUMX con la EXPRESIÓN', 24690688),
            ], 2,
        ),
    ],
    "topn": [
        (
            [
                ('colores distintos', 15),
                ('TOPN 3 por N', 4),
                ('TOPN 5 por N', 6),
                ('TOPN 3 con desempate por Color', 3),
            ], 4,
        ),
    ],
    "values": [
        (
            [
                (1, 'USD', 'US Dollar', '$', 'en'),
                (2, 'EUR', 'Euro', '€', 'fr'),
            ], 2,
        ),
        (
            [
                ('un solo color', 'Black'),
            ], 1,
        ),
        ("error", "Calculation error in measure '_Measures'[forzado]: A table of multiple"),
    ],
}
