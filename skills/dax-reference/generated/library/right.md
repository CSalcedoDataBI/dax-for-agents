---
name: RIGHT
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/right-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# RIGHT

RIGHT returns the last character or characters in a text string, based on the number of characters you specify.

## Syntax

```dax
RIGHT(<text>, <num_chars>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|The text string that contains the characters you want to extract, or a reference to a column that contains text.|
|`num_chars`|(optional) The number of characters you want RIGHT to extract; is omitted, 1. You can also use a reference to a column that contains numbers.|

If the column reference does not contain text, it is implicitly cast as text.

## Return value

A text string containing the specified right-most characters.

## Remarks

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example: Returning a Fixed Number of Characters

The following formula returns the last two digits of the product code in the New Products table.

```dax
= RIGHT('New Products'[ProductCode],2)
```

## Example: Using a Column Reference to Specify Character Count

The following formula returns a variable number of digits from the product code in the New Products table, depending on the number in the column, MyCount. If there is no value in the column, MyCount, or the value is a blank, RIGHT also returns a blank.

```dax
= RIGHT('New Products'[ProductCode],[MyCount])
```

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
- [LEFT](./left.md)
- [MID](./mid.md)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/right.md`](../../examples/text/right.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
