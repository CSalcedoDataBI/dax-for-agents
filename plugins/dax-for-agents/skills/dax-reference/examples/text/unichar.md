---
function: UNICHAR
model: ninguno
---

# UNICHAR — examples

## 1. It is how you write the characters you cannot type

The real use: naming an invisible character so it can be cleaned out, or putting a line break in a
label.

```dax
EVALUATE
ROW(
  "espacio_duro", UNICODE(UNICHAR(160)),
  "salto_linea",  LEN("a" & UNICHAR(10) & "b"),
  "tabulador",    LEN("a" & UNICHAR(9) & "b"),
  "letra_normal", UNICHAR(65)
)
```

```result
espacio_duro | salto_linea | tabulador | letra_normal
160 | 3 | 3 | A
```

See [`substitute`](./substitute.md), where `UNICHAR(160)` is what makes possible the clean-up
[`trim`](./trim.md) cannot do.

## 2. Emoji take two positions, and cutting them produces invalid text

A character above 65535 is stored as a pair. `LEN` says 2, and keeping half of it does not give a
strange character: it gives something the engine **can no longer process**.

```dax
EVALUATE
ROW(
  "emoji",         UNICHAR(128512),
  "longitud",      LEN(UNICHAR(128512)),
  "vuelta_entera", UNICODE(UNICHAR(128512))
)
```

```result
emoji | longitud | vuelta_entera
😀 | 2 | 128512
```

Asking for that half's code aborts:

```dax
EVALUATE ROW("medio_emoji", UNICODE(LEFT(UNICHAR(128512), 1)))
```

```result
ERROR: An argument of function 'UNICODE' has the wrong data type or has an invalid value.
```

So a `LEFT` over a column with emoji does not trim: it breaks the query further along, at a place
that looks nothing like the cause.

## 3. The real range is shorter than Unicode's

Below 65536 it takes one; from there on, two. That is the surrogate-pair frontier.

```dax
EVALUATE
ROW(
  "tabulador",     UNICODE(UNICHAR(9)),
  "ultimo_simple", LEN(UNICHAR(65533)),
  "primero_doble", LEN(UNICHAR(65536))
)
```

```result
tabulador | ultimo_simple | primero_doble
9 | 1 | 2
```

It is shown with **65533** and not 65535 because the engine returns results in **XML**, and what
XML does not allow is out. There are three groups, and they are worth knowing before picking a
character "the data will never carry".

The controls below 32 — except tab, line feed and carriage return:

```dax
EVALUATE ROW("control", UNICHAR(1))
```

```result
ERROR: Function 'UNICHAR' does not return invalid XML characters.
```

The last two code points of the basic plane, which Unicode marks as "non-characters":

```dax
EVALUATE ROW("no_caracter", UNICHAR(65535))
```

```result
ERROR: The code point does not correspond to a valid character.
```

And the extremes: zero, for being out of range, and the standard's theoretical maximum.

```dax
EVALUATE ROW("cero", UNICHAR(0))
```

```result
ERROR: An argument of function 'UNICHAR' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE ROW("maximo_unicode", UNICHAR(1114111))
```

```result
ERROR: The code point does not correspond to a valid character.
```

That closes off the trick of using a control character as a delimiter — see
[`combinevalues`](./combinevalues.md), where it also has to be a literal.
