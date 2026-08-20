## Trampa: devuelve el mes anterior **entero**, mires lo que mires

`PREVIOUSMONTH` no desplaza tu selección: la ignora, se ancla en la **primera** fecha del
contexto y devuelve el mes natural completo anterior a esa. Con un mes completo seleccionado
eso es lo que quieres. Con un mes a medias —el mes en curso, una quincena, un filtro de días
laborables— estás comparando un trozo contra un mes entero.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[Dias] = COUNTROWS(DimDate)
EVALUATE
VAR Quincena =
  CALCULATETABLE(VALUES(DimDate[Date]), ALL(DimDate),
                 DimDate[Year] = 2024, DimDate[Month] = 3, DimDate[DayOfMonth] <= 15)
RETURN
{
  ("periodo actual (1-15 mar 2024)", CALCULATE([Dias], Quincena),               CALCULATE([Ventas], Quincena)),
  ("PREVIOUSMONTH",                  CALCULATE([Dias], PREVIOUSMONTH(Quincena)), CALCULATE([Ventas], PREVIOUSMONTH(Quincena))),
  ("DATEADD -1 MONTH",               CALCULATE([Dias], DATEADD(Quincena, -1, MONTH)), CALCULATE([Ventas], DATEADD(Quincena, -1, MONTH)))
}
```

| periodo comparado | días | ventas |
|---|---|---|
| actual (1-15 mar 2024) | 15 | 436.666,83 |
| `PREVIOUSMONTH` | **29** ❌ | 802.337,00 |
| [`DATEADD(-1, MONTH)`](./dateadd.md) | **15** ✅ | 421.591,51 |

29 días, no 28: febrero de 2024 fue bisiesto. Ese detalle es la otra mitad del problema —
los meses no miden lo mismo, así que "mes anterior" nunca es una comparación limpia salvo que
los dos estén completos.

## A caballo entre dos meses devuelve el anterior al **primero**

Con la selección del 15 de febrero al 10 de marzo, "el mes anterior" no es febrero:

```dax
EVALUATE
VAR ACaballo =
  CALCULATETABLE(VALUES(DimDate[Date]), ALL(DimDate),
                 DimDate[Date] >= DATE(2024,2,15), DimDate[Date] <= DATE(2024,3,10))
VAR Prev = CALCULATETABLE(VALUES(DimDate[Date]), PREVIOUSMONTH(ACaballo))
RETURN
{
  ("contexto: min",       FORMAT(MINX(ACaballo, DimDate[Date]), "yyyy-MM-dd")),
  ("contexto: max",       FORMAT(MAXX(ACaballo, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: min",  FORMAT(MINX(Prev, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: max",  FORMAT(MAXX(Prev, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: días", FORMAT(COUNTROWS(Prev), "0"))
}
```

| | fecha |
|---|---|
| contexto, primera | 2024-02-15 |
| contexto, última | 2024-03-10 |
| `PREVIOUSMONTH`, primera | **2024-01-01** |
| `PREVIOUSMONTH`, última | **2024-01-31** |
| días devueltos | **31** |

Enero. Ni febrero ni marzo, los dos meses que el usuario tiene delante. Un rango que cruza el
cambio de mes —una selección de slicer, un "últimos 30 días"— convierte la comparación en algo
que nadie pidió, y sigue devolviendo un número.

## Dónde sí es la función correcta

Cuando el periodo actual **está cerrado**: un informe mensual del mes pasado, un acumulado a
cierre. Ahí `PREVIOUSMONTH` dice exactamente lo que quieres decir y se lee mejor que un
`DATEADD` con parámetros.

Para el mes en curso, la comparación honesta es mes-a-fecha contra mes-a-fecha, y eso lo da
`DATEADD` sobre las fechas seleccionadas.

## No confundir con
- [`DATEADD`](./dateadd.md) — desplaza la selección tal cual, sin completar el periodo.
- `PREVIOUSYEAR` / `PREVIOUSQUARTER` / `PREVIOUSDAY` — misma familia, mismo comportamiento de
  periodo completo.
- `DATESMTD` — el mes hasta la fecha del contexto, que es lo que suele querer decirse con
  "el mes en curso".

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
