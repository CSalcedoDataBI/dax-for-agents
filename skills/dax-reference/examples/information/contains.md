---
function: CONTAINS
model: ninguno
---

# CONTAINS — examples

## 1. It asks about the COMBINATION, not about each value on its own

It is the misunderstanding that produces filters that look right and return too little.

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

The second column is the whole lesson. `"Bici"` is in the table and `2` is in the table, and yet
the answer is **false**: there is no row where *both* appear together. `CONTAINS` walks rows, not
columns. If what you wanted was "does Bici exist? and does 2 exist?", those are two questions and
they need two calls.

## 2. The order of the pairs does not matter, because each column comes by name

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

The first two are the same question written in a different order and give the same answer: each
value travels attached to **its** column, so reordering the pairs is harmless. The third is false
and should be — nobody travels from Lisboa to Madrid in this table.

That immunity to ordering is exactly what [`containsrow`](./containsrow.md) does **not** have, as
it identifies columns by position. It is the reason to prefer `CONTAINS` when the table has
several columns of the same type, where an inversion gives no error: it gives a wrong result.

## 3. If the types do not match, it brings the query down

It returns neither false nor blank. It aborts.

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("numero_buscado_como_texto", CONTAINS(T, [N], "1"))
```

```result
ERROR: Function 'CONTAINS' does not support comparing values of type Integer with values of type Text. Consider using the VALUE or FORMAT function to convert one of the values.
```

The message carries the solution inside it, and it works:

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

The second column is there so the first means something: converting does not make everything
match, it only makes comparison possible.

It matters because in a real model the value being searched for usually comes from a parameter,
from a disconnected table or from `SELECTEDVALUE`, and its type is not visible from reading the
formula: it becomes visible the day the query dies in production. Convert it explicitly instead
of trusting that it arrives with the right type.

Note: this is the opposite of what [`containsstring`](./containsstring.md) does, which converts
numbers to text without complaint. Two functions in the same family with opposite criteria.

See [`containsrow`](./containsrow.md), its positional version, and
[`containsstring`](./containsstring.md) for searching inside text.
