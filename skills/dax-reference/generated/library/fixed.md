---
name: FIXED
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/fixed-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 3
---
# FIXED

Rounds a number to the specified number of decimals and returns the result as text. You can specify that the result be returned with or without commas.

## Syntax

```dax
FIXED(<number>, <decimals>, <no_commas>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number you want to round and convert to text, or a column containing a number.|
|`decimals`|(optional) The number of digits to the right of the decimal point; if omitted, 2.|
|`no_commas`|(optional) A logical value: if 1, don't display commas in the returned text; if 0 or omitted, display commas in the returned text.|

## Return value

A number represented as text.

## Remarks

- If the value used for the `decimals` parameter is negative, `number` is rounded to the left of the decimal point.

- If you omit `decimals`, it's assumed to be 2.

- If `no_commas` is 0 or omitted, then the returned text includes commas as usual.

- The major difference between formatting a cell containing a number by using a command and formatting a number directly with the FIXED function is that FIXED converts its result to text. A number formatted with a command from the formatting menu is still a number.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/fixed.md`](../../examples/text/fixed.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula used in a calculated column gets the numeric value for the current row in Product[List Price] and returns it as text with 2 decimal places and no commas.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
=
FIXED ( [List Price], 2, 1 )
```

## Related content

- [CEILING](./ceiling.md)
- [FLOOR](./floor.md)
- [ISO.CEILING](./iso-ceiling.md)
- [MROUND](./mround.md)
- [ROUND](./round.md)
- [ROUNDDOWN](./rounddown.md)
- [ROUNDUP](./roundup.md)
