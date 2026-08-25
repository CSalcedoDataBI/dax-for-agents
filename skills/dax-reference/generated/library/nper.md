---
name: NPER
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/nper-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NPER

Returns the number of periods for an investment based on periodic, constant payments and a constant interest rate.

## Syntax

```dax
NPER(<rate>, <pmt>, <pv>[, <fv>[, <type>]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`rate`|The interest rate per period.|
|`pmt`|The payment made each period; it cannot change over the life of the annuity. Typically, pmt contains principal and interest but no other fees or taxes.|
|`pv`|The present value, or the lump-sum amount that a series of future payments is worth right now.|
|`fv`|(Optional) The future value, or a cash balance you want to attain after the last payment is made. If fv is omitted, it is assumed to be BLANK.|
|`type`|(Optional) The number 0 or 1 and indicates when payments are due. If type is omitted, it is assumed to be 0. The accepted values are listed below this table.|

The `type` parameter accepts the following values:

| **Set type equal to** | **If payments are due**        |
| --------------------- | ------------------------------ |
| 0 or omitted          | At the end of the period       |
| 1                     | At the beginning of the period |

## Return Value

The number of periods for an investment.

## Remarks

- type is rounded to the nearest integer.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

| **Data** | **Description**                                           |
| -------- | --------------------------------------------------------- |
| 12%      | Annual interest rate                                      |
| -100    | Payment made each period                                  |
| -1000   | Present value                                             |
| 10000    | Future value                                              |
| 1        | Payment is due at the beginning of the period (see above) |

The following DAX query:

```dax
EVALUATE
{
  NPER(0.12/12, -100, -1000, 10000, 1)
}
```

Returns the number of periods for the investment described by the terms specified above.

| **[Value]**    |
| ---------------- |
| 59.6738656742946 |
