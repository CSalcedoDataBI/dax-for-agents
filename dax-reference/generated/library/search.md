---
name: SEARCH
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/search-function-dax.md@323524c
sourceDate: 06/29/2026
notes: true
examples: 4
---
# SEARCH

Returns the number of the character at which a specific character or text string is first found, reading left to right. Search is case-insensitive, kanatype-insensitive, width-insensitive, and accent sensitive.

## Syntax

```dax
SEARCH(<find_text>, <within_text>[, [<start_num>][, <NotFoundValue>]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`find_text`|The text that you want to find.<br /><br />You can use wildcard characters — the question mark (?) and asterisk (\*) — in `find_text`. A question mark matches any single character; an asterisk matches any sequence of characters. If you want to find an actual question mark or asterisk, type a tilde (~) before the character.|
|`within_text`|The text in which you want to search for `find_text`, or a column containing text.|
|`start_num`|(optional) The character position in `within_text` at which you want to start searching. If omitted, 1.|
|`NotFoundValue`|(optional, but strongly recommended) The value to return when the operation doesn't find a matching substring, typically 0, -1, or BLANK(). If you don't specify it, the function returns an error.|

## Return value

The number of the starting position of the first text string from the first character of the second text string.

## Remarks

- The search function is case insensitive. Searching for "N" finds the first occurrence of 'N' or 'n'.

- The search function is kanatype-insensitive, width-insensitive. Searching for "か" finds the first occurrence of 「か」 (hiragana), 「カ」 (katakana), or 「ｶ」 (half-width katakana).

- The search function is accent sensitive. Searching for "á" finds the first occurrence of 'á' but no occurrences of 'a', 'à', or the capitalized versions 'A', 'Á'.

- You can use the SEARCH function to determine the location of a character or text string within another text string, and then use the MID function to return the text, or use the REPLACE function to change the text.

- If the `find_text` can't be found in `within_text`, the formula returns an error. This behavior is like Excel, which returns #VALUE if the substring isn't found. Nulls in `within_text` are interpreted as an empty string in this context.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/search.md`](../../examples/text/search.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query finds the position of the first letter of "cycle", in the string that contains the reseller name. If not found, SEARCH returns Blank.

SEARCH is case-insensitive. In this example, if you use "cycle" or "Cycle" in the `find_text` argument, the query returns results for either case. Use [FIND](https://learn.microsoft.com/en-us/dax/FIND-function-dax) for case-sensitive.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
EVALUATE
CALCULATETABLE (
    ADDCOLUMNS (
        TOPN ( 10, SUMMARIZE ( 'Reseller', [Reseller], [Business Type] ) ),
        "Position of cycle", SEARCH ( "cycle", 'Reseller'[Reseller], 1, BLANK () )
    ),
    'Reseller'[Business Type]
        IN { "Specialty Bike Shop", "Value Added Reseller", "Warehouse" }
)
```

Returns,

|Reseller  |Business Type | Position of cycle |
|---------|---------|---------|
|Volume Bike Sellers    |Warehouse|        |
|Mass Market Bikes     |Value Added Reseller|         |
|Twin Cycles     |Value Added Reseller|     6    |
|Rich Department Store     |Warehouse|         |
|Rental Gallery     |Specialty Bike Shop|         |
|Budget Toy Store     |Warehouse|         |
|Global Sports Outlet     |Warehouse|         |
|Online Bike Catalog     |Warehouse|         |
|Helmets and Cycles     |Value Added Reseller|    13     |
|Jumbo Bikes     |Specialty Bike Shop|         |

## Related content

- [FIND](./find.md)
- [REPLACE](./replace.md)
- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
