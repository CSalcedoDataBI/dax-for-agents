---
name: NOMINAL
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/nominal-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NOMINAL

Returns the nominal annual interest rate, given the effective rate and the number of compounding periods per year.

## Syntax

```dax
NOMINAL(<effect_rate>, <npery>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`effect_rate`|The effective interest rate.|
|`npery`|The number of compounding periods per year.|

## Return Value

The nominal annual interest rate.

## Remarks

- The relationship between NOMINAL and EFFECT is shown in the following equation:

    $$\text{EFFECT} = \Big( 1 + \frac{\text{nominal\_rate}}{\text{npery}} \Big)^{\text{npery}} - 1$$

- npery is rounded to the nearest integer.

- An error is returned if:
  - effect_rate ≤ 0.
  - npery < 1.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

| **Data** | **Description**                        |
| -------- | -------------------------------------- |
| 5.3543%  | Effective interest rate                |
| 4        | Number of compounding periods per year |

The following DAX query:

```dax
EVALUATE
{
  NOMINAL(0.053543, 4)
}
```

Returns the nominal interest rate, using the terms specified above.

| **[Value]**     |
| ----------------- |
| 0.052500319868356 |
