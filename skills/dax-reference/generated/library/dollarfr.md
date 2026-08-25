---
name: DOLLARFR
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/dollarfr-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DOLLARFR

Converts a dollar price expressed as a decimal number into a dollar price expressed as an integer part and a fraction part, such as 1.02. Fractional dollar numbers are sometimes used for security prices.

## Syntax

```dax
DOLLARFR(<decimal_dollar>, <fraction>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`decimal_dollar`|A decimal number.|
|`fraction`|The integer to use in the denominator of the fraction.|

## Return Value

The fractional value of `decimal_dollar`, expressed as an integer part and a fraction part.

## Remarks

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
  DOLLARFR(1.125, 16)
}
```

Returns 1.02, read as 1 and 2/16, which is the corresponding fraction price of the original decimal price, 1.125. Since the fraction value is 16, the price has a precision of 1/16 of a dollar.
