---
name: NOT
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/not-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# NOT

Changes `FALSE` to `TRUE`, or `TRUE` to `FALSE`.

## Syntax

```dax
NOT(<logical>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`logical`|A value or expression that can be evaluated to `TRUE` or `FALSE`.|

## Return value

`TRUE` OR `FALSE`.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/not.md`](../../examples/logical/not.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example retrieves values from the calculated column that was created to illustrate the IF function. For that example, the calculated column was named using the default name, **Calculated Column1**, and contains the following formula: `= IF([Orders]<300,"true","false")`

The formula checks the value in the column, [Orders], and returns "true" if the number of orders is under 300.

Now create a new calculated column, **Calculated Column2**, and type the following formula.

```dax
= NOT([CalculatedColumn1])
```

For each row in **Calculated Column1**, the values "true" and "false" are interpreted as the logical values `TRUE` or `FALSE`, and the NOT function returns the logical opposite of that value.

## Related content

- [TRUE function](./true.md)
- [FALSE function](./false.md)
- [IF function](./if.md)
