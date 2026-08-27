---
name: CONTAINSSTRINGEXACT
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/containsstringexact-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# CONTAINSSTRINGEXACT

Returns `TRUE` or `FALSE` indicating whether one string contains another string.

## Syntax

```dax
CONTAINSSTRINGEXACT(<within_text>, <find_text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`within_text`|The text in which you want to search for find_text.|
|`find_text`|The text you want to find.|

## Return value

 `TRUE`  if find_text is a substring of within_text; otherwise `FALSE`.

## Remarks

CONTAINSSTRINGEXACT is case-sensitive.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/containsstringexact.md`](../../examples/information/containsstringexact.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

DAX query

```DAX
EVALUATE
    ROW(
        "Case 1", CONTAINSSTRINGEXACT("abcd", "bc"), 
        "Case 2", CONTAINSSTRINGEXACT("abcd", "BC"),
        "Case 3", CONTAINSSTRINGEXACT("abcd", "a*d"),
        "Case 4", CONTAINSSTRINGEXACT("abcd", "ef")
    )

```

Returns

|[Case 1]  |[Case 2]  |[Case 3]  |[Case 4]  |
|---------|---------|---------|---------|
|`TRUE`     | `FALSE`         | `FALSE`         |`FALSE`          |
