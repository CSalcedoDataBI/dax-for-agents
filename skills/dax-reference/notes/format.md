## Trap: it returns **text**, and text sorts by character

`FORMAT` does not change how a number looks: it turns it into a string. From then on it does not
add up, it does not compare as a number, and the visual sorts it alphabetically — where 9 comes
after 10.

> The numbers in this note are printed exactly as the engine returned them, under the model's
> culture. They are output, not prose, which is the whole subject here.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[VentasTexto] = FORMAT([Ventas], "#,##0")
EVALUATE
{
  ("tipo de [Ventas]",            IF(ISTEXT([Ventas]), "TEXTO", "NUMERO")),
  ("tipo de FORMAT([Ventas])",    IF(ISTEXT([VentasTexto]), "TEXTO", "NUMERO")),
  ("FORMAT devuelve",             [VentasTexto]),
  ("comparar 9 y 10 como texto",  IF("9" > "10", "9 va DESPUES de 10", "9 va ANTES de 10")),
  ("comparar 9 y 10 como número", IF(9 > 10, "9 va DESPUES de 10", "9 va ANTES de 10"))
}
```

| expression | result |
|---|---|
| type of `[Ventas]` | NUMERO |
| type of `FORMAT([Ventas])` | **TEXTO** |
| `FORMAT([Ventas], "#,##0")` | `19.903.678` |
| `"9" > "10"` | **9 va DESPUES de 10** ❌ |
| `9 > 10` | 9 va ANTES de 10 ✅ |

Sorting by that column puts `9.500` behind `10.200`, and a chart axis, conditional formatting, or
any measure that uses it in a subtraction stop working: they expect a number and get a string.

**The total does not warn you.** A measure is an expression, so on the totals row it is evaluated
again in the total's context and returns the formatted total:

| row | `[Ventas]` | `FORMAT([Ventas], "#,##0")` |
|---|---|---|
| Sony | 1.273.417,32 | `1.273.417` |
| Microsoft | 1.164.898,94 | `1.164.899` |
| **TOTAL** | 19.903.677,62 | **`19.903.678`** ← correct |

That correct total is what makes the problem slow to surface: the table looks fine, and what fails
is the sort order, the axis or the conditional, which nobody connects to the formatting.

## What almost always should have been done

Set the **measure's format** (`formatString` in the model, "Format" in Power BI Desktop). The value
stays numeric, the visual paints it formatted, and everything that depends on it being a number —
totals, sorting, conditionals, axes — keeps working.

`FORMAT` has its place when the result genuinely **is** text: a label mixing number and words, a
dynamic title, a string for export.

## The format depends on the regional settings

`FORMAT(date, "Short Date")` and the named formats follow the model's or the user's settings. In a
report viewed across several countries, the same number comes out with a different separator.
Custom formats (`"#,##0"`, `"yyyy-MM-dd"`) are the predictable ones; the third argument pins the
culture if you need it.

## Not to be confused with
- `CONVERT` — changes the data type, not the appearance.
- `VALUE` — the way back: text to number. It errors if the string is not convertible.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
