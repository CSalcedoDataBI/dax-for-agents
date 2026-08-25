## Trampa: distingue mayúsculas, y lo que la rodea no

`FIND` distingue mayúsculas. El operador `=`, los filtros del modelo y
[`SEARCH`](./search.md) —lo que tienes alrededor cuando escribes una— **no**. Así que la
misma comparación cambia de respuesta según con qué la escribas.

No es la única sensible: `CONTAINSSTRINGEXACT` y `EXACT` también lo son, y ese es justo el
problema. La sensibilidad no sigue una regla que se pueda deducir del nombre; va función por
función.

| función | ¿distingue mayúsculas? | medido con `sony` contra `Sony` |
|---|---|---|
| `=` (operador) | no | `TRUE` |
| [`SEARCH`](./search.md) | no | `1` (encontrado) |
| `CONTAINSSTRING` | no | `TRUE` |
| **`FIND`** | **sí** | `-1` (no encontrado) |
| **`CONTAINSSTRINGEXACT`** | **sí** | `FALSE` |
| **`EXACT`** | **sí** | `FALSE` |

```dax
EVALUATE
{
  ("comparar sony con Sony",       IF("sony" = "Sony", "TRUE", "FALSE")),
  ("filas filtrando en minuscula", FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "sony")), "0")),
  ("filas filtrando en mayuscula", FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "Sony")), "0")),
  ("FIND sony en Sony Bravia",     FORMAT(FIND("sony", "Sony Bravia", 1, -1), "0")),
  ("SEARCH sony en Sony Bravia",   FORMAT(SEARCH("sony", "Sony Bravia", 1, -1), "0"))
}
```

| expresión | resultado |
|---|---|
| `"sony" = "Sony"` | **TRUE** |
| `FILTER(DimProduct, Brand = "sony")` | **9 filas** |
| `FILTER(DimProduct, Brand = "Sony")` | **9 filas** |
| `FIND("sony", "Sony Bravia")` | **-1** ← no encontrado |
| [`SEARCH`](./search.md)`("sony", "Sony Bravia")` | **1** ← encontrado |

Las etiquetas de la consulta dicen "minúscula" y "mayúscula" en vez de `= "sony"` y
`= "Sony"` por lo mismo que estás leyendo. Con las etiquetas literales, esto:

```dax
EVALUATE { ("filas con Brand = sony", 9), ("filas con Brand = Sony", 9) }
```

devuelve **las dos filas** —no las junta— pero las dos salen impresas como
`filas con Brand = sony`: al ser iguales ignorando mayúsculas, el motor las devuelve con una
sola grafía, la primera que vio. Dos etiquetas idénticas en pantalla para dos filas
distintas, que es la trampa de esta nota enseñándose sola.

El filtro en minúscula devuelve las mismas 9 filas que en mayúscula: **el modelo no distingue
mayúsculas.** Solo `FIND` lo hace, y por eso es la que sorprende.

## Sin el cuarto argumento, no encontrar es un error

`FIND("sony", "Sony Bravia")` sin `<NotFoundValue>` no devuelve blanco: **falla la consulta.**

```
The search Text provided to function 'FIND' could not be found in the given text.
```

Un `-1` o un `BLANK()` como cuarto argumento convierte el error en un valor con el que se
puede seguir trabajando. En una columna calculada sobre miles de filas, una sola que no
coincida tumba el refresco entero.

## Cuándo quieres FIND

Casi nunca por su sensibilidad a mayúsculas, sino cuando esa sensibilidad **es** el requisito:
códigos donde `AB` y `ab` significan cosas distintas. Para buscar texto que escribió una
persona, [`SEARCH`](./search.md) es lo que esperas.

Y si lo que necesitas es "¿aparece?" sin la posición, `CONTAINSSTRINGEXACT` dice lo mismo con
menos ruido y sin el caso de error.

## No confundir con
- [`SEARCH`](./search.md) — misma firma, insensible a mayúsculas, y admite comodines.
- `CONTAINSSTRING` / `CONTAINSSTRINGEXACT` — devuelven booleano en vez de una posición; la
  primera es insensible, la segunda no.
- `EXACT` — compara dos cadenas enteras distinguiendo mayúsculas, no busca dentro de una.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura y no toca el modelo. Se ejecuta y se compara sola con `python
> lab/check_lab.py contoso localhost:<puerto>`.
