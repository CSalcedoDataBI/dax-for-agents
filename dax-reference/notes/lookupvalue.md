## Trampa: el argumento de "no encontrado" también se traga los valores en conflicto

`LOOKUPVALUE` falla cuando las filas que encuentra no coinciden **en el valor que le pides**.
El cuarto argumento, `<alternateResult>`, existe para el caso de "no hay coincidencia" — pero
**también** se devuelve en ese conflicto. Los dos casos salen por la misma puerta y no se
distinguen.

Lo que decide no es cuántas filas coinciden, sino cuántos **valores distintos** devuelven:

```dax
EVALUATE
{
  ("filas con Brand = Sony",              FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "Sony")), "0")),
  ("ProductName distintos entre ellas",   FORMAT(COUNTROWS(CALCULATETABLE(VALUES(DimProduct[ProductName]), DimProduct[Brand] = "Sony")), "0")),
  ("LOOKUPVALUE de ProductName",          LOOKUPVALUE(DimProduct[ProductName], DimProduct[Brand], "Sony", "SIN RESULTADO")),
  ("LOOKUPVALUE de Brand",                LOOKUPVALUE(DimProduct[Brand], DimProduct[Brand], "Sony", "SIN RESULTADO")),
  ("LOOKUPVALUE de CategoryName",         LOOKUPVALUE(DimProduct[CategoryName], DimProduct[Brand], "Sony", "SIN RESULTADO"))
}
```

| expresión | resultado |
|---|---|
| filas con `Brand = "Sony"` | **9** |
| `ProductName` distintos entre ellas | **8** |
| `LOOKUPVALUE(ProductName, Brand, "Sony", …)` | **`SIN RESULTADO`** ❌ 8 valores en conflicto |
| `LOOKUPVALUE(Brand, Brand, "Sony", …)` | **`Sony`** ✅ 9 filas, un solo valor |
| `LOOKUPVALUE(CategoryName, Brand, "Sony", …)` | **`SIN RESULTADO`** ❌ Sony está en varias categorías |

La cuarta fila es la que rompe la intuición: **nueve filas coinciden y aun así devuelve un
valor**, porque las nueve dicen lo mismo. Y la tercera es la peligrosa: hay 9 productos Sony,
la respuesta correcta no es "sin resultado" sino "la pregunta está mal planteada", y el
informe enseña lo segundo como si fuera lo primero.

(9 filas y 8 nombres: dos productos Sony comparten `ProductName`. En un modelo de verdad esas
cosas están.)

Sin el cuarto argumento la misma expresión falla, y el mensaje es claro:

```
A table of multiple values was supplied where a single value was expected.
```

Que es más útil que un `SIN RESULTADO` silencioso. **Poner `alternateResult` sin estar seguro
de que el valor es único convierte un error en un dato falso.**

## Cómo usarlo con red

- Búsqueda por clave única → `LOOKUPVALUE` sin cuarto argumento, y que reviente si el modelo
  cambia.
- Búsqueda que puede no encontrar nada → cuarto argumento, pero **solo** si sabes que no puede
  haber conflicto.
- Búsqueda que puede devolver valores distintos → no es un lookup. Es una agregación:
  [`MAXX`](./maxx.md) o `MINX`, [`CONCATENATEX`](./concatenatex.md) o
  [`SELECTEDVALUE`](./selectedvalue.md), que dice qué hacer con el empate.

## No confundir con
- [`RELATED`](./related.md) — sigue una relación existente y es más barato. `LOOKUPVALUE` no
  necesita relación, y por eso se usa donde debería haberla.
- [`SELECTEDVALUE`](./selectedvalue.md) — un valor del contexto actual, con salida explícita
  para el caso de varios.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura y no toca el modelo. Se ejecuta y se compara sola con `python
> lab/check_lab.py contoso localhost:<puerto>`.
