---
function: RIGHT
model: ninguno
---

# RIGHT — examples

## 1. The "last N" pattern that breaks on short data

Just like [`left`](./left.md): asking for too much returns whatever is there, without warning.

```dax
EVALUATE
ROW(
  "normal",       RIGHT("Contoso", 3),
  "mas_de_largo", RIGHT("ab", 10),
  "cero",         "[" & RIGHT("Contoso", 0) & "]",
  "sin_segundo",  RIGHT("Contoso")
)
```

```result
normal | mas_de_largo | cero | sin_segundo
oso | ab | [] | o
```

## 2. For keeping the extension or the suffix, it is fragile

The usual pattern — `RIGHT(text, LEN(text) - FIND(".", text))` — depends on the separator
existing. When it is not there, the count goes wrong.

```dax
EVALUATE
VAR ConPunto = "informe.pbix"
RETURN
ROW(
  "posicion",  FIND(".", ConPunto),
  "extension", RIGHT(ConPunto, LEN(ConPunto) - FIND(".", ConPunto)),
  "dos_puntos", RIGHT("a.b.c", LEN("a.b.c") - FIND(".", "a.b.c")),
  "ultimo_punto_no", RIGHT("a.b.c", 1)
)
```

```result
posicion | extension | dos_puntos | ultimo_punto_no
8 | pbix | b.c | c
```

With two dots it cuts at the **first**, not the last: `FIND` searches left to right. See
[`find`](./find.md).

## 3. Padding on the left: the use that does hold up

`RIGHT` over already-padded text is the short way to force a fixed width, and it works whether the
original was short or long.

```dax
EVALUATE
ROW(
  "corto",  RIGHT("0000" & 42, 4),
  "justo",  RIGHT("0000" & 1234, 4),
  "largo",  RIGHT("0000" & 123456, 4),
  "blanco", RIGHT("0000" & BLANK(), 4)
)
```

```result
corto | justo | largo | blanco
0042 | 1234 | 3456 | 0000
```

The `largo` case is the warning: it trims from the front and takes the significant digits with it
without saying anything.
