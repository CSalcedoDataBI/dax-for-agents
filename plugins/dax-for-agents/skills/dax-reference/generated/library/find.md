---
name: FIND
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/find-function-dax.md@323524c
sourceDate: 06/29/2026
notes: true
examples: 5
---
# FIND

Returns the starting position of one text string within another text string. FIND is case-sensitive.

## Syntax

```dax
FIND(<find_text>, <within_text>[, [<start_num>][, <NotFoundValue>]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`find_text`|The text you want to find. Use double quotes (empty text) to match the first character in `within_text`. |
|`within_text`|The text containing the text you want to find.|
|`start_num`|(optional) The character at which to start the search; if omitted, `start_num` = 1. The first character in `within_text` is character number 1.|
|`NotFoundValue`|(optional, but strongly recommended) The value to return when the operation doesn't find a matching substring, typically 0, -1, or BLANK(). If you don't specify it, the function returns an error.|

## Return value

Number that shows the starting point of the text string you want to find.

## Remarks

- Whereas Microsoft Excel has multiple versions of the FIND function to accommodate single-byte character set (SBCS) and double-byte character set (DBCS) languages, DAX uses Unicode and counts each character the same way; therefore, you don't need to use a different version depending on the character type.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

- FIND doesn't support wildcards. To use wildcards, use [SEARCH](./search.md).

- This function returns different results depending on [the UnicodeCharacterBehavior setting of your model](https://learn.microsoft.com/en-us/dax/best-practices/dax-unicode-character-behavior).

## Ejemplos ejecutables

**5** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/find.md`](../../examples/text/find.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query finds the position of the first letter of "Bike", in the string that contains the reseller name. If not found, FIND returns Blank.

FIND is case-sensitive. In this example, if you used "bike" in the `find_text` argument, the query returns no results. Use [SEARCH](./search.md) for case-insensitive.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
EVALUATE
CALCULATETABLE (
    ADDCOLUMNS (
        TOPN ( 10, SUMMARIZE ( 'Reseller', [Reseller], [Business Type] ) ),
        "Position of Bike", FIND ( "Bike", 'Reseller'[Reseller], 1, BLANK () )
    ),
    'Reseller'[Business Type]
        IN { "Specialty Bike Shop", "Value Added Reseller", "Warehouse" }
)
```

Returns,

|Reseller  |Business Type | Position of Bike |
|---------|---------|---------|
|Volume Bike Sellers    |Warehouse|     8    |
|Mass Market Bikes     |Value Added Reseller|    13     |
|Twin Cycles     |Value Added Reseller|         |
|Rich Department Store     |Warehouse|         |
|Rental Gallery     |Specialty Bike Shop|         |
|Budget Toy Store     |Warehouse|         |
|Global Sports Outlet     |Warehouse|         |
|Online Bike Catalog     |Warehouse|     8    |
|Helmets and Cycles     |Value Added Reseller|         |
|Jumbo Bikes     |Specialty Bike Shop|    7     |

## Related content

- [SEARCH](./search.md)
- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
