---
function: CONTAINSROW
model: ninguno
---

# CONTAINSROW — ejemplos

## 1. Es lo que hay debajo del operador `IN`

Casi nadie la escribe por su nombre, y casi todo el mundo la usa: `IN` con una tupla compila a
esto.

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN
ROW(
  "por_su_nombre", CONTAINSROW(T, "Bici", 1),
  "con_el_operador_in", ("Bici", 1) IN T,
  "pareja_que_no_esta", ("Bici", 2) IN T,
  "ignora_mayusculas", CONTAINSROW(T, "bici", 1)
)
```

```result
por_su_nombre | con_el_operador_in | pareja_que_no_esta | ignora_mayusculas
True | True | False | True
```

Las dos primeras columnas son la misma llamada. Saberlo cambia cómo se depura un `IN` que no
devuelve lo esperado: el problema no está en el operador, está en la semántica de esta función.

Y la tercera repite la lección de [`contains`](./contains.md): pregunta por la **fila entera**.
`"Bici"` existe y `2` existe, pero no juntos.

## 2. Identifica las columnas por POSICIÓN, y por eso puede mentir en silencio

Esta es la razón de que exista una ficha aparte de la de `CONTAINS`.

```dax
EVALUATE
VAR T =
  DATATABLE("Origen", STRING, "Destino", STRING, {{"Madrid", "Lisboa"}, {"Roma", "Paris"}})
RETURN
ROW(
  "en_el_orden_correcto", CONTAINSROW(T, "Madrid", "Lisboa"),
  "con_los_valores_invertidos", CONTAINSROW(T, "Lisboa", "Madrid"),
  "lo_mismo_con_contains", CONTAINS(T, [Destino], "Lisboa", [Origen], "Madrid")
)
```

```result
en_el_orden_correcto | con_los_valores_invertidos | lo_mismo_con_contains
True | False | True
```

Las tres columnas son lo que escribe alguien que **cree** estar preguntando por el viaje
Madrid→Lisboa. La primera y la tercera lo preguntan de verdad y dicen que sí. La segunda dice
que no.

Y la segunda tiene razón: `CONTAINSROW` empareja por posición, así que `("Lisboa", "Madrid")`
no es la misma pregunta escrita al revés — es la pregunta contraria, un viaje de Lisboa a
Madrid, que efectivamente no está en la tabla. La función hace lo correcto; lo que falla es la
lectura.

Ahí está el peligro: **con dos columnas del mismo tipo, invertir los valores no da error**. Da
`False`, que es una respuesta perfectamente creíble y que nadie va a ir a comprobar.

Con tipos distintos no habría pasado — y esa es justo la mala suerte del caso de arriba:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("tipos_invertidos", CONTAINSROW(T, 1, "Bici"))
```

```result
ERROR: Function 'CONTAINSROW' does not support comparing values of type Text with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

Invertir texto y número mata la consulta en el sitio. Invertir dos textos devuelve `False`. El
motor te protege exactamente donde no lo necesitas, porque una tabla `Origen`/`Destino` es
precisamente el caso donde el orden es fácil de equivocar.

Regla práctica: con una sola columna, `IN` es cómodo y seguro. Con varias del mismo tipo, usa
[`contains`](./contains.md), que las nombra.

## 3. Blancos y tamaño de la tupla

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN
ROW(
  "dos_blancos", CONTAINSROW(T, BLANK(), BLANK()),
  "existe_de_verdad", CONTAINSROW(T, "Casco", 2),
  "primera_fila", CONTAINSROW(T, "Bici", 1)
)
```

```result
dos_blancos | existe_de_verdad | primera_fila
False | True | True
```

La primera columna dice `False`, pero **no porque el blanco no cuente**: dice `False` porque
esta tabla no tiene ninguna fila en blanco. El blanco se compara como un valor más, y donde
existe, coincide:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {BLANK(), BLANK()}})
RETURN
ROW(
  "tabla_que_si_tiene_fila_en_blanco", CONTAINSROW(T, BLANK(), BLANK()),
  "y_la_fila_normal", CONTAINSROW(T, "Bici", 1)
)
```

```result
tabla_que_si_tiene_fila_en_blanco | y_la_fila_normal
True | True
```

Por eso importa cuando la tupla se arma con medidas: una que devuelva blanco no produce error
ni «todas las filas», produce una **pregunta distinta de la que creías hacer**, y su respuesta
depende de si la tabla tiene esa combinación. Comprueba los valores con
[`isblank`](./isblank.md) antes de montarlos.

La tupla debe tener **tantos valores como columnas tiene la tabla**. Si faltan, no hay
resultado parcial ni blanco:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("tupla_corta", CONTAINSROW(T, "Bici"))
```

```result
ERROR: The number of arguments is invalid. Function CONTAINSROW must have a value for each column in the table expression.
```

Con eso son **dos** las protecciones automáticas de esta función: el número de valores (aquí) y
la incompatibilidad de tipos (sección 2). Las dos saltan fuerte y a tiempo. Ninguna de las dos
cubre el error que de verdad se comete —invertir dos valores del mismo tipo—, que es el único
que no hace ruido.

Ver [`contains`](./contains.md), su versión con columnas nombradas.
