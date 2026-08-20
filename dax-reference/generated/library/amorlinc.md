---
name: AMORLINC
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/amorlinc-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# AMORLINC

Returns the depreciation for each accounting period. This function is provided for the French accounting system. If an asset is purchased in the middle of the accounting period, the prorated depreciation is taken into account.

## Syntax

```dax
AMORLINC(<cost>, <date_purchased>, <first_period>, <salvage>, <period>, <rate>[, <basis>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`cost`|The cost of the asset.|
|`date_purchased`|The date of the purchase of the asset.|
|`first_period`|The date of the end of the first period.|
|`salvage`|The salvage value at the end of the life of the asset.|
|`period`|The period.|
|`rate`|The rate of depreciation.|
|`basis`|(Optional) The type of day count basis to use. If basis is omitted, it is assumed to be 0. The accepted values are listed below this table.|

The `basis` parameter accepts the following values:

| `Basis`    | **Date system**                      |
| ------------ | ------------------------------------ |
| 0 or omitted | 360 days (NASD method)               |
| 1            | Actual                               |
| 3            | 365 days in a year                   |
| 4            | 360 days in a year (European method) |

## Return Value

The depreciation for each accounting period.

## Remarks

- Dates are stored as sequential serial numbers so they can be used in calculations. In DAX, December 30, 1899 is day 0, and January 1, 2008 is 39448 because it is 39,448 days after December 30, 1899.

- period and basis are rounded to the nearest integer.

- An error is returned if:
  - `cost` < 0.
  - `first_period` or `date_purchased` is not a valid date.
  - `date_purchased` > `first_period`.
  - `salvage` < 0 or `salvage` > `cost`.
  - `period` < 0.
  - `rate` ≤ 0.
  - `basis` is any number other than 0, 1, 3, or 4.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

| **Data**         | **Description**          |
| ---------------- | ------------------------ |
| 2400             | Cost                     |
| 19-August-2008   | Date purchased           |
| 31-December-2008 | End of the first period  |
| 300              | Salvage value            |
| 1                | Period                   |
| 15%              | Depreciation rate        |
| 1                | Actual basis (see above) |

The following DAX query:

```dax
EVALUATE
{
  AMORLINC(2400, DATE(2008,8,19), DATE(2008,12,31), 300, 1, 0.15, 1)
}
```

Returns the first period's depreciation, given the terms specified above.

| **[Value]** |
| ------------- |
| 360           |
