---
name: LOWER
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/lower-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# LOWER

Converts all letters in a text string to lowercase.

## Syntax

```dax
LOWER(<text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text you want to convert to lowercase, or a reference to a column that contains text.|

## Return value

Text in lowercase.

## Remarks

Characters that are not letters are not changed. For example, the formula `= LOWER("123ABC")` returns `123abc`.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/lower.md`](../../examples/text/lower.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula gets each row in the column, [ProductCode], and converts the value to all lowercase. Numbers in the column are not affected.

```dax
= LOWER('New Products'[ProductCode])
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
