---
name: DDB
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/ddb-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DDB

Returns the depreciation of an asset for a specified period using the double-declining balance method or some other method you specify.

## Syntax

```dax
DDB(<cost>, <salvage>, <life>, <period>[, <factor>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`cost`|The initial cost of the asset.|
|`salvage`|The value at the end of the depreciation (sometimes called the salvage value of the asset). This value can be 0.|
|`life`|The number of periods over which the asset is being depreciated (sometimes called the useful life of the asset).|
|`period`|The period for which you want to calculate the depreciation. Period must use the same units as life. Must be between 1 and life (inclusive).|
|`factor`|(Optional) The rate at which the balance declines. If factor is omitted, it is assumed to be 2 (the double-declining balance method).|

## Return Value

The depreciation over the specified period.

## Remarks

- The double-declining balance method computes depreciation at an accelerated rate. Depreciation is highest in the first period and decreases in successive periods. DDB uses the following formula to calculate depreciation for a period:

  $$\text{Min}((\text{cost} - \text{total depreciation from prior periods}) \times (\frac{\text{factor}}{\text{life}}),(\text{cost} - \text{salvage} - \text{total depreciation from prior periods}))$$

- Change factor if you do not want to use the double-declining balance method.

- Use the VDB function if you want to switch to the straight-line depreciation method when depreciation is greater than the declining balance calculation.

- period is rounded to the nearest integer.

- An error is returned if:
  - cost < 0.
  - salvage < 0.
  - life < 1.
  - period < 1 or period > life.
  - factor ≤ 0.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

### Example 1

The following DAX query:

```dax
EVALUATE
{
  DDB(1000000, 0, 10, 5, 1.5)
}
```

Returns an asset's depreciation in the 5$^{th}$ year, assuming it will be worth \\$0 after 10 years. This calculation uses a factor of 1.5.

| **[Value]** |
| ------------- |
| 78300.9375    |

### Example 2

The following calculates the total depreciation of all assets in different years over their lifetimes. This calculation uses the default factor of 2 (the double-declining balance method).

```dax
DEFINE
VAR NumDepreciationPeriods = MAX(Asset[LifeTimeYears])
VAR DepreciationPeriods = GENERATESERIES(1, NumDepreciationPeriods)
EVALUATE
  ADDCOLUMNS (
  DepreciationPeriods,
  "Current Period Total Depreciation",
  SUMX (
    FILTER (
      Asset,
      [Value] <= [LifetimeYears]
    ),
    DDB([InitialCost], [SalvageValue], [LifetimeYears], [Value])
  )
)
```
