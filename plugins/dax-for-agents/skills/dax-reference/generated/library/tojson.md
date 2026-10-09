---
name: TOJSON
category: [other]
primaryCategory: other
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/tojson-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# TOJSON

Returns a table as a string using JSON format.

## Syntax

```dax
TOJSON(<Table>, [MaxRows])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Table`|The table to be converted to JSON.|
|`MaxRows`|(Optional) The maximum number fo rows to convert. Default is 10 rows.|

## Return value

A string with JSON representation of the table. The representation contains column names as "header", count-of-rows as "rowCount", and values as "data".

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
EVALUATE
{TOJSON(DimSalesTerritory)}
```

Returns:

```json
{
"header": ["'DimSalesTerritory'[SalesTerritoryKey]", "'DimSalesTerritory'[SalesTerritoryAlternateKey]", "'DimSalesTerritory'[SalesTerritoryRegion]", "'DimSalesTerritory'[SalesTerritoryCountry]", "'DimSalesTerritory'[SalesTerritoryGroup]"],<br>
"rowCount": 11,
"data": [
[1, 1, "Northwest", "United States", "North America"],
[2, 2, "Northeast", "United States", "North America"],
[3, 3, "Central", "United States", "North America"],
[4, 4, "Southwest", "United States", "North America"],
[5, 5, "Southeast", "United States", "North America"],
[6, 6, "Canada", "Canada", "North America"],
[7, 7, "France", "France", "Europe"],
[8, 8, "Germany", "Germany", "Europe"],
[9, 9, "Australia", "Australia", "Pacific"],
[10, 10, "United Kingdom", "United Kingdom", "Europe"]
]
}
```

## Related content

- [TOCSV](./tocsv.md)
- [EVALUATEANDLOG](./evaluateandlog.md)
