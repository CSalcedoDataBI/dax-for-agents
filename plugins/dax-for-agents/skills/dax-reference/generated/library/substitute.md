---
name: SUBSTITUTE
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/substitute-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# SUBSTITUTE

Replaces existing text with new text in a text string.

## Syntax

```dax
SUBSTITUTE(<text>, <old_text>, <new_text>, <instance_num>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text in which you want to substitute characters, or a reference to a column containing text.|
|`old_text`|The existing text that you want to replace.|
|`new_text`|The text you want to replace `old_text` with.|
|`instance_num`|(optional) The occurrence of `old_text` you want to replace. If omitted, every instance of `old_text` is replaced|

## Return value

A string of text.

## Remarks

- Use the SUBSTITUTE function when you want to replace specific text in a text string; use the REPLACE function when you want to replace any text of variable length that occurs in a specific location in a text string.

- The SUBSTITUTE function is case-sensitive. If case does not match between `text` and `old_text`, SUBSTITUTE will not replace the text.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example: Substitution within a String

The following formula creates a copy of the column [Product Code] that substitutes the new product code `NW` for the old product code `PA` wherever it occurs in the column.

```dax
= SUBSTITUTE([Product Code], "NW", "PA")
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
- [REPLACE](./replace.md)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/substitute.md`](../../examples/text/substitute.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
