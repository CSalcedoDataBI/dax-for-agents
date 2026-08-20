---
function: CONVERT
model: ninguno
---

# CONVERT — ejemplos

## 1. Al convertir texto a número manda la CULTURA del modelo, no la sintaxis de DAX

Este es el que muerde. Un literal `1.5` escrito en DAX siempre es uno y medio; la **cadena**
`"1.5"` depende del idioma del modelo. Estos resultados son de un modelo en **es-ES**.

```dax
EVALUATE
ROW(
  "literal_dax", 1.5,
  "cadena_con_punto", CONVERT("1.5", DOUBLE),
  "cadena_con_coma", CONVERT("1,5", DOUBLE),
  "con_separador_de_miles", CONVERT("1.234,5", DOUBLE)
)
```

```result
literal_dax | cadena_con_punto | cadena_con_coma | con_separador_de_miles
1.5 | 15 | 1.5 | 1234.5
```

`CONVERT("1.5", DOUBLE)` devuelve **15**, no 1,5: el punto se lee como separador de millares.
No hay error, no hay aviso — solo un número diez veces mayor. Ese mismo modelo, con la cultura
en inglés, daría 1,5, así que la fórmula es correcta o incorrecta según dónde se abra.

## 2. A entero REDONDEA, no trunca — al revés que `INT`

```dax
EVALUATE
ROW(
  "convert_1_9", CONVERT(1.9, INTEGER),
  "int_1_9", INT(1.9),
  "convert_menos_1_9", CONVERT(-1.9, INTEGER),
  "int_menos_1_9", INT(-1.9),
  "trunc_menos_1_9", TRUNC(-1.9)
)
```

```result
convert_1_9 | int_1_9 | convert_menos_1_9 | int_menos_1_9 | trunc_menos_1_9
2 | 1 | -2 | -2 | -1
```

Tres funciones y tres resultados distintos para -1,9. `CONVERT` redondea, [`int`](./int.md)
baja siempre, y `TRUNC` va hacia el cero. Elegir por costumbre es elegir mal dos de cada tres
veces.

## 3. Los tipos que acepta, y lo que hace con un blanco

```dax
EVALUATE
ROW(
  "a_double", CONVERT("123", DOUBLE),
  "a_entero", CONVERT("123", INTEGER),
  "a_booleano", CONVERT(1, BOOLEAN),
  "cero_a_booleano", CONVERT(0, BOOLEAN),
  "blanco_a_entero", CONVERT(BLANK(), INTEGER),
  "sigue_en_blanco", ISBLANK(CONVERT(BLANK(), INTEGER))
)
```

```result
a_double | a_entero | a_booleano | cero_a_booleano | blanco_a_entero | sigue_en_blanco
123 | 123 | True | False | (blank) | True
```

El blanco **sigue en blanco**: `CONVERT` fuerza el tipo pero no inventa un valor. Conviene
saberlo porque la intuición dice lo contrario —un entero «no puede estar vacío»— y porque
[`randbetween`](./randbetween.md), con dos blancos, sí devuelve un 0.

Ver [`currency`](./currency.md), [`int`](./int.md) y [`value`](../text/value.md).
