## Trampa: la alternativa sale con CERO valores y con VARIOS, no solo con varios

`SELECTEDVALUE(col, alternativa)` devuelve el valor **solo si queda exactamente uno**. Con
ninguno y con dos o más devuelve la alternativa, que por defecto es blanco — así que una
tarjeta vacía no distingue "el usuario seleccionó varios" de "no hay nada seleccionado".

```dax
DEFINE
  MEASURE _Measures[sel] = SELECTEDVALUE(DimProduct[Color], "-- alternativa --")
  MEASURE _Measures[n] = COALESCE(COUNTROWS(VALUES(DimProduct[Color])), 0)
EVALUATE
UNION(
  CALCULATETABLE(ROW("caso","un valor",   "sel",[sel],"n",[n]), DimProduct[Color] = "Black"),
  CALCULATETABLE(ROW("caso","dos valores","sel",[sel],"n",[n]), DimProduct[Color] IN {"Black","White"}),
  CALCULATETABLE(ROW("caso","CERO valores","sel",[sel],"n",[n]), DimProduct[Color] = "NoExisteEsteColor")
)
```

| caso | nº de valores | SELECTEDVALUE |
|---|---|---|
| un valor | 1 | **Black** |
| dos valores | 2 | **-- alternativa --** |
| cero valores | 0 | **-- alternativa --** |

Si necesitas separar los dos casos, `HASONEVALUE` **no** sirve: es falso en ambos, que es
justo lo que hace que los dos devuelvan la alternativa. Y ojo al contar, porque `COUNTROWS`
sobre una tabla vacía devuelve **blanco, no cero**:

```dax
EVALUATE
CALCULATETABLE(
  ROW(
    "COUNTROWS",     COUNTROWS(VALUES(DimProduct[Color])),
    "es_blank",      ISBLANK(COUNTROWS(VALUES(DimProduct[Color]))),
    "con_COALESCE",  COALESCE(COUNTROWS(VALUES(DimProduct[Color])), 0),
    "ISEMPTY",       ISEMPTY(VALUES(DimProduct[Color]))
  ),
  DimProduct[Color] = "NoExisteEsteColor"
)
```

| expresión, con cero valores en el contexto | resultado |
|---|---|
| `COUNTROWS(VALUES(col))` | **(en blanco)** |
| `ISBLANK(COUNTROWS(...))` | TRUE |
| `COALESCE(COUNTROWS(...), 0)` | 0 |
| `ISEMPTY(VALUES(col))` | TRUE |

Por eso la consulta de arriba envuelve el conteo en `COALESCE`. Para preguntar "¿hay cero?",
`ISEMPTY` es más directo que contar.

## No confundir con
`VALUES`, que devuelve la tabla entera y da error al forzarla a escalar con más de una fila.
Microsoft
[recomienda SELECTEDVALUE](https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue)
para evitarlo; esa página no está en la ficha de la función.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
