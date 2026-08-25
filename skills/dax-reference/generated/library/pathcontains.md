---
name: PATHCONTAINS
category: [parent-and-child]
primaryCategory: parent-and-child
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pathcontains-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PATHCONTAINS

Returns `TRUE` if the specified `item` exists within the specified `path`.

## Syntax

```dax
PATHCONTAINS(<path>, <item>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`path`| A string created as the result of evaluating a PATH function.  |
|`item`|  A text expression to look for in the path result.  |

## Return value

A value of `TRUE` if `item` exists in `path`; otherwise `FALSE`.

## Remarks

- If `item` is an integer number it is converted to text and then the function is evaluated. If conversion fails then the function returns an error.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example creates a calculated column that takes a manager ID and checks a set of employees. If the manager ID is among the list of managers returned by the PATH function, the PATHCONTAINS function returns true; otherwise it returns false.

```dax
= PATHCONTAINS(PATH(Employee[EmployeeKey], Employee[ParentEmployeeKey]), "23")
```
