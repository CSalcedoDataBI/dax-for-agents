---
name: LEFT
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/left-function-dax.md@323524c
sourceDate: 07/08/2026
notes: false
examples: 3
---
# LEFT

Returns the specified number of characters from the start of a text string.

## Syntax

```dax
LEFT(<text>, <num_chars>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text string containing the characters you want to extract, or a reference to a column that contains text.|
|`num_chars`|(optional) The number of characters you want LEFT to extract; if omitted, 1.|

## Return value

A text string.

## Remarks

- Whereas Microsoft Excel contains different functions for working with text in single-byte and double-byte character languages, DAX works with Unicode and stores all characters as the same length; therefore, a single function is enough.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/left.md`](../../examples/text/left.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

The following example returns the first five characters of the company city in the column [City] and the first five letters of the reseller key in the column [ResellerKey] and concatenates them, to create an identifier.

```dax
=
CONCATENATE (
    LEFT ( 'Reseller'[City], 5 ),
    LEFT ( 'Reseller'[ResellerKey], 5 )
)
```

If the `num_chars` argument is larger than the number of characters available, the function returns the maximum characters available and doesn't raise an error. For example, the column [ResellerKey] contains numbers such as 5, 24, and 312, so the result also has variable length.

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
