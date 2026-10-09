---
name: MID
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/mid-function-dax.md@323524c
sourceDate: 
notes: false
examples: 5
---
# MID

Returns a string of characters from the middle of a text string, given a starting position and length.

## Syntax

```dax
MID(<text>, <start_num>, <num_chars>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text string from which you want to extract the characters, or a column that contains text.|
|`start_num`|The position of the first character you want to extract. Positions start at 1.|
|`num_chars`|The number of characters to return.|

## Return value
A string of text of the specified length.

## Remarks

- Whereas Microsoft Excel has different functions for working with single-byte and double-byte characters languages, DAX uses Unicode and stores all characters with the same length.

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

## Ejemplos ejecutables

**5** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/mid.md`](../../examples/text/mid.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following expression,

```dax
MID("abcde",2,3))
```

Returns `"bcd"`.

The following expression,

```dax
MID('Reseller'[ResellerName],1,5))
```

Returns the same result as `LEFT([ResellerName],5)`. Both expressions return the first 5 letters of column, `[ResellerName]`.

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
