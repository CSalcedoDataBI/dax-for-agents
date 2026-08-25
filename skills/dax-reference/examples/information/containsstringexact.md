---
function: CONTAINSSTRINGEXACT
model: ninguno
---

# CONTAINSSTRINGEXACT — examples

## 1. It distinguishes case, which is what the name promises

```dax
EVALUATE
ROW(
  "minusculas", CONTAINSSTRINGEXACT("Bicicleta", "bici"),
  "capitalizado", CONTAINSSTRINGEXACT("Bicicleta", "Bici"),
  "lo_mismo_con_containsstring", CONTAINSSTRING("Bicicleta", "bici"),
  "acento", CONTAINSSTRINGEXACT("Almacén", "Almacen")
)
```

```result
minusculas | capitalizado | lo_mismo_con_containsstring | acento
False | True | True | False
```

The first two columns are the advertised difference. The third puts it next to
[`containsstring`](./containsstring.md), which does find `"bici"`. The fourth is a reminder that
the accent counts here **too** — as it does in the other one, which does not ignore them either.

## 2. The difference it does not advertise: here `*` and `?` are NOT wildcards

The two functions are documented as if only case-sensitivity changed. There are two differences,
not one, and this second one changes the result of an entire search.

```dax
EVALUATE
ROW(
  "exacto_con_asterisco", CONTAINSSTRINGEXACT("aXXXb", "a*b"),
  "containsstring_con_asterisco", CONTAINSSTRING("aXXXb", "a*b"),
  "exacto_asterisco_literal", CONTAINSSTRINGEXACT("a*b", "a*b"),
  "exacto_con_interrogante", CONTAINSSTRINGEXACT("aXb", "a?b"),
  "exacto_interrogante_literal", CONTAINSSTRINGEXACT("a?b", "a?b")
)
```

```result
exacto_con_asterisco | containsstring_con_asterisco | exacto_asterisco_literal | exacto_con_interrogante | exacto_interrogante_literal
False | True | True | False | True
```

The first two columns are the same call with the same needle over the same haystack, and they
return opposites. In `CONTAINSSTRINGEXACT` the `*` is an asterisk and nothing more: it finds
`"a*b"` because there is a real asterisk there, and it does not find `"aXXXb"` because there is
not.

That makes it convenient for **searching for characters that are wildcards**: references with
`*`, codes with `?`, any field where those symbols are data.

What is **not** true is that it is the only way to do it. `CONTAINSSTRING` accepts the `~` escape,
and with it searches for the literal character without giving up case-insensitivity — it is
measured in [`containsstring`](./containsstring.md), section 4. The real choice is this:

| what you want | use |
|---|---|
| literal wildcard, **ignoring** case | `CONTAINSSTRING` with `~*` / `~?` |
| literal wildcard, **distinguishing** case | `CONTAINSSTRINGEXACT`, escaping nothing |

And the `~` is **not** an escape here. The following measures it, alongside the trick of
normalising with [`upper`](../text/upper.md):

```dax
EVALUATE
ROW(
  "tilde_no_escapa_aqui", CONTAINSSTRINGEXACT("a*b", "a~*b"),
  "upper_en_los_dos_lados", CONTAINSSTRINGEXACT(UPPER("Bicicleta"), UPPER("bici")),
  "pero_upper_no_arregla_el_acento", CONTAINSSTRINGEXACT(UPPER("Almacén"), UPPER("almacen"))
)
```

```result
tilde_no_escapa_aqui | upper_en_los_dos_lados | pero_upper_no_arregla_el_acento
False | True | False
```

The first column is false because here `"a~*b"` is searched for as it stands, tilde included, and
that is not in `"a*b"`. The second confirms that normalising with `UPPER` on both sides does
restore case-insensitivity. The third warns how far that fix goes: **the accent is still not
forgiven**, because `UPPER` changes the case, not the diacritics.

## 3. A blank needle also always finds

```dax
EVALUATE
ROW(
  "aguja_vacia", CONTAINSSTRINGEXACT("Bicicleta", ""),
  "aguja_blanca", CONTAINSSTRINGEXACT("Bicicleta", BLANK()),
  "acento_igual", CONTAINSSTRINGEXACT("Almacén", "macén"),
  "trozo_en_medio", CONTAINSSTRINGEXACT("Bicicleta", "cicle")
)
```

```result
aguja_vacia | aguja_blanca | acento_igual | trozo_en_medio
True | True | True | True
```

It inherits the same hole as [`containsstring`](./containsstring.md): an empty or blank search
term returns true for everything, so the filter stops filtering without saying so.

And it inherits the nuance too: **`ISBLANK` is no guard here**, because `ISBLANK("")` is false and
the empty string slips through anyway. Use `IF(LEN([Buscado]) > 0, ...)`, which covers both cases
— it is measured in [`containsstring`](./containsstring.md), section 3.

The last two confirm the expected: it finds at any position, not only at the start.

See [`containsstring`](./containsstring.md) and [`contains`](./contains.md).
