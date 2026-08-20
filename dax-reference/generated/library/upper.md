---
name: UPPER
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/upper-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# UPPER

Converts a text string to all uppercase letters.

## Syntax

```dax
UPPER (<text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text you want converted to uppercase, or a reference to a column that contains text.|

## Return value

Same text, in uppercase.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/upper.md`](../../examples/text/upper.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula converts the string in the column, [ProductCode], to all uppercase. Non-alphabetic characters are not affected.

```dax
= UPPER(['New Products'[Product Code])
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
- [LOWER function](./lower.md)
