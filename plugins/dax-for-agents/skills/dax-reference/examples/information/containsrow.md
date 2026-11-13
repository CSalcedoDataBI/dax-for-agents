---
function: CONTAINSROW
model: ninguno
---

# CONTAINSROW — examples

## 1. It is what sits under the `IN` operator

Almost nobody writes it by name, and almost everybody uses it: `IN` with a tuple compiles to
this.

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

The first two columns are the same call. Knowing that changes how you debug an `IN` that does not
return what you expected: the problem is not in the operator, it is in this function's semantics.

And the third repeats [`contains`](./contains.md)'s lesson: it asks about the **whole row**.
`"Bici"` exists and `2` exists, but not together.

## 2. It identifies columns by POSITION, and that is why it can lie silently

This is the reason it has a card separate from `CONTAINS`.

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

All three columns are what somebody writes when they **believe** they are asking about the
Madrid→Lisboa trip. The first and the third really do ask it and say yes. The second says no.

And the second is right: `CONTAINSROW` matches by position, so `("Lisboa", "Madrid")` is not the
same question written backwards — it is the opposite question, a trip from Lisboa to Madrid,
which is indeed not in the table. The function does the right thing; what fails is the reading.

There is the danger: **with two columns of the same type, inverting the values gives no error**.
It gives `False`, which is a perfectly believable answer that nobody is going to go and check.

With different types it would not have happened — and that is exactly the bad luck of the case
above:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("tipos_invertidos", CONTAINSROW(T, 1, "Bici"))
```

```result
ERROR: Function 'CONTAINSROW' does not support comparing values of type Text with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

Inverting text and number kills the query on the spot. Inverting two texts returns `False`. The
engine protects you exactly where you do not need it, because an `Origen`/`Destino` table is
precisely the case where the order is easy to get wrong.

Practical rule: with a single column, `IN` is convenient and safe. With several of the same type,
use [`contains`](./contains.md), which names them.

## 3. Blanks and the size of the tuple

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

The first column says `False`, but **not because the blank does not count**: it says `False`
because this table has no blank row. The blank is compared like any other value, and where it
exists, it matches:

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

That is why it matters when the tuple is assembled from measures: one that returns blank produces
neither an error nor "all the rows", it produces **a different question from the one you thought
you were asking**, and its answer depends on whether the table holds that combination. Check the
values with [`isblank`](./isblank.md) before assembling them.

The tuple must have **as many values as the table has columns**. If any are missing, there is no
partial result and no blank:

```dax
EVALUATE
VAR T =
  DATATABLE("Cat", STRING, "N", INTEGER, {{"Bici", 1}, {"Casco", 2}})
RETURN ROW("tupla_corta", CONTAINSROW(T, "Bici"))
```

```result
ERROR: The number of arguments is invalid. Function CONTAINSROW must have a value for each column in the table expression.
```

That makes **two** automatic protections on this function: the number of values (here) and the
type incompatibility (section 2). Both fire loudly and in time. Neither covers the mistake that
actually gets made — inverting two values of the same type — which is the only one that makes no
noise.

See [`contains`](./contains.md), its named-column version.
