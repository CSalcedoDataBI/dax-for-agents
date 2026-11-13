---
function: CONTAINSSTRING
model: ninguno
---

# CONTAINSSTRING — examples

## 1. It ignores case but NOT accents

A half-truth is worse than none, and here the half-truth is "it does not distinguish case". True.
What nobody says is that it does distinguish accents, and in Spanish that is half the catalogue.

```dax
EVALUATE
ROW(
  "minusculas", CONTAINSSTRING("Bicicleta", "bici"),
  "acento_perdido", CONTAINSSTRING("Almacén", "almacen"),
  "acento_puesto", CONTAINSSTRING("Almacén", "MACÉN"),
  "enie", CONTAINSSTRING("Año", "ano")
)
```

```result
minusculas | acento_perdido | acento_puesto | enie
True | False | True | False
```

`"bici"` finds `"Bicicleta"` and `"MACÉN"` finds `"Almacén"` — case makes no difference. But
`"almacen"` does **not** find `"Almacén"`, and `"ano"` does not find `"Año"`. A report search box
where the user types without accents returns zero results and looks broken.

## 2. `*` and `?` are wildcards, not characters

This is not in the function's name and is not what you expect from something called "contains
string".

```dax
EVALUATE
ROW(
  "asterisco", CONTAINSSTRING("aXXXb", "a*b"),
  "interrogante", CONTAINSSTRING("aXb", "a?b"),
  "interrogante_exige_uno", CONTAINSSTRING("ab", "a?b"),
  "asterisco_sobre_si_mismo", CONTAINSSTRING("a*b", "a*b")
)
```

```result
asterisco | interrogante | interrogante_exige_uno | asterisco_sobre_si_mismo
True | True | False | True
```

`"a*b"` finds `"aXXXb"`: the `*` swallows anything. The `?` stands for **exactly one** character,
so `"a?b"` does not find `"ab"` — where there is no character, there is no match.

The fourth column is the fine trap: `CONTAINSSTRING("a*b", "a*b")` is true, but **not because it
found the asterisk**. It is true because `a`, anything, `b` describes `"a*b"` just as it describes
`"aXXXb"`. As written, this call cannot tell a real asterisk from an imaginary one. That is what
the escape in the next section is for.

## 3. A blank needle always finds

```dax
EVALUATE
ROW(
  "aguja_vacia", CONTAINSSTRING("Bicicleta", ""),
  "aguja_blanca", CONTAINSSTRING("Bicicleta", BLANK()),
  "pajar_blanco", CONTAINSSTRING(BLANK(), "a"),
  "numeros", CONTAINSSTRING(12345, 234)
)
```

```result
aguja_vacia | aguja_blanca | pajar_blanco | numeros
True | True | False | True
```

The first two columns are the reason to read this. An empty search box translates into
`CONTAINSSTRING([Producto], [TextoBuscado])` with the second argument blank, and **that returns
true for every row**: the filter filters nothing. It is not a bug, it is that the empty string is
contained in any string. But it goes unnoticed because the report shows exactly what it would show
with no filter.

The defence is not to call the function when there is no term. But **`ISBLANK` is not enough**,
and it is an easy mistake to make because the two columns above look like the same case and are
not: `ISBLANK("")` is false — the empty string is text, measured in [`isblank`](./isblank.md) —
so a guard using `ISBLANK` lets exactly half the problem through. The one that covers both is
`LEN`:

```dax
EVALUATE
ROW(
  "len_de_blanco", LEN(BLANK()),
  "len_de_cadena_vacia", LEN(""),
  "guardia_con_blanco", LEN(BLANK()) > 0,
  "guardia_con_vacia", LEN("") > 0,
  "guardia_con_termino", LEN("bici") > 0,
  "isblank_no_ve_la_vacia", ISBLANK("")
)
```

```result
len_de_blanco | len_de_cadena_vacia | guardia_con_blanco | guardia_con_vacia | guardia_con_termino | isblank_no_ve_la_vacia
(blank) | 0 | False | False | True | False
```

Look at the first column: `LEN(BLANK())` is **not 0, it is blank**. The guard works anyway, and
the reason is worth measuring separately because it is easy to tell it wrong:

```dax
EVALUATE
ROW(
  "blanco_igual_a_cero", BLANK() = 0,
  "blanco_mayor_que_cero", BLANK() > 0,
  "blanco_menor_que_cero", BLANK() < 0,
  "blanco_mayor_o_igual_cero", BLANK() >= 0,
  "blanco_mayor_que_menos_uno", BLANK() > -1
)
```

```result
blanco_igual_a_cero | blanco_mayor_que_cero | blanco_menor_que_cero | blanco_mayor_o_igual_cero | blanco_mayor_que_menos_uno
True | False | False | True | True
```

It is not that comparing a blank with a number gives false — `BLANK() = 0` is **true**, and so is
`BLANK() > -1`. It is that in a numeric comparison **the blank behaves as a zero**. That is why
`LEN(BLANK()) > 0` is false: not because the comparison fails, but because zero is not greater
than zero.

So the correct form is `IF(LEN([Buscado]) > 0, CONTAINSSTRING(...))`, and it works for the same
reason on the blank and on the empty string.

And the last column: numbers go in converted to text, so `234` is found inside `12345` even though
neither is a string.

## 4. `~` switches the wildcard off, and then it really does search for the character

```dax
EVALUATE
ROW(
  "escapado_encuentra_el_literal", CONTAINSSTRING("a*b", "a~*b"),
  "escapado_ya_no_es_comodin", CONTAINSSTRING("aXXXb", "a~*b"),
  "sin_escapar_encuentra_los_dos", CONTAINSSTRING("aXXXb", "a*b"),
  "interrogante_escapado", CONTAINSSTRING("a?b", "a~?b"),
  "interrogante_escapado_no_es_comodin", CONTAINSSTRING("aXb", "a~?b")
)
```

```result
escapado_encuentra_el_literal | escapado_ya_no_es_comodin | sin_escapar_encuentra_los_dos | interrogante_escapado | interrogante_escapado_no_es_comodin
True | False | True | True | False
```

With a `~` in front, the asterisk goes back to being an asterisk: it finds `"a*b"` and **stops
finding** `"aXXXb"`. The first two columns are exactly the distinction the previous section could
not make.

That changes the practical recommendation: to search for a literal wildcard **without** losing
case-insensitivity, the answer is `CONTAINSSTRING` with `~`, not
[`containsstringexact`](./containsstringexact.md) — which does treat `*` as a literal, but in
exchange forces you to get the case right. And note: the `~` is an escape **only here**; in
`CONTAINSSTRINGEXACT` it is just another character, measured on its card.

Less obvious consequence: if the term is typed by a user, a stray `*` in their search does **not
behave as text**. If you want it to, escape it yourself — `SUBSTITUTE([Buscado], "*", "~*")` —
before passing it on.

See [`containsstringexact`](./containsstringexact.md) and [`contains`](./contains.md) for
searching in tables rather than in text.
