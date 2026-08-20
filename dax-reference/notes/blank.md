## Trampa: `BLANK() = 0` es verdadero, y `BLANK() = ""` también

En una comparación, el blanco se convierte al tipo del otro operando. Así que un filtro
`[Importe] = 0` **también captura los blancos**, y `[Texto] = ""` captura los vacíos.

```dax
EVALUATE
ROW(
  "BLANK_mas_20",        BLANK() + 20,
  "BLANK_igual_0",       BLANK() = 0,
  "BLANK_estricto_0",    BLANK() == 0,
  "BLANK_igual_vacio",   BLANK() = "",
  "BLANK_estricto_vacio", BLANK() == ""
)
```

| expresión | resultado |
|---|---|
| `BLANK() + 20` | **20** |
| `BLANK() = 0` | **TRUE** |
| `BLANK() == 0` | **FALSE** |
| `BLANK() = ""` | **TRUE** |
| `BLANK() == ""` | **FALSE** |

Para distinguir "no hay dato" de "el dato es cero" tienes dos herramientas, y la diferencia
entre ellas es un solo carácter:

- **`==`** es la igualdad **estricta**: no convierte el blanco, así que `[Importe] == 0`
  deja fuera los blancos mientras que `[Importe] = 0` los mete.
- **`ISBLANK`** pregunta directamente por el blanco, y es lo que se lee mejor cuando esa es
  la pregunta.

Lo que no sirve es `= 0` a secas, que es justo lo que se escribe sin pensar.

## No confundir con
SQL. `NULL = 0` es desconocido en SQL; en DAX es verdadero. La analogía correcta es la
celda vacía de Excel, no `NULL`.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
