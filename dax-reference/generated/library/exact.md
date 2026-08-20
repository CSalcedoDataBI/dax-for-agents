---
name: EXACT
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/exact-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 3
---
# EXACT

Compares two text strings and returns `TRUE` if they're exactly the same, otherwise returns `FALSE`. EXACT is case-sensitive but ignores formatting differences.

## Syntax

```dax
EXACT(<text1>,<text2>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text1`|The first text string or column that contains text.|
|`text2`|The second text string or column that contains text.|

## Return value

True or False. (Boolean)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/exact.md`](../../examples/text/exact.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula in a calculated column in the Product table checks the value of Product for the current row against the value of Model for the current row. It returns True if they're the same, and False if they're different.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
=
EXACT ( [Product], [Model] )
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
