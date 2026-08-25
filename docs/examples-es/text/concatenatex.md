---
function: CONCATENATEX
model: contoso
---

# CONCATENATEX — ejemplos

> La nota de campo [`concatenatex`](../../notes/concatenatex.md) cubre el orden. Aquí van el
> tamaño del resultado y qué hace con los duplicados y los blancos.

## 1. Recorre la tabla que le des, con sus duplicados

Si la tabla tiene una fila por valor —una dimensión limpia— dan lo mismo. En cuanto la columna
se repite dentro de la tabla, `CONCATENATEX` la repite también, y lo que se quería era
`VALUES` de la columna.

```dax
EVALUATE
ROW(
  "marcas_distintas", COUNTROWS(VALUES(DimProduct[Brand])),
  "productos",        COUNTROWS(DimProduct),
  "por_valores",      LEN(CONCATENATEX(VALUES(DimProduct[Brand]), DimProduct[Brand], ", ")),
  "por_la_tabla",     LEN(CONCATENATEX(DimProduct, DimProduct[Brand], ", "))
)
```

```result
marcas_distintas | productos | por_valores | por_la_tabla
58 | 137 | 494 | 1193
```

La longitud del segundo es varias veces la del primero: una entrada por producto en vez de
una por marca.

## 2. No tiene tope corto: sobre una columna grande devuelve un texto enorme

Nada avisa. La medida no falla, el visual se queda pensando y el tooltip es ilegible.

```dax
EVALUATE
ROW(
  "cuantos_productos", COUNTROWS(VALUES(DimProduct[ProductName])),
  "longitud_total",    LEN(CONCATENATEX(VALUES(DimProduct[ProductName]), DimProduct[ProductName], ", ")),
  "primeros_60",       LEFT(CONCATENATEX(VALUES(DimProduct[ProductName]), DimProduct[ProductName], ", "), 60)
)
```

```result
cuantos_productos | longitud_total | primeros_60
128 | 3006 | Dell Desktop M3 Pro/36GB, Microsoft Workstation i7/32GB/1TB,
```

El patrón sano es acotar con [`topn`](../../notes/topn.md) y decir cuántos faltan, no volcar
la columna entera.

## 3. Los blancos NO se saltan: dejan el separador doblado

Lo escribí al revés y lo corrigió el motor. Un hueco no desaparece de la lista — ocupa su
sitio como elemento vacío, así que salen dos separadores seguidos. Es feo en el visual, y a
la vez es lo único que avisa de que faltaba un valor.

```dax
EVALUATE
VAR ConHuecos = { "a", BLANK(), "c" }
RETURN
ROW(
  "filas",    COUNTROWS(ConHuecos),
  "unidos",   CONCATENATEX(ConHuecos, [Value], "-"),
  "longitud", LEN(CONCATENATEX(ConHuecos, [Value], "-")),
  "vacia",    ISBLANK(CONCATENATEX(FILTER(ConHuecos, FALSE()), [Value], "-"))
)
```

```result
filas | unidos | longitud | vacia
3 | a--c | 4 | True
```

Sobre una tabla vacía sí devuelve blanco, no cadena vacía — la misma distinción de siempre.
