---
function: LEN
model: ninguno
---

# LEN — examples

## 1. LEN of a blank is BLANK, but it compares like 0

I wrote it the other way round and the engine corrected it: `LEN(BLANK())` does **not** return 0,
it returns blank. And even so `LEN(BLANK()) = 0` is true, because `=` equates the blank to its
neutral value. Both facts at once are the trap.

```dax
EVALUATE
ROW(
  "len_blanco",       LEN(BLANK()),
  "es_blanco",        ISBLANK(LEN(BLANK())),
  "len_cadena_vacia", LEN(""),
  "compara_con_cero", LEN(BLANK()) = 0,
  "estricto",         LEN(BLANK()) == 0
)
```

```result
len_blanco | es_blanco | len_cadena_vacia | compara_con_cero | estricto
(blank) | True | 0 | True | False
```

So `LEN(column) = 0` does **not distinguish** "empty" from "no data": both pass. To tell them
apart you need `ISBLANK`, or the strict `==`.

## 2. Over a number, it counts the characters of its representation

`LEN` converts to text before counting, and that conversion uses the **model's culture**, not the
measure's format. This model is `es-ES`, so the decimal separator is the comma.

```dax
EVALUATE
ROW(
  "entero",    LEN(12345),
  "decimal",   LEN(1.5),
  "negativo",  LEN(-42),
  "cero_coma", LEN(0.50)
)
```

```result
entero | decimal | negativo | cero_coma
5 | 3 | 3 | 3
```

`0.50` measures 3 and not 4: the trailing zero does not exist in the number, only in how it was
written.

## 3. It counts code units, not visible characters

With emoji the count stops matching what you see: one outside the basic plane takes **two**.
Accents and the ñ, on the other hand, take one.

```dax
EVALUATE
ROW(
  "con_acento",  LEN("café"),
  "con_enye",    LEN("año"),
  "emoji",       LEN(UNICHAR(128512)),
  "texto_emoji", LEN("ok" & UNICHAR(128512))
)
```

```result
con_acento | con_enye | emoji | texto_emoji
4 | 3 | 2 | 4
```

If you cut with [`left`](./left.md) or [`mid`](./mid.md) counting by eye, that is where a
character gets split in half.
