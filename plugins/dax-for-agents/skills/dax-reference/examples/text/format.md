---
function: FORMAT
model: ninguno
---

# FORMAT — examples

> The [`format`](../../notes/format.md) field note covers what matters: it returns **text**, and
> with that the numeric ordering is lost. Here are the format strings and their edges.

## 1. The named formats are the ones to use

They are stable and they translate with the model's culture. The custom ones are written by hand
and are where the surprises show up.

```dax
EVALUATE
ROW(
  "general",   FORMAT(1234.567, "General Number"),
  "fijo",      FORMAT(1234.567, "Fixed"),
  "estandar",  FORMAT(1234.567, "Standard"),
  "porcentaje", FORMAT(0.1234, "Percent")
)
```

```result
general | fijo | estandar | porcentaje
1234,567 | 1234,57 | 1.234,57 | 12,34%
```

`Percent` **multiplies by 100**: a value already converted to a percentage gets the point moved
again, and comes out a hundred times larger with nobody checking.

## 2. A custom format with sections changes according to the sign

Separated by `;` come the positive, the negative and the zero. It is powerful and it is where the
mistakes creep in, because they only show up with data of all three kinds.

```dax
EVALUATE
ROW(
  "positivo", FORMAT(1234, "#,##0;(#,##0);cero"),
  "negativo", FORMAT(-1234, "#,##0;(#,##0);cero"),
  "cero",     FORMAT(0, "#,##0;(#,##0);cero"),
  "blanco",   FORMAT(BLANK(), "#,##0;(#,##0);cero")
)
```

```result
positivo | negativo | cero | blanco
1.234 | (1.234) | cero | (blank)
```

The blank does **not** take the zero section: it stays blank. That is the good news — "no data"
and "zero" do not end up written the same — and at the same time the reason a third section
written to cover the gaps does not cover them. For that you need `COALESCE` before the `FORMAT`,
not another section.

## 3. A format string that does not exist gives no error

It returns the string's text as it stands, or something like it. There is no validation, so a
typo survives until somebody looks at the visual.

```dax
EVALUATE
ROW(
  "valido",       FORMAT(1234.5, "#,##0.00"),
  "errata",       FORMAT(1234.5, "#,##O.OO"),
  "inventado",    FORMAT(1234.5, "no soy un formato"),
  "fecha_sobre_numero", FORMAT(1234.5, "yyyy-mm-dd")
)
```

```result
valido | errata | inventado | fecha_sobre_numero
1.234,50 | 1.235O,OO | 0o 0o138 u0 for5ato | 1903-05-18
```

The last is the most treacherous: a number interpreted as a date gives a believable date, not an
error.
