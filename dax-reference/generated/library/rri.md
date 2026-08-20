---
name: RRI
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/rri-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# RRI

Returns an equivalent interest rate for the growth of an investment.

## Syntax

```dax
RRI(<nper>, <pv>, <fv>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`nper`|The number of periods for the investment.|
|`pv`|The present value of the investment.|
|`fv`|The future value of the investment.|

## Return Value

The equivalent interest rate.

## Remarks

- RRI returns the interest rate given $\text{nper}$ (the number of periods), $\text{pv}$ (present value), and $\text{fv}$ (future value), calculated by using the following equation:

  $$\bigg( \frac{\text{fv}}{\text{pv}} \bigg)^{(\frac{1}{\text{}nper})} - 1$$

- An error is returned if:
  - nper ≤ 0.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

| **Data** | **Description** |
| -------- | --------------- |
| \\$10,000  | Present value   |
| \\$21,000  | Future value    |
| 4        | Years invested  |

The following DAX query:

```dax
EVALUATE
{
  RRI(4*12, 10000, 21000)
}
```

Returns an equivalent interest rate for the growth of an investment with the terms specified above.

| **[Value]**      |
| ------------------ |
| 0.0155771057566627 |
