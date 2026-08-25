## Trampa: no encontrar es un error, no un blanco

`SEARCH` sin su cuarto argumento **falla la consulta** cuando el texto no aparece. Es el
mismo comportamiento de [`FIND`](./find.md) y sorprende igual, porque la intuición dice que
una búsqueda que no encuentra devuelve "nada".

```dax
EVALUATE
{
  ("SEARCH sony en 'Sony Bravia'", FORMAT(SEARCH("sony", "Sony Bravia", 1, -1), "0")),
  ("FIND sony en 'Sony Bravia'",   FORMAT(FIND("sony", "Sony Bravia", 1, -1), "0"))
}
```

| expresión | resultado |
|---|---|
| `SEARCH("sony", "Sony Bravia", 1, -1)` | **1** ← encontrado, insensible a mayúsculas |
| [`FIND`](./find.md)`("sony", "Sony Bravia", 1, -1)` | **-1** ← no encontrado, sensible |

Misma firma, misma posición de argumentos, respuesta contraria. Eso es lo que hace fácil
escribir una y pensar en la otra.

En una columna calculada el fallo es peor que en una medida: una sola fila sin coincidencia
tumba el refresco del modelo entero, y el mensaje apunta a la función, no a la fila.

## El cuarto argumento y el tercero

- `<start>` (tercero) empieza en **1**, no en 0. Un 0 da error.
- `<NotFoundValue>` (cuarto) es lo que convierte la búsqueda en algo utilizable:
  `SEARCH(texto, donde, 1, BLANK())` para un blanco, o `, 0)` si vas a comparar con `> 0`.

Para "¿aparece?" sin importar dónde, `CONTAINSSTRING` se lee mejor y no tiene el caso de
error.

## Admite comodines, y eso también sorprende

`SEARCH` interpreta `?` y `*`. Buscar literalmente esos caracteres exige escaparlos con `~`.
[`FIND`](./find.md) no los interpreta, así que para una búsqueda literal es la segura.

## No confundir con
- [`FIND`](./find.md) — sensible a mayúsculas, sin comodines.
- `CONTAINSSTRING` / `CONTAINSSTRINGEXACT` — devuelven booleano; la segunda es la sensible.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura y no toca el modelo. Se ejecuta y se compara sola con `python
> lab/check_lab.py contoso localhost:<puerto>`.
