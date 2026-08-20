---
name: DOLLARDE
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/dollarde-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DOLLARDE

Converts a dollar price expressed as an integer part and a fraction part, such as 1.02, into a dollar price expressed as a decimal number. Fractional dollar numbers are sometimes used for security prices.

## Syntax

```dax
DOLLARDE(<fractional_dollar>, <fraction>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`fractional_dollar`|A number expressed as an integer part and a fraction part, separated by a decimal symbol.|
|`fraction`|The integer to use in the denominator of the fraction.|

## Return Value

The decimal value of `fractional_dollar`.

## Remarks

- The fraction part of the value is divided by an integer that you specify. For example, if you want your price to be expressed to a precision of 1/16 of a dollar, you divide the fraction part by 16. In this case, 1.02 represents \\$1.125 (\\$1 + 2/16 = \\$1.125).

- fraction is rounded to the nearest integer.

- An error is returned if:
  - fraction < 1.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
EVALUATE
{
  DOLLARDE(1.02, 16)
}
```

Returns 1.125, the decimal price of the original fractional price, 1.02, read as 1 and 2/16. Since the fraction value is 16, the price has a precision of 1/16 of a dollar.
