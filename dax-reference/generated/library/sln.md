---
name: SLN
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sln-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SLN

Returns the straight-line depreciation of an asset for one period.

## Syntax

```dax
SLN(<cost>, <salvage>, <life>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`cost`|The initial cost of the asset.|
|`salvage`|The value at the end of the depreciation (sometimes called the salvage value of the asset).|
|`life`|The number of periods over which the asset is depreciated (sometimes called the useful life of the asset).|

## Return Value

The straight-line depreciation for one period.

## Remarks

- An error is returned if:
  life = 0.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

| **Data** | **Description**      |
| -------- | -------------------- |
| \\$30,000  | Cost                 |
| \\$7,500   | Salvage value        |
| 10       | Years of useful life |

The following DAX query:

```dax
EVALUATE
{
  SLN(30000, 7500, 10)
}
```

Returns the yearly depreciation allowance using the terms specified above.

| **[Value]** |
| ------------- |
| 2250          |
