## Trampa: un filtro de fecha en el MISMO `CALCULATE` sobrevive al acumulado

`DATESYTD` devuelve las fechas desde el 1 de enero hasta el final del periodo actual. Es un
argumento de filtro más, así que convive con los otros argumentos del mismo `CALCULATE`: si
añades ahí una condición sobre la tabla de fechas, se **intersecta** con el rango del
acumulado y el resultado deja de acumular.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[YTD] = CALCULATE([Unidades], DATESYTD(DimDate[Date]))
  MEASURE _Measures[YTD con filtro de mes] =
    CALCULATE([Unidades], DATESYTD(DimDate[Date]), DimDate[Month] = 2)
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]), "unidades", [Unidades],
             "YTD", [YTD], "YTD_con_filtro_mes", [YTD con filtro de mes]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2,3}
)
```

| mes | unidades | YTD | YTD con filtro de mes |
|---|---|---|---|
| 2024-01 | 7.483 | **7.483** | (en blanco) |
| 2024-02 | 7.059 | **14.542** | 7.059 |
| 2024-03 | 7.978 | **22.520** | 7.059 |

El YTD correcto crece; el otro se queda clavado en febrero.

Lo medido aquí es el filtro escrito **dentro del mismo `CALCULATE`**. El filtro de fila del
propio visual (la columna `YearMonth`) no estorba: es lo que define "hasta cuándo" acumular,
y por eso la columna YTD sí avanza. La trampa está en añadir condiciones de fecha a mano
junto a la función, no en que el visual filtre.

## Trampa: con la fecha del hecho deja de acumular, sin avisar

Pasarle la fecha de la tabla de hechos en lugar de la de la tabla de fechas no da error ni
blanco: devuelve el valor del periodo **sin acumular**.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[YTD con DimDate]  = CALCULATE([Unidades], DATESYTD(DimDate[Date]))
  MEASURE _Measures[YTD con el hecho] = CALCULATE([Unidades], DATESYTD(FactSales[OrderDate]))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]),
             "unidades", [Unidades],
             "YTD_DimDate", [YTD con DimDate],
             "YTD_FactSales", [YTD con el hecho]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2,3}
)
ORDER BY DimDate[YearMonth]
```

| mes | unidades | `DATESYTD(DimDate[Date])` | `DATESYTD(FactSales[OrderDate])` |
|---|---|---|---|
| 2024-01 | 7.483 | 7.483 | 7.483 |
| 2024-02 | 7.059 | **14.542** | **7.059** |
| 2024-03 | 7.978 | **22.520** | **7.978** |

En enero coinciden, que es lo peor que podía pasar: si compruebas el primer mes, parece
correcto.

## No confundir con
Que la tabla de fechas esté incompleta. Ver también
[`SAMEPERIODLASTYEAR`](./sameperiodlastyear.md), donde el mismo error sí produce blanco: la
causa es la misma y el síntoma no.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
