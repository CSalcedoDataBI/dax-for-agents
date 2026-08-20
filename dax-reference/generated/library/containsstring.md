---
name: CONTAINSSTRING
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/containsstring-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CONTAINSSTRING

Returns `TRUE` or `FALSE` indicating whether one string contains another string.

## Syntax

```dax
CONTAINSSTRING(<within_text>, <find_text>) 
```

### Parameters

|Term|Definition|
|--------|--------------|
|`within_text`|The text in which you want to search for find_text.|
|`find_text`|The text you want to find.|

## Return value

 `TRUE`  if find_text is a substring of within_text; otherwise `FALSE`.

## Remarks

- CONTAINSSTRING is case-insensitive, kanatype-insensitive, width-insensitive and accent sensitive.

- You can use `?` and `*` wildcard characters. Use `~` to escape wildcard characters.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

DAX query

```DAX
EVALUATE
    ROW(
        "Case 1", CONTAINSSTRING("abcd", "bc"), 
        "Case 2", CONTAINSSTRING("abcd", "BC"),
        "Case 3", CONTAINSSTRING("abcd", "a*d"),
        "Case 4", CONTAINSSTRING("abcd", "ef")
    )
```

Returns

|[Case 1]  |[Case 2]  |[Case 3]  |[Case 4]  |
|---------|---------|---------|---------|
|`TRUE`     | `TRUE`         | `TRUE`         |`FALSE`          |
