---
name: UNICODE
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/unicode-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# UNICODE

Returns the number (code point) corresponding to the first character of the text.

## Syntax

```dax
UNICODE( <Text> )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Text`|Text is the character for which you want the Unicode value.|

## Return value

A numeric code for the first character in a text string.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/unicode.md`](../../examples/text/unicode.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
