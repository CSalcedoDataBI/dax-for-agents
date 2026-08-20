## Trampa: con la fecha del hecho el resultado sale en blanco, sin error

La función devuelve un conjunto de fechas desplazado un año, y ese conjunto filtra **la
columna que le pasaste**. Si le pasas la fecha de la tabla de hechos, el filtro cae sobre
`FactSales[OrderDate]` — mientras que el contexto del visual sigue filtrando `DimDate`. Las
dos condiciones tienen que cumplirse a la vez: fechas de 2023 en el hecho **y** 2024 en la
dimensión. No hay ninguna fila así, y el resultado es blanco.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[LY bien] = CALCULATE([Unidades], SAMEPERIODLASTYEAR(DimDate[Date]))
  MEASURE _Measures[LY mal]  = CALCULATE([Unidades], SAMEPERIODLASTYEAR(FactSales[OrderDate]))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]), "unidades", [Unidades],
             "LY_DimDate", [LY bien], "LY_FactSales", [LY mal]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2}
)
```

| mes | unidades | LY con DimDate | LY con FactSales |
|---|---|---|---|
| 2024-01 | 7.483 | **7.272** ✅ | **(en blanco)** ❌ |
| 2024-02 | 7.059 | **6.782** ✅ | **(en blanco)** ❌ |

Con `DimDate[Date]` el filtro desplazado sustituye al del propio contexto, porque cae sobre
la misma columna. Ese es el motivo por el que la familia entera pide la columna de la tabla
de fechas: no es una regla arbitraria, es que el filtro tiene que aterrizar donde ya está
filtrando el visual.

Una columna interanual entera en blanco casi siempre es esto, no falta de histórico.

**El blanco no es la única forma del fallo.** El mismo error con `DATESYTD` no devuelve
blanco: devuelve el valor del periodo **sin acumular**, que es más difícil de detectar porque
parece un número razonable. La consulta que lo mide está en
[`datesytd`](./datesytd.md) y da:

| mes | YTD con `DimDate[Date]` | YTD con `FactSales[OrderDate]` |
|---|---|---|
| 2024-01 | 7.483 | 7.483 |
| 2024-02 | **14.542** | **7.059** |
| 2024-03 | **22.520** | **7.978** |

`DATESYTD` no desplaza al año anterior, así que no hay contradicción que deje la intersección
vacía: el filtro simplemente cae en la columna equivocada y no acumula. Cada función de la
familia falla a su manera; lo común es la causa, no el síntoma.

## No confundir con
Que falte histórico. Comprueba a qué columna apunta la función; el dato suele estar.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
