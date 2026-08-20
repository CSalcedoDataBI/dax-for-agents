---
function: CONTAINS
model: ninguno
---

# CONTAINS — ejemplos

## 1. Pregunta por la COMBINACIÓN, no por cada valor suelto

Es el malentendido que produce filtros que parecen correctos y devuelven de menos.

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}, {"Bici", 3}})
RETURN
ROW(
  "pareja_que_existe", CONTAINS(T, [Cat], "Bici", [N], 1),
  "cada_uno_existe_por_separado", CONTAINS(T, [Cat], "Bici", [N], 2),
  "solo_una_columna", CONTAINS(T, [Cat], "Bici"),
  "ignora_mayusculas", CONTAINS(T, [Cat], "bici")
)
```

```result
pareja_que_existe | cada_uno_existe_por_separado | solo_una_columna | ignora_mayusculas
True | False | True | True
```

La segunda columna es la lección entera. `"Bici"` está en la tabla y `2` está en la tabla, y
sin embargo la respuesta es **falso**: no hay ninguna fila donde estén *los dos a la vez*.
`CONTAINS` recorre filas, no columnas. Si lo que querías era «¿existe Bici? ¿y existe el 2?»,
son dos preguntas y hacen falta dos llamadas.

## 2. El orden de los pares da igual, porque cada columna va con nombre

```dax
EVALUATE
VAR T =
  DATATABLE("Origen", STRING, "Destino", STRING, {{"Madrid", "Lisboa"}, {"Roma", "París"}})
RETURN
ROW(
  "como_estan_declaradas", CONTAINS(T, [Origen], "Madrid", [Destino], "Lisboa"),
  "pares_al_reves", CONTAINS(T, [Destino], "Lisboa", [Origen], "Madrid"),
  "valores_cruzados", CONTAINS(T, [Origen], "Lisboa", [Destino], "Madrid")
)
```

```result
como_estan_declaradas | pares_al_reves | valores_cruzados
True | True | False
```

Las dos primeras son la misma pregunta escrita en distinto orden y dan lo mismo: cada valor
viaja pegado a **su** columna, así que reordenar los pares es inofensivo. La tercera es falsa y
debe serlo — nadie viaja de Lisboa a Madrid en esta tabla.

Esa inmunidad al orden es justo lo que **no** tiene
[`containsrow`](./containsrow.md), que identifica las columnas por posición. Es la razón para
preferir `CONTAINS` cuando la tabla tiene varias columnas del mismo tipo, donde una inversión
no da error: da un resultado equivocado.

## 3. Si los tipos no casan, tumba la consulta

No devuelve falso ni blanco. Aborta.

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("numero_buscado_como_texto", CONTAINS(T, [N], "1"))
```

```result
ERROR: Function 'CONTAINS' does not support comparing values of type Integer with values of type Text. Consider using the VALUE or FORMAT function to convert one of the values.
```

El mensaje trae la solución dentro, y funciona:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
VAR Buscado = "1"
RETURN
ROW(
  "convertido_con_value", CONTAINS(T, [N], VALUE(Buscado)),
  "convertido_y_no_existe", CONTAINS(T, [N], VALUE("9"))
)
```

```result
convertido_con_value | convertido_y_no_existe
True | False
```

La segunda columna está para que la primera signifique algo: convertir no hace que todo
coincida, solo permite comparar.

Importa porque en un modelo real el valor buscado suele venir de un parámetro, de una tabla
desconectada o de `SELECTEDVALUE`, y su tipo no se ve leyendo la fórmula: se ve el día que la
consulta muere en producción. Conviértelo de forma explícita en vez de confiar en que llegue
con el tipo correcto.

Ojo: esto es lo contrario de lo que hace [`containsstring`](./containsstring.md), que convierte
números a texto sin quejarse. Dos funciones de la misma familia con criterios opuestos.

Ver [`containsrow`](./containsrow.md), su versión posicional, y
[`containsstring`](./containsstring.md) para buscar dentro de un texto.
