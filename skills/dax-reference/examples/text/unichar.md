---
function: UNICHAR
model: ninguno
---

# UNICHAR — ejemplos

## 1. Es como se escriben los caracteres que no se pueden teclear

El uso real: nombrar un carácter invisible para poder limpiarlo, o meter un salto de línea en
una etiqueta.

```dax
EVALUATE
ROW(
  "espacio_duro", UNICODE(UNICHAR(160)),
  "salto_linea",  LEN("a" & UNICHAR(10) & "b"),
  "tabulador",    LEN("a" & UNICHAR(9) & "b"),
  "letra_normal", UNICHAR(65)
)
```

```result
espacio_duro | salto_linea | tabulador | letra_normal
160 | 3 | 3 | A
```

Ver [`substitute`](./substitute.md), donde `UNICHAR(160)` es lo que hace posible la limpieza
que [`trim`](./trim.md) no puede.

## 2. Los emoji ocupan dos posiciones, y cortarlos produce texto inválido

Un carácter por encima de 65535 se guarda como un par. `LEN` dice 2, y quedarse con la mitad
no da un carácter raro: da algo que el motor **ya no puede procesar**.

```dax
EVALUATE
ROW(
  "emoji",         UNICHAR(128512),
  "longitud",      LEN(UNICHAR(128512)),
  "vuelta_entera", UNICODE(UNICHAR(128512))
)
```

```result
emoji | longitud | vuelta_entera
😀 | 2 | 128512
```

Al pedir el código de esa mitad, aborta:

```dax
EVALUATE ROW("medio_emoji", UNICODE(LEFT(UNICHAR(128512), 1)))
```

```result
ERROR: An argument of function 'UNICODE' has the wrong data type or has an invalid value.
```

Así que un `LEFT` sobre una columna con emoji no recorta: rompe la consulta más adelante, en
un sitio que no se parece a la causa.

## 3. El rango real es más corto que el de Unicode

Por debajo de 65536 ocupa uno; a partir de ahí, dos. Esa es la frontera del par sustituto.

```dax
EVALUATE
ROW(
  "tabulador",     UNICODE(UNICHAR(9)),
  "ultimo_simple", LEN(UNICHAR(65533)),
  "primero_doble", LEN(UNICHAR(65536))
)
```

```result
tabulador | ultimo_simple | primero_doble
9 | 1 | 2
```

Se enseña con **65533** y no con 65535 porque el motor devuelve los resultados en **XML**, y
lo que XML no admite queda fuera. Son tres grupos, y conviene conocerlos antes de elegir un
carácter «que el dato nunca traiga».

Los controles por debajo de 32 —salvo tabulador, salto y retorno—:

```dax
EVALUATE ROW("control", UNICHAR(1))
```

```result
ERROR: Function 'UNICHAR' does not return invalid XML characters.
```

Los dos últimos puntos del plano básico, que Unicode marca como «no caracteres»:

```dax
EVALUATE ROW("no_caracter", UNICHAR(65535))
```

```result
ERROR: The code point does not correspond to a valid character.
```

Y los extremos: el cero, por quedar fuera de rango, y el máximo teórico del estándar.

```dax
EVALUATE ROW("cero", UNICHAR(0))
```

```result
ERROR: An argument of function 'UNICHAR' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE ROW("maximo_unicode", UNICHAR(1114111))
```

```result
ERROR: The code point does not correspond to a valid character.
```

Eso deja sin salida el truco de usar un carácter de control como delimitador — ver
[`combinevalues`](./combinevalues.md), donde además tiene que ser literal.
