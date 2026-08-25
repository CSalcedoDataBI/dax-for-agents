## Trampa: desplaza lo que hay seleccionado, no el periodo entero

`DATEADD` coge las fechas del contexto y las mueve. Si el contexto son 15 días, devuelve 15
días. Eso es justo lo que quieres para comparar mes a mes **en curso** — y es justo lo que
[`PREVIOUSMONTH`](./previousmonth.md) no hace, aunque en un mes completo los dos den lo mismo
y parezcan intercambiables.

Con la primera quincena de marzo de 2024 seleccionada:

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
  ("periodo actual (1-15 mar 2024)", CALCULATE([Dias], Quincena),                    CALCULATE([Ventas], Quincena)),
  ("DATEADD -1 MONTH",               CALCULATE([Dias], DATEADD(Quincena, -1, MONTH)), CALCULATE([Ventas], DATEADD(Quincena, -1, MONTH))),
  ("PREVIOUSMONTH",                  CALCULATE([Dias], PREVIOUSMONTH(Quincena)),      CALCULATE([Ventas], PREVIOUSMONTH(Quincena)))
}
```

| periodo comparado | días | ventas |
|---|---|---|
| actual (1-15 mar 2024) | 15 | 436.666,83 |
| `DATEADD(-1, MONTH)` | **15** | 421.591,51 ✅ comparable |
| `PREVIOUSMONTH` | **29** | 802.337,00 ❌ mes entero |

802.337 contra 436.666 no es una caída del 46%: es medio mes contra uno entero. El informe
no avisa, porque los dos números son correctos — lo que está mal es compararlos.

## Necesita una tabla de fechas de verdad

`DATEADD` exige una columna de fechas **continua**: sin huecos y con años completos. Sobre
una columna de fechas de la tabla de hechos devuelve resultados incompletos en los bordes, y
en algunos modelos ni siquiera avisa.

El primer periodo siempre sale **en blanco**, porque no hay nada antes que desplazar. Un
`Ventas YoY %` sobre el primer año del modelo es blanco, no cero, y eso es correcto: no hay
comparación que hacer.

## No confundir con
- [`SAMEPERIODLASTYEAR`](./sameperiodlastyear.md) — es `DATEADD(-1, YEAR)` con nombre propio.
- [`PREVIOUSMONTH`](./previousmonth.md) / `PREVIOUSYEAR` — periodo **completo** anterior.
- Sumar días a mano (`Fecha - 365`): pierde los años bisiestos y no alinea los días de la
  semana.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
