## Trampa: sobre una tabla vacía devuelve **blanco**, y el blanco vale cero al compararlo

`MAXX` de nada no es cero: es `BLANK()`. Y como el blanco se convierte al tipo del otro
operando, `[Máximo] = 0` da verdadero — así que la comprobación con la que ibas a
protegerte no distingue "no hay filas" de "el máximo es cero".

```dax
EVALUATE
VAR Vacia = FILTER(DimProduct, DimProduct[Brand] = "NoExiste")
RETURN
{
  ("MAXX real sobre DimProduct", FORMAT(MAXX(DimProduct, DimProduct[Price]), "0.00")),
  ("filas de la tabla vacía",    IF(ISBLANK(COUNTROWS(Vacia)), "BLANK", FORMAT(COUNTROWS(Vacia), "0"))),
  ("MAXX sobre tabla vacía",     IF(ISBLANK(MAXX(Vacia, DimProduct[Price])), "BLANK", "algo")),
  ("MAXX + 0",                   FORMAT(MAXX(Vacia, DimProduct[Price]) + 0, "0.00")),
  ("MAXX = 0",                   IF(MAXX(Vacia, DimProduct[Price]) = 0, "IGUAL A CERO", "distinto")),
  ("MAXX == 0",                  IF(MAXX(Vacia, DimProduct[Price]) == 0, "IGUAL A CERO", "distinto"))
}
```

| expresión | resultado |
|---|---|
| `MAXX(DimProduct, [Price])` | 3.804,72 |
| `COUNTROWS(<tabla vacía>)` | **BLANK** ← no 0 |
| `MAXX(<tabla vacía>, [Price])` | **BLANK** |
| `MAXX(…) + 0` | 0,00 ← la suma convierte el blanco |
| `MAXX(…) = 0` | **IGUAL A CERO** ❌ |
| `MAXX(…) == 0` | distinto ✅ |

`COUNTROWS` también devuelve blanco, no cero, así que `IF(COUNTROWS(T) = 0, …)` sufre lo
mismo. Para preguntar de verdad si hay filas: `ISEMPTY(T)`, que responde a esa pregunta y no
a otra.

Ver [`blank`](./blank.md) para el mecanismo de conversión y la diferencia entre `=` y `==`.

## El máximo de columnas distintas no es `MAX` de la fila

`MAXX(T, expr)` recorre filas y devuelve el mayor de la expresión. Para el mayor **entre dos
columnas de la misma fila** la función es `MAXX` sobre un `{}` de valores, o directamente
`MAX(a, b)` con dos argumentos escalares — que es una sobrecarga distinta de la agregación
`MAX(columna)` y se confunde con ella.

## Ignora los blancos, no los cuenta como cero

Si la columna tiene blancos, `MAXX` los salta. Eso suele ser lo que quieres; deja de serlo
cuando el blanco significaba "cero" en el origen. Es la misma decisión que hay detrás de
[`AVERAGEX`](./averagex.md), y allí cambia el resultado mucho más.

## No confundir con
- `MAX(columna)` — la agregación simple, sin contexto de fila. Más barata y más clara.
- [`TOPN`](./topn.md) — te da la **fila** del máximo, no el valor.
- `MAXA` — la variante que trata `TRUE`/`FALSE` y el texto como números.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura y no toca el modelo. Se ejecuta y se compara sola con `python
> lab/check_lab.py contoso localhost:<puerto>`.
