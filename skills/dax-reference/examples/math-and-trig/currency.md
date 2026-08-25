---
function: CURRENCY
model: ninguno
---

# CURRENCY — ejemplos

## 1. Existe para que las sumas de dinero cuadren, y esa diferencia se puede ver

Un `double` no representa 0,1 exactamente. `CURRENCY` usa punto fijo con cuatro decimales, y
ahí la aritmética del dinero se comporta como uno espera.

```dax
EVALUATE
ROW(
  "en_coma_flotante", 0.1 + 0.2 = 0.3,
  "en_currency", CURRENCY(0.1) + CURRENCY(0.2) = CURRENCY(0.3),
  "residuo_flotante_x1e17", ROUND((0.1 + 0.2 - 0.3) * POWER(10, 17), 4)
)
```

```result
en_coma_flotante | en_currency | residuo_flotante_x1e17
False | True | 5.5511
```

La primera columna es falsa. La tercera enseña por qué: sobran 5,55 × 10⁻¹⁷, que el formato de
salida no muestra pero la comparación sí ve. Con `CURRENCY` la igualdad se cumple.

## 2. Cuatro decimales, redondeando al alejarse del cero

No es un formato de presentación: **recorta el valor**.

```dax
EVALUATE
ROW(
  "hacia_arriba", CURRENCY(0.33335),
  "hacia_abajo", CURRENCY(0.33334),
  "negativo", CURRENCY(-0.33335),
  "un_tercio", CURRENCY(1/3)
)
```

```result
hacia_arriba | hacia_abajo | negativo | un_tercio
0.3334 | 0.3333 | -0.3334 | 0.3333
```

El quinto decimal decide y se pierde. En un precio unitario con más de cuatro decimales —tipos
de cambio, costes por millar— eso es una pérdida real que se multiplica por la cantidad.

## 3. Con texto hereda la trampa de la cultura

```dax
EVALUATE
ROW(
  "cadena_con_coma", CURRENCY("12,3456"),
  "cadena_con_punto", CURRENCY("12.3456"),
  "numero_directo", CURRENCY(12.3456)
)
```

```result
cadena_con_coma | cadena_con_punto | numero_directo
12.3456 | 123456 | 12.3456
```

En este modelo, que está en **es-ES**, `CURRENCY("12.3456")` devuelve **123456**: el punto se
lee como separador de millares y los cuatro decimales se convierten en cuatro cifras enteras.
Es el mismo agujero que [`convert`](./convert.md), y multiplicado por diez mil.

La regla práctica: no conviertas texto a dinero. Convierte a número en el origen, donde la
cultura la controlas tú.

Ver [`convert`](./convert.md) y [`round`](./round.md).
