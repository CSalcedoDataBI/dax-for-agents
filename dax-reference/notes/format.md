## Trampa: devuelve **texto**, y el texto ordena por caracteres

`FORMAT` no cambia cómo se ve un número: lo convierte en una cadena. A partir de ahí no se
suma, no se compara como número, y el visual lo ordena alfabéticamente — donde el 9 va
después del 10.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[VentasTexto] = FORMAT([Ventas], "#,##0")
EVALUATE
{
  ("tipo de [Ventas]",            IF(ISTEXT([Ventas]), "TEXTO", "NUMERO")),
  ("tipo de FORMAT([Ventas])",    IF(ISTEXT([VentasTexto]), "TEXTO", "NUMERO")),
  ("FORMAT devuelve",             [VentasTexto]),
  ("comparar 9 y 10 como texto",  IF("9" > "10", "9 va DESPUES de 10", "9 va ANTES de 10")),
  ("comparar 9 y 10 como número", IF(9 > 10, "9 va DESPUES de 10", "9 va ANTES de 10"))
}
```

| expresión | resultado |
|---|---|
| tipo de `[Ventas]` | NUMERO |
| tipo de `FORMAT([Ventas])` | **TEXTO** |
| `FORMAT([Ventas], "#,##0")` | `19.903.678` |
| `"9" > "10"` | **9 va DESPUES de 10** ❌ |
| `9 > 10` | 9 va ANTES de 10 ✅ |

Ordenar por esa columna coloca `9.500` detrás de `10.200`, y el eje de un gráfico, el formato
condicional o cualquier medida que la use en una resta dejan de funcionar: esperan un número
y reciben una cadena.

**El total no avisa.** Una medida es una expresión, así que en la fila de totales se vuelve a
evaluar en el contexto del total y devuelve el total formateado:

| fila | `[Ventas]` | `FORMAT([Ventas], "#,##0")` |
|---|---|---|
| Sony | 1.273.417,32 | `1.273.417` |
| Microsoft | 1.164.898,94 | `1.164.899` |
| **TOTAL** | 19.903.677,62 | **`19.903.678`** ← correcto |

Ese total correcto es lo que hace que el problema tarde en aparecer: la tabla se ve bien, y lo
que falla es el orden, el eje o el condicional, que nadie relaciona con el formato.

## Lo que casi siempre había que hacer

Poner el **formato de la medida** (`formatString` en el modelo, "Formato" en Power BI
Desktop). El valor sigue siendo numérico, el visual lo pinta formateado, y todo lo que
depende de que sea un número —totales, orden, condicionales, ejes— sigue funcionando.

`FORMAT` tiene su sitio cuando el resultado **es** texto de verdad: una etiqueta que mezcla
número y palabras, un título dinámico, una cadena para exportar.

## El formato depende de la configuración regional

`FORMAT(fecha, "Short Date")` y los formatos con nombre siguen la configuración del modelo o
del usuario. En un informe que se ve en varios países, el mismo número sale con distinto
separador. Los formatos personalizados (`"#,##0"`, `"yyyy-MM-dd"`) son los predecibles; el
tercer argumento fija la cultura si hace falta.

## No confundir con
- `CONVERT` — cambia el tipo de dato, no la apariencia.
- `VALUE` — el camino de vuelta: texto a número. Da error si la cadena no es convertible.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
