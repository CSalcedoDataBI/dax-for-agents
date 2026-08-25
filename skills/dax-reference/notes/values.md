## Trampa: sobre una COLUMNA devuelve una columna; sobre una TABLA devuelve la tabla

`VALUES` tiene dos formas y solo una da algo convertible a escalar:

- `VALUES(tabla[columna])` → una tabla de **una** columna.
- `VALUES(tabla)` → las filas de la tabla, con **todas** sus columnas.

```dax
EVALUATE TOPN(2, VALUES(DimCurrency))
```

devuelve 5 columnas (`CurrencyKey`, `CurrencyCode`, `CurrencyName`, `Symbol`, `Language`),
no una.

La conversión automática a escalar solo ocurre con una tabla de **una columna y una fila**.
`VALUES(DimCurrency)` nunca la cumple porque la tabla tiene cinco columnas; una tabla de una
sola columna sí podría. Con la forma de columna depende del contexto:

La medida fuerza la conversión concatenando, que es lo que hace cualquier expresión que
espera un escalar. Son **dos consultas**, porque la segunda no llega a devolver tabla: aborta.

```dax
-- 1. un solo color -> devuelve "Black"
DEFINE MEASURE _Measures[forzado] = VALUES(DimProduct[Color]) & ""
EVALUATE
CALCULATETABLE(ROW("caso", "un solo color", "forzado", [forzado]),
               DimProduct[Color] = "Black")
```

```dax
-- 2. dos colores -> la consulta falla
DEFINE MEASURE _Measures[forzado] = VALUES(DimProduct[Color]) & ""
EVALUATE
CALCULATETABLE(ROW("caso", "dos colores", "forzado", [forzado]),
               DimProduct[Color] IN {"Black", "White"})
```

| contexto | resultado |
|---|---|
| un solo color | **`Black`** — la conversión funciona |
| dos colores | **error**: *A table of multiple values was supplied where a single value was expected* |

El segundo caso no devuelve un valor raro: **aborta la consulta**. Y aparece solo cuando el
usuario amplía la selección, así que pasa las pruebas con un color y falla en producción con
dos.

## No confundir con
[`SELECTEDVALUE`](./selectedvalue.md), que es este patrón ya resuelto y sin error.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
