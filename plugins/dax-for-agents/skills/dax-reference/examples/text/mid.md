---
function: MID
model: ninguno
---

# MID — examples

## 1. The position starts at 1, and 0 is not "from the beginning": it aborts

It is the most common translation error from any programming language, where the index starts at
zero. Here it returns neither the whole string nor an empty one — it brings the query down.

```dax
EVALUATE ROW("desde_0", MID("Contoso", 0, 3))
```

```result
ERROR: An argument of function 'MID' has the wrong data type or has an invalid value.
```

What is valid:

```dax
EVALUATE
ROW(
  "desde_1",  MID("Contoso", 1, 3),
  "desde_3",  MID("Contoso", 3, 3),
  "mas_alla", "[" & MID("Contoso", 20, 3) & "]",
  "pide_de_mas", MID("Contoso", 5, 99)
)
```

```result
desde_1 | desde_3 | mas_alla | pide_de_mas
Con | nto | [] | oso
```

Starting past the end does **not** give an error: it returns empty. So the silent failure and the
noisy one are one character apart.

## 2. Combined with FIND, to split on a separator

The real pattern. And its weak point: if the separator is not there, `FIND` aborts and takes the
whole query with it.

```dax
EVALUATE
VAR Codigo = "ES-2024-0042"
RETURN
ROW(
  "primer_guion",  FIND("-", Codigo),
  "segundo_guion", FIND("-", Codigo, FIND("-", Codigo) + 1),
  "el_ano",        MID(Codigo, FIND("-", Codigo) + 1, 4),
  "el_pais",       LEFT(Codigo, FIND("-", Codigo) - 1)
)
```

```result
primer_guion | segundo_guion | el_ano | el_pais
3 | 8 | 2024 | ES
```

## 3. Over a blank, with zero length and with negative length

```dax
EVALUATE
ROW(
  "blanco",        "[" & MID(BLANK(), 1, 3) & "]",
  "longitud_cero", "[" & MID("Contoso", 2, 0) & "]"
)
```

```result
blanco | longitud_cero
[] | []
```

A negative length does abort, with the same generic message as position 0 — so the error does not
say which of the two arguments was wrong:

```dax
EVALUATE ROW("longitud_negativa", MID("Contoso", 2, -1))
```

```result
ERROR: An argument of function 'MID' has the wrong data type or has an invalid value.
```

See [`left`](./left.md), [`right`](./right.md) and [`find`](./find.md).
