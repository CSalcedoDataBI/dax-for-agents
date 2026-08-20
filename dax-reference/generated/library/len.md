---
name: LEN
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/len-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# LEN

Returns the number of characters in a text string.

## Syntax

```dax
LEN(<text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text whose length you want to find, or a column that contains text. Spaces count as characters.|

## Return value

A whole number indicating the number of characters in the text string.

## Remarks

- Whereas Microsoft Excel has different functions for working with single-byte and double-byte character languages, DAX uses Unicode and stores all characters with the same length.

- If you use LEN with a column that contains non-text values, such as dates or Booleans, the function implicitly casts the value to text, using the current column format.

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/len.md`](../../examples/text/len.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula sums the lengths of addresses in the columns, [AddressLine1] and [AddressLine2].

```dax
= LEN([AddressLine1])+LEN([AddressLin2])
```
