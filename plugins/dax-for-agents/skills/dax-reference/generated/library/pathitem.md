---
name: PATHITEM
category: [parent-and-child]
primaryCategory: parent-and-child
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pathitem-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PATHITEM

Returns the item at the specified `position` from a string resulting from evaluation of a PATH function. Positions are counted from left to right.

## Syntax

```dax
PATHITEM(<path>, <position>[, <type>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`path`| A text string in the form of the results of a PATH function.    |
|`position`|  An integer expression with the position of the item to be returned.  |
|`type`|  (Optional)An enumeration that defines the data type of the result:  |

#### type enumeration

|Enumeration|Alternate Enumeration|Description|
|-----|-----|-----|
|`TEXT`|0|Results are returned with the data type text. (default).|
|`INTEGER`|1|Results are returned as integers.|

## Return value

The identifier returned by the PATH function at the specified position in the list of identifiers. Items returned by the PATH function are ordered by most distant to current.

## Remarks

- This function can be used to return a specific level from a hierarchy returned by a PATH function. For example, you could return just the skip-level managers for all employees.

- If you specify a number for `position` that is less than one (1) or greater than the number of elements in `path`, the PATHITEM function returns BLANK

- If `type` is not a valid enumeration element an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns the third tier manager of the current employee; it takes the employee and manager IDs as the input to a PATH function that returns a string with the hierarchy of parents to current employee. From that string PATHITEM returns the third entry as an integer.

```dax
= PATHITEM(PATH(Employee[EmployeeKey], Employee[ParentEmployeeKey]), 3, 1)
```
