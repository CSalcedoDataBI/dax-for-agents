---
name: TOCSV
category: [other]
primaryCategory: other
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/tocsv-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# TOCSV

Returns a table as a string in CSV format.

## Syntax

```dax
TOCSV(<Table>, [MaxRows], [Delimiter], [IncludeHeaders])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Table`|The table to be converted to CSV.|
|`MaxRows`| (Optional) The maximum number fo rows to convert. Default is 10 rows.|
|`Delimiter`|(Optional) A column delimiter. Default is comma ",".|
|`IncludeHeaders`|(Optional) Specifies a header with column name as the first row. Default is True.|

## Return value

A string with CSV representation of the table.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
EVALUATE
{TOCSV(DimSalesTerritory)}

```

Returns:

```
'DimSalesTerritory'[SalesTerritoryKey],'DimSalesTerritory'[SalesTerritoryAlternateKey],'DimSalesTerritory'[SalesTerritoryRegion],'DimSalesTerritory'[SalesTerritoryCountry],'DimSalesTerritory'[SalesTerritoryGroup]
1,1,Northwest,United States,North America
2,2,Northeast,United States,North America
3,3,Central,United States,North America
4,4,Southwest,United States,North America
5,5,Southeast,United States,North America
6,6,Canada,Canada,North America
7,7,France,France,Europe
8,8,Germany,Germany,Europe
9,9,Australia,Australia,Pacific
10,10,United Kingdom,United Kingdom,Europe
```

## Related content

- [TOJSON](./tojson.md)
- [EVALUATEANDLOG](./evaluateandlog.md)
