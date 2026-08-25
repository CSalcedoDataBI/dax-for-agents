---
function: SWITCH
model: ninguno
---

# SWITCH — ejemplos

## 1. Sin `else` y sin coincidencia, devuelve blanco

Igual que `IF`. Un `SWITCH` que cubre cinco casos y se encuentra el sexto no da error ni cero:
desaparece del visual.

```dax
EVALUATE
ROW(
  "coincide",        SWITCH(2, 1, "uno", 2, "dos", 3, "tres"),
  "no_coincide",     SWITCH(9, 1, "uno", 2, "dos", 3, "tres"),
  "es_blanco",       ISBLANK(SWITCH(9, 1, "uno")),
  "con_else",        SWITCH(9, 1, "uno", 2, "dos", "ninguno")
)
```

```result
coincide | no_coincide | es_blanco | con_else
dos | (blank) | True | ninguno
```

## 2. `SWITCH(TRUE(), ...)` es el patrón de rangos

Es la forma de escribir una escalera de condiciones sin anidar cinco `IF`. La primera que se
cumple gana, así que **el orden importa**: una condición amplia colocada arriba tapa a las de
abajo.

```dax
EVALUATE
VAR Valor = 95
RETURN
ROW(
  "valor",         Valor,
  "bien_ordenado", SWITCH(TRUE(), Valor >= 90, "alto", Valor >= 50, "medio", "bajo"),
  "mal_ordenado",  SWITCH(TRUE(), Valor >= 50, "medio", Valor >= 90, "alto", "bajo"),
  "primera_gana",  SWITCH(TRUE(), TRUE(), "primera", TRUE(), "segunda")
)
```

```result
valor | bien_ordenado | mal_ordenado | primera_gana
95 | alto | medio | primera
```

Con 95, `mal_ordenado` devuelve «medio»: la rama de `>= 50` está antes y se lleva todo lo que
supera 50, así que la de `>= 90` no llega a evaluarse nunca. No da error — da una respuesta
plausible y equivocada, que es peor. Con un valor entre 50 y 90 las dos formas coinciden, y
por eso este fallo pasa las pruebas.

## 3. El blanco NO encaja con la rama del cero

Es lo contrario de lo que hace un `IF`, y por eso sorprende: en un `IF` el blanco se convierte
en `FALSE` y sigue la rama del `else`, pero `SWITCH` compara valores y un blanco no es igual a
`0` ni a `""` a efectos de coincidencia. Se va al `else` sin tocar ninguna rama.

```dax
EVALUATE
ROW(
  "cero_con_blanco",  SWITCH(BLANK(), 0, "encontró el cero", "no coincidió"),
  "texto_con_blanco", SWITCH(BLANK(), "", "encontró la cadena vacía", "no coincidió"),
  "cero_con_cero",    SWITCH(0, 0, "encontró el cero", "no coincidió")
)
```

```result
cero_con_blanco | texto_con_blanco | cero_con_cero
no coincidió | no coincidió | encontró el cero
```

Así que una rama escrita para el cero **no** captura las filas sin dato: se van todas al
`else`, y si no hay `else`, desaparecen. Para tratarlas hace falta una rama propia con
`ISBLANK`, o un `SWITCH(TRUE(), ...)` donde la condición se escribe entera.

Ver [`if`](./if.md) para las mismas conversiones con dos ramas.
