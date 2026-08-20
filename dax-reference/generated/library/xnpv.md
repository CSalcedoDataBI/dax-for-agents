---
name: XNPV
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/xnpv-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# XNPV

Returns the present value for a schedule of cash flows that is not necessarily periodic.

## Syntax

```dax
XNPV(<table>, <values>, <dates>, <rate>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|A table for which the values and dates expressions should be calculated.|
|`values`|An expression that returns the cash flow value for each row of the table.|
|`dates`|An expression that returns the cash flow date for each row of the table.|
|`rate`|The discount rate to apply to the cash flow for each row of the table.|

## Return value

Net present value.

## Remarks

- The value is calculated as the following summation:

    $$\sum^{N}\_{j=1} \frac{P\_{j}}{(1 + \text{rate})^{\frac{d\_{j} - d\_{1}}{365}}}$$

    Where:

  - $P\_{j}$ is the $j^{th}$ payment
  - $d\_{j}$ is the $j^{th}$ payment date
  - $d\_{1}$ is the first payment date

- The series of cash flow values must contain at least one positive number and one negative number.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following calculates the present value of the CashFlows table:

```dax
= XNPV( CashFlows, [Payment], [Date], 0.09 )
```

|`Date`|Payment|
|--------|-----------|
|`1/1/2014`|-10000|
|`3/1/2014`|2750|
|`10/30/2014`|4250|
|`2/15/2015`|3250|
|`4/1/2015`|2750|

Present value = 2089.50
