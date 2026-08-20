---
function: COALESCE
model: ninguno
---

# COALESCE — ejemplos

## 1. Devuelve el primero que NO esté en blanco, y el cero sí cuenta

Cero no es blanco. Es la confusión que hace que un `COALESCE` puesto «por seguridad» devuelva
el cero que venía del dato en vez del valor por defecto que se quería.

```dax
EVALUATE
ROW(
  "blanco_luego_diez", COALESCE(BLANK(), 10),
  "cero_luego_diez",   COALESCE(0, 10),
  "vacio_luego_diez",  COALESCE("", 10),
  "todos_blancos",     ISBLANK(COALESCE(BLANK(), BLANK()))
)
```

```result
blanco_luego_diez | cero_luego_diez | vacio_luego_diez | todos_blancos
10 | 0 | (empty) | True
```

La cadena vacía tampoco es blanco: `COALESCE("", 10)` devuelve la cadena vacía. Si el origen
trae `""` en vez de nulos, `COALESCE` no hará nada y el problema seguirá ahí.

## 2. Acepta muchos argumentos, pero nunca uno solo

Al contrario que `AND` y `OR`, que están limitadas a dos, `COALESCE` encadena los que hagan
falta. El límite está en el otro extremo:

```dax
EVALUATE
ROW(
  "tres_argumentos",  COALESCE(BLANK(), BLANK(), "tercero"),
  "cinco_argumentos", COALESCE(BLANK(), BLANK(), BLANK(), BLANK(), 5)
)
```

```result
tres_argumentos | cinco_argumentos
tercero | 5
```

Con uno solo aborta, y el mensaje lo dice sin rodeos:

```dax
EVALUATE ROW("uno_solo", COALESCE(BLANK()))
```

```result
ERROR: Too few arguments were passed to the COALESCE function. The minimum argument count for the function is 2.
```

## 3. Mezcla tipos sin protestar

Se puede dar un número por defecto a una expresión de texto. Corre, y el problema aparece
más tarde, cuando algo intenta formatear o sumar lo que salga.

```dax
EVALUATE
ROW(
  "texto_o_numero", COALESCE(BLANK(), 42),
  "numero_o_texto", COALESCE(BLANK(), "sin dato"),
  "suma_despues",   COALESCE(BLANK(), 42) + 1
)
```

```result
texto_o_numero | numero_o_texto | suma_despues
42 | sin dato | 43
```

Es el reemplazo directo de `IF(ISBLANK(x), y, x)` — más corto y sin evaluar `x` dos veces.
Ver [`if`](./if.md).
