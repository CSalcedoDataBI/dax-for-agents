---
function: SUBSTITUTE
model: ninguno
---

# SUBSTITUTE — examples

## 1. It distinguishes upper from lower case

Unlike [`search`](./search.md), which does not. It is the asymmetry that makes a clean-up "work"
in testing and leave half the rows untouched in production.

```dax
EVALUATE
ROW(
  "coincide",     SUBSTITUTE("Sony Bravia", "Sony", "SONY"),
  "no_coincide",  SUBSTITUTE("Sony Bravia", "sony", "SONY"),
  "todas",        SUBSTITUTE("aaa", "a", "b"),
  "sin_encontrar", SUBSTITUTE("hola", "z", "!")
)
```

```result
coincide | no_coincide | todas | sin_encontrar
SONY Bravia | Sony Bravia | bbb | hola
```

When it finds nothing it **gives no error**: it returns the text unchanged. The failure is silent.

## 2. It replaces ALL occurrences, unless you say which

The fourth argument picks the occurrence. Without it, it changes them all — which is almost never
what you want when cleaning a separator.

```dax
EVALUATE
ROW(
  "todas",     SUBSTITUTE("a-b-c-d", "-", "/"),
  "solo_la_1", SUBSTITUTE("a-b-c-d", "-", "/", 1),
  "solo_la_3", SUBSTITUTE("a-b-c-d", "-", "/", 3),
  "la_9",      SUBSTITUTE("a-b-c-d", "-", "/", 9)
)
```

```result
todas | solo_la_1 | solo_la_3 | la_9
a/b/c/d | a/b-c-d | a-b-c/d | a-b-c-d
```

Asking for an occurrence that does not exist does not fail either: it returns the text untouched.

## 3. It is the tool for the non-breaking space TRIM does not remove

The real case it gets used for. You have to **name** the character, because you cannot see it.

```dax
EVALUATE
VAR Sucio = "  hola" & UNICHAR(160) & "mundo  "
RETURN
ROW(
  "solo_trim",         LEN(TRIM(Sucio)),
  "substitute_y_trim", LEN(TRIM(SUBSTITUTE(Sucio, UNICHAR(160), " "))),
  "resultado",         TRIM(SUBSTITUTE(Sucio, UNICHAR(160), " ")),
  "borrar_del_todo",   SUBSTITUTE("a b c", " ", "")
)
```

```result
solo_trim | substitute_y_trim | resultado | borrar_del_todo
10 | 10 | hola mundo | abc
```

See [`trim`](./trim.md) for why it is not enough on its own, and [`replace`](./replace.md) for
substituting **by position** instead of by content.
