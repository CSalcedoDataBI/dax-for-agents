---
function: CONCATENATE
model: ninguno
---

# CONCATENATE — examples

## 1. Only two arguments, like AND and OR

With three it aborts. For chaining there is the `&` operator, which also reads better.

```dax
EVALUATE
ROW(
  "dos",       CONCATENATE("Power", " BI"),
  "anidada",   CONCATENATE("Power", CONCATENATE(" ", "BI")),
  "operador",  "Power" & " " & "BI"
)
```

```result
dos | anidada | operador
Power BI | Power BI | Power BI
```

```dax
EVALUATE ROW("tres", CONCATENATE("a", "b", "c"))
```

```result
ERROR: Too many arguments were passed to the CONCATENATE function. The maximum argument count for the function is 2.
```

## 2. A blank next to text disappears; two blanks are still blank

It is half the rule you expect. Next to text, the blank behaves as an empty string: it disappears
without a trace, and with it the signal that a value was missing. But
`CONCATENATE(BLANK(), BLANK())` does **not** return an empty string: it returns blank.

```dax
EVALUATE
ROW(
  "blanco_delante", "[" & CONCATENATE(BLANK(), "hola") & "]",
  "blanco_detras",  "[" & CONCATENATE("hola", BLANK()) & "]",
  "los_dos",        "[" & CONCATENATE(BLANK(), BLANK()) & "]",
  "es_blanco",      ISBLANK(CONCATENATE(BLANK(), BLANK()))
)
```

```result
blanco_delante | blanco_detras | los_dos | es_blanco
[hola] | [hola] | [] | True
```

A full name assembled with `&` over a missing surname comes out with the extra space and nobody
notices. And the whole row only disappears from the visual if **everything** came in blank.

## 3. It converts numbers to text using the model's culture

What comes out is not what the report shows: the measure's format plays no part.

```dax
EVALUATE
ROW(
  "entero",   CONCATENATE("n=", 1234),
  "decimal",  CONCATENATE("x=", 1.5),
  "negativo", CONCATENATE("t=", -3),
  "booleano", CONCATENATE("b=", TRUE())
)
```

```result
entero | decimal | negativo | booleano
n=1234 | x=1,5 | t=-3 | b=TRUE
```

To control how the number is written you have to say so with [`format`](./format.md) — and then
the result stops sorting as a number, which is that card's trap.

See [`concatenatex`](./concatenatex.md) for joining the values of a **column**.
