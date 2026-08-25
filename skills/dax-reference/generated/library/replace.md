---
name: REPLACE
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/replace-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# REPLACE

REPLACE replaces part of a text string, based on the number of characters you specify, with a different text string.

## Syntax

```dax
REPLACE(<old_text>, <start_num>, <num_chars>, <new_text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`old_text`|The string of text that contains the characters you want to replace, or a reference to a column that contains text.|
|`start_num`|The position of the character in `old_text` that you want to replace with `new_text`.|
|`num_chars`|The number of characters that you want to replace. **Warning:** If the argument, `num_chars`, is a blank or references a column that evaluates to a blank, the string for `new_text` is inserted at the position, `start_num`, without replacing any characters. This is the same behavior as in Excel.|
|`new_text`|The replacement text for the specified characters in `old_text`.|

## Return value

A text string.

## Remarks

- Whereas Microsoft Excel has different functions for use with single-byte and double-byte character languages, DAX uses Unicode and therefore stores all characters as the same length.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/replace.md`](../../examples/text/replace.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula creates a new calculated column that replaces the first two characters of the product code in column, [ProductCode], with a new two-letter code, OB.

```dax
= REPLACE('New Products'[Product Code],1,2,"OB")
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
- [SUBSTITUTE function](./substitute.md)
