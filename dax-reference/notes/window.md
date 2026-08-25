## Trampa: se corrigió la ventana, no el número que promedia

`WINDOW` recibe un `relation` explícito para no heredar el filtro por defecto sobre
`ALLSELECTED()` — la trampa que ya documenta [`dax-window-functions`](../../dax-window-functions/SKILL.md#the-gotchas-read-before-shipping).
Pero corregir la `relation` solo arregla **qué filas ve la ventana**. La métrica que
`AVERAGEX` promedia por cada fila se sigue evaluando por transición de contexto, y esa
transición **combina** con cualquier otro filtro que ya estuviera activo — no lo reemplaza.

Es la misma trampa de [`ALL`](./all.md) — *quita los filtros de su tabla, y solo esos* — un
piso más abajo, donde nadie mira: dentro de cada fila que `AVERAGEX` abre.

### El escenario: una media móvil de 3 meses, con año y mes filtrados a la vez

Cualquier informe con un slicer de `Year` y una matriz a nivel de `YearMonth` deja **los dos
filtros vivos a la vez** — aunque uno implique al otro. `Year = 2024` y `YearMonth = "2024-02"`
son redundantes, pero viven en columnas distintas de la misma tabla, y eso basta.

```dax
DEFINE
    FUNCTION Contoso.Lab.MediaMovil3M = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
            metric
        )
    FUNCTION Contoso.Lab.MediaMovil3M_Corregida = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            ADDCOLUMNS(
                WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
                "@p", periodCol
            ),
            VAR _cur = [@p]
            RETURN CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
        )
EVALUATE
CALCULATETABLE(
    ROW(
        "sin_filtro_de_Year_rota",      ROUND(Contoso.Lab.MediaMovil3M(DimDate, DimDate[YearMonth], [Total Sales]), 2),
        "sin_filtro_de_Year_corregida", ROUND(Contoso.Lab.MediaMovil3M_Corregida(DimDate, DimDate[YearMonth], [Total Sales]), 2)
    ),
    DimDate[YearMonth] = "2024-02"
)
```

| columna | resultado |
|---|---|
| `sin_filtro_de_Year_rota` | **805.753,73** |
| `sin_filtro_de_Year_corregida` | **805.753,73** |

Con solo el filtro de mes, las dos versiones coinciden: es el control. Ahora se añade el
filtro de año — redundante, y de la misma tabla:

```dax
DEFINE
    FUNCTION Contoso.Lab.MediaMovil3M = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
            metric
        )
    FUNCTION Contoso.Lab.MediaMovil3M_Corregida = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            ADDCOLUMNS(
                WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
                "@p", periodCol
            ),
            VAR _cur = [@p]
            RETURN CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
        )
EVALUATE
CALCULATETABLE(
    ROW(
        "con_filtro_Year2024_rota",      ROUND(Contoso.Lab.MediaMovil3M(DimDate, DimDate[YearMonth], [Total Sales]), 2),
        "con_filtro_Year2024_corregida", ROUND(Contoso.Lab.MediaMovil3M_Corregida(DimDate, DimDate[YearMonth], [Total Sales]), 2)
    ),
    DimDate[Year] = 2024,
    DimDate[YearMonth] = "2024-02"
)
```

| columna | resultado |
|---|---|
| `con_filtro_Year2024_rota` | **834.142,57** ❌ |
| `con_filtro_Year2024_corregida` | **805.753,73** ✅ |

Nada avisa. No hay error, no hay BLANK, no hay una fila de menos visible en ningún sitio: la
cifra rota es un número plausible, distinto del correcto por una fracción que cualquiera
firmaría sin mirar dos veces.

### Por qué

`ALL(dateTable)` dentro de `SUMMARIZE` sí construye la relación completa — las 24
combinaciones de `YearMonth`, incluido diciembre de 2023 — eso ya está comprobado, no es la
parte que falla:

```dax
EVALUATE
CALCULATETABLE(
  ROW("meses_visibles_con_ALL", COUNTROWS(SUMMARIZE(ALL(DimDate), DimDate[YearMonth]))),
  DimDate[Year] = 2024
)
```
Devuelve **24**, no 12: la relación de la ventana ignora el filtro de año, como se le pidió.

Lo que falla es el paso siguiente. `AVERAGEX` itera esa relación y, por cada fila, evalúa
`metric` — y evaluarla dispara transición de contexto: la fila (`YearMonth = "2023-12"`) se
convierte en un filtro que se **añade** al que ya había (`Year = 2024`), no lo sustituye. La
intersección de `YearMonth = "2023-12"` y `Year = 2024` no tiene filas, así que `[Total
Sales]` de esa fila da **BLANK** — y `AVERAGEX`, como `AVERAGE`, descarta los BLANK tanto del
numerador como del denominador. La ventana rota no promedia 3 meses: promedia los 2 que no
chocan con el filtro de fuera, en silencio.

```dax
EVALUATE
CALCULATETABLE(
  ROW("Diciembre_2023_bajo_Year_2024", CALCULATE([Total Sales], DimDate[YearMonth] = "2023-12")),
  DimDate[Year] = 2024
)
```
Da **BLANK**. Ahí está la fila que desapareció: 834.142,57 = (865.948,13 + 802.337,00) / 2 —
enero y febrero de 2024 solos, sin diciembre.

### El arreglo

No basta con `ALL` en la relación de `WINDOW`. Hay que **capturar el valor del período de
cada fila antes de entrar en `CALCULATE`** — con `ADDCOLUMNS` — y usarlo como el único filtro
sobre la tabla de fechas, después de quitarlos todos con `REMOVEFILTERS`:

```
CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
```

`REMOVEFILTERS(dateTable)` sí borra el `Year = 2024` que sobraba — pero si se escribiera sin
capturar antes el valor (`periodCol` a secas, dejando que la transición de contexto lo ponga),
`REMOVEFILTERS` **también se llevaría por delante ese mismo filtro** que la transición acaba
de crear, porque los dos viven sobre la misma tabla y `REMOVEFILTERS` no distingue cuál es
cuál. Materializar el valor con `ADDCOLUMNS` antes es lo que lo saca de la carrera.

### Cómo se llegó aquí

Cuatro consultas, en el orden en que un agente las usaría: **`dax-lib`** encontró
`TimeSeries.MovingAverage` (Tate Bowman, v0.1.1 — Simple, Weighted, Exponential y otras)
ya publicado para esto — pero
solo el índice, no el código, así que no bastaba por sí solo. **`dax-reference`** mostró que
`MOVINGAVERAGE` nativo es `appliesTo: [visual-calculation]` — no se puede llamar desde una
consulta ni desde una medida, así que quedaba fuera para este caso. **`dax-window-functions`**
dio el patrón real (`AVERAGEX` sobre `WINDOW`) y ya avisa del `ALLSELECTED` por defecto — la
media capa de esta trampa. **`dax-udf-authoring`** dio la mecánica para envolverlo en una
función reutilizable (`ANYREF EXPR`, parámetros opcionales). Escribir la versión propia con
esa guía — y medirla contra un filtro que un informe real sí pone — encontró la capa que
ninguna de las cuatro había escrito todavía: que `ALL`/`ALLSELECTED` en la `relation` no
protege el número que se promedia. Este archivo es esa capa.

## No confundir con
- [`ALL`](./all.md) — la misma trampa, un nivel más arriba: quita los filtros de su tabla, y
  solo esos. Aquí "su tabla" es la que ya se había filtrado por fuera.
- [`ALLSELECTED`](./allselected.md) — el otro lado del mismo problema: `WINDOW` sin
  `relation` explícito hereda `ALLSELECTED()` por defecto, que es donde empieza todo esto.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-24. La consulta es de
> solo lectura: define sus funciones con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
