---
function: REPLACE
model: ninguno
---

# REPLACE — ejemplos

## 1. Sustituye por POSICIÓN, no por contenido

Es la diferencia con [`substitute`](./substitute.md), y la que hace que se elija mal. `REPLACE`
no busca nada: le dices dónde empezar y cuántos caracteres tapar.

```dax
EVALUATE
ROW(
  "por_posicion",  REPLACE("Contoso", 1, 3, "XXX"),
  "por_contenido", SUBSTITUTE("Contoso", "Con", "XXX"),
  "en_medio",      REPLACE("Contoso", 4, 2, "--"),
  "hasta_el_final", REPLACE("Contoso", 4, 99, "!")
)
```

```result
por_posicion | por_contenido | en_medio | hasta_el_final
XXXtoso | XXXtoso | Con--so | Con!
```

Pedir más caracteres de los que quedan no da error: tapa hasta el final.

## 2. Con longitud 0, inserta en vez de sustituir

El uso menos obvio y el más útil: es la forma de meter algo en mitad de una cadena.

```dax
EVALUATE
ROW(
  "inserta",      REPLACE("2024", 5, 0, "-01"),
  "al_principio", REPLACE("2024", 1, 0, "AÑO "),
  "mas_alla",     REPLACE("2024", 99, 0, "!"),
  "vacia",        REPLACE("Contoso", 1, 3, "")
)
```

```result
inserta | al_principio | mas_alla | vacia
2024-01 | AÑO 2024 | 2024! | toso
```

Insertar más allá del final **añade al final**, en vez de fallar o dejar hueco.

## 3. La posición 0 aborta, igual que en MID

```dax
EVALUATE ROW("posicion_0", REPLACE("Contoso", 0, 3, "X"))
```

```result
ERROR: An argument of function 'REPLACE' has the wrong data type or has an invalid value.
```

Y sobre blanco pasa algo que conviene ver: `REPLACE(BLANK(), 1, 3, "X")` **no** devuelve
blanco, devuelve `"X"`. El blanco se trata como cadena vacía y el texto nuevo se inserta
igual, así que una columna con huecos se rellena sola con el reemplazo.

```dax
EVALUATE
ROW(
  "blanco",     "[" & REPLACE(BLANK(), 1, 3, "X") & "]",
  "es_blanco",  ISBLANK(REPLACE(BLANK(), 1, 3, "X")),
  "numero",     REPLACE(12345, 2, 2, "--")
)
```

```result
blanco | es_blanco | numero
[X] | False | 1--45
```

Sobre un número convierte a texto primero — con la cultura del modelo, así que la posición
depende de si el separador decimal es coma o punto.
