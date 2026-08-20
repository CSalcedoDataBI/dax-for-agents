---
name: FALSE
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/false-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# FALSE

Returns the logical value `FALSE`.

## Syntax

```dax
FALSE()
```

## Return value

Always `FALSE`.

## Remarks

The word `FALSE` is also interpreted as the logical value `FALSE`.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/false.md`](../../examples/logical/false.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The formula returns the logical value `FALSE` when the value in the column, 'InternetSales_USD'[SalesAmount_USD], is less than or equal to 200000.

```dax
= IF(SUM('InternetSales_USD'[SalesAmount_USD]) >200000, TRUE(), false())
```

The following table shows the results when the example formula is used with 'ProductCategory'[ProductCategoryName] in Row Labels and 'DateTime'[CalendarYear] in Column Labels.

|Row Labels|2005|2006|2007|2008|-|Grand Total|
|---------------|-----------------|----|----|----|----|----|
|Accessories|``FALSE``|``FALSE``|``TRUE``|``TRUE``|``FALSE``|``TRUE``|
|Bikes|``TRUE``|``TRUE``|``TRUE``|``TRUE``|``FALSE``|``TRUE``|
|Clothing|``FALSE``|``FALSE``|``FALSE``|``FALSE``|``FALSE``|``TRUE``|
|Components|``FALSE``|``FALSE``|``FALSE``|``FALSE``|``FALSE``|``FALSE``|
||``FALSE``|``FALSE``|``FALSE``|``FALSE``|``FALSE``|``FALSE``|
|Grand Total|``TRUE``|``TRUE``|``TRUE``|``TRUE``|``FALSE``|``TRUE``|

## Related content

- [TRUE function](./true.md)
- [NOT function](./not.md)
- [IF function](./if.md)
